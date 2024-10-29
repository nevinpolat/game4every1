import streamlit as st
from rag_flow import get_answer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Feedback, ChatHistory, SearchedGame
import weaviate
from datetime import datetime, timedelta
import traceback
import analytics  # Import analytics.py
import re  # Import regular expressions module for username validation

# Configure Streamlit Page
st.set_page_config(
    page_title="🎮 Game Instructor Assistant",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session timeout settings
SESSION_TIMEOUT_MINUTES = 15  # You can adjust the timeout duration here

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Welcome", "Ask Questions", "Analytics"])

# Initialize Weaviate Client
@st.cache_resource
def init_weaviate_client():
    try:
        WEAVIATE_URL = st.secrets["WEAVIATE"]["URL"]
        client = weaviate.Client(WEAVIATE_URL)
        if not client.is_ready():
            st.error(f"🚨 Cannot connect to Weaviate at {WEAVIATE_URL}. Please ensure it's running.")
            st.stop()
        return client
    except KeyError:
        st.error("🚨 WEAVIATE URL not found in secrets.")
        st.stop()

client = init_weaviate_client()

# Database Connection
@st.cache_resource
def init_db():
    try:
        DB_USER = st.secrets["DB"]["USER"]
        DB_PASSWORD = st.secrets["DB"]["PASSWORD"]
        DB_HOST = st.secrets["DB"]["HOST"]
        DB_PORT = st.secrets["DB"]["PORT"]
        DB_NAME = st.secrets["DB"]["NAME"]
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        return engine
    except KeyError as e:
        st.error(f"🚨 Missing database configuration for {e}.")
        st.stop()

engine = init_db()

# ORM Setup and Table Creation
Base.metadata.create_all(engine, checkfirst=True)
SessionLocal = sessionmaker(bind=engine)

# Function Definitions

def save_feedback_to_db(user_id, feedback_type):
    try:
        session = SessionLocal()
        feedback = Feedback(
            user_id=user_id,
            feedback_type=feedback_type,
            feedback_time=datetime.utcnow()
        )
        session.add(feedback)
        session.commit()
        session.refresh(feedback)
        feedback_id = feedback.feedback_id
        session.close()
        return feedback_id
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")
        st.error(traceback.format_exc())
        return None

def update_feedback(feedback_id, feedback_type):
    try:
        session = SessionLocal()
        feedback = session.query(Feedback).filter_by(feedback_id=feedback_id).first()
        if feedback:
            feedback.feedback_type = feedback_type
            feedback.feedback_time = datetime.utcnow()
            session.commit()
        session.close()
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")
        st.error(traceback.format_exc())

def get_feedback_type(feedback_id):
    try:
        session = SessionLocal()
        feedback = session.query(Feedback).filter_by(feedback_id=feedback_id).first()
        feedback_type = feedback.feedback_type if feedback else None
        session.close()
        return feedback_type
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")
        st.error(traceback.format_exc())
        return None

def save_chat_history_to_db(user_id, question, answer, game_id=None, feedback_id=None, is_related=False):
    try:
        session = SessionLocal()
        # If feedback_id is None, save a 'neutral' feedback
        if feedback_id is None:
            feedback = Feedback(
                user_id=user_id,
                feedback_type='neutral',
                feedback_time=datetime.utcnow()
            )
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            feedback_id = feedback.feedback_id
        chat_history = ChatHistory(
            user_id=user_id,
            question=question,
            answer=answer,
            timestamp=datetime.utcnow(),
            game_id=game_id,
            feedback_id=feedback_id,
            is_related=is_related
        )
        session.add(chat_history)
        session.commit()
        session.refresh(chat_history)
        chat_id = chat_history.chat_id  # Use chat_id instead of chat_history_id
        session.close()
        return feedback_id, chat_id
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")
        st.error(traceback.format_exc())
        return None, None

def validate_user_info(user_info):
    errors = []

    # Username validation: only letters and numbers
    if not user_info['userName'].strip():
        errors.append("🔴 **User Name** cannot be empty.")
    elif not re.match("^[A-Za-z0-9]+$", user_info['userName']):
        errors.append("🔴 **User Name** can only contain letters and numbers (no spaces or symbols).")

    if user_info['gender'] not in ['Male', 'Female', 'Other', 'Prefer not to say']:
        errors.append("🔴 **Gender** must be selected.")

    if not (1 <= user_info['age'] <= 120):
        errors.append("🔴 **Age** must be between 1 and 120.")

    return errors

def save_user_info_to_db(user_info):
    try:
        session = SessionLocal()
        existing_user = session.query(User).filter(User.user_name.ilike(user_info['userName'])).first()
        if existing_user:
            st.error("🚨 Username already exists. Please choose a different username.")
            session.close()
            return None

        user = User(
            user_name=user_info['userName'],
            gender=user_info['gender'],
            age=user_info['age'],
            registration_time=datetime.utcnow()
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        user_id = user.user_id
        session.close()
        return user_id
    except Exception as e:
        st.error(f"🚨 Database Error: {e}")
        st.error(traceback.format_exc())
        return None

def load_chat_history_from_db(user_id):
    session = SessionLocal()
    chat_entries = session.query(ChatHistory).filter_by(user_id=user_id).order_by(ChatHistory.timestamp.asc()).all()
    chat_history = []
    for entry in chat_entries:
        feedback_type = 'neutral'
        if entry.feedback_id:
            feedback = session.query(Feedback).filter_by(feedback_id=entry.feedback_id).first()
            if feedback:
                feedback_type = feedback.feedback_type
        chat_history.append({
            "question": entry.question,
            "answer": entry.answer,
            "game_id": entry.game_id,
            "is_related": entry.is_related,
            "feedback_id": entry.feedback_id,
            "feedback_type": feedback_type,
            "rewritten_question": None  # You may need to add this field to your database to store rewritten question
        })
    session.close()
    return chat_history

def check_session_timeout():
    if 'last_activity' in st.session_state:
        now = datetime.utcnow()
        if now - st.session_state['last_activity'] > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
            st.warning("🕒 Session timed out due to inactivity.")
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.stop()  # Stop the script execution
    st.session_state['last_activity'] = datetime.utcnow()

# Page Content Based on Selection

if page == "Welcome":
    check_session_timeout()
    st.title("🎮 Game Instructor Assistant")
    st.markdown("""
    Welcome to the **Game Instructor Assistant**! Here, you can register or log in to ask questions about your favorite games and receive detailed answers.

    **Features:**
    - **User Registration & Login:** Create your profile or log in with your username.
    - **Ask Questions:** Get insights, rules, strategies, and more about various games.

    Let's get started!
    """)
    st.info("ℹ️ You can ask up to 3 questions.")

    st.header("👤 User Registration & Login")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = {
            'userName': '',
            'gender': '',
            'age': 25
        }
        st.session_state['info_submitted'] = False

    tab1, tab2 = st.tabs(["📝 Register", "🔑 Login"])

    with tab1:
        with st.form("registration_form"):
            user_info = {
                'userName': '',
                'gender': '',
                'age': 25
            }

            user_info['userName'] = st.text_input("📝 **User Name**", value=user_info['userName'])

            gender_options = ['Male', 'Female', 'Other', 'Prefer not to say']
            user_info['gender'] = st.selectbox(
                "⚧ **Gender**",
                options=gender_options
            )

            user_info['age'] = st.number_input(
                "🎂 **Age**",
                min_value=1,
                max_value=120,
                value=user_info['age'],
                step=1
            )

            submit_reg = st.form_submit_button("✅ Register")

        if submit_reg:
            errors = validate_user_info(user_info)
            if errors:
                for error in errors:
                    st.error(error)
            else:
                user_id = save_user_info_to_db(user_info)
                if user_id:
                    st.success("✅ Registration successful! You can now log in.")
                    st.session_state['info_submitted'] = True

    with tab2:
        with st.form("login_form"):
            login_username = st.text_input("📝 **Username**", key="login_username")
            submit_login = st.form_submit_button("🔑 Login")

        if submit_login:
            if not login_username.strip():
                st.error("🔴 **Username** cannot be empty.")
            else:
                session = SessionLocal()
                user = session.query(User).filter(User.user_name.ilike(login_username.strip())).first()
                session.close()
                if user:
                    st.success(f"✅ Logged in as {user.user_name}!")
                    # Clear session state before setting new user data
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.session_state['logged_in'] = True
                    st.session_state['user_id'] = user.user_id
                    st.session_state['user_info'] = {
                        'userName': user.user_name,
                        'gender': user.gender,
                        'age': user.age
                    }
                    # Load user's chat history from the database
                    st.session_state['chat_history'] = load_chat_history_from_db(user.user_id)
                    st.session_state['last_activity'] = datetime.utcnow()
                    st.success(f"Welcome, {user.user_name}!")  # Display a welcome message
                else:
                    st.error("🚨 Username not found. Please register first.")

    if st.session_state.get('logged_in', False):
        if st.button("🔄 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ Logged out successfully.")
            st.stop()

elif page == "Ask Questions":
    check_session_timeout()
    if st.session_state.get('logged_in', False):
        st.title("💬 Ask a Question")
        st.subheader("👤 Your Information")
        st.write(f"**Name:** {st.session_state['user_info']['userName']}")
        st.write(f"**Gender:** {st.session_state['user_info']['gender']}")
        st.write(f"**Age:** {st.session_state['user_info']['age']}")
        st.markdown(f"### Welcome, **{st.session_state['user_info']['userName']}**! You can ask up to 3 questions.")
        user_query = st.text_input("💡 **Enter your question about games:**", key="user_query")

        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        if 'feedback_given' not in st.session_state:
            st.session_state['feedback_given'] = {}

        if st.button("🗨️ Get Answer") and user_query:
            try:
                session_db = SessionLocal()
                question_count = session_db.query(ChatHistory).filter(ChatHistory.user_id == st.session_state['user_id']).count()
                session_db.close()
                if question_count >= 3:
                    st.warning("⚠️ You have reached the maximum of 3 questions allowed.")
                else:
                    with st.spinner("🔍 Processing your question..."):
                        answer_result = get_answer(
                            user_query.strip(),
                            st.session_state['user_id'],
                            SessionLocal(),  # Pass a new session instance
                            k=1,  # Fetch only 1 relevant game
                            hybrid=False,  # Indicate that we're using pure vector search
                            weaviate_client=client
                        )

                    if answer_result['is_related']:
                        rewritten_question = answer_result.get('rewritten_question', '')
                        if rewritten_question and rewritten_question != user_query.strip():
                            st.markdown(f"**Rewritten Question:** {rewritten_question}")
                        if "answers" in answer_result:
                            for idx, ans in enumerate(answer_result["answers"], 1):
                                st.subheader(f"**Game Name:** {ans['game_name']}")
                                st.write(ans["answer"])
                                feedback_id, chat_id = save_chat_history_to_db(
                                    user_id=st.session_state['user_id'],
                                    question=user_query.strip(),
                                    answer=ans["answer"],
                                    game_id=ans["game_id"],
                                    is_related=True
                                )
                                st.session_state['chat_history'].append({
                                    "question": user_query.strip(),
                                    "answer": ans["answer"],
                                    "game_id": ans["game_id"],
                                    "is_related": True,
                                    "feedback_id": feedback_id,
                                    "feedback_type": 'neutral',
                                    "rewritten_question": rewritten_question
                                })
                        else:
                            st.warning(answer_result['message'])
                            rewritten_question = answer_result.get('rewritten_question', '')
                            if rewritten_question and rewritten_question != user_query.strip():
                                st.markdown(f"**Rewritten Question:** {rewritten_question}")
                            feedback_id, chat_id = save_chat_history_to_db(
                                user_id=st.session_state['user_id'],
                                question=user_query.strip(),
                                answer=answer_result['message'],
                                is_related=True
                            )
                            st.session_state['chat_history'].append({
                                "question": user_query.strip(),
                                "answer": answer_result['message'],
                                "game_id": None,
                                "is_related": True,
                                "feedback_id": feedback_id,
                                "feedback_type": 'neutral',
                                "rewritten_question": rewritten_question
                            })
                    else:
                        # Save the non-related question and the message
                        st.warning(answer_result['message'])
                        rewritten_question = answer_result.get('rewritten_question', '')
                        if rewritten_question and rewritten_question != user_query.strip():
                            st.markdown(f"**Rewritten Question:** {rewritten_question}")
                        feedback_id, chat_id = save_chat_history_to_db(
                            user_id=st.session_state['user_id'],
                            question=user_query.strip(),
                            answer=answer_result['message'],
                            is_related=False
                        )
                        st.session_state['chat_history'].append({
                            "question": user_query.strip(),
                            "answer": answer_result['message'],
                            "game_id": None,
                            "is_related": False,
                            "feedback_id": feedback_id,
                            "feedback_type": 'neutral',
                            "rewritten_question": rewritten_question
                        })
                st.session_state['last_activity'] = datetime.utcnow()
            except Exception as e:
                st.error(f"🚨 An error occurred: {e}")
                st.error(traceback.format_exc())

        if st.session_state.get('chat_history'):
            st.markdown("### 📝 Your Chat History:")
            feedbacks_given = 0
            total_questions = len(st.session_state['chat_history'])
            for idx, chat in enumerate(st.session_state['chat_history'], 1):
                st.markdown(f"**Q{idx}:** {chat['question']}")
                rewritten_question = chat.get('rewritten_question', '')
                if rewritten_question and rewritten_question != chat['question']:
                    st.markdown(f"**Rewritten Question:** {rewritten_question}")
                st.markdown(f"**A{idx}:**\n{chat['answer']}", unsafe_allow_html=True)

                if chat.get('game_id'):
                    session_db = SessionLocal()
                    searched_game = session_db.query(SearchedGame).filter_by(game_id=chat['game_id']).first()
                    session_db.close()
                    if searched_game:
                        st.markdown(f"**Searched Game ID:** {searched_game.game_id} | **Search Time:** {searched_game.searched_time}")
                st.markdown(f"**Game Related:** {'Yes' if chat.get('is_related') else 'No'}")

                # Add feedback buttons
                feedback_id = chat.get('feedback_id')
                feedback_type = st.session_state['feedback_given'].get(feedback_id, chat.get('feedback_type', 'neutral'))
                if feedback_id is not None:
                    if feedback_type == 'neutral':
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("👍", key=f"upvote_{feedback_id}"):
                                update_feedback(feedback_id, 'up')
                                st.session_state['feedback_given'][feedback_id] = 'up'
                                chat['feedback_type'] = 'up'
                                feedback_type = 'up'
                        with col2:
                            if st.button("😐", key=f"neutral_{feedback_id}"):
                                update_feedback(feedback_id, 'neutral')
                                st.session_state['feedback_given'][feedback_id] = 'neutral'
                                chat['feedback_type'] = 'neutral'
                                feedback_type = 'neutral'
                        with col3:
                            if st.button("👎", key=f"downvote_{feedback_id}"):
                                update_feedback(feedback_id, 'down')
                                st.session_state['feedback_given'][feedback_id] = 'down'
                                chat['feedback_type'] = 'down'
                                feedback_type = 'down'
                    if feedback_type != 'neutral':
                        feedback_display = {
                            'up': '👍 Upvote',
                            'down': '👎 Downvote',
                            'neutral': '😐 Neutral'
                        }
                        st.markdown(f"**Feedback Given:** {feedback_display.get(feedback_type, '😐 Neutral')}")
                        feedbacks_given += 1
                st.markdown("\n")

            # Display the message only after all feedbacks are given
            if feedbacks_given == total_questions and total_questions > 0:
                st.info("✅ You have provided feedback for all your questions.")

    else:
        st.warning("🔒 Please log in to ask questions.")

elif page == "Analytics":
    #st.title("📈 Comprehensive Analytics Dashboard")
    session = SessionLocal()
    analytics.show_analytics(session)
    session.close()
