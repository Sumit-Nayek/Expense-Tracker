# app.py
import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Expense Tracker", page_icon="Money Bag", layout="wide")

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
st.title("Expense Tracker")
st.caption(f"{len(df)} expense(s) in `{CSV_FILE}`")

menu = st.sidebar.selectbox("Action", [
    "Add Expense", "View", "Total", "Delete", "Edit",
    "By Category", "Sort by Date", "Search"
])

# ADD
if menu == "Add Expense":
    st.subheader("Add New Expense")
    col1, col2 = st.columns(2)
    with col1:
        cat = st.text_input("Category")
    with col2:
        amt = st.number_input("Amount ($)", min_value=0.01, step=0.01)
    today = datetime.date.today().strftime("%Y-%m-%d")
    st.info(f"Date: **{today}**")

    if st.button("Add Expense"):
        if not cat.strip():
            st.error("Enter a category")
        else:
            new_row = pd.DataFrame({
                "category": [cat],
                "amount": [amt],
                "date": [today]
            })
            st.session_state.df = pd.concat([df, new_row], ignore_index=True) if not df.empty else new_row
            save_and_rerun()
            st.success("Added!")

# VIEW
elif menu == "View":
    st.subheader("All Expenses")
    if df.empty:
        st.info("No expenses yet.")
    else:
        st.dataframe(df, use_container_width=True)

# TOTAL
elif menu == "Total":
    st.subheader("Summary")
    if df.empty:
        st.info("No data")
    else:
        total = df["amount"].sum()
        st.metric("Total", f"${total:,.2f}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Count", len(df))
        c2.metric("Avg", f"${df['amount'].mean():.2f}")
        c3.metric("Max", f"${df['amount'].max():.2f}")

# DELETE
elif menu == "Delete":
    st.subheader("Delete Row")
    if df.empty:
        st.info("Nothing to delete")
    else:
        st.dataframe(df, use_container_width=True)
        idx = st.number_input("Row # (1-based)", 1, len(df), step=1)
        if st.button("Delete"):
            st.session_state.df = df.drop(index=idx-1).reset_index(drop=True)
            save_and_rerun()

# EDIT
elif menu == "Edit":
    st.subheader("Edit Row")
    if df.empty:
        st.info("Nothing to edit")
    else:
        st.dataframe(df, use_container_width=True)
        idx = st.number_input("Row #", 1, len(df), step=1)
        row = df.iloc[idx-1]
        c1, c2 = st.columns(2)
        with c1:
            new_cat = st.text_input("Category", value=row["category"])
        with c2:
            new_amt = st.number_input("Amount", value=float(row["amount"]), step=0.01)
        new_date = st.date_input("Date", value=pd.to_datetime(row["date"]))
        if st.button("Update"):
            st.session_state.df.at[idx-1, "category"] = new_cat
            st.session_state.df.at[idx-1, "amount"] = new_amt
            st.session_state.df.at[idx-1, "date"] = new_date.strftime("%Y-%m-%d")
            save_and_rerun()

# BY CATEGORY
elif menu == "By Category":
    st.subheader("By Category")
    if df.empty:
        st.info("No data")
    else:
        sums = df.groupby("category")["amount"].sum().reset_index()
        st.dataframe(sums, use_container_width=True)
        st.metric("Total", f"${sums['amount'].sum():,.2f}")

# SORT BY DATE
elif menu == "Sort by Date":
    st.subheader("Sorted by Date")
    if df.empty:
        st.info("No data")
    else:
        sorted_df = df.sort_values("date").reset_index(drop=True)
        st.dataframe(sorted_df, use_container_width=True)
        if st.button("Save Sorted"):
            st.session_state.df = sorted_df
            save_and_rerun()

# SEARCH
elif menu == "Search":
    st.subheader("Search by Category")
    term = st.text_input("Keyword")
    if term and not df.empty:
        hits = df[df["category"].str.contains(term, case=False, na=False)]
        st.dataframe(hits if not hits.empty else pd.DataFrame(), use_container_width=True)
    else:
        st.info("Enter a term")
