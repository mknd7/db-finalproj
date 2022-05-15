## DB Project

by **Mukund Vijayaraghavan**

**Net ID:** mv2167

The objective of this project is to create a **Q&A system** using a database and incorporate functionality via a simple web app capable of running locally. Here, [Streamlit](https://github.com/streamlit/streamlit) (a lightweight Python framework) is used, as this is a fairly data-centered application. Questions (categorised into topics and subtopics), answers, users, topics (and subtopics) are all modelled in a MySQL database - the app connects with an instance of this DB to view and insert data.



**Users are able to**:

- register
- log in/out
- view questions
- view specific question
- post a new question
- view answers to a question
- post answer for a question
- search across questions (full-text search)



**Running the project**:

1. First, the DB must be created (preferably using MYSQL Workbench) - this can be done using `queries/project_mv2167.sql`, which contains the `CREATE` statements.

   Alternatively, the `project.mwb` file can be opened directly in MySQL Workbench - it contains the ERR (Enhanced Entity-Relationship) design that can create and administer the DB.

2. (Optional) Populate DB with data, either using Workbench's GUI or manual SQL statements.

3. To enable full-text search (across the `qnbody` attribute - question content):

   ```
   ALTER TABLE question
   ADD FULLTEXT(qnbody)
   ```

4. Add a `.streamlit/secrets.toml` file that looks like this:

   ```
   [mysql]
   host = "localhost"
   port = 3306
   database = "my-db-name"
   user = "my-user-name"
   password = "my-password"
   ```

5. Ensure that the MySQL server is running, then run the app:

   ```
   streamlit run project.py
   ```

6. Populate DB with data using app interface, then test out the functionality!
