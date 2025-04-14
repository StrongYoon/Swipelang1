import streamlit as st
from utils.data_manager import *
from utils.quiz_generator import generate_quiz
from utils.tts import speak_in_browser
import random
import pandas as pd

st.set_page_config(page_title="SwipeLang", page_icon="📚", layout="centered")

slangs = load_slang_data()
history = load_user_history()
today = get_today_key()

if today not in history:
    history[today] = {"known": [], "review": [], "viewed": []}
    save_user_history(history)

available_slangs = [s for s in slangs if s["phrase"] not in history[today]["viewed"]]

# ✅ 세션 상태 초기화
if "current" not in st.session_state and available_slangs:
    st.session_state.current = random.choice(available_slangs)

if "show_meaning" not in st.session_state:
    st.session_state.show_meaning = False

if "quiz_active" not in st.session_state:
    st.session_state.quiz_active = False

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "quiz_result" not in st.session_state:
    st.session_state.quiz_result = None

# ✅ UI 시작
st.markdown("<h1 style='text-align: left; font-size: 40px;'>📚 SwipeLang</h1>", unsafe_allow_html=True)
st.markdown("### 오늘의 슬랭")

if available_slangs:
    current = st.session_state.current
    st.write(f"🗯️ **{current['phrase']}**")

    if st.button("🔊 발음 듣기"):
        audio_html = speak_in_browser(current["phrase"])
        st.markdown(audio_html, unsafe_allow_html=True)

    if st.button("📖 해석 보기"):
        st.session_state.show_meaning = True

    if st.session_state.show_meaning:
        st.success(f"📖 해석: {current['meaning']}")
        if "example" in current and not pd.isna(current["example"]):
            st.markdown(f"💬 예문: *{current['example']}*")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ 기억했어"):
            history[today]["known"].append(current)
            history[today]["viewed"].append(current["phrase"])
            save_user_history(history)
            del st.session_state["current"]
            st.session_state.show_meaning = False
            st.rerun()
    with col2:
        if st.button("🔁 복습할래"):
            history[today]["review"].append(current)
            history[today]["viewed"].append(current["phrase"])
            save_user_history(history)
            del st.session_state["current"]
            st.session_state.show_meaning = False
            st.rerun()
else:
    st.warning("오늘 모든 표현을 다 학습하셨습니다!")

st.markdown("---")
st.markdown(f"✅ 오늘 외운 표현: {len(history[today]['known'])}개")
st.markdown(f"🔁 복습할 표현: {len(history[today]['review'])}개")

with st.expander("📋 복습/기억한 표현 보기"):
    st.subheader("✅ 기억한 표현")
    for item in history[today]["known"]:
        st.markdown(f"- {item['phrase']} : {item['meaning']}")
    st.subheader("🔁 복습할 표현")
    for item in history[today]["review"]:
        st.markdown(f"- {item['phrase']} : {item['meaning']}")

# ✅ 퀴즈 모드
if st.button("🧠 퀴즈 모드 시작"):
    if len(history[today]["known"]) < 3:
        st.warning("퀴즈를 시작하려면 최소 3개의 기억한 표현이 필요합니다.")
    else:
        st.session_state.quiz = generate_quiz(history[today]["known"])
        st.session_state.quiz_active = True
        st.session_state.quiz_result = None

# ✅ 퀴즈 실행 & 결과 유지
if st.session_state.quiz_active and st.session_state.quiz:
    quiz = st.session_state.quiz
    st.markdown(f"**문제: {quiz['question']}의 의미는?**")

    for i, option in enumerate(quiz["choices"], 1):
        if st.button(f"{i}. {option}"):
            if option == quiz["answer"]:
                st.session_state.quiz_result = ("⭕ 정답입니다! 🎉", "success")
            else:
                st.session_state.quiz_result = (f"❌ 오답입니다. 정답은 👉 {quiz['answer']}", "error")

    if st.session_state.quiz_result:
        msg, msg_type = st.session_state.quiz_result
        if msg_type == "success":
            st.success(msg)
        else:
            st.error(msg)
