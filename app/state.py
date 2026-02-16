import streamlit as st

from app.config import DEFAULT_DIFFICULTY, MODEL_BY_DIFFICULTY


def init_state() -> None:
    if "stage" not in st.session_state:
        st.session_state.stage = "instructions"
    if "uploaded_text" not in st.session_state:
        st.session_state.uploaded_text = ""
    if "uploaded_name" not in st.session_state:
        st.session_state.uploaded_name = ""
    if "messages_used" not in st.session_state:
        if "attempts_used" in st.session_state:
            st.session_state.messages_used = st.session_state.attempts_used
        else:
            st.session_state.messages_used = 0
    if "turns" not in st.session_state:
        st.session_state.turns = []
    if "uploader_nonce" not in st.session_state:
        st.session_state.uploader_nonce = 0
    legacy_difficulty = st.session_state.get("difficulty")
    if "selected_difficulty" not in st.session_state:
        if legacy_difficulty in MODEL_BY_DIFFICULTY:
            st.session_state.selected_difficulty = legacy_difficulty
        else:
            st.session_state.selected_difficulty = DEFAULT_DIFFICULTY
    if "difficulty_input" not in st.session_state:
        st.session_state.difficulty_input = st.session_state.selected_difficulty


def get_selected_difficulty() -> str:
    difficulty = st.session_state.get("selected_difficulty", DEFAULT_DIFFICULTY)
    if difficulty not in MODEL_BY_DIFFICULTY:
        return DEFAULT_DIFFICULTY
    return difficulty


def get_selected_model_name() -> str:
    return MODEL_BY_DIFFICULTY[get_selected_difficulty()]


def reset_round(keep_uploaded_file: bool) -> None:
    st.session_state.messages_used = 0
    st.session_state.turns = []

    if not keep_uploaded_file:
        st.session_state.uploaded_text = ""
        st.session_state.uploaded_name = ""
        st.session_state.uploader_nonce += 1
