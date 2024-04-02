"""Research Grant Council Database Main"""

import sqlite3

database = sqlite3.connect("Research-Grant-Council-Database.db")

print("Welcome to the Research Grant Council Database!\n")

while True:
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
        month = input("Enter the month (1-12): ").zfill(2)
        
        with database:
            cursor = database.cursor()

            QUERY = "SELECT competitionID, title FROM Competition WHERE strftime('%m', deadline) >= :month AND strftime('%m', startDate) < :month AND competitionID IN (SELECT competitionID FROM Proposal WHERE requestedAmount >= 20000 OR proposalID IN (SELECT proposalID FROM Collaborator GROUP BY proposalID HAVING COUNT(collaboratorID) >= 10));"

            cursor.execute(QUERY, {"month":month})

            rows = cursor.fetchall()

            if rows:
                print("The following competitions are open in the specified month and have at least one submitted large proposal:\n")
            else:
                print("No competitions are open in the specified month and have at least one submitted large proposal.\n")

            for row in rows:
                for column in row:
                    print(column, end=", ")
                print("\n")

    elif option == "2":
        area = input("Enter the area: ")

        with database:
            cursor = database.cursor()

            QUERY = "SELECT * FROM Proposal WHERE competitionID IN (SELECT competitionID FROM Competition WHERE area=:area) AND requestedAmount >= (SELECT MAX(requestedAmount) FROM Proposal WHERE competitionID IN (SELECT competitionID FROM Competition WHERE area=:area));"

            cursor.execute(QUERY, {"area":area})

            rows = cursor.fetchall()

            if rows:
                print("The proposal(s) that request(s) the largest amount of money in the specified area: ")
            else:
                print("No proposals found.")

            for row in rows:
                for column in row:
                    print(column, end=", ")
                print("\n")

    elif option == "3":
        date = input("Enter the date (YYYY-MM-DD): ")

        with database:
            cursor = database.cursor()

            QUERY = "SELECT * FROM Proposal WHERE submissionDate < :date AND status = 'awarded' AND awardedAmount >= (SELECT MAX(awardedAmount) FROM Proposal WHERE submissionDate < :date AND status = 'awarded');"

            cursor.execute(QUERY, {"date":date})

            rows = cursor.fetchall()

            if rows:
                print("The proposals submitted before the specified date that are awarded the largest amount of money: ")
            else:
                print("No proposals found.")

            for row in rows:
                for column in row:
                    print(column, end=", ")
                print("\n")

    elif option == "4":
        area = input("Enter the area: ")

        with database:
            cursor = database.cursor()

            QUERY = "SELECT AVG(ABS(requestedAmount - awardedAmount)) FROM Proposal WHERE competitionID IN (SELECT competitionID FROM Competition WHERE area=:area);"

            cursor.execute(QUERY, {"area":area})

            row = cursor.fetchone()

            if row:
                print("The average requested/awarded discrepancy for the specified area: ", row[0])
            else:
                print("No proposals found.")

    elif option == "5":
        proposalID = input("Enter the proposal ID: ")
        deadline = input("Enter the deadline for the new review (YYYY-MM-DD): ")
        reviewID = ""

        with database:
            cursor = database.cursor()

            QUERY = "INSERT INTO Review (proposalID, deadline, status) VALUES (:proposalID, :deadline, 'not submitted');"

            cursor.execute(QUERY, {"proposalID":proposalID, "deadline":deadline})

            database.commit()

            reviewID = cursor.lastrowid

        with database:
            cursor = database.cursor()

            QUERY = "SELECT R.* FROM Reviewer R JOIN (SELECT reviewerID, COUNT(*) AS reviewCount FROM Assignment A JOIN Review RV ON A.reviewID = RV.reviewID WHERE RV.status = 'not submitted' GROUP BY reviewerID HAVING reviewCount < 3) AS Subquery ON R.reviewerID = Subquery.reviewerID WHERE R.reviewerID NOT IN (SELECT DISTINCT A.reviewerID FROM Assignment A JOIN Reviewer R ON A.reviewerID = R.reviewerID JOIN Review RV ON A.reviewID = RV.reviewID JOIN Proposal P ON RV.proposalID = P.proposalID JOIN Collaborator C ON P.proposalID = C.proposalID JOIN Conflict CF ON R.researcherID = CF.researcherID WHERE C.proposalID = :proposal)"

            cursor.execute(QUERY, {"proposal":proposalID})

            rows = cursor.fetchall()

            if rows:
                print("The reviewers who can review the specified proposal: ")
            else:
                print("No reviewers found.")
            
            for row in rows:
                for column in row:
                    print(column, end=", ")
                print("\n")

        print("Choose a reviewer from the list above to assign to the proposal.")

        reviewerID = input("Enter the reviewer ID: ")

        with database:
            cursor = database.cursor()

            QUERY = "INSERT INTO Assignment (reviewerID, reviewID) VALUES (:reviewerID, :reviewID);"

            cursor.execute(QUERY, {"reviewerID":reviewerID, "reviewID":reviewID})

            database.commit()

            print("The reviewer has been assigned to the proposal.")

    elif option == "6":
        firstName = input("Enter the first name: ").capitalize()
        lastName = input("Enter the last name: ").capitalize()

        with database:
            cursor = database.cursor()

            QUERY = "SELECT * FROM Proposal WHERE proposalID IN (SELECT proposalID FROM Review WHERE reviewID IN (SELECT reviewID FROM Assignment WHERE reviewerID IN (SELECT reviewerID FROM Reviewer WHERE firstName=:firstName AND lastName=:lastName)));"

            cursor.execute(QUERY, {"firstName":firstName, "lastName":lastName})

            rows = cursor.fetchall()

            if rows:
                print("The proposal(s) that the specified reviewer needs to review: ")
            else:
                print("No proposals found.")

            for row in rows:
                for column in row:
                    print(column, end=", ")
                print("\n")

    elif option == "7":
        break
    else:
        print("Invalid option. Please try again.")

if database:
    database.close()
