import html

import streamlit as st

from app.config import DEFAULT_DIFFICULTY, DIFFICULTY_OPTIONS, MODEL_BY_DIFFICULTY
from app.state import get_selected_model_name, reset_round
from app.ui.components import render_hero
from app.utils import decode_text_file


def render_setup_screen() -> None:
    render_hero(
        "Round Setup",
        "Red Team uploads the Blue Team defense file and starts the arena.",
    )

    st.markdown(
        """
<div class="panel">
  <h3>Upload Blue Team .txt file</h3>
  <p class="micro">This file is used as the model system prompt for the full round.</p>
</div>
        """,
        unsafe_allow_html=True,
    )

    st.radio(
        "Choose model difficulty",
        options=DIFFICULTY_OPTIONS,
        format_func=lambda level: level.title(),
        horizontal=True,
        key="difficulty_input",
    )
    if st.session_state.difficulty_input in MODEL_BY_DIFFICULTY:
        st.session_state.selected_difficulty = st.session_state.difficulty_input
    else:
        st.session_state.selected_difficulty = DEFAULT_DIFFICULTY
    st.markdown(
        f'<p class="micro selected-model-line">Selected model: <span class="selected-model-name">{html.escape(get_selected_model_name())}</span></p>',
        unsafe_allow_html=True,
    )

    uploader_key = f"blue_file_{st.session_state.uploader_nonce}"
    uploaded = st.file_uploader(
        "Choose a text file",
        type=["txt"],
        key=uploader_key,
    )
    if uploaded is not None:
        st.session_state.uploaded_text = decode_text_file(uploaded.getvalue())
        st.session_state.uploaded_name = uploaded.name

    if st.session_state.uploaded_text:
        st.success(f"Loaded {st.session_state.uploaded_name}")

        start_col, back_col = st.columns(2)
        with start_col:
            start_arena = st.button("Enter Attack Arena", type="primary", use_container_width=True)
        with back_col:
            back_to_instructions = st.button("Back to Instructions", use_container_width=True)

        if start_arena:
            st.session_state.selected_difficulty = st.session_state.get("difficulty_input", DEFAULT_DIFFICULTY)
            reset_round(keep_uploaded_file=True)
            st.session_state.stage = "arena"
            st.rerun()

        if back_to_instructions:
            st.session_state.stage = "instructions"
            st.rerun()
    else:
        st.info("Upload a .txt file to continue.")
        back_clicked = st.button("Back to Instructions", use_container_width=True)
        if back_clicked:
            st.session_state.stage = "instructions"
            st.rerun()
