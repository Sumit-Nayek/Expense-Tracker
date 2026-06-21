# # app.py
# import streamlit as st
# import pandas as pd
# import datetime
# import os

# st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# CSV_FILE = "expenses.csv"

# # Initialize session state
# if "df" not in st.session_state:
#     if os.path.exists(CSV_FILE):
#         st.session_state.df = pd.read_csv(CSV_FILE)
#     else:
#         st.session_state.df = pd.DataFrame(columns=["category", "amount", "date"])
#         st.session_state.df.to_csv(CSV_FILE, index=False)

# df = st.session_state.df

# def save_and_rerun():
#     st.session_state.df.to_csv(CSV_FILE, index=False)
#     st.rerun()

# # UI
# st.title("💰 Expense Tracker")
# st.caption(f"{len(df)} expense(s) in `{CSV_FILE}`")

# menu = st.sidebar.selectbox("Action", [
#     "Add Expense", "View", "Total", "Delete", "Edit",
#     "By Category", "Sort by Date", "Search"
# ])

# # ADD EXPENSE SECTION
# if menu == "Add Expense":
#     st.subheader("Add New Expense")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         cat = st.text_input("Category", placeholder="e.g., Food, Transport, Shopping")
#     with col2:
#         amt = st.number_input("Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
    
#     # Date selection with default as current date
#     st.write("### Date Selection")
#     date_option = st.radio(
#         "Choose date:",
#         ["Use Today's Date", "Select Specific Date"],
#         horizontal=True
#     )
    
#     if date_option == "Use Today's Date":
#         selected_date = datetime.date.today()
#         st.info(f"📅 Using today's date: **{selected_date.strftime('%Y-%m-%d')}**")
#     else:
#         selected_date = st.date_input(
#             "Select Expense Date",
#             value=datetime.date.today(),
#             max_value=datetime.date.today()
#         )
#         st.success(f"📅 Selected date: **{selected_date.strftime('%Y-%m-%d')}**")

#     if st.button("💾 Add Expense", type="primary"):
#         if not cat.strip():
#             st.error("❌ Please enter a category name")
#         elif amt <= 0:
#             st.error("❌ Please enter a valid amount")
#         else:
#             new_row = pd.DataFrame({
#                 "category": [cat.strip()],
#                 "amount": [amt],
#                 "date": [selected_date.strftime("%Y-%m-%d")]
#             })
#             st.session_state.df = pd.concat([df, new_row], ignore_index=True) if not df.empty else new_row
#             save_and_rerun()
#             st.success("✅ Expense added successfully!")

# # VIEW ALL EXPENSES
# elif menu == "View":
#     st.subheader("All Expenses")
#     if df.empty:
#         st.info("📝 No expenses recorded yet. Add your first expense!")
#     else:
#         # Format the dataframe for better display
#         display_df = df.copy()
#         display_df['amount'] = display_df['amount'].apply(lambda x: f"₹{x:,.2f}")
#         st.dataframe(display_df, use_container_width=True)
        
#         # Quick summary
#         total_amount = df['amount'].sum()
#         st.info(f"💡 Total amount across all expenses: **₹{total_amount:,.2f}**")

# # TOTAL SUMMARY
# elif menu == "Total":
#     st.subheader("Expense Summary")
#     if df.empty:
#         st.info(" No data available for summary")
#     else:
#         total = df["amount"].sum()
#         st.metric("💰 Total Expenses", f"₹{total:,.2f}")
        
#         c1, c2, c3 = st.columns(3)
#         c1.metric("📋 Count", len(df))
#         c2.metric(" Average", f"₹{df['amount'].mean():.2f}")
#         c3.metric("📈 Maximum", f"₹{df['amount'].max():.2f}")

# # DELETE EXPENSE
# elif menu == "Delete":
#     st.subheader("Delete Expense")
#     if df.empty:
#         st.info("🗑️ Nothing to delete")
#     else:
#         st.dataframe(df, use_container_width=True)
#         st.warning("⚠️ Be careful - this action cannot be undone!")
        
#         idx = st.number_input("Enter Row Number to Delete (starting from 1)", 
#                             min_value=1, max_value=len(df), step=1)
        
#         if st.button("🗑️ Delete Selected Row", type="primary"):
#             deleted_expense = df.iloc[idx-1]
#             st.session_state.df = df.drop(index=idx-1).reset_index(drop=True)
#             save_and_rerun()
#             st.success(f"✅ Deleted expense: {deleted_expense['category']} - ₹{deleted_expense['amount']:.2f}")

# # EDIT EXPENSE
# elif menu == "Edit":
#     st.subheader("Edit Expense")
#     if df.empty:
#         st.info("✏️ Nothing to edit")
#     else:
#         st.dataframe(df, use_container_width=True)
#         idx = st.number_input("Select Row Number to Edit", 1, len(df), step=1)
        
#         if idx <= len(df):
#             row = df.iloc[idx-1]
#             st.success(f"Editing: **{row['category']}** - ₹{row['amount']:.2f} on {row['date']}")
            
#             col1, col2 = st.columns(2)
#             with col1:
#                 new_cat = st.text_input("Category", value=row["category"])
#             with col2:
#                 new_amt = st.number_input("Amount (₹)", value=float(row["amount"]), 
#                                         min_value=0.01, step=0.01, format="%.2f")
            
#             # Date selection for editing
#             st.write("### Update Date")
#             current_date = pd.to_datetime(row["date"]).date()
#             date_option_edit = st.radio(
#                 "Choose date option:",
#                 ["Keep Current Date", "Select New Date"],
#                 horizontal=True,
#                 key="edit_date"
#             )
            
#             if date_option_edit == "Keep Current Date":
#                 new_date = current_date
#                 st.info(f"📅 Keeping current date: **{current_date.strftime('%Y-%m-%d')}**")
#             else:
#                 new_date = st.date_input(
#                     "Select New Date",
#                     value=current_date,
#                     max_value=datetime.date.today(),
#                     key="new_date_picker"
#                 )
#                 st.success(f"📅 New date selected: **{new_date.strftime('%Y-%m-%d')}**")
            
#             if st.button("💾 Update Expense", type="primary"):
#                 if not new_cat.strip():
#                     st.error("❌ Please enter a category name")
#                 else:
#                     st.session_state.df.at[idx-1, "category"] = new_cat.strip()
#                     st.session_state.df.at[idx-1, "amount"] = new_amt
#                     st.session_state.df.at[idx-1, "date"] = new_date.strftime("%Y-%m-%d")
#                     save_and_rerun()
#                     st.success("✅ Expense updated successfully!")

# # EXPENSES BY CATEGORY
# elif menu == "By Category":
#     st.subheader("Expenses by Category")
#     if df.empty:
#         st.info(" No data available for category analysis")
#     else:
#         category_sums = df.groupby("category")["amount"].sum().reset_index()
#         category_sums = category_sums.sort_values("amount", ascending=False)
        
#         # Format amounts with ₹ symbol
#         display_sums = category_sums.copy()
#         display_sums['amount'] = display_sums['amount'].apply(lambda x: f"₹{x:,.2f}")
        
#         st.dataframe(display_sums, use_container_width=True)
        
#         total_all_categories = category_sums['amount'].sum()
#         st.metric("💰 Total Across All Categories", f"₹{total_all_categories:,.2f}")

# # SORT BY DATE
# elif menu == "Sort by Date":
#     st.subheader("Expenses Sorted by Date")
#     if df.empty:
#         st.info("📅 No data available to sort")
#     else:
#         sorted_df = df.sort_values("date", ascending=False).reset_index(drop=True)
        
#         # Format for display
#         display_sorted = sorted_df.copy()
#         display_sorted['amount'] = display_sorted['amount'].apply(lambda x: f"₹{x:,.2f}")
        
#         st.dataframe(display_sorted, use_container_width=True)
        
#         if st.button("💾 Save This Sorting", type="primary"):
#             st.session_state.df = sorted_df
#             save_and_rerun()
#             st.success("✅ Expenses permanently sorted by date!")

# # SEARCH EXPENSES
# elif menu == "Search":
#     st.subheader("Search Expenses")
#     search_term = st.text_input("🔍 Enter category name to search", 
#                                placeholder="e.g., food, transport, etc.")
    
#     if search_term and not df.empty:
#         # Case-insensitive search
#         search_results = df[df['category'].str.contains(search_term, case=False, na=False)]
        
#         if not search_results.empty:
#             st.success(f"✅ Found {len(search_results)} matching expense(s)")
            
#             # Format for display
#             display_results = search_results.copy()
#             display_results['amount'] = display_results['amount'].apply(lambda x: f"₹{x:,.2f}")
            
#             st.dataframe(display_results, use_container_width=True)
            
#             # Summary of search results
#             total_search = search_results['amount'].sum()
#             st.info(f"💰 Total amount in search results: **₹{total_search:,.2f}**")
#         else:
#             st.warning("❌ No expenses found matching your search term")
#     elif df.empty:
#         st.info("📝 No expenses available to search")
#     else:
#         st.info("💡 Enter a search term to find specific expenses")

# # Footer with helpful information
# st.sidebar.markdown("---")
# st.sidebar.markdown("### 💡 Quick Tips")
# st.sidebar.info(
#     "- Use **Today's Date** for current expenses\n"
#     "- Select **Specific Date** for past expenses\n"
#     "- All amounts are in **Indian Rupees (₹)**\n"
#     "- Data is automatically saved to CSV file"
# )

# st.sidebar.markdown("###  Data Status")
# if not df.empty:
#     total_expenses = df['amount'].sum()
#     st.sidebar.success(f"Total Expenses: ₹{total_expenses:,.2f}")
#     st.sidebar.info(f"Records: {len(df)}")
# else:
#     st.sidebar.warning("No expenses recorded")
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime

# --- CONFIGURATION & VISUAL THEME ---
st.set_page_config(page_title="FinTrack Enterprise", page_icon="💳", layout="wide")

# AUTOMATIC SYSTEM MODE: Leveraging native Streamlit CSS variables
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

DB_FILE = "expenses.db"
CATEGORIES = ["Food", "Utilities", "Transport", "Entertainment", "Housing", "Other"]

# --- DATABASE CONTROLLER OPERATORS ---
def init_db():
    """Initializes multi-tenant tables and auto-migrates old single-user schemas if detected."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # --- AUTO-MIGRATION CHECK ---
    # Inspect the current columns in the expenses table if it exists
    cursor.execute("PRAGMA table_info(expenses)")
    existing_columns = [col[1] for col in cursor.fetchall()]
    
    # If the table exists but doesn't have 'user_id', drop the legacy structure
    if existing_columns and "user_id" not in existing_columns:
        cursor.execute("DROP TABLE IF EXISTS expenses")
        cursor.execute("DROP TABLE IF EXISTS budgets")
        conn.commit()
    
    # 1. Users Table Schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL
        )
    """)
    
    # 2. Expenses Table Schema (Linked to User via Foreign Key)
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
    
    # 3. Budget Table Schema (Composite Key unique per User per Category)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            limit_amount REAL NOT NULL,
            PRIMARY KEY (user_id, category),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    
    # Seed default user profile if database is entirely empty
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
        # Automatically generate baseline starting budgets for the new profile
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
    query = "SELECT date AS Date, category AS Category, amount AS Amount, notes AS Notes FROM expenses WHERE user_id = ?"
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Amount'] = pd.to_numeric(df['Amount'])
    else:
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Notes"])
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

# Initialize Database Pipeline Configuration
init_db()

# --- SIDEBAR: USER AUTHENTICATION ROUTER ---
with st.sidebar:
    st.title("👤 Account Workspace")
    
    user_map = get_all_users()
    user_list = list(user_map.keys())
    
    # User Profile Switcher Dropdown Menu
    selected_username = st.selectbox("Switch Active Profile", user_list)
    active_user_id = user_map[selected_username]
    
    # Expandable Form Panel to Add a New Family Member/Client
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
    
    # Pull contextual information mapped precisely to this specific user profile
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
            
            # Isolated warning verification checks calculated strictly on active user profile
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

    # Expandable user isolated Target Configuration customizer drawer
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

# Render active warning notifications
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

# 1. PROFILE CONTEXT PERFORMANCE METRICS
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

# 2. ISOLATED PROFILE METRIC PANELS
layout_left_panel, layout_right_panel = st.columns([1, 1])

with layout_left_panel:
    st.subheader("📊 Category Distribution Vector")
    if not user_df.empty:
        grouped_df = user_df.groupby("Category")["Amount"].sum().reset_index()
        donut_chart = px.pie(
            grouped_df, 
            values='Amount', 
            names='Category', 
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        donut_chart.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="gray")
        )
        st.plotly_chart(donut_chart, use_container_width=True)
    else:
        st.info(f"No transactions populated yet for workspace profile: {selected_username}")

with layout_right_panel:
    st.subheader("📋 Relational Database Log View")
    if not user_df.empty:
        sorted_display_df = user_df.sort_values(by="Date", ascending=False).copy()
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
            height=340
        )
    else:
        st.info("The SQLite data partition holds zero ledger entries for this profile.")
