# app.py
import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Expense Tracker", page_icon="Money Bag", layout="wide")

CSV_FILE = "expenses.csv"          # <-- must be in the repo root

# ------------------------------------------------------------------
# 1. Load (and create if missing)
# ------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_FILE):
        # First run → create empty CSV with header
        empty = pd.DataFrame(columns=["category", "amount", "date"])
        empty.to_csv(CSV_FILE, index=False)
        st.toast("Created empty expenses.csv")
    return pd.read_csv(CSV_FILE)

# ------------------------------------------------------------------
# 2. Save
# ------------------------------------------------------------------
def save_data(df: pd.DataFrame):
    df.to_csv(CSV_FILE, index=False)

# ------------------------------------------------------------------
# 3. Main UI
# ------------------------------------------------------------------
def main():
    st.title("Expense Tracker")
    st.caption("Add, view, edit, delete – data lives in **expenses.csv**")

    df = load_data()
    st.write(f"**{len(df)}** expense(s) loaded from `{CSV_FILE}`")

    # --------------------------------------------------------------
    # Sidebar menu
    # --------------------------------------------------------------
    menu = st.sidebar.selectbox(
        "Action",
        [
            "Add Expense", "View Expenses", "Total", "Delete",
            "Edit", "Sum by Category", "Sort by Date", "Search"
        ],
    )

    # ------------------------------------------------------------------
    # ADD
    # ------------------------------------------------------------------
    if menu == "Add Expense":
        st.subheader("Add New Expense")
        c1, c2 = st.columns(2)
        with c1:
            cat = st.text_input("Category")
        with c2:
            amt = st.number_input("Amount ($)", min_value=0.01, step=0.01)

        today = datetime.date.today().strftime("%Y-%m-%d")
        st.info(f"Date: **{today}** (auto)")

        if st.button("Add"):
            if not cat:
                st.error("Category required")
            else:
                new = pd.DataFrame(
                    {"category": [cat], "amount": [amt], "date": [today]}
                )
                # ---- avoid FutureWarning ----
                global df
                if df.empty:
                    df = new
                else:
                    df = pd.concat([df, new], ignore_index=True)
                save_data(df)
                st.success("Added!")
                st.rerun()

    # ------------------------------------------------------------------
    # VIEW
    # ------------------------------------------------------------------
    elif menu == "View Expenses":
        st.subheader("All Expenses")
        if df.empty:
            st.info("Nothing yet – add an expense!")
        else:
            st.dataframe(df, use_container_width=True)

    # ------------------------------------------------------------------
    # TOTAL
    # ------------------------------------------------------------------
    elif menu == "Total":
        st.subheader("Summary")
        if df.empty:
            st.info("No data")
        else:
            total = df["amount"].sum()
            st.metric("Total Spent", f"${total:,.2f}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Count", len(df))
            c2.metric("Avg", f"${df['amount'].mean():.2f}")
            c3.metric("Max", f"${df['amount'].max():.2f}")

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    elif menu == "Delete":
        st.subheader("Delete Row")
        if df.empty:
            st.info("Nothing to delete")
        else:
            st.dataframe(df, use_container_width=True)
            idx = st.number_input(
                "Row # (1-based)", min_value=1, max_value=len(df), step=1
            )
            if st.button("Delete"):
                df.drop(index=idx - 1, inplace=True)
                df.reset_index(drop=True, inplace=True)
                save_data(df)
                st.success("Deleted")
                st.rerun()

    # ------------------------------------------------------------------
    # EDIT
    # ------------------------------------------------------------------
    elif menu == "Edit":
        st.subheader("Edit Row")
        if df.empty:
            st.info("Nothing to edit")
        else:
            st.dataframe(df, use_container_width=True)
            idx = st.number_input(
                "Row # (1-based)", min_value=1, max_value=len(df), step=1
            )
            row = df.iloc[idx - 1]
            c1, c2 = st.columns(2)
            with c1:
                new_cat = st.text_input("Category", value=row["category"])
            with c2:
                new_amt = st.number_input(
                    "Amount", value=float(row["amount"]), step=0.01
                )
            new_date = st.date_input("Date", value=pd.to_datetime(row["date"]))

            if st.button("Update"):
                df.at[idx - 1, "category"] = new_cat
                df.at[idx - 1, "amount"] = new_amt
                df.at[idx - 1, "date"] = new_date.strftime("%Y-%m-%d")
                save_data(df)
                st.success("Updated")
                st.rerun()

    # ------------------------------------------------------------------
    # SUM BY CATEGORY
    # ------------------------------------------------------------------
    elif menu == "Sum by Category":
        st.subheader("By Category")
        if df.empty:
            st.info("No data")
        else:
            sums = (
                df.groupby("category")["amount"]
                .sum()
                .reset_index()
                .sort_values("amount", ascending=False)
            )
            st.dataframe(sums, use_container_width=True)
            st.metric("Grand Total", f"${sums['amount'].sum():,.2f}")

    # ------------------------------------------------------------------
    # SORT BY DATE
    # ------------------------------------------------------------------
    elif menu == "Sort by Date":
        st.subheader("Sorted by Date")
        if df.empty:
            st.info("No data")
        else:
            sorted_df = df.sort_values("date").reset_index(drop=True)
            st.dataframe(sorted_df, use_container_width=True)
            if st.button("Save sorted order"):
                df = sorted_df
                save_data(df)
                st.success("Saved")
                st.rerun()

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------
    elif menu == "Search":
        st.subheader("Search by Category")
        term = st.text_input("Keyword (case-insensitive)")
        if term:
            hits = df[
                df["category"].str.contains(term, case=False, na=False)
            ]
            if hits.empty:
                st.info("No match")
            else:
                st.dataframe(hits, use_container_width=True)

if __name__ == "__main__":
    main()# app.py
import streamlit as st
import pandas as pd
import datetime
import os

st.set_page_config(page_title="Expense Tracker", page_icon="Money Bag", layout="wide")

CSV_FILE = "expenses.csv"          # <-- must be in the repo root

# ------------------------------------------------------------------
# 1. Load (and create if missing)
# ------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_FILE):
        # First run → create empty CSV with header
        empty = pd.DataFrame(columns=["category", "amount", "date"])
        empty.to_csv(CSV_FILE, index=False)
        st.toast("Created empty expenses.csv")
    return pd.read_csv(CSV_FILE)

# ------------------------------------------------------------------
# 2. Save
# ------------------------------------------------------------------
def save_data(df: pd.DataFrame):
    df.to_csv(CSV_FILE, index=False)

# ------------------------------------------------------------------
# 3. Main UI
# ------------------------------------------------------------------
def main():
    st.title("Expense Tracker")
    st.caption("Add, view, edit, delete – data lives in **expenses.csv**")

    df = load_data()
    st.write(f"**{len(df)}** expense(s) loaded from `{CSV_FILE}`")

    # --------------------------------------------------------------
    # Sidebar menu
    # --------------------------------------------------------------
    menu = st.sidebar.selectbox(
        "Action",
        [
            "Add Expense", "View Expenses", "Total", "Delete",
            "Edit", "Sum by Category", "Sort by Date", "Search"
        ],
    )

    # ------------------------------------------------------------------
    # ADD
    # ------------------------------------------------------------------
    if menu == "Add Expense":
        st.subheader("Add New Expense")
        c1, c2 = st.columns(2)
        with c1:
            cat = st.text_input("Category")
        with c2:
            amt = st.number_input("Amount ($)", min_value=0.01, step=0.01)

        today = datetime.date.today().strftime("%Y-%m-%d")
        st.info(f"Date: **{today}** (auto)")

        if st.button("Add"):
            if not cat:
                st.error("Category required")
            else:
                new = pd.DataFrame(
                    {"category": [cat], "amount": [amt], "date": [today]}
                )
                # ---- avoid FutureWarning ----
                global df
                if df.empty:
                    df = new
                else:
                    df = pd.concat([df, new], ignore_index=True)
                save_data(df)
                st.success("Added!")
                st.rerun()

    # ------------------------------------------------------------------
    # VIEW
    # ------------------------------------------------------------------
    elif menu == "View Expenses":
        st.subheader("All Expenses")
        if df.empty:
            st.info("Nothing yet – add an expense!")
        else:
            st.dataframe(df, use_container_width=True)

    # ------------------------------------------------------------------
    # TOTAL
    # ------------------------------------------------------------------
    elif menu == "Total":
        st.subheader("Summary")
        if df.empty:
            st.info("No data")
        else:
            total = df["amount"].sum()
            st.metric("Total Spent", f"${total:,.2f}")
            c1, c2, c3 = st.columns(3)
            c1.metric("Count", len(df))
            c2.metric("Avg", f"${df['amount'].mean():.2f}")
            c3.metric("Max", f"${df['amount'].max():.2f}")

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------
    elif menu == "Delete":
        st.subheader("Delete Row")
        if df.empty:
            st.info("Nothing to delete")
        else:
            st.dataframe(df, use_container_width=True)
            idx = st.number_input(
                "Row # (1-based)", min_value=1, max_value=len(df), step=1
            )
            if st.button("Delete"):
                df.drop(index=idx - 1, inplace=True)
                df.reset_index(drop=True, inplace=True)
                save_data(df)
                st.success("Deleted")
                st.rerun()

    # ------------------------------------------------------------------
    # EDIT
    # ------------------------------------------------------------------
    elif menu == "Edit":
        st.subheader("Edit Row")
        if df.empty:
            st.info("Nothing to edit")
        else:
            st.dataframe(df, use_container_width=True)
            idx = st.number_input(
                "Row # (1-based)", min_value=1, max_value=len(df), step=1
            )
            row = df.iloc[idx - 1]
            c1, c2 = st.columns(2)
            with c1:
                new_cat = st.text_input("Category", value=row["category"])
            with c2:
                new_amt = st.number_input(
                    "Amount", value=float(row["amount"]), step=0.01
                )
            new_date = st.date_input("Date", value=pd.to_datetime(row["date"]))

            if st.button("Update"):
                df.at[idx - 1, "category"] = new_cat
                df.at[idx - 1, "amount"] = new_amt
                df.at[idx - 1, "date"] = new_date.strftime("%Y-%m-%d")
                save_data(df)
                st.success("Updated")
                st.rerun()

    # ------------------------------------------------------------------
    # SUM BY CATEGORY
    # ------------------------------------------------------------------
    elif menu == "Sum by Category":
        st.subheader("By Category")
        if df.empty:
            st.info("No data")
        else:
            sums = (
                df.groupby("category")["amount"]
                .sum()
                .reset_index()
                .sort_values("amount", ascending=False)
            )
            st.dataframe(sums, use_container_width=True)
            st.metric("Grand Total", f"${sums['amount'].sum():,.2f}")

    # ------------------------------------------------------------------
    # SORT BY DATE
    # ------------------------------------------------------------------
    elif menu == "Sort by Date":
        st.subheader("Sorted by Date")
        if df.empty:
            st.info("No data")
        else:
            sorted_df = df.sort_values("date").reset_index(drop=True)
            st.dataframe(sorted_df, use_container_width=True)
            if st.button("Save sorted order"):
                df = sorted_df
                save_data(df)
                st.success("Saved")
                st.rerun()

    # ------------------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------------------
    elif menu == "Search":
        st.subheader("Search by Category")
        term = st.text_input("Keyword (case-insensitive)")
        if term:
            hits = df[
                df["category"].str.contains(term, case=False, na=False)
            ]
            if hits.empty:
                st.info("No match")
            else:
                st.dataframe(hits, use_container_width=True)

if __name__ == "__main__":
    main()
