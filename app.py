import streamlit as st

Members = ["Nikki", "Quan Vu", "Quan Nguyen"]

st.title("Cafe Pieuvre Expense Tracker")
st.write("Welcome to Cafe Pieuvre's Expense Tracker!")


# -------------------------
# EVENT INFORMATION
# -------------------------

if "events" not in st.session_state:

    st.session_state.events = {

        "Greenville Pop Up": {
            "date": "9/20/2026",
            "expenses": [
                {
                    "item": "Vendor Fee",
                    "cost": 150,
                    "paid_by": "Quan Nguyen"
                },
                {
                    "item": "Amazon Haul",
                    "cost": 115,
                    "paid_by": "Nikki"
                },
                {
                    "item": "Canopy Weights",
                    "cost": 70,
                    "paid_by": "Quan Vu"
                },
                {
                    "item": "Target Haul",
                    "cost": 30,
                    "paid_by": "Quan Nguyen"
                },
                {
                    "item": "Gas",
                    "cost": 30,
                    "paid_by": "Quan Vu"
                },
                {
                    "item": "Canopy Tent",
                    "cost": 80,
                    "paid_by": "Nikki"
                }
            ],
            "revenue": 646
        },

        "Augusta Pop Up": {
            "date": "10/4/2026",
            "expenses": [],
            "revenue": 0
        },

        "Myrtle Beach Pop Up": {
            "date": "10/18/2026",
            "expenses": [],
            "revenue": 0
        }
    }


# -------------------------
# CHOOSE EVENT
# -------------------------

selected_event_name = st.selectbox(
    "Choose an event:",
    list(st.session_state.events.keys())
)

event = st.session_state.events[selected_event_name]

st.header(selected_event_name)
st.write("Event Date:", event["date"])


# -------------------------
# CALCULATE TOTAL EXPENSES
# -------------------------

total_expenses = 0

for expense in event["expenses"]:
    total_expenses += expense["cost"]


# -------------------------
# CALCULATE PROFIT
# -------------------------

profit = event["revenue"] - total_expenses


# -------------------------
# CALCULATE HOW MUCH
# EACH MEMBER PAID
# -------------------------

amount_paid = {}

for person in Members:
    amount_paid[person] = 0


for expense in event["expenses"]:

    person = expense["paid_by"]
    cost = expense["cost"]

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
    "Enter your name:"
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
    "expense_form",
    clear_on_submit=True
):

    paid_by = st.selectbox(
        "Who paid?",
        Members
    )

    item = st.text_input(
        "What was the expense?"
    )

    cost = st.number_input(
        "How much did it cost?",
        min_value=0.00,
        step=0.01,
        format="%.2f"
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

            new_expense = {
                "item": item,
                "cost": cost,
                "paid_by": paid_by
            }

            event["expenses"].append(
                new_expense
            )

            st.rerun()


# -------------------------
# EXPENSE LIST
# -------------------------

st.subheader("Expense List")

st.dataframe(
    event["expenses"],
    use_container_width=True
)

