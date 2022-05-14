## DB Project

by **Mukund Vijayaraghavan**

**Net ID:** mv2167

The objective of this project is to create a **Q&A system** using a database and incorporate functionality via a simple web app capable of running locally. Here, [Streamlit](https://github.com/streamlit/streamlit) (a lightweight Python framework) is used, as this is a fairly data-centered application. Questions (categorised into topics and subtopics), answers, users, topics (and subtopics) are all modelled in a MySQL database - the app connects with an instance of this DB to view and insert data.

Users are able to:
- register
- log in/out
- view questions
- view specific question
- post a new question
- view answers to a question
- post answer for a question
- search across questions (full-text search)

Run the app:
```
streamlit run project.py
```
