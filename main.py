Members = ["Nikki", "Quan V", "Quan N"]

event_location = input("Enter the event location: ")


events = {
    "name": event_location + " pop-up",
    "date": "9/20/2026",
    "expenses": [
        {
            "item": "Vendor Greenville Fee",
            "cost": 150,
            "paid_by": "Quan N"
        },
        {
            "item": "Vendor Augusta Fee",
            "cost": 50,
            "paid_by": "Quan V"
        },
        {
            "item": "Vendor Myrtle Fee",
            "cost": 50,
            "paid_by": "Quan N"
        },
        {
            "item": "Amazon haul",
            "cost": 115,
            "paid_by": "Nikki"
        },
        {
            "item": "Canopy Weights",
            "cost": 70,
            "paid_by": "Quan V"
        },
        {
            "item": "Target Haul",
            "cost": 30,
            "paid_by": "Quan N"
        },
        {
            "item": "Gas",
            "cost": 30,
            "paid_by": "Quan V"
        },
        {
            "item": "Canopy Tent",
            "cost": 80,
            "paid_by": "Nikki"
        }
    ],
    "revenue": 646
}

#TOTAL EXPENSES

total_expenses = 0

for expense in events["expenses"]:
    total_expenses += expense["cost"]

#PROFIT

profit = events["revenue"] - total_expenses


#HOW MUCH EACH PERSON PAID

amount_paid = {
    "Nikki": 0,
    "Quan V": 0,
    "Quan N": 0
}

for expense in events["expenses"]:
    person = expense["paid_by"]
    cost = expense["cost"]

    amount_paid[person] += cost


#PROFIT PER PERSON
profit_per_person = profit / len(Members)

#GENERAL SUMMARY

print("\n" + "=" * 45)
print("             GENERAL SUMMARY")
print("=" * 45)

print(f"Event Location: {events['name']}")
print(f"Event Date: {events['date']}")
print(f"Revenue: ${events['revenue']}")
print(f"Total Expenses: ${total_expenses}")
print(f"Net Profit: ${profit}")
print(f"Profit per Person: ${profit_per_person:.2f}")

#Member Summary 

print("\n" + "=" * 45)
print("              MEMBER SUMMARY")
print("=" * 45)

for person in Members:
    print(f"{person:<10} | Amount Paid: ${amount_paid[person]:.2f}")

#PAYOUT 
while True: 
    print("\n" + "-" * 45)

    person_name = input("Enter your name to see your reimbursement and profit share: ").strip().lower()

    if person_name == "exit":
        print("Goodbye")
        break

    for person in Members:

        if person.lower() == person_name:

            reimbursement = amount_paid[person]
            final_payout = reimbursement + profit_per_person

            print("\n" + "=" * 45)
            print("               PAYOUT SUMMARY")
            print("=" * 45)

            print(f"Member:          {person}")
            print(f"Reimbursement:   ${reimbursement:.2f}")
            print(f"Profit Share:    ${profit_per_person:.2f}")
            print("-" * 45)
            print(f"TOTAL PAYOUT:    ${final_payout:.2f}")

            break
    else:
        print("Member not found.")
