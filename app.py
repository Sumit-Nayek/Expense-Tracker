
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION & VISUAL THEME ---
st.set_page_config(page_title="FinTrack Enterprise", page_icon="💳", layout="wide")

st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color) !important; 
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    div[data-testid="stMetricLabel"] > div {
        color: var(--text-color) !important;
        opacity: 0.7;
        font-size: 0.95rem !important;
    }
    div[data-testid="stMetricValue"] > div {
        color: var(--text-color) !important;
        font-weight: 700 !important;
    }
    div[data-testid="stForm"] {
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 12px;
        padding: 20px;
        background-color: var(--background-color) !important;
    }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "expenses_v2.db"
CATEGORIES = ["Food", "Utilities", "Transport", "Entertainment", "Housing", "Other"]

# --- DATABASE CONTROLLER OPERATORS ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            limit_amount REAL NOT NULL,
            PRIMARY KEY (user_id, category),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username) VALUES (?)", ("Primary Account",))
        default_user_id = cursor.lastrowid
        
        dummy_expenses = [
            (default_user_id, "2026-06-01", "Food", 120.50, "Weekly Groceries"),
            (default_user_id, "2026-06-05", "Utilities", 85.00, "Electric Bill"),
            (default_user_id, "2026-06-12", "Transport", 45.00, "Fuel refill")
        ]
        cursor.executemany("INSERT INTO expenses (user_id, date, category, amount, notes) VALUES (?, ?, ?, ?, ?)", dummy_expenses)
        
        default_budgets = [(default_user_id, cat, 250.00) for cat in CATEGORIES]
        cursor.executemany("INSERT INTO budgets (user_id, category, limit_amount) VALUES (?, ?, ?)", default_budgets)
        
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT id, username FROM users", conn)
    conn.close()
    return dict(zip(df['username'], df['id']))

def create_new_user(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        new_id = cursor.lastrowid
        default_budgets = [(new_id, cat, 200.00) for cat in CATEGORIES]
        cursor.executemany("INSERT INTO budgets (user_id, category, limit_amount) VALUES (?, ?, ?)", default_budgets)
        conn.commit()
        return new_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def load_user_expenses(user_id):
    conn = sqlite3.connect(DB_FILE)
    # Crucial change: pulling the actual DB record ID to facilitate deletion mapping
    query = "SELECT id, date AS Date, category AS Category, amount AS Amount, notes AS Notes FROM expenses WHERE user_id = ?"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Amount'] = pd.to_numeric(df['Amount'])
    else:
        df = pd.DataFrame(columns=["id", "Date", "Category", "Amount", "Notes"])
    return df

def load_user_budgets(user_id):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT category, limit_amount FROM budgets WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    return dict(zip(df['category'], df['limit_amount']))

def update_user_budget(user_id, cat, amt):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO budgets (user_id, category, limit_amount) VALUES (?, ?, ?)", (user_id, cat, amt))
    conn.commit()
    conn.close()

def insert_expense_to_db(user_id, date_str, cat, amt, note_str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (user_id, date, category, amount, notes) VALUES (?, ?, ?, ?, ?)", (user_id, date_str, cat, amt, note_str))
    conn.commit()
    conn.close()

def delete_expense_from_db(expense_id):
    """Removes an operational transaction record permanently by unique system ID."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

# Start application lifecycle database verification
init_db()

# --- SIDEBAR: OPERATIONAL WORKSPACE CONTROL ---
with st.sidebar:
    st.title("👤 Account Workspace")
    
    user_map = get_all_users()
    user_list = list(user_map.keys())
    
    selected_username = st.selectbox("Switch Active Profile", user_list)
    active_user_id = user_map[selected_username]
    
    with st.expander("👤 Register New Profile"):
        new_user_input = st.text_input("Username", placeholder="e.g., Jane Doe").strip()
        if st.button("Create Account Profile"):
            if new_user_input:
                created_id = create_new_user(new_user_input)
                if created_id:
                    st.success(f"Profile '{new_user_input}' initialized!")
                    st.rerun()
                else:
                    st.error("Username already taken.")
            else:
                st.warning("Username field cannot be blank.")

    st.markdown("---")
    st.subheader("➕ Add Transaction")
    
    user_df = load_user_expenses(active_user_id)
    user_budgets = load_user_budgets(active_user_id)
    
    with st.form("transaction_entry_form", clear_on_submit=True):
        input_amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
        input_category = st.selectbox("Category Allocation", CATEGORIES)
        input_date = st.date_input("Transaction Date", datetime.now())
        input_notes = st.text_input("Memo / Description", placeholder="e.g., Gas station")
        
        submit_btn = st.form_submit_button("Securely Record Entry")
        
        if submit_btn:
            formatted_date = input_date.strftime("%Y-%m-%d")
            
            current_cat_total = user_df[user_df["Category"] == input_category]["Amount"].sum() if not user_df.empty else 0.0
            new_cat_total = current_cat_total + input_amount
            cat_ceiling = user_budgets.get(input_category, 200.00)
            usage_ratio = new_cat_total / cat_ceiling
            
            if usage_ratio >= 1.0:
                st.session_state.budget_alert = {
                    "type": "error",
                    "msg": f"❌ **Critical Budget Overrun!** Spending in **{input_category}** has hit **${new_cat_total:,.2f}**, blowing past the user cap of **${cat_ceiling:,.2f}**!"
                }
            elif usage_ratio >= 0.85:
                st.session_state.budget_alert = {
                    "type": "warning",
                    "msg": f"⚠️ **Budget Warning Flag!** Transaction pushes **{input_category}** to **{usage_ratio*100:.1f}%** of the profile limit."
                }
            else:
                st.session_state.budget_alert = None

            insert_expense_to_db(active_user_id, formatted_date, input_category, input_amount, input_notes)
            st.toast("Transaction logged successfully!", icon="🚀")
            st.rerun()

    # Handy New Feature Integration: Interactive Delete/Void Entry Panel
    if not user_df.empty:
        st.markdown("---")
        with st.expander("🗑️ Void / Delete Transaction"):
            # Format selection label dynamically for quick visual picking
            user_df['Selector_Text'] = user_df['Date'].dt.strftime('%m-%d') + " | " + user_df['Category'] + " | $" + user_df['Amount'].astype(str)
            delete_target = st.selectbox("Select Target Entry", options=user_df['Selector_Text'].tolist())
            
            target_id = user_df[user_df['Selector_Text'] == delete_target]['id'].values[0]
            
            if st.button("Permanently Delete Entry", type="primary"):
                delete_expense_from_db(target_id)
                st.toast("Transaction erased from registry.", icon="🗑️")
                st.rerun()

    with st.expander("🎯 Customize Profile Budgets"):
        st.caption(f"Manage threshold caps for user: **{selected_username}**")
        for cat in CATEGORIES:
            current_val = user_budgets.get(cat, 200.0)
            new_val = st.number_input(f"{cat} Limit ($)", min_value=1.0, value=float(current_val), step=10.0, key=f"adj_{cat}_{active_user_id}")
            if new_val != current_val:
                update_user_budget(active_user_id, cat, new_val)
                st.rerun()

# --- MAIN REAL-TIME DASHBOARD CORE ---
st.title("📈 Real-Time Expense Analytics Dashboard")
st.subheader(f"Active Session: `{selected_username}`")

if "budget_alert" in st.session_state and st.session_state.budget_alert is not None:
    alert = st.session_state.budget_alert
    if alert["type"] == "error":
        st.error(alert["msg"], icon="🚨")
    else:
        st.warning(alert["msg"], icon="⚠️")
    
    if st.button("Clear Alert Notification Banner"):
        st.session_state.budget_alert = None
        st.rerun()

st.markdown("---")

# 1. METRICS PRESENTATION PANEL
monthly_budget_ceiling = sum(user_budgets.values())
total_outflow = user_df["Amount"].sum() if not user_df.empty else 0.00
remaining_balance = monthly_budget_ceiling - total_outflow

kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
with kpi_col1:
    st.metric(label="Total Profile Outflow", value=f"${total_outflow:,.2f}")
with kpi_col2:
    st.metric(label="Profile Monthly Cap", value=f"${monthly_budget_ceiling:,.2f}")
with kpi_col3:
    delta_indicator = f"${remaining_balance:,.2f} Left"
    st.metric(
        label="Profile Allocation Runway", 
        value=delta_indicator,
        delta="Safe Zone" if remaining_balance >= 0 else "System Deficit",
        delta_color="normal" if remaining_balance >= 0 else "inverse"
    )

st.markdown("<br>", unsafe_allow_html=True)

# 2. DUAL INTERACTIVE VISUAL DISPLAY PANELS
layout_left_panel, layout_right_panel = st.columns([1, 1])

with layout_left_panel:
    st.subheader("📊 Category Distribution Vector")
    if not user_df.empty:
        grouped_df = user_df.groupby("Category")["Amount"].sum().reset_index()
        
        # Donut Visual construction
        donut_chart = px.pie(
            grouped_df, 
            values='Amount', 
            names='Category', 
            hole=0.48,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        
        # FIX: Explicitly forcing text visibility parameters to display categories directly
        donut_chart.update_traces(
            textinfo='label+percent', 
            textposition='outside', # Renders data indicators cleanly outside slices
            insidetextorientation='radial'
        )
        
        donut_chart.update_layout(
            margin=dict(t=30, b=30, l=30, r=30),
            showlegend=False, # Removed standard box legend as values map directly to lines now
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(donut_chart, use_container_width=True)
    else:
        st.info(f"No transactions populated yet for workspace profile: {selected_username}")

with layout_right_panel:
    st.subheader("📋 Relational Database Log View")
    if not user_df.empty:
        # Hide internal engine row IDs from front-end sheet grid layout presentation
        display_clean_df = user_df.drop(columns=['id', 'Selector_Text'], errors='ignore')
        sorted_display_df = display_clean_df.sort_values(by="Date", ascending=False).copy()
        sorted_display_df['Date'] = sorted_display_df['Date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            sorted_display_df,
            column_config={
                "Amount": st.column_config.NumberColumn("Amount ($)", format="$ %.2f"),
                "Category": st.column_config.TextColumn("Classification"),
                "Notes": st.column_config.TextColumn("Transaction Memo")
            },
            use_container_width=True,
            hide_index=True,
            height=280
        )
        
        # Handy New Feature Integration: One-Click Data Portability Export Engine
        csv_data = sorted_display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Current Ledger to CSV File",
            data=csv_data,
            file_name=f"fintrack_ledger_{selected_username}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("The SQLite data partition holds zero ledger entries for this profile.")
