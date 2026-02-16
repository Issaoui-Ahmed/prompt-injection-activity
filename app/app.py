import streamlit as st

from app.config import PAGE_CONFIG
from app.screens.arena import render_arena_screen
from app.screens.instructions import render_instructions_screen
from app.screens.setup import render_setup_screen
from app.state import init_state
from app.ui.styles import apply_styles


def run_app() -> None:
    st.set_page_config(**PAGE_CONFIG)
    init_state()
    apply_styles()

    stage = st.session_state.stage
    if stage == "instructions":
        render_instructions_screen()
    elif stage == "setup":
        render_setup_screen()
    else:
        render_arena_screen()
