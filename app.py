import streamlit as st
from supabase import create_client


# -------------------------
# SUPABASE CONNECTION
# -------------------------

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


# -------------------------
# MEMBERS
# -------------------------

Members = ["Nikki Le", "Quan Vu", "Quan Nguyen"]


# -------------------------
# EVENT INFORMATION
# Expenses are now stored in Supabase
# -------------------------

EVENTS = {
    "Greenville Pop Up": {
        "date": "9/20/2026",
        "revenue": 646
    },

    "Augusta Pop Up": {
        "date": "10/02/2026",
        "revenue": 0
    },

    "Myrtle Beach Pop Up": {
        "date": "10/03/2026",
        "revenue": 0
    },

    "Thrift Street Pt. 2": {
        "date": "10/10/2026",
        "revenue": 0
    }
}


# -------------------------
# SUPABASE FUNCTIONS
# -------------------------

def load_expenses(event_name):
    response = (
        supabase
        .table("expenses")
        .select("*")
        .eq("event", event_name)
        .order("id")
        .execute()
    )

    expenses = response.data

    # Make sure cost behaves like a number
    for expense in expenses:
        expense["cost"] = float(expense["cost"])

    return expenses


def add_expense(event_name, item, cost, paid_by):
    supabase.table("expenses").insert({
        "event": event_name,
        "item": item,
        "cost": float(cost),
        "paid_by": paid_by
    }).execute()


def delete_expense(expense_id):
    (
        supabase
        .table("expenses")
        .delete()
        .eq("id", expense_id)
        .execute()
    )


# -------------------------
# PAGE TITLE
# -------------------------

st.image(
    "images/weedmatcha.png",
    use_container_width=True
)

st.title("Cafe Pieuvre")
st.caption("matcha matcha matcha")


# -------------------------
# EVENT PAGE FUNCTION
# -------------------------

def show_event(selected_event_name):

    event = EVENTS[selected_event_name]

    # Load current expenses directly from Supabase
    event_expenses = load_expenses(selected_event_name)

    st.header(selected_event_name)
    st.write("Event Date:", event["date"])


    # -------------------------
    # CALCULATE TOTAL EXPENSES
    # -------------------------

    total_expenses = 0

    for expense in event_expenses:
        total_expenses += expense["cost"]


    # -------------------------
    # CALCULATE PROFIT
    # -------------------------

    profit = event["revenue"] - total_expenses


    # -------------------------
    # CALCULATE AMOUNT PAID
    # -------------------------

    amount_paid = {}

    for person in Members:
        amount_paid[person] = 0

    for expense in event_expenses:

        person = expense["paid_by"]
        cost = expense["cost"]

        if person in amount_paid:
            amount_paid[person] += cost


    # -------------------------
    # PROFIT PER PERSON
    # -------------------------

    profit_per_person = profit / len(Members)


    # -------------------------
    # GENERAL SUMMARY
    # -------------------------

    st.subheader("General Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Revenue",
        f"${event['revenue']:.2f}"
    )

    col2.metric(
        "Expenses",
        f"${total_expenses:.2f}"
    )

    col3.metric(
        "Net Profit",
        f"${profit:.2f}"
    )

    col4.metric(
        "Profit Per Person",
        f"${profit_per_person:.2f}"
    )


    # -------------------------
    # MEMBER SUMMARY
    # -------------------------

    st.subheader("Member Summary")

    for person in Members:

        st.write(
            f"**{person}** — Paid ${amount_paid[person]:.2f}"
        )


    # -------------------------
    # VIEW PAYOUT
    # -------------------------

    st.subheader("View Your Payout")

    person_name = st.text_input(
        "Enter your name:",
        key=f"name_{selected_event_name}"
    ).strip().lower()

    if person_name:

        member_found = False

        for person in Members:

            if person.lower() == person_name:

                member_found = True

                reimbursement = amount_paid[person]

                final_payout = (
                    reimbursement
                    + profit_per_person
                )

                st.write(
                    f"### Payout for {person}"
                )

                st.write(
                    f"Reimbursement: **${reimbursement:.2f}**"
                )

                st.write(
                    f"Profit Share: **${profit_per_person:.2f}**"
                )

                st.write(
                    f"Total Payout: **${final_payout:.2f}**"
                )

                break

        if member_found == False:

            st.error(
                "Member not found."
            )


    # -------------------------
    # ADD AN EXPENSE
    # -------------------------

    st.subheader("Add an Expense")

    with st.form(
        f"expense_form_{selected_event_name}",
        clear_on_submit=True
    ):

        paid_by = st.selectbox(
            "Who paid?",
            Members,
            key=f"paid_by_{selected_event_name}"
        )

        item = st.text_input(
            "What was the expense?",
            key=f"item_{selected_event_name}"
        )

        cost = st.number_input(
            "How much did it cost?",
            min_value=0.00,
            step=0.01,
            format="%.2f",
            key=f"cost_{selected_event_name}"
        )

        submit = st.form_submit_button(
            "Add Expense"
        )

        if submit:

            if item.strip() == "":

                st.error(
                    "Please enter what the expense was."
                )

            elif cost <= 0:

                st.error(
                    "Please enter a cost greater than $0."
                )

            else:

                try:

                    add_expense(
                        selected_event_name,
                        item.strip(),
                        cost,
                        paid_by
                    )

                    st.success(
                        f"Added: {item.strip()}"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Could not add expense: {e}"
                    )


    # -------------------------
    # EXPENSE LIST
    # -------------------------

    st.subheader("Expense List")

    if len(event_expenses) > 0:

        # Don't display the database ID or event name
        display_expenses = []

        for expense in event_expenses:

            display_expenses.append({
                "Item": expense["item"],
                "Cost": expense["cost"],
                "Paid By": expense["paid_by"]
            })

        st.dataframe(
            display_expenses,
            use_container_width=True,
            hide_index=True
        )


        # -------------------------
        # DELETE AN EXPENSE
        # -------------------------

        st.subheader("Delete an Expense")

        expense_options = []

        for i, expense in enumerate(event_expenses):

            expense_options.append(
                f"{i + 1}. {expense['item']} - "
                f"${expense['cost']:.2f} - "
                f"Paid by {expense['paid_by']}"
            )

        expense_to_delete = st.selectbox(
            "Select the expense you want to delete:",
            expense_options,
            key=f"delete_expense_{selected_event_name}"
        )

        if st.button(
            "Delete Expense",
            key=f"delete_button_{selected_event_name}"
        ):

            index_to_delete = expense_options.index(
                expense_to_delete
            )

            deleted_expense = event_expenses[
                index_to_delete
            ]

            try:

                delete_expense(
                    deleted_expense["id"]
                )

                st.success(
                    f"Deleted: {deleted_expense['item']}"
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Could not delete expense: {e}"
                )

    else:

        st.write(
            "No expenses have been added yet."
        )


# -------------------------
# EVENT TABS
# -------------------------

home_tab, greenville_tab, augusta_tab, myrtle_tab, thriftstreet_tab = st.tabs(
    [
        "🏠 Home",
        "Greenville",
        "Augusta",
        "Myrtle Beach",
        "Thrift Street Pt. 2"
    ]
)


# -------------------------
# HOME PAGE
# -------------------------

with home_tab:

    st.header(
        "Track expenses, revenue, profits, and payouts for each Cafe Pieuvre pop-up."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write("**Greenville**")
        st.write("📅 September 20, 2026")
        st.write("Completed")

    with col2:
        st.write("**Augusta**")
        st.write("📅 October 2, 2026")
        st.write("Upcoming")

    with col3:
        st.write("**Myrtle Beach**")
        st.write("📅 October 3, 2026")
        st.write("Upcoming")

    with col4:
        st.write("**Thrift Street**")
        st.write("📅 October 10, 2026")
        st.write("Upcoming")


# -------------------------
# GREENVILLE
# -------------------------

with greenville_tab:
    show_event("Greenville Pop Up")


# -------------------------
# AUGUSTA
# -------------------------

with augusta_tab:
    show_event("Augusta Pop Up")


# -------------------------
# MYRTLE BEACH
# -------------------------

with myrtle_tab:
    show_event("Myrtle Beach Pop Up")


# -------------------------
# THRIFT STREET
# -------------------------

with thriftstreet_tab:
    show_event("Thrift Street Pt. 2")