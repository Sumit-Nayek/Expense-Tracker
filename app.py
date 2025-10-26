import streamlit as st
import pandas as pd
import datetime
import os

# Page config
st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# File path for CSV
CSV_FILE = "expenses.csv"

# Function to load data
@st.cache_data
def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["category", "amount", "date"])

# Function to save data
def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# Main app
def main():
    st.title("💰 Expense Tracker")
    st.markdown("A simple web app to manage your expenses using CSV storage.")

    # Load data
    df = load_data()

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.selectbox("Choose action:", 
                                ["Add Expense", "View Expenses", "Total Expenses", 
                                 "Delete Expense", "Edit Expense", "Sum by Category", 
                                 "Sort by Date", "Search by Category"])

    if menu == "Add Expense":
        st.header("Add New Expense")
        col1, col2 = st.columns(2)
        with col1:
            category = st.text_input("Category (e.g., Food, Travel):")
        with col2:
            amount = st.number_input("Amount ($):", min_value=0.01, step=0.01)
        
        date = datetime.date.today().strftime("%Y-%m-%d")  # Auto date
        st.info(f"Date: {date} (auto-set)")

        if st.button("Add Expense"):
            if category:
                new_row = pd.DataFrame({
                    "category": [category],
                    "amount": [amount],
                    "date": [date]
                })
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("Expense added successfully!")
                st.rerun()
            else:
                st.error("Please enter a category.")

    elif menu == "View Expenses":
        st.header("All Expenses")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No expenses recorded yet.")

    elif menu == "Total Expenses":
        st.header("Total Expenses")
        if not df.empty:
            total = df["amount"].sum()
            st.metric("Total Amount", f"${total:.2f}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Expenses Count", len(df))
            col2.metric("Avg Amount", f"${df['amount'].mean():.2f}")
            col3.metric("Max Expense", f"${df['amount'].max():.2f}")
        else:
            st.info("No expenses to calculate.")

    elif menu == "Delete Expense":
        st.header("Delete Expense")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            index = st.number_input("Enter row number to delete (1-based):", 
                                    min_value=1, max_value=len(df), step=1)
            if st.button("Delete"):
                df = df.drop(index - 1).reset_index(drop=True)
                save_data(df)
                st.success("Expense deleted!")
                st.rerun()
        else:
            st.info("No expenses to delete.")

    elif menu == "Edit Expense":
        st.header("Edit Expense")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            index = st.number_input("Enter row number to edit (1-based):", 
                                    min_value=1, max_value=len(df), step=1)
            if index <= len(df):
                row = df.iloc[index - 1]
                col1, col2 = st.columns(2)
                with col1:
                    new_category = st.text_input("New Category:", value=str(row["category"]))
                with col2:
                    new_amount = st.number_input("New Amount ($):", value=float(row["amount"]), step=0.01)
                new_date = st.date_input("New Date:", value=pd.to_datetime(row["date"]))
                
                if st.button("Update"):
                    df.at[index - 1, "category"] = new_category
                    df.at[index - 1, "amount"] = new_amount
                    df.at[index - 1, "date"] = new_date.strftime("%Y-%m-%d")
                    save_data(df)
                    st.success("Expense updated!")
                    st.rerun()
        else:
            st.info("No expenses to edit.")

    elif menu == "Sum by Category":
        st.header("Expenses by Category")
        if not df.empty:
            category_sums = df.groupby("category")["amount"].sum().reset_index()
            st.dataframe(category_sums, use_container_width=True)
            total = category_sums["amount"].sum()
            st.metric("Grand Total", f"${total:.2f}")
        else:
            st.info("No expenses.")

    elif menu == "Sort by Date":
        st.header("Sort Expenses by Date")
        if not df.empty:
            sorted_df = df.sort_values("date").reset_index(drop=True)
            st.dataframe(sorted_df, use_container_width=True)
            if st.button("Apply Sort"):
                df = sorted_df
                save_data(df)
                st.success("Expenses sorted and saved!")
                st.rerun()
        else:
            st.info("No expenses.")

    elif menu == "Search by Category":
        st.header("Search Expenses")
        search_category = st.text_input("Enter category to search:")
        if search_category:
            filtered = df[df["category"].str.contains(search_category, case=False, na=False)]
            if not filtered.empty:
                st.dataframe(filtered, use_container_width=True)
            else:
                st.info("No expenses found.")
        else:
            st.info("Enter a category to search.")

if __name__ == "__main__":
    main()