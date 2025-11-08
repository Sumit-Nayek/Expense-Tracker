# # app.py
# import streamlit as st
# import pandas as pd
# import datetime
# import os

# st.set_page_config(page_title="Expense Tracker", page_icon="Money Bag", layout="wide")

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
# st.title("Expense Tracker")
# st.caption(f"{len(df)} expense(s) in `{CSV_FILE}`")

# menu = st.sidebar.selectbox("Action", [
#     "Add Expense", "View", "Total", "Delete", "Edit",
#     "By Category", "Sort by Date", "Search"
# ])

# # ADD
# if menu == "Add Expense":
#     st.subheader("Add New Expense")
#     col1, col2 = st.columns(2)
#     with col1:
#         cat = st.text_input("Category")
#     with col2:
#         amt = st.number_input("Amount ($)", min_value=0.01, step=0.01)
#     today = datetime.date.today().strftime("%Y-%m-%d")
#     st.info(f"Date: **{today}**")

#     if st.button("Add Expense"):
#         if not cat.strip():
#             st.error("Enter a category")
#         else:
#             new_row = pd.DataFrame({
#                 "category": [cat],
#                 "amount": [amt],
#                 "date": [today]
#             })
#             st.session_state.df = pd.concat([df, new_row], ignore_index=True) if not df.empty else new_row
#             save_and_rerun()
#             st.success("Added!")

# # VIEW
# elif menu == "View":
#     st.subheader("All Expenses")
#     if df.empty:
#         st.info("No expenses yet.")
#     else:
#         st.dataframe(df, use_container_width=True)

# # TOTAL
# elif menu == "Total":
#     st.subheader("Summary")
#     if df.empty:
#         st.info("No data")
#     else:
#         total = df["amount"].sum()
#         st.metric("Total", f"${total:,.2f}")
#         c1, c2, c3 = st.columns(3)
#         c1.metric("Count", len(df))
#         c2.metric("Avg", f"${df['amount'].mean():.2f}")
#         c3.metric("Max", f"${df['amount'].max():.2f}")

# # DELETE
# elif menu == "Delete":
#     st.subheader("Delete Row")
#     if df.empty:
#         st.info("Nothing to delete")
#     else:
#         st.dataframe(df, use_container_width=True)
#         idx = st.number_input("Row # (1-based)", 1, len(df), step=1)
#         if st.button("Delete"):
#             st.session_state.df = df.drop(index=idx-1).reset_index(drop=True)
#             save_and_rerun()

# # EDIT
# elif menu == "Edit":
#     st.subheader("Edit Row")
#     if df.empty:
#         st.info("Nothing to edit")
#     else:
#         st.dataframe(df, use_container_width=True)
#         idx = st.number_input("Row #", 1, len(df), step=1)
#         row = df.iloc[idx-1]
#         c1, c2 = st.columns(2)
#         with c1:
#             new_cat = st.text_input("Category", value=row["category"])
#         with c2:
#             new_amt = st.number_input("Amount", value=float(row["amount"]), step=0.01)
#         new_date = st.date_input("Date", value=pd.to_datetime(row["date"]))
#         if st.button("Update"):
#             st.session_state.df.at[idx-1, "category"] = new_cat
#             st.session_state.df.at[idx-1, "amount"] = new_amt
#             st.session_state.df.at[idx-1, "date"] = new_date.strftime("%Y-%m-%d")
#             save_and_rerun()

# # BY CATEGORY
# elif menu == "By Category":
#     st.subheader("By Category")
#     if df.empty:
#         st.info("No data")
#     else:
#         sums = df.groupby("category")["amount"].sum().reset_index()
#         st.dataframe(sums, use_container_width=True)
#         st.metric("Total", f"${sums['amount'].sum():,.2f}")

# # SORT BY DATE
# elif menu == "Sort by Date":
#     st.subheader("Sorted by Date")
#     if df.empty:
#         st.info("No data")
#     else:
#         sorted_df = df.sort_values("date").reset_index(drop=True)
#         st.dataframe(sorted_df, use_container_width=True)
#         if st.button("Save Sorted"):
#             st.session_state.df = sorted_df
#             save_and_rerun()

# # SEARCH
# elif menu == "Search":
#     st.subheader("Search by Category")
#     term = st.text_input("Keyword")
#     if term and not df.empty:
#         hits = df[df["category"].str.contains(term, case=False, na=False)]
#         st.dataframe(hits if not hits.empty else pd.DataFrame(), use_container_width=True)
#     else:
#         st.info("Enter a term")
# app.py
import streamlit as st
import pandas as pd
import datetime
import os
import plotly.express as px

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
    "By Category", "Sort by Date", "Search", "Filter & Visualize"  # Added new option
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

# NEW: FILTER & VISUALIZE
elif menu == "Filter & Visualize":
    st.subheader("📊 Filter & Visualize Expenses")
    
    if df.empty:
        st.info("No expenses to visualize. Add some expenses first!")
    else:
        # Get unique categories for filtering
        categories = df['category'].unique().tolist()
        categories.sort()
        
        # Filter section with buttons
        st.write("### Filter by Category")
        
        # Create columns for category buttons
        cols = st.columns(4)
        selected_category = None
        
        # Add "All" button first
        with cols[0]:
            if st.button("📋 All Categories", use_container_width=True):
                selected_category = "All"
        
        # Add buttons for each category
        for i, category in enumerate(categories):
            col_idx = (i % 3) + 1  # Distribute across columns 1-3
            with cols[col_idx]:
                if st.button(f"📁 {category}", use_container_width=True):
                    selected_category = category
        
        # Display current filter
        if selected_category:
            if selected_category == "All":
                filtered_df = df
                st.success(f"Showing all categories")
            else:
                filtered_df = df[df['category'] == selected_category]
                st.success(f"Filtering by: **{selected_category}**")
        else:
            filtered_df = df
            st.info("Click any category button to filter")
        
        # Display filtered data
        st.write("### Filtered Expenses")
        if not filtered_df.empty:
            st.dataframe(filtered_df, use_container_width=True)
            
            # Summary metrics for filtered data
            total_filtered = filtered_df['amount'].sum()
            count_filtered = len(filtered_df)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Amount", f"${total_filtered:,.2f}")
            col2.metric("Number of Expenses", count_filtered)
            col3.metric("Average", f"${filtered_df['amount'].mean():.2f}")
            
            # Visualization section
            st.write("### 📈 Visualizations")
            
            # Prepare data for charts
            category_totals = filtered_df.groupby('category')['amount'].sum().reset_index()
            category_totals = category_totals.sort_values('amount', ascending=False)
            
            # Create two columns for charts
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                st.write("#### Pie Chart - Expense Distribution")
                if len(category_totals) > 1:
                    # Create pie chart
                    fig_pie = px.pie(
                        category_totals, 
                        values='amount', 
                        names='category',
                        title=f"Expense Distribution{' - ' + selected_category if selected_category and selected_category != 'All' else ''}",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    st.plotly_chart(fig_pie, use_container_width=True)
                else:
                    st.info("Need at least 2 categories for pie chart")
            
            with chart_col2:
                st.write("#### Bar Chart - Category Comparison")
                # Create bar chart
                fig_bar = px.bar(
                    category_totals,
                    x='category',
                    y='amount',
                    title=f"Expenses by Category{' - ' + selected_category if selected_category and selected_category != 'All' else ''}",
                    color='amount',
                    color_continuous_scale='Blues'
                )
                fig_bar.update_layout(xaxis_title="Category", yaxis_title="Amount ($)")
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Monthly trend chart (if we have date data)
            st.write("#### Monthly Trend")
            try:
                filtered_df['date'] = pd.to_datetime(filtered_df['date'])
                monthly_totals = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['amount'].sum().reset_index()
                monthly_totals['date'] = monthly_totals['date'].astype(str)
                
                if len(monthly_totals) > 1:
                    fig_line = px.line(
                        monthly_totals,
                        x='date',
                        y='amount',
                        title="Monthly Expense Trend",
                        markers=True
                    )
                    fig_line.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
                    st.plotly_chart(fig_line, use_container_width=True)
                else:
                    st.info("Need data across multiple months for trend analysis")
            except:
                st.info("Could not generate monthly trend chart")
        
        else:
            st.warning("No expenses match the current filter")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips")
st.sidebar.info(
    "Use the **Filter & Visualize** section to see your spending patterns "
    "with interactive charts and category filtering!"
)
