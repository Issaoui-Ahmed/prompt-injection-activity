import streamlit as st


def render_hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
<div class="hero">
  <h1>{title}</h1>
  <p>{subtitle}</p>
  <div class="chip-row">
    <span class="chip chip-blue">Blue Team: prompt design</span>
    <span class="chip chip-red">Red Team: jailbreak testing</span>
  </div>
</div>
        """,
        unsafe_allow_html=True,
    )
