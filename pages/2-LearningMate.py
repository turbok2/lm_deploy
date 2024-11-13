import streamlit as st
from openai import OpenAI
import os
import time

MY_OPENAI_API_KEY = os.getenv("MY_OPENAI_API_KEY")
LM_ASSISTANT_ID = os.getenv("LM_ASSISTANT_ID")
LM_THREAD_ID = os.getenv("LM_THREAD_ID")

client = OpenAI(api_key=MY_OPENAI_API_KEY)
assistant = client.beta.assistants.retrieve(assistant_id=LM_ASSISTANT_ID)

# 사이드바 페이지 링크
with st.sidebar:
    st.page_link("pages/1-QuizBot.py", label="QuizBot")
    st.page_link("pages/2-LearningMate.py", label="LearningMate")


# 메시지를 보내고 응답을 받아오는 함수
@st.spinner("요청 처리중...")
def run_message(message):
    client.beta.threads.messages.create(
        thread_id=LM_THREAD_ID, role="user", content=message
    )
    response = client.beta.threads.runs.create_and_poll(
        thread_id=LM_THREAD_ID, assistant_id=LM_ASSISTANT_ID
    )
    while response.status != "completed":
        print(response.status)
        time.sleep(1)
    messages = client.beta.threads.messages.list(thread_id=LM_THREAD_ID)
    if messages and messages.data:
        return messages.data[0].content[0].text.value
    return "응답을 받을 수 없습니다."

    # if messages and messages.data:
    #     # 메시지를 역순으로 순회
    #     for msg in reversed(messages.data):
    #         print(msg.content[0].text.value)
    #         if msg.role == "assistant":
    #             return msg.content[0].text.value
    # return "응답을 받을 수 없습니다."
        # 일정 시간 동안 최신 메시지가 나올 때까지 대기


# 버튼을 클릭했을 때 공통으로 처리하는 함수
def handle_button_click(message):
    st.session_state.messages.append({"role": "user", "content": message})
    response = run_message(message)
    st.session_state.messages.append({"role": "assistant", "content": response})


# 세션 상태에 메시지 리스트가 없으면 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "무엇을 도와드릴까요?"}
    ]


# 대화 기록 지우기
def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "무엇을 도와드릴까요?"}
    ]


st.sidebar.button("대화 기록 지우기", on_click=clear_chat_history)

# starter UI 버튼 구성
col1, col2, col3, col4 = st.columns([1] * 4)

# 버튼이 클릭되면 handle_button_click 함수 호출
with col1:
    if st.button("현재 나의 학습 주제를 모두 보여줘"):
        handle_button_click("현재 나의 학습 주제를 모두 보여줘")
with col2:
    if st.button("내가 틀린 문제의 주제들을 모두 보여줘"):
        handle_button_click("내가 틀린 문제의 주제들을 모두 보여줘")
with col3:
    if st.button("내가 틀린 문제들을 보여줘"):
        handle_button_click("내가 틀린 문제들을 보여줘")
with col4:
    if st.button("학습 데이터를 초기화해줘"):
        handle_button_click("학습 데이터를 초기화해줘")


# 프롬프트 입력 처리
if prompt := st.chat_input("메시지를 입력하세요."):
    response = run_message(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})

# 세션에 저장된 모든 메시지를 채팅에 표시
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# print(st.session_state.messages)
