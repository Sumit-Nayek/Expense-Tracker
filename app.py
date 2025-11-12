# app.py
import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

CSV_FILE = "expenses.csv"

# Initialize session state
if "df" not in st.session_state:
    if os.path.exists(CSV_FILE):
        st.session_state.df = pd.read_csv(CSV_FILE)
    else:
        st.session_state.df = pd.DataFrame(columns=["category", "amount", "date"])
        st.session_state.df.to_csv(CSV_FILE, index=False)

df = st.session_state.df

def save_and_rerun():
    st.session_state.df.to_csv(CSV_FILE, index=False)
    st.rerun()

# UI
st.title("💰 Expense Tracker")
st.caption(f"{len(df)} expense(s) in `{CSV_FILE}`")

menu = st.sidebar.selectbox("Action", [
    "Add Expense", "View", "Total", "Delete", "Edit",
    "By Category", "Sort by Date", "Search"
])

# ADD EXPENSE SECTION
if menu == "Add Expense":
    st.subheader("Add New Expense")
    
    col1, col2 = st.columns(2)
    with col1:
        cat = st.text_input("Category", placeholder="e.g., Food, Transport, Shopping")
    with col2:
        amt = st.number_input("Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
    
    # Date selection with default as current date
    st.write("### Date Selection")
    date_option = st.radio(
        "Choose date:",
        ["Use Today's Date", "Select Specific Date"],
        horizontal=True
    )
    
    if date_option == "Use Today's Date":
        selected_date = datetime.date.today()
        st.info(f"📅 Using today's date: **{selected_date.strftime('%Y-%m-%d')}**")
    else:
        selected_date = st.date_input(
            "Select Expense Date",
            value=datetime.date.today(),
            max_value=datetime.date.today()
        )
        st.success(f"📅 Selected date: **{selected_date.strftime('%Y-%m-%d')}**")

    if st.button("💾 Add Expense", type="primary"):
        if not cat.strip():
            st.error("❌ Please enter a category name")
        elif amt <= 0:
            st.error("❌ Please enter a valid amount")
        else:
            new_row = pd.DataFrame({
                "category": [cat.strip()],
                "amount": [amt],
                "date": [selected_date.strftime("%Y-%m-%d")]
            })
            st.session_state.df = pd.concat([df, new_row], ignore_index=True) if not df.empty else new_row
            save_and_rerun()
            st.success("✅ Expense added successfully!")

# VIEW ALL EXPENSES
elif menu == "View":
    st.subheader("All Expenses")
    if df.empty:
        st.info("📝 No expenses recorded yet. Add your first expense!")
    else:
        # Format the dataframe for better display
        display_df = df.copy()
        display_df['amount'] = display_df['amount'].apply(lambda x: f"₹{x:,.2f}")
        st.dataframe(display_df, use_container_width=True)
        
        # Quick summary
        total_amount = df['amount'].sum()
        st.info(f"💡 Total amount across all expenses: **₹{total_amount:,.2f}**")

# TOTAL SUMMARY
elif menu == "Total":
    st.subheader("Expense Summary")
    if df.empty:
        st.info("📊 No data available for summary")
    else:
        total = df["amount"].sum()
        st.metric("💰 Total Expenses", f"₹{total:,.2f}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("📋 Count", len(df))
        c2.metric("📊 Average", f"₹{df['amount'].mean():.2f}")
        c3.metric("📈 Maximum", f"₹{df['amount'].max():.2f}")

# DELETE EXPENSE
elif menu == "Delete":
    st.subheader("Delete Expense")
    if df.empty:
        st.info("🗑️ Nothing to delete")
    else:
        st.dataframe(df, use_container_width=True)
        st.warning("⚠️ Be careful - this action cannot be undone!")
        
        idx = st.number_input("Enter Row Number to Delete (starting from 1)", 
                            min_value=1, max_value=len(df), step=1)
        
        if st.button("🗑️ Delete Selected Row", type="primary"):
            deleted_expense = df.iloc[idx-1]
            st.session_state.df = df.drop(index=idx-1).reset_index(drop=True)
            save_and_rerun()
            st.success(f"✅ Deleted expense: {deleted_expense['category']} - ₹{deleted_expense['amount']:.2f}")

# EDIT EXPENSE
elif menu == "Edit":
    st.subheader("Edit Expense")
    if df.empty:
        st.info("✏️ Nothing to edit")
    else:
        st.dataframe(df, use_container_width=True)
        idx = st.number_input("Select Row Number to Edit", 1, len(df), step=1)
        
        if idx <= len(df):
            row = df.iloc[idx-1]
            st.success(f"Editing: **{row['category']}** - ₹{row['amount']:.2f} on {row['date']}")
            
            col1, col2 = st.columns(2)
            with col1:
                new_cat = st.text_input("Category", value=row["category"])
            with col2:
                new_amt = st.number_input("Amount (₹)", value=float(row["amount"]), 
                                        min_value=0.01, step=0.01, format="%.2f")
            
            # Date selection for editing
            st.write("### Update Date")
            current_date = pd.to_datetime(row["date"]).date()
            date_option_edit = st.radio(
                "Choose date option:",
                ["Keep Current Date", "Select New Date"],
                horizontal=True,
                key="edit_date"
            )
            
            if date_option_edit == "Keep Current Date":
                new_date = current_date
                st.info(f"📅 Keeping current date: **{current_date.strftime('%Y-%m-%d')}**")
            else:
                new_date = st.date_input(
                    "Select New Date",
                    value=current_date,
                    max_value=datetime.date.today(),
                    key="new_date_picker"
                )
                st.success(f"📅 New date selected: **{new_date.strftime('%Y-%m-%d')}**")
            
            if st.button("💾 Update Expense", type="primary"):
                if not new_cat.strip():
                    st.error("❌ Please enter a category name")
                else:
                    st.session_state.df.at[idx-1, "category"] = new_cat.strip()
                    st.session_state.df.at[idx-1, "amount"] = new_amt
                    st.session_state.df.at[idx-1, "date"] = new_date.strftime("%Y-%m-%d")
                    save_and_rerun()
                    st.success("✅ Expense updated successfully!")

# EXPENSES BY CATEGORY
elif menu == "By Category":
    st.subheader("Expenses by Category")
    if df.empty:
        st.info("📊 No data available for category analysis")
    else:
        category_sums = df.groupby("category")["amount"].sum().reset_index()
        category_sums = category_sums.sort_values("amount", ascending=False)
        
        # Format amounts with ₹ symbol
        display_sums = category_sums.copy()
        display_sums['amount'] = display_sums['amount'].apply(lambda x: f"₹{x:,.2f}")
        
        st.dataframe(display_sums, use_container_width=True)
        
        total_all_categories = category_sums['amount'].sum()
        st.metric("💰 Total Across All Categories", f"₹{total_all_categories:,.2f}")

# SORT BY DATE
elif menu == "Sort by Date":
    st.subheader("Expenses Sorted by Date")
    if df.empty:
        st.info("📅 No data available to sort")
    else:
        sorted_df = df.sort_values("date", ascending=False).reset_index(drop=True)
        
        # Format for display
        display_sorted = sorted_df.copy()
        display_sorted['amount'] = display_sorted['amount'].apply(lambda x: f"₹{x:,.2f}")
        
        st.dataframe(display_sorted, use_container_width=True)
        
        if st.button("💾 Save This Sorting", type="primary"):
            st.session_state.df = sorted_df
            save_and_rerun()
            st.success("✅ Expenses permanently sorted by date!")

# SEARCH EXPENSES
elif menu == "Search":
    st.subheader("Search Expenses")
    search_term = st.text_input("🔍 Enter category name to search", 
                               placeholder="e.g., food, transport, etc.")
    
    if search_term and not df.empty:
        # Case-insensitive search
        search_results = df[df['category'].str.contains(search_term, case=False, na=False)]
        
        if not search_results.empty:
            st.success(f"✅ Found {len(search_results)} matching expense(s)")
            
            # Format for display
            display_results = search_results.copy()
            display_results['amount'] = display_results['amount'].apply(lambda x: f"₹{x:,.2f}")
            
            st.dataframe(display_results, use_container_width=True)
            
            # Summary of search results
            total_search = search_results['amount'].sum()
            st.info(f"💰 Total amount in search results: **₹{total_search:,.2f}**")
        else:
            st.warning("❌ No expenses found matching your search term")
    elif df.empty:
        st.info("📝 No expenses available to search")
    else:
        st.info("💡 Enter a search term to find specific expenses")

# Footer with helpful information
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Quick Tips")
st.sidebar.info(
    "- Use **Today's Date** for current expenses\n"
    "- Select **Specific Date** for past expenses\n"
    "- All amounts are in **Indian Rupees (₹)**\n"
    "- Data is automatically saved to CSV file"
)

st.sidebar.markdown("### 📊 Data Status")
if not df.empty:
    total_expenses = df['amount'].sum()
    st.sidebar.success(f"Total Expenses: ₹{total_expenses:,.2f}")
    st.sidebar.info(f"Records: {len(df)}")
else:
    st.sidebar.warning("No expenses recorded")
