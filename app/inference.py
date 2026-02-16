from typing import Any

import streamlit as st
from huggingface_hub import InferenceClient


@st.cache_resource
def get_client() -> InferenceClient:
    return InferenceClient()


def normalize_response_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(content)


def run_inference(file_text: str, prompt: str, turns: list[dict[str, str]], model_name: str) -> str:
    client = get_client()
    messages = [{"role": "system", "content": file_text}]
    for turn in turns:
        messages.append({"role": "user", "content": turn["prompt"]})
        messages.append({"role": "assistant", "content": turn["response"]})
    messages.append({"role": "user", "content": prompt})

    completion = client.chat.completions.create(
        model=model_name,
        messages=messages,
    )

    content = completion.choices[0].message.content
    return normalize_response_content(content)
