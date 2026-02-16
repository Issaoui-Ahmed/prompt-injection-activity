import html

import streamlit as st

from app.config import MAX_MESSAGES
from app.inference import run_inference
from app.state import get_selected_difficulty, get_selected_model_name, reset_round
from app.ui.components import render_hero


def render_arena_screen() -> None:
    if not st.session_state.uploaded_text:
        st.session_state.stage = "setup"
        st.rerun()

    render_hero(
        "Attack Arena",
        f"Target file: {st.session_state.uploaded_name}",
    )

    messages_used = st.session_state.messages_used
    messages_left = MAX_MESSAGES - messages_used
    selected_difficulty = get_selected_difficulty()
    safe_difficulty = html.escape(selected_difficulty.title())
    safe_model_name = html.escape(get_selected_model_name())

    st.markdown(
        f"""
<div class="status-grid">
  <div class="status-card">
    <p class="status-label">Difficulty</p>
    <p class="status-value">{safe_difficulty}</p>
  </div>
  <div class="status-card">
    <p class="status-label">Model</p>
    <p class="status-value status-value-model">{safe_model_name}</p>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(min(1.0, messages_used / MAX_MESSAGES), text=f"{messages_used}/{MAX_MESSAGES} messages used")

    reset_col, change_col = st.columns(2)
    with reset_col:
        reset_clicked = st.button("Restart 10 Messages", use_container_width=True)
    with change_col:
        new_file_clicked = st.button("Load New File", use_container_width=True)

    if reset_clicked:
        reset_round(keep_uploaded_file=True)
        st.rerun()

    if new_file_clicked:
        reset_round(keep_uploaded_file=False)
        st.session_state.stage = "setup"
        st.rerun()

    st.markdown("### Live Conversation")
    if not st.session_state.turns:
        st.info("No messages yet. Start the chat below.")
    else:
        for turn in st.session_state.turns:
            with st.chat_message("user"):
                st.markdown(turn["prompt"])
            with st.chat_message("assistant"):
                st.markdown(turn["response"])

    if messages_left <= 0:
        st.error("No messages left. Round complete.")

    if messages_left > 0:
        with st.form("attack_prompt_form", clear_on_submit=True):
            prompt = st.text_area(
                "Attack prompt",
                placeholder="Send a red-team message...",
                height=120,
                label_visibility="collapsed",
            )
            submitted = st.form_submit_button("Send", use_container_width=True, type="primary")

        if submitted:
            if not prompt.strip():
                st.warning("Write a message before sending.")
                return

            with st.spinner("Executing attack against model..."):
                try:
                    response = run_inference(
                        file_text=st.session_state.uploaded_text,
                        prompt=prompt,
                        turns=st.session_state.turns,
                        model_name=get_selected_model_name(),
                    )
                except Exception as exc:
                    st.error(f"Inference failed: {exc}")
                else:
                    st.session_state.turns.append({"prompt": prompt, "response": response})
                    st.session_state.messages_used += 1
                    st.rerun()
