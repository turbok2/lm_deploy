import hmac
import streamlit as st

# def check_password():
#     """Returns `True` if the user had the correct password."""

#     def password_entered():
#         """Checks whether a password entered by the user is correct."""
#         if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
#             st.session_state["password_correct"] = True
#             del st.session_state["password"]  # Don't store the password.
#         else:
#             st.session_state["password_correct"] = False

#     # Return True if the password is validated.
#     if st.session_state.get("password_correct", False):
#         return True

#     # Show input for password.
#     st.text_input(
#         "Password", type="password", on_change=password_entered, key="password"
#     )
#     if "password_correct" in st.session_state:
#         st.error("😕 Password incorrect")
#     return False

# if not check_password():
#     st.stop()  # Do not continue if check_password is not True.


st.set_page_config(page_title="LearningMate", page_icon="📖", layout="wide")
st.title("📖 Learners' LearningMate")
st.markdown(
    """
### QuizBot: 입력된 학습 내용을 기반으로 퀴즈를 생성하고 풀어볼 수 있는 서비스입니다.
### LearningMate: 자유롭게 사용할 수 있는 학습용 챗봇입니다.
    """
)
st.sidebar.page_link("pages/1-QuizBot.py", label="QuizBot")
st.sidebar.page_link("pages/2-LearningMate.py", label="LearningMate")
