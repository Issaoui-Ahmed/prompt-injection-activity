import os

MODEL_BY_DIFFICULTY = {
    "easy": os.getenv("HF_MODEL_EASY", os.getenv("HF_MODEL", "Qwen/Qwen2.5-1.5B-Instruct:featherless-ai")),
    "medium": os.getenv("HF_MODEL_MEDIUM", "ruslandev/llama-3-8b-gpt-4o-ru1.0:featherless-ai"),
    "difficult": os.getenv("HF_MODEL_DIFFICULT", "openai/gpt-oss-20b:groq"),
}
DIFFICULTY_OPTIONS = ["easy", "medium", "difficult"]
DEFAULT_DIFFICULTY = "easy"

PAGE_CONFIG = {
    "page_title": "Prompt Shield Arena",
    "page_icon": ":shield:",
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}
