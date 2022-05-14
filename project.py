import re
import mysql.connector
import streamlit as st

# Initialize connection (using st.experimental_singleton to only run once)
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets['mysql'])

def run_query(operation, params=None):
    with conn.cursor() as cur:
        # Operation and params separately, SQL injection-safe
        cur.execute(operation, params)
        return cur.fetchall()

def login(user_input, pass_input):
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
        st.session_state['login_valid'] = True
        st.session_state['userid'] = userQuery[0][0]
    else:
        st.session_state['login_valid'] = False

def logout():
    del st.session_state['login_valid']
    del st.session_state['userid']

def show_login():
    user_input = st.sidebar.text_input('Username: ')
    pass_input = st.sidebar.text_input('Password: ', type='password')
    st.sidebar.button('Login', on_click=login, args=(user_input, pass_input))

def validate_reg(email, passw, cpass):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(email_regex, email):
        return False
    if passw != cpass:
        return False
    return True

def show_register():
    st.write('Register')

    with st.form('register_form'):
        fd_email = st.text_input('Email: ')
        fd_user = st.text_input('Username: ')
        fd_passw = st.text_input('Password: ', type='password')
        fd_cpass = st.text_input('Confirm password: ', type='password')
        
        fd_city = st.text_input('City: ')
        fd_state = st.text_input('State: ')
        fd_country = st.text_input('Country: ')
        fd_profile = st.text_area('Profile: ')
        
        submitted = st.form_submit_button('Submit')
        if submitted:
            if not fd_user or not fd_city or not fd_state or not fd_country:
                st.error('All details but profile are required')
            elif not validate_reg(fd_email, fd_passw, fd_cpass):
                st.error('Invalid email or unmatching password')
            else:
                run_query("""INSERT INTO user (username, email, password, profile, addr_city, addr_state, addr_country)
                        VALUES (%(uname)s, %(email)s, %(passw)s, %(profile)s, %(city)s, %(state)s, %(country)s);""",
                        {'uname': fd_user, 'email': fd_email, 'passw': fd_passw, 'profile': fd_profile,
                        'city': fd_city, 'state': fd_state, 'country': fd_country})
                st.success('Registered!')

# Start of app control flow
st.title('Q&A webapp')
st.sidebar.title('Q&A webapp')
st.sidebar.info('by Mukund Vijayaraghavan [mv2167]')

conn = init_connection()
conn.autocommit = True

if 'login_valid' not in st.session_state:
    show_login()
    show_register()
elif not st.session_state['login_valid']:
    show_login()
    show_register()
    st.sidebar.error('Invalid credentials!')
else:
    # show username on the side
    username = run_query("""SELECT username
                         FROM user
                         WHERE userid=%(userid)s;""",
                         {'userid': st.session_state['userid']})[0][0]
    st.sidebar.write('Hello {}!'.format(username))
    st.sidebar.success('Logged in!')
    st.sidebar.button('Logout', on_click=logout)
    
    

# rows = run_query("SELECT * from user;")
# for row in rows:
#     st.write(f"{row[0]} is {row[1]}")
