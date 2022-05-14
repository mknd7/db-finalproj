from ast import arg
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
    st.sidebar.header("Log in to get started.")
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
        # show questions page by default
        st.session_state['questions-page'] = True
    else:
        st.session_state['login_valid'] = False

def logout():
    del st.session_state['login_valid']
    del st.session_state['userid']

def show_login():
    user_input = st.sidebar.text_input('Username: ')
    pass_input = st.sidebar.text_input('Password: ', type='password')
    st.sidebar.button('Log in', on_click=login, args=(user_input, pass_input))

def change_page_state(prev, curr):
    del st.session_state[prev]
    st.session_state[curr] = True

def validate_reg(email, passw, cpass):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.match(email_regex, email):
        return False
    if passw != cpass:
        return False
    return True

def show_register():
    st.subheader('Register')

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
                st.error('All details except profile are required')
            elif not validate_reg(fd_email, fd_passw, fd_cpass):
                st.error('Invalid email or unmatching password')
            else:
                run_query("""INSERT INTO user (username, email, password, profile, addr_city, addr_state, addr_country)
                        VALUES (%(uname)s, %(email)s, %(passw)s, %(profile)s, %(city)s, %(state)s, %(country)s);""",
                        {'uname': fd_user, 'email': fd_email, 'passw': fd_passw, 'profile': fd_profile,
                        'city': fd_city, 'state': fd_state, 'country': fd_country})
                st.success('Registered!')

def show_questions():
    st.button('Post new question', on_click=change_page_state, args=('questions-page', 'post-question'))
    
    st.subheader('Questions')
    questions = run_query("""SELECT qnid, date_format(qnwhen, "%D %M %Y %r"), title, 
                          T.topicname as topic, ST.topicname as subtopic
                          FROM question Q
                          JOIN topic T ON Q.topicid=T.topicid
                          LEFT JOIN topicinner ST ON Q.tinnerid=ST.tinnerid
                          ORDER BY qnwhen DESC;""")
    
    col1, col2 = st.columns(2)
    col1.text_input('Question to open:', placeholder='Enter qnid here', key='openedQuestion')
    col2.text('Open:')
    col2.button(">", on_click=change_page_state, args=('questions-page', 'question-single'))
    st.table(questions)

def show_single_question():
    st.button('Go back', on_click=change_page_state, args=('question-single', 'questions-page'))
    
    openedQnid = st.session_state['openedQuestion'] if 'openedQuestion' in st.session_state else st.session_state['Qnid']
    question = run_query("""SELECT T.topicname as topic, ST.topicname as subtopic, 
                         date_format(qnwhen, "%D %M %Y %r"), title, qnbody, resolved
                         FROM question Q
                         JOIN topic T ON Q.topicid=T.topicid
                         LEFT JOIN topicinner ST ON Q.tinnerid=ST.tinnerid
                         WHERE qnid=%(qnid)s;""",
                         {'qnid': openedQnid})[0]
    
    st.subheader(question[3])
    st.markdown('**Topic**: {}'.format(question[0]))
    st.markdown('**Subtopic**: {}'.format(question[1]))
    st.caption('Posted on: {}'.format(question[2]))
    st.write(question[4])
    
    resolved = question[5]
    if resolved:
        st.session_state['Qnid'] = openedQnid
        st.button('View answers', on_click=change_page_state, args=('question-single', 'answers-page'))
    else:
        st.warning("Unresolved - no answers yet.")

def show_answers():
    st.button('Go back', on_click=change_page_state, args=('answers-page', 'question-single'))
    
    st.subheader('Answers')
    openedQnid = st.session_state['Qnid']
    question = run_query("""SELECT title, qnbody
                         FROM question
                         WHERE qnid=%(qnid)s;""",
                         {'qnid': openedQnid})[0]
    answers = run_query("""SELECT date_format(answhen, "%D %M %Y %r"), ansbody, upvotes
                        FROM answer
                        WHERE qnid=%(qnid)s;""",
                        {'qnid': openedQnid})
    
    st.markdown('**Question**: {}'.format(question[0]))
    st.write(question[1])
    st.table(answers)

def show_postnew():
    st.button('Go back', on_click=change_page_state, args=('post-question', 'questions-page'))
    st.subheader('Post new question')

    topics = run_query("""SELECT topicname
                        FROM topic""")
    topics = [t for sublist in topics for t in sublist]
    fd_topic = None
    
    def get_topic_id():
        return run_query("""SELECT topicid
                            FROM topic
                            WHERE topicname=%(tname)s;""",
                            {'tname': fd_topic})[0][0]
    
    fd_topic = st.selectbox('Select topic:', topics, on_change=get_topic_id)
    fd_topicid = get_topic_id()
    
    def get_subtopic_id():
        return run_query("""SELECT tinnerid
                         FROM topicinner
                         WHERE topicname=%(tname)s;""",
                         {'tname': fd_subtopic})[0][0]
    
    subtopics = run_query("""SELECT topicname
                            FROM topicinner
                            WHERE topicid=%(parenttopic)s;""",
                            {'parenttopic': fd_topicid})
    fd_subtopicid = None
    
    if subtopics:
        subtopics = [t for sublist in subtopics for t in sublist]
        fd_subtopic = st.selectbox('Select subtopic:', subtopics)
        fd_subtopicid = get_subtopic_id()
    else:
        fd_subtopic = st.selectbox('Select subtopic:', subtopics, disabled=True)
    
    with st.form('register_form'):
        fd_title = st.text_input('Title: ')
        fd_body = st.text_area('Body: ')
        
        posted = st.form_submit_button('Post')
        if posted:
            if not fd_topic or not fd_title or not fd_body:
                st.error('All details except subtopic are required')
            else:
                run_query("""INSERT INTO question (userid, topicid, tinnerid, title, qnbody, qnwhen)
                        VALUES (%(userid)s, %(topicid)s, %(subtopicid)s, %(title)s, %(qnbody)s, NOW());""",
                        {'userid': st.session_state['userid'], 'topicid': fd_topicid, 
                         'subtopicid': fd_subtopicid, 'title': fd_title, 'qnbody': fd_body})
                st.success('Posted!')

# Start of app control flow
st.title('Q&A webapp')
st.sidebar.title('Q&A webapp')
st.sidebar.info('by Mukund Vijayaraghavan [mv2167]')

conn = init_connection()
conn.autocommit = True


# hardcode for testing
# st.session_state['login_valid'] = True
# st.session_state['userid'] = 1
# st.session_state['questions-page'] = True


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
    st.sidebar.header('Hello {}.'.format(username))
    st.sidebar.success('Logged in!')
    st.sidebar.button('Log out', on_click=logout)
    
    if 'questions-page' in st.session_state:
        show_questions()
    elif 'post-question' in st.session_state:
        show_postnew()
    elif 'question-single' in st.session_state:
        show_single_question()
    elif 'answers-page' in st.session_state:
        show_answers()
