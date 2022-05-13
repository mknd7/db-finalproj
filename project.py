from tkinter import E
import streamlit as st
import mysql.connector

# Initialize connection (using st.experimental_singleton to only run once)
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

# Perform query (using st.experimental_memo to only rerun when the query changes or after 10 min)
@st.experimental_memo(ttl=600)
def run_query(operation, params=None):
    with conn.cursor() as cur:
        # Operation and params separately, SQL injection-safe
        cur.execute(operation, params)
        return cur.fetchall()

def attempt_login(user_input, pass_input):
   
    userQuery = run_query("""SELECT userid
                     FROM user
                     WHERE username=%(username)s;""",
                     {'username': user_input})

    passQuery = None
    if userQuery:
        passQuery = run_query("""SELECT userid
                        FROM user
                        WHERE userid=%(userid)s
                        AND password=%(password)s;""",
                        {'userid': userQuery[0][0],
                         'password': pass_input})

    if passQuery:
        st.session_state["login_valid"] = True
        st.session_state["userid"] = userQuery[0][0]
    else:
        st.session_state["login_valid"] = False

def logout():
    del st.session_state["login_valid"]
    del st.session_state["userid"]

def show_login():
    user_input = st.sidebar.text_input("Username: ")
    pass_input = st.sidebar.text_input("Password: ", type="password")
    st.sidebar.button("Login", on_click=attempt_login, args=(user_input, pass_input))

def show_register():
    st.write("Register")
    with st.form("my_form"):
        
        f_email = st.text_input("Email: ")
        f_user = st.text_input("Username: ")
        f_pass = st.text_input("Password: ", type="password")
        f_cpass = st.text_input("Confirm password: ", type="password")
        
        f_city = st.text_input("City: ")
        f_state = st.text_input("State: ")
        f_country = st.text_input("Country: ")
        f_profile = st.text_area("Profile: ")

        registered = st.form_submit_button("Register")
        if registered:
            st.write("Registered!")

# Start of app control flow
st.title("Q&A webapp")
conn = init_connection()

if "login_valid" not in st.session_state:
    show_login()
    show_register()
elif not st.session_state["login_valid"]:
    show_login()
    show_register()
    st.sidebar.error("Invalid credentials!")
else:
    username = run_query("""SELECT username
                         FROM user
                         WHERE userid=%(userid)s;""",
                         {'userid': st.session_state["userid"]})[0][0]
    st.sidebar.write("Hello {}!".format(username))
    st.sidebar.success("Logged in!")
    st.sidebar.button("Logout", on_click=logout)

# rows = run_query("SELECT * from user;")
# for row in rows:
#     st.write(f"{row[0]} is {row[1]}")
