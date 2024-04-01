import sqlite3

database = sqlite3.connect("Research-Grant-Council-Database.db")
query = ""

while True:
    print("Welcome to the Research Grant Council Database!")

    print("Please select an option from the following menu:\n")

    print("1. Find all competitions (calls for grant proposals) open at a user-specified month, which already have at least one submitted large proposal.")
    print("2. For a user-specified area, find the proposal(s) that request(s) the largest amount of money.")
    print("3. For a user-specified date, find the proposals submitted before that date that are awarded the largest amount of money.")
    print("4. For an area specified by the user, output its average requested/awarded discrepancy, that is, the absolute value of the difference between the amounts.")
    print("5. assigning a set of reviewers to review a specific grant application (research proposal)")
    print("6. For a user-specified name,  find the proposal(s) he/she needs to review.")
    print("7. Exit.\n")

    option = input("Enter your choice: ")

    if option == "1":
        month = input("Enter the month (1-12): ")
                
        with database:
            cursor = database.cursor()

            query = "SELECT competitionID, title FROM Competition WHERE strftime('%m', deadline) >= :month AND competitionID IN (SELECT competitionID FROM Proposal WHERE requestedAmount >= 20000 OR proposalID IN (SELECT proposalID FROM Collaborator GROUP BY proposalID HAVING COUNT(collaboratorID) >= 10));"

            cursor.execute(query, {"month":month})

            rows = cursor.fetchall()

            if rows:
                print("The following competitions are open in the specified month and have at least one submitted large proposal: ")
            else:
                print("No competitions are open in the specified month and have at least one submitted large proposal.")

            for row in rows:
                print(row[0], row[1])

    elif option == "7":
        break
    else:
        print("Invalid option. Please try again.")

if database:
    database.close()
