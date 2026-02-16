import streamlit as st

STYLE_BLOCK = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

:root {
  --bg-top: #e8f4ee;
  --bg-bottom: #cfe4d8;
  --ink: #0d2019;
  --muted: #24463a;
  --card: rgba(250, 255, 252, 0.95);
  --card-strong: rgba(255, 255, 255, 0.98);
  --surface-soft: rgba(255, 255, 255, 0.9);
  --surface-input: rgba(255, 255, 255, 0.96);
  --stroke: rgba(12, 54, 40, 0.28);
  --stroke-strong: rgba(12, 54, 40, 0.42);
  --blue: #1459cf;
  --blue-ink: #0c3b8a;
  --red: #c0323c;
  --red-ink: #6f131a;
  --green: #0f7a4f;
  --amber: #936608;
}

html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] * {
  font-family: 'Chakra Petch', sans-serif;
  color: var(--ink);
}

[data-testid="stAppViewContainer"] a {
  color: var(--blue-ink);
}

[data-testid="stAppViewContainer"] {
  background:
    linear-gradient(120deg, rgba(23, 120, 86, 0.11) 0%, transparent 45%),
    linear-gradient(300deg, rgba(28, 111, 255, 0.08) 0%, transparent 50%),
    repeating-linear-gradient(0deg, rgba(17, 37, 29, 0.035) 0, rgba(17, 37, 29, 0.035) 1px, transparent 1px, transparent 42px),
    repeating-linear-gradient(90deg, rgba(17, 37, 29, 0.03) 0, rgba(17, 37, 29, 0.03) 1px, transparent 1px, transparent 42px),
    linear-gradient(165deg, var(--bg-top), var(--bg-bottom));
}

#MainMenu {
  visibility: hidden;
}

[data-testid="stHeader"] {
  display: none;
}

[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
  display: none !important;
}

.hero {
  margin-bottom: 0.7rem;
  animation: reveal 420ms ease-out;
}

.hero h1 {
  margin: 0;
  font-size: clamp(2rem, 4vw, 3rem);
  line-height: 1.05;
  letter-spacing: 0.03em;
  font-family: 'Share Tech Mono', monospace;
  text-transform: uppercase;
}

.hero p {
  margin: 0.55rem 0 0 0;
  color: var(--muted);
  font-size: 1.02rem;
}

.chip-row {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  margin-top: 0.55rem;
}

.chip {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 0.25rem 0.7rem;
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  border: 1px solid transparent;
}

.chip-blue {
  background: rgba(20, 89, 207, 0.2);
  border-color: rgba(20, 89, 207, 0.42);
  color: var(--blue-ink);
}

.chip-red {
  background: rgba(192, 50, 60, 0.17);
  border-color: rgba(192, 50, 60, 0.42);
  color: var(--red-ink);
}

.panel {
  border: 1px solid var(--stroke);
  border-radius: 16px;
  background: var(--card);
  box-shadow: 0 16px 34px rgba(8, 39, 30, 0.11);
  padding: 1rem 1.1rem;
  animation: reveal 440ms ease-out;
}

.panel h3 {
  margin: 0 0 0.55rem 0;
  font-size: 1.06rem;
  letter-spacing: 0.02em;
}

.status-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 0.7rem;
  margin: 0.4rem 0 0.8rem 0;
  max-width: 460px;
}

.status-card {
  border: 1px solid var(--stroke);
  border-radius: 12px;
  background: var(--card-strong);
  padding: 0.6rem 0.8rem;
}

.status-label {
  margin: 0;
  font-size: 0.76rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--muted);
  font-family: 'Share Tech Mono', monospace;
}

.status-value {
  margin: 0.2rem 0 0 0;
  font-weight: 700;
  font-size: 1.18rem;
}

.status-value-model {
  font-family: 'Share Tech Mono', monospace;
  font-size: 1.02rem;
  word-break: break-word;
}

.blue-note {
  border-left: 4px solid var(--blue);
}

.red-note {
  border-left: 4px solid var(--red);
}

.micro {
  color: var(--muted);
  font-size: 0.88rem;
  margin: 0.35rem 0 0 0;
}

.selected-model-line {
  margin-top: 0.25rem;
}

.selected-model-name {
  display: inline-block;
  font-family: 'Share Tech Mono', monospace;
  color: var(--ink);
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid var(--stroke);
  border-radius: 8px;
  padding: 0.05rem 0.4rem;
}

[data-testid="stRadio"] > label,
[data-testid="stRadio"] [role="radiogroup"] label,
[data-testid="stRadio"] [role="radiogroup"] span,
[data-testid="stRadio"] [role="radiogroup"] div {
  color: var(--ink) !important;
}

[data-testid="stRadio"] [role="radiogroup"] > label {
  border: 1px solid var(--stroke-strong) !important;
  border-radius: 10px !important;
  background: var(--surface-soft) !important;
  padding: 0.28rem 0.7rem !important;
}

[data-testid="stFileUploaderDropzone"] {
  border-radius: 14px;
  border: 1.5px dashed rgba(12, 88, 60, 0.58);
  background: var(--surface-soft);
}

[data-testid="stFileUploaderDropzone"],
[data-testid="stFileUploaderDropzone"] * {
  color: var(--ink) !important;
}

.stButton > button {
  border-radius: 11px;
  border: none;
  font-weight: 700;
  letter-spacing: 0.01em;
  background: linear-gradient(120deg, #0a6f45, #145e46);
  color: #f3fff8 !important;
}

.stButton > button:hover {
  background: linear-gradient(120deg, #085a39, #104c38);
}

.stButton > button:focus,
.stButton > button:focus-visible {
  box-shadow: 0 0 0 3px rgba(20, 89, 207, 0.28) !important;
}

[data-testid="stBaseButton-secondary"] {
  border: 1px solid var(--stroke-strong) !important;
  background: var(--surface-soft) !important;
  color: var(--ink) !important;
}

[data-testid="stBaseButton-secondary"]:hover {
  background: #e9f6ef !important;
}

div[data-testid="stTextArea"] textarea {
  border: 1px solid #c7ced6 !important;
  border-radius: 8px !important;
  background: #ffffff !important;
  box-shadow: none !important;
  color: #111111 !important;
}

[data-testid="stChatMessage"] {
  border: 1px solid var(--stroke);
  border-radius: 14px;
  background: var(--card-strong);
  box-shadow: 0 8px 20px rgba(8, 39, 30, 0.08);
  padding: 0.2rem 0.45rem;
}

[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] * {
  color: var(--ink) !important;
}

[data-testid="stBottomBlockContainer"] {
  background: transparent !important;
  border-top: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

[data-testid="stBottomBlockContainer"] > div {
  background: transparent !important;
}

[data-testid="stChatInput"],
[data-testid="stBottomBlockContainer"] [data-baseweb="textarea"] {
  background: #ffffff !important;
  border: 1px solid #c7ced6 !important;
  border-radius: 8px !important;
  box-shadow: none !important;
}

[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] input,
[data-testid="stChatInput"] div[contenteditable="true"],
[data-testid="stBottomBlockContainer"] textarea,
[data-testid="stBottomBlockContainer"] input,
[data-testid="stBottomBlockContainer"] div[contenteditable="true"] {
  color: #111111 !important;
  caret-color: #111111 !important;
  -webkit-text-fill-color: #111111 !important;
  background: transparent !important;
  opacity: 1 !important;
}

[data-testid="stChatInput"] textarea::placeholder,
[data-testid="stChatInput"] input::placeholder,
[data-testid="stBottomBlockContainer"] textarea::placeholder,
[data-testid="stBottomBlockContainer"] input::placeholder {
  color: #6b7280 !important;
  opacity: 1 !important;
}

[data-testid="stChatInput"] button {
  color: #111111 !important;
}

[data-testid="stChatInput"] button:hover {
  background: #f3f4f6 !important;
}

[data-testid="stAlert"],
[data-testid="stAlert"] * {
  color: var(--ink) !important;
}

[data-baseweb="notification"] {
  border: 1px solid var(--stroke);
  border-radius: 12px;
  background: var(--surface-soft) !important;
}

[data-baseweb="notification"] *,
[data-baseweb="notification"] svg {
  color: var(--ink) !important;
  fill: currentColor !important;
}

[data-testid="stExpander"] {
  border: 1px solid var(--stroke);
  border-radius: 12px;
  background: var(--surface-soft);
}

[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary * {
  color: var(--ink) !important;
}

@media (max-width: 860px) {
  .status-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@keyframes reveal {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
"""


def apply_styles() -> None:
    st.markdown(STYLE_BLOCK, unsafe_allow_html=True)
