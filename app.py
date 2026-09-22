import streamlit as st

# -------------------------
# MEMBERS
# -------------------------

Members = ["Nikki", "Quan Vu", "Quan Nguyen"]


# -------------------------
# PAGE TITLE
# -------------------------

st.title("Cafe Pieuvre")
st.caption("Pop Up Expense Tracker!")


# -------------------------
# EVENT INFORMATION
# -------------------------

if "events" not in st.session_state:

    st.session_state.events = {

        "Greenville Pop Up": {
            "date": "9/20/2026",
            "expenses": [
                {
                    "item": "Greenville Vendor Fee",
                    "cost": 150,
                    "paid_by": "Quan Nguyen"
                },
                {
                    "item": "Augusta Vendor Fee",
                    "cost": 50,
                    "paid_by": "Quan Vu"
                },
                {
                    "item": "Myrtle Vendor Fee",
                    "cost": 50,
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
            "date": "10/02/2026",
            "expenses": [],
            "revenue": 0
        },

        "Myrtle Beach Pop Up": {
            "date": "10/03/2026",
            "expenses": [],
            "revenue": 0
        },

        "Thrift Street Pt. 2": {
            "date": "10/10/2026",
            "expenses": [],
            "revenue": 0
        }
    }


# -------------------------
# EVENT PAGE FUNCTION
# -------------------------

def show_event(selected_event_name):

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
    # CALCULATE AMOUNT PAID
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

    if len(event["expenses"]) > 0:

        st.dataframe(
            event["expenses"],
            use_container_width=True
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

    st.header("Welcome to Cafe Pieuvre 🍵")

    st.write(
        "Track expenses, revenue, profits, and payouts for each Cafe Pieuvre pop-up."
    )

    st.divider()

    st.markdown(
        """
        <style>
        .event-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 25px;
            margin-top: 20px;
        }

        .event-card h3 {
            margin-top: 0;
            margin-bottom: 15px;
            min-height: 38px;
        }

        .event-date {
            margin: 0 0 12px 0;
        }

        .event-status {
            margin: 0;
            font-weight: 600;
        }

        @media (max-width: 700px) {
            .event-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        </style>

        <div class="event-grid">

            <div class="event-card">
                <h3>Greenville</h3>
                <p class="event-date">📅 September 20, 2026</p>
                <p class="event-status">Completed</p>
            </div>

            <div class="event-card">
                <h3>Augusta</h3>
                <p class="event-date">📅 October 2, 2026</p>
                <p class="event-status">Upcoming</p>
            </div>

            <div class="event-card">
                <h3>Myrtle Beach</h3>
                <p class="event-date">📅 October 3, 2026</p>
                <p class="event-status">Upcoming</p>
            </div>

            <div class="event-card">
                <h3>Thrift Street</h3>
                <p class="event-date">📅 October 10, 2026</p>
                <p class="event-status">Upcoming</p>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )
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