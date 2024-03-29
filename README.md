# Research Grant Council Database Specifications
![Entity Relationship Diagram](assets/erd.png)

## Objective
The primary objective of this database is to efficiently manage and store information related to grant competitions, submissions, reviewers, and the outcomes of these submissions for a research grant council. The database will facilitate tracking grant proposals, review assignments, and the allocation of funds to researchers across various disciplines.

## Entities and Requirements

### 1. Researchers:
- Store personal information including first and last name, email address, and affiliated organization (university).
- Track their submissions to grant competitions as principal investigators or collaborators.

### 2. Grant Competitions (Calls for Proposals):
- Each competition should have a unique identifier, title, application deadline, a brief description, area of research (e.g., biology, computer science), and its status (open/closed).
- Track all submissions related to each grant competition.

### 3. Grant Proposals:
- Proposals need a unique identifier, requested amount, related competition, principal investigator, collaborators, application status (submitted, awarded, not awarded), and the awarded amount (if any).
- The database should allow tracking of changes in the status or awarded amounts over time.

### 4. Reviewers:
- Track which grant applications they have reviewed and any conflicts of interest with certain proposals.
- Record assignments to Grant Selection Committees and their participation in meetings.

### 5. Review:
- Track all reviews that were assigned, their deadline and whether they were submitted or not.
- Record who reviewed which review and find co-reviewers of certain reviewers.

### 6. Meetings:
- Track which competitions were discussed at which meetings including the date of the meeting.
- Limit meetings to only reviewers who reviewed a proposal from the competition being discussed.

## Additional Considerations
- The database should allow for querying active competitions, proposals by area, and large proposals (defined by a request of more than $20,000 or involving more than 10 participants).
- It should support the assignment of reviewers to proposals, ensuring no conflict of interest and adherence to review capacity (e.g., a maximum of three proposals per reviewer).
- The schema should be designed to easily retrieve proposals requiring review by a specific reviewer and to support analysis such as calculating average discrepancies between requested and awarded amounts by area.

## Functional Requirements
- Scalability: Design the database to handle an increasing number of proposals, competitions, and users without performance degradation.
- Data Integrity: Enforce constraints and validations to maintain accurate and consistent data across the database.

## Installation

This project requires Python 3.8 or later, Jupyter Notebook, and SQLite. Follow the steps below to set up the environment and run the project:

1. **Install Python:** Download and install Python from [python.org](https://www.python.org/). Ensure that Python and pip are added to your system's PATH.

2. **Install Jupyter Notebook:** Run the following command in your terminal or command prompt to install Jupyter Notebook:
   ```
   pip install notebook
   ```

3. **Clone the Repository:** Clone the project repository to your local machine using Git:
   ```
   git clone https://github.com/ahmad-masud/Research-Grant-Council-Database.git
   ```

4. **Navigate to the Project Directory:** Change into the project directory:
   ```
   cd Research-Grant-Council-Database
   ```

5. **Install Required Libraries:** Install the required Python libraries specified in the `requirements.txt` file:
   ```
   pip install -r requirements.txt
   ```

6. **Launch Jupyter Notebook:** Start Jupyter Notebook by running the following command in the project directory:
   ```
   jupyter notebook
   ```

7. **Open the Project Notebook:** In the Jupyter Notebook interface, navigate to the project notebook file (`.ipynb`) and open it to start working on the project.

Follow these steps to set up and run the project locally on your machine. Ensure that you have SQLite installed on your system, as it is used for the database component of this project. SQLite can be installed and configured following the instructions on the [SQLite official website](https://www.sqlite.org/).
