
# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import sqlite3
# from datetime import datetime

# # --- CONFIGURATION & VISUAL THEME ---
# st.set_page_config(page_title="FinTrack Enterprise", page_icon="💳", layout="wide")

# st.markdown("""
#     <style>
#     div[data-testid="stMetric"] {
#         background-color: var(--secondary-background-color) !important; 
#         padding: 20px;
#         border-radius: 12px;
#         border: 1px solid rgba(128, 128, 128, 0.2) !important;
#         box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
#     }
#     div[data-testid="stMetricLabel"] > div {
#         color: var(--text-color) !important;
#         opacity: 0.7;
#         font-size: 0.95rem !important;
#     }
#     div[data-testid="stMetricValue"] > div {
#         color: var(--text-color) !important;
#         font-weight: 700 !important;
#     }
#     div[data-testid="stForm"] {
#         border: 1px solid rgba(128, 128, 128, 0.2) !important;
#         border-radius: 12px;
#         padding: 20px;
#         background-color: var(--background-color) !important;
#     }
#     </style>
# """, unsafe_allow_html=True)

# DB_FILE = "expenses_v2.db"
# CATEGORIES = ["Food", "Utilities", "Transport", "Entertainment", "Housing", "Other"]

# # --- DATABASE CONTROLLER OPERATORS ---
# def init_db():
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS expenses (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             date TEXT NOT NULL,
#             category TEXT NOT NULL,
#             amount REAL NOT NULL,
#             notes TEXT,
#             FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
#         )
#     """)
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS budgets (
#             user_id INTEGER NOT NULL,
#             category TEXT NOT NULL,
#             limit_amount REAL NOT NULL,
#             PRIMARY KEY (user_id, category),
#             FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
#         )
#     """)
    
#     cursor.execute("SELECT COUNT(*) FROM users")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute("INSERT INTO users (username) VALUES (?)", ("Primary Account",))
#         default_user_id = cursor.lastrowid
        
#         dummy_expenses = [
#             (default_user_id, "2026-06-01", "Food", 120.50, "Weekly Groceries"),
#             (default_user_id, "2026-06-05", "Utilities", 85.00, "Electric Bill"),
#             (default_user_id, "2026-06-12", "Transport", 45.00, "Fuel refill")
#         ]
#         cursor.executemany("INSERT INTO expenses (user_id, date, category, amount, notes) VALUES (?, ?, ?, ?, ?)", dummy_expenses)
        
#         default_budgets = [(default_user_id, cat, 250.00) for cat in CATEGORIES]
#         cursor.executemany("INSERT INTO budgets (user_id, category, limit_amount) VALUES (?, ?, ?)", default_budgets)
        
#     conn.commit()
#     conn.close()

# def get_all_users():
#     conn = sqlite3.connect(DB_FILE)
#     df = pd.read_sql_query("SELECT id, username FROM users", conn)
#     conn.close()
#     return dict(zip(df['username'], df['id']))

# def create_new_user(username):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     try:
#         cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
#         new_id = cursor.lastrowid
#         default_budgets = [(new_id, cat, 200.00) for cat in CATEGORIES]
#         cursor.executemany("INSERT INTO budgets (user_id, category, limit_amount) VALUES (?, ?, ?)", default_budgets)
#         conn.commit()
#         return new_id
#     except sqlite3.IntegrityError:
#         return None
#     finally:
#         conn.close()

# def load_user_expenses(user_id):
#     conn = sqlite3.connect(DB_FILE)
#     # Crucial change: pulling the actual DB record ID to facilitate deletion mapping
#     query = "SELECT id, date AS Date, category AS Category, amount AS Amount, notes AS Notes FROM expenses WHERE user_id = ?"
#     df = pd.read_sql_query(query, conn, params=(user_id,))
#     conn.close()
#     if not df.empty:
#         df['Date'] = pd.to_datetime(df['Date'])
#         df['Amount'] = pd.to_numeric(df['Amount'])
#     else:
#         df = pd.DataFrame(columns=["id", "Date", "Category", "Amount", "Notes"])
#     return df

# def load_user_budgets(user_id):
#     conn = sqlite3.connect(DB_FILE)
#     df = pd.read_sql_query("SELECT category, limit_amount FROM budgets WHERE user_id = ?", conn, params=(user_id,))
#     conn.close()
#     return dict(zip(df['category'], df['limit_amount']))

# def update_user_budget(user_id, cat, amt):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("INSERT OR REPLACE INTO budgets (user_id, category, limit_amount) VALUES (?, ?, ?)", (user_id, cat, amt))
#     conn.commit()
#     conn.close()

# def insert_expense_to_db(user_id, date_str, cat, amt, note_str):
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO expenses (user_id, date, category, amount, notes) VALUES (?, ?, ?, ?, ?)", (user_id, date_str, cat, amt, note_str))
#     conn.commit()
#     conn.close()

# def delete_expense_from_db(expense_id):
#     """Removes an operational transaction record permanently by unique system ID."""
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
#     conn.commit()
#     conn.close()

# # Start application lifecycle database verification
# init_db()

# # --- SIDEBAR: OPERATIONAL WORKSPACE CONTROL ---
# with st.sidebar:
#     st.title("👤 Account Workspace")
    
#     user_map = get_all_users()
#     user_list = list(user_map.keys())
    
#     selected_username = st.selectbox("Switch Active Profile", user_list)
#     active_user_id = user_map[selected_username]
    
#     with st.expander("👤 Register New Profile"):
#         new_user_input = st.text_input("Username", placeholder="e.g., Jane Doe").strip()
#         if st.button("Create Account Profile"):
#             if new_user_input:
#                 created_id = create_new_user(new_user_input)
#                 if created_id:
#                     st.success(f"Profile '{new_user_input}' initialized!")
#                     st.rerun()
#                 else:
#                     st.error("Username already taken.")
#             else:
#                 st.warning("Username field cannot be blank.")

#     st.markdown("---")
#     st.subheader("➕ Add Transaction")
    
#     user_df = load_user_expenses(active_user_id)
#     user_budgets = load_user_budgets(active_user_id)
    
#     with st.form("transaction_entry_form", clear_on_submit=True):
#         input_amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
#         input_category = st.selectbox("Category Allocation", CATEGORIES)
#         input_date = st.date_input("Transaction Date", datetime.now())
#         input_notes = st.text_input("Memo / Description", placeholder="e.g., Gas station")
        
#         submit_btn = st.form_submit_button("Securely Record Entry")
        
#         if submit_btn:
#             formatted_date = input_date.strftime("%Y-%m-%d")
            
#             current_cat_total = user_df[user_df["Category"] == input_category]["Amount"].sum() if not user_df.empty else 0.0
#             new_cat_total = current_cat_total + input_amount
#             cat_ceiling = user_budgets.get(input_category, 200.00)
#             usage_ratio = new_cat_total / cat_ceiling
            
#             if usage_ratio >= 1.0:
#                 st.session_state.budget_alert = {
#                     "type": "error",
#                     "msg": f"❌ **Critical Budget Overrun!** Spending in **{input_category}** has hit **${new_cat_total:,.2f}**, blowing past the user cap of **${cat_ceiling:,.2f}**!"
#                 }
#             elif usage_ratio >= 0.85:
#                 st.session_state.budget_alert = {
#                     "type": "warning",
#                     "msg": f"⚠️ **Budget Warning Flag!** Transaction pushes **{input_category}** to **{usage_ratio*100:.1f}%** of the profile limit."
#                 }
#             else:
#                 st.session_state.budget_alert = None

#             insert_expense_to_db(active_user_id, formatted_date, input_category, input_amount, input_notes)
#             st.toast("Transaction logged successfully!", icon="🚀")
#             st.rerun()

#     # Handy New Feature Integration: Interactive Delete/Void Entry Panel
#     if not user_df.empty:
#         st.markdown("---")
#         with st.expander("🗑️ Void / Delete Transaction"):
#             # Format selection label dynamically for quick visual picking
#             user_df['Selector_Text'] = user_df['Date'].dt.strftime('%m-%d') + " | " + user_df['Category'] + " | $" + user_df['Amount'].astype(str)
#             delete_target = st.selectbox("Select Target Entry", options=user_df['Selector_Text'].tolist())
            
#             target_id = user_df[user_df['Selector_Text'] == delete_target]['id'].values[0]
            
#             if st.button("Permanently Delete Entry", type="primary"):
#                 delete_expense_from_db(target_id)
#                 st.toast("Transaction erased from registry.", icon="🗑️")
#                 st.rerun()

#     with st.expander("🎯 Customize Profile Budgets"):
#         st.caption(f"Manage threshold caps for user: **{selected_username}**")
#         for cat in CATEGORIES:
#             current_val = user_budgets.get(cat, 200.0)
#             new_val = st.number_input(f"{cat} Limit ($)", min_value=1.0, value=float(current_val), step=10.0, key=f"adj_{cat}_{active_user_id}")
#             if new_val != current_val:
#                 update_user_budget(active_user_id, cat, new_val)
#                 st.rerun()

# # --- MAIN REAL-TIME DASHBOARD CORE ---
# st.title("📈 Real-Time Expense Analytics Dashboard")
# st.subheader(f"Active Session: `{selected_username}`")

# if "budget_alert" in st.session_state and st.session_state.budget_alert is not None:
#     alert = st.session_state.budget_alert
#     if alert["type"] == "error":
#         st.error(alert["msg"], icon="🚨")
#     else:
#         st.warning(alert["msg"], icon="⚠️")
    
#     if st.button("Clear Alert Notification Banner"):
#         st.session_state.budget_alert = None
#         st.rerun()

# st.markdown("---")

# # 1. METRICS PRESENTATION PANEL
# monthly_budget_ceiling = sum(user_budgets.values())
# total_outflow = user_df["Amount"].sum() if not user_df.empty else 0.00
# remaining_balance = monthly_budget_ceiling - total_outflow

# kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
# with kpi_col1:
#     st.metric(label="Total Profile Outflow", value=f"${total_outflow:,.2f}")
# with kpi_col2:
#     st.metric(label="Profile Monthly Cap", value=f"${monthly_budget_ceiling:,.2f}")
# with kpi_col3:
#     delta_indicator = f"${remaining_balance:,.2f} Left"
#     st.metric(
#         label="Profile Allocation Runway", 
#         value=delta_indicator,
#         delta="Safe Zone" if remaining_balance >= 0 else "System Deficit",
#         delta_color="normal" if remaining_balance >= 0 else "inverse"
#     )

# st.markdown("<br>", unsafe_allow_html=True)

# # 2. DUAL INTERACTIVE VISUAL DISPLAY PANELS
# layout_left_panel, layout_right_panel = st.columns([1, 1])

# with layout_left_panel:
#     st.subheader("📊 Category Distribution Vector")
#     if not user_df.empty:
#         grouped_df = user_df.groupby("Category")["Amount"].sum().reset_index()
        
#         # Donut Visual construction
#         donut_chart = px.pie(
#             grouped_df, 
#             values='Amount', 
#             names='Category', 
#             hole=0.48,
#             color_discrete_sequence=px.colors.qualitative.Safe
#         )
        
#         # FIX: Explicitly forcing text visibility parameters to display categories directly
#         donut_chart.update_traces(
#             textinfo='label+percent', 
#             textposition='outside', # Renders data indicators cleanly outside slices
#             insidetextorientation='radial'
#         )
        
#         donut_chart.update_layout(
#             margin=dict(t=30, b=30, l=30, r=30),
#             showlegend=False, # Removed standard box legend as values map directly to lines now
#             paper_bgcolor='rgba(0,0,0,0)',
#             plot_bgcolor='rgba(0,0,0,0)'
#         )
#         st.plotly_chart(donut_chart, use_container_width=True)
#     else:
#         st.info(f"No transactions populated yet for workspace profile: {selected_username}")

# with layout_right_panel:
#     st.subheader("📋 Relational Database Log View")
#     if not user_df.empty:
#         # Hide internal engine row IDs from front-end sheet grid layout presentation
#         display_clean_df = user_df.drop(columns=['id', 'Selector_Text'], errors='ignore')
#         sorted_display_df = display_clean_df.sort_values(by="Date", ascending=False).copy()
#         sorted_display_df['Date'] = sorted_display_df['Date'].dt.strftime('%Y-%m-%d')
        
#         st.dataframe(
#             sorted_display_df,
#             column_config={
#                 "Amount": st.column_config.NumberColumn("Amount ($)", format="$ %.2f"),
#                 "Category": st.column_config.TextColumn("Classification"),
#                 "Notes": st.column_config.TextColumn("Transaction Memo")
#             },
#             use_container_width=True,
#             hide_index=True,
#             height=280
#         )
        
#         # Handy New Feature Integration: One-Click Data Portability Export Engine
#         csv_data = sorted_display_df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="📥 Export Current Ledger to CSV File",
#             data=csv_data,
#             file_name=f"fintrack_ledger_{selected_username}.csv",
#             mime="text/csv",
#             use_container_width=True
#         )
#     else:
#         st.info("The SQLite data partition holds zero ledger entries for this profile.")
import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os
from datetime import datetime
from openai import OpenAI

# --- CONFIGURATION & VISUAL THEME ---
st.set_page_config(page_title="FinTrack Voice Enterprise", page_icon="🎙️", layout="wide")

st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color) !important; 
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }
    div[data-testid="stForm"] {
        border: 1px solid rgba(128, 128, 128, 0.2) !important;
        border-radius: 12px;
        padding: 20px;
        background-color: var(--background-color) !important;
    }
    .voice-box {
        background-color: rgba(79, 70, 229, 0.1);
        border: 1px solid #4f46e5;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

DB_FILE = "expenses_v2.db"
CATEGORIES = ["Food", "Utilities", "Transport", "Entertainment", "Housing", "Other"]

# --- INITIALIZE VOICE SESSION STATES ---
if "voice_state" not in st.session_state:
    st.session_state.voice_state = "GREETING"  # States: GREETING, ASK_DATE, ASK_AMOUNT, ASK_PURPOSE, ASK_REMARKS, ASK_CONFIRM
if "voice_data" not in st.session_state:
    st.session_state.voice_data = {"date": "", "amount": 0.0, "category": "", "notes": ""}

# --- DATABASE CONTROLLER OPERATORS ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, date TEXT NOT NULL,
            category TEXT NOT NULL, amount REAL NOT NULL, notes TEXT, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            user_id INTEGER NOT NULL, category TEXT NOT NULL, limit_amount REAL NOT NULL,
            PRIMARY KEY (user_id, category), FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username) VALUES (?)", ("Primary Account",))
        uid = cursor.lastrowid
        cursor.executemany("INSERT INTO expenses (user_id, date, category, amount, notes) VALUES (?, ?, ?, ?, ?)", 
                           [(uid, "2026-06-01", "Food", 120.50, "Weekly Groceries")])
        cursor.executemany("INSERT INTO budgets (user_id, category, limit_amount) VALUES (?, ?, ?)", 
                           [(uid, cat, 250.00) for cat in CATEGORIES])
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT id, username FROM users", conn)
    conn.close()
    return dict(zip(df['username'], df['id']))

def load_user_expenses(user_id):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT id, date AS Date, category AS Category, amount AS Amount, notes AS Notes FROM expenses WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Amount'] = pd.to_numeric(df['Amount'])
    return df

def load_user_budgets(user_id):
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT category, limit_amount FROM budgets WHERE user_id = ?", conn, params=(user_id,))
    conn.close()
    return dict(zip(df['category'], df['limit_amount']))

def insert_expense_to_db(user_id, date_str, cat, amt, note_str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (user_id, date, category, amount, notes) VALUES (?, ?, ?, ?, ?)", (user_id, date_str, cat, amt, note_str))
    conn.commit()
    conn.close()

init_db()

# --- NVIDIA NIM INTELLIGENT COGNITION LAYER ---
def query_nvidia_nim(system_prompt, user_text):
    """Queries NVIDIA NIM endpoint via OpenAI-standard client specs."""
    api_key = os.getenv("NVIDIA_API_KEY", st.secrets.get("NVIDIA_API_KEY", ""))
    if not api_key:
        return "ERROR: Missing NVIDIA_API_KEY"
    
    try:
        client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=api_key)
        completion = client.chat.completions.create(
            model="meta/llama-3.1-8b-instruct",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            temperature=0.1
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

def transcribe_audio_stub(audio_file):
    """
    Placeholder for ASR Transcription layer. 
    In production, replace this with a call to NVIDIA Riva Speech NIM or OpenAI Whisper API.
    """
    # For prototyping purposes, we fallback to a simple text input if transcription isn't wired.
    return st.text_input("🎙️ [ASR Simulation] Type what you would say to the app here:")

# --- APP LAYOUT NAVIGATION ---
user_map = get_all_users()
with st.sidebar:
    st.title("👤 Account Settings")
    selected_username = st.selectbox("Switch Active Profile", list(user_map.keys()))
    active_user_id = user_map[selected_username]
    user_df = load_user_expenses(active_user_id)
    user_budgets = load_user_budgets(active_user_id)

# --- VOICE ASSISTANT PIPELINE GRID PANEL ---
st.title("📈 Real-Time Voice Intelligence Dashboard")
st.markdown("---")

st.subheader("🎙️ FinTrack Voice Assistant Portal")

# State-driven conversational prompt messages
prompts_map = {
    "GREETING": "Hello! Would you like to add new transaction details? (Say: 'Yes' or 'No')",
    "ASK_DATE": "Perfect. What is the **Date** of this transaction? (e.g., 'Today', 'Yesterday', or 'June 22nd')",
    "ASK_AMOUNT": "Got it. What is the expenditure **Amount** in dollars?",
    "ASK_PURPOSE": f"What is the **Purpose/Category** of this expense? Choose from: {', '.join(CATEGORIES)}",
    "ASK_REMARKS": "Understood. Please state any **Remarks or Description** for this entry.",
    "ASK_CONFIRM": "All details collected! Say **'Save'** to log this entry, or **'Add More'** to append another transaction to this same day."
}

st.markdown(f"<div class='voice-box'><h4>🤖 Assistant: {prompts_map[st.session_state.voice_state]}</h4></div>", unsafe_allow_html=True)

# Audio Input Module Integration
voice_audio = st.audio_input("Record your voice command input:")
simulated_text = transcribe_audio_stub(voice_audio)

if st.button("🚀 Submit Voice Command", use_container_width=True):
    user_speech_text = simulated_text.strip() if simulated_text else ""
    
    if user_speech_text:
        current_state = st.session_state.voice_state
        
        if current_state == "GREETING":
            sys_p = "Analyze the text response. If the user intends to add a new transaction or says yes, reply with 'YES'. Otherwise, reply with 'NO'."
            res = query_nvidia_nim(sys_p, user_speech_text)
            if "YES" in res.upper():
                st.session_state.voice_state = "ASK_DATE"
            st.rerun()
            
        elif current_state == "ASK_DATE":
            sys_p = f"Extract the date from the text and output it strictly in YYYY-MM-DD format. Today is {datetime.now().strftime('%Y-%m-%d')}. Year is 2026. Return ONLY the YYYY-MM-DD string."
            res = query_nvidia_nim(sys_p, user_speech_text)
            st.session_state.voice_data["date"] = res
            st.session_state.voice_state = "ASK_AMOUNT"
            st.rerun()
            
        elif current_state == "ASK_AMOUNT":
            sys_p = "Extract the numerical value/amount from the text sentence. Return ONLY the raw number value as a float (e.g., 45.00). Do not include dollar symbols."
            res = query_nvidia_nim(sys_p, user_speech_text)
            try:
                st.session_state.voice_data["amount"] = float(res)
                st.session_state.voice_state = "ASK_PURPOSE"
            except:
                st.error(f"Could not parse numerical value from: {res}. Please try stating the amount clearly again.")
            st.rerun()
            
        elif current_state == "ASK_PURPOSE":
            sys_p = f"Classify the input into exactly one of these categories: {', '.join(CATEGORIES)}. Return ONLY the exact category name."
            res = query_nvidia_nim(sys_p, user_speech_text)
            matched_cat = next((c for c in CATEGORIES if c.lower() in res.lower()), "Other")
            st.session_state.voice_data["category"] = matched_cat
            st.session_state.voice_state = "ASK_REMARKS"
            st.rerun()
            
        elif current_state == "ASK_REMARKS":
            st.session_state.voice_data["notes"] = user_speech_text
            st.session_state.voice_state = "ASK_CONFIRM"
            st.rerun()
            
        elif current_state == "ASK_CONFIRM":
            sys_p = "Analyze the input phrase. If the user explicitly says 'add more' or 'more', reply with 'ADD_MORE'. If they say 'save' or confirm, reply with 'SAVE'."
            res = query_nvidia_nim(sys_p, user_speech_text)
            
            # Persist data on confirmation triggers
            v_data = st.session_state.voice_data
            insert_expense_to_db(active_user_id, v_data["date"], v_data["category"], v_data["amount"], v_data["notes"])
            
            if "ADD_MORE" in res.upper():
                # Retain date matrix scope, reset metadata parameters for immediate sequential entry
                st.session_state.voice_data = {"date": v_data["date"], "amount": 0.0, "category": "", "notes": ""}
                st.session_state.voice_state = "ASK_AMOUNT"
                st.toast("Transaction recorded! Keeping current date workspace open.", icon="📝")
            else:
                # Absolute system baseline reset returning to idle pool
                st.session_state.voice_data = {"date": "", "amount": 0.0, "category": "", "notes": ""}
                st.session_state.voice_state = "GREETING"
                st.toast("Transaction safely committed to permanent ledger!", icon="🔒")
            st.rerun()

# Display real-time form preview context mapping
with st.expander("📝 Live Transaction Form Status Mirror", expanded=True):
    v_form = st.session_state.voice_data
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.text_input("Date Stamp", value=v_form["date"], disabled=True)
    col_b.number_input("Amount ($)", value=v_form["amount"], disabled=True)
    col_c.text_input("Category Classification", value=v_form["category"], disabled=True)
    col_d.text_input("Remarks Memo", value=v_form["notes"], disabled=True)

st.markdown("---")

# --- DATA RENDERING GRAPHS MATRIX ---
layout_left_panel, layout_right_panel = st.columns([1, 1])
with layout_left_panel:
    st.subheader("📊 Category Distribution Vector")
    if not user_df.empty:
        grouped_df = user_df.groupby("Category")["Amount"].sum().reset_index()
        donut_chart = px.pie(grouped_df, values='Amount', names='Category', hole=0.48, color_discrete_sequence=px.colors.qualitative.Safe)
        donut_chart.update_traces(textinfo='label+percent', textposition='outside')
        donut_chart.update_layout(margin=dict(t=30, b=30, l=30, r=30), showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="gray"))
        st.plotly_chart(donut_chart, use_container_width=True)
    else:
        st.info("No logs populated yet.")

with layout_right_panel:
    st.subheader("📋 Relational Database Log View")
    if not user_df.empty:
        sorted_display_df = user_df.sort_values(by="Date", ascending=False).copy()
        sorted_display_df['Date'] = sorted_display_df['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(sorted_display_df.drop(columns=['id'], errors='ignore'), column_config={"Amount": st.column_config.NumberColumn("Amount ($)", format="$ %.2f")}, use_container_width=True, hide_index=True, height=280)
