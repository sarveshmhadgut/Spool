import os
import sys

import streamlit as st
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage

from src.ui.core import initialize_session_state, get_video_title, initialize_pipeline
from src.ui.components import (
    inject_custom_css,
    render_sidebar,
    render_video_banner,
    render_chat_history,
)


def main() -> None:
    st.set_page_config(page_title="Spool", layout="centered")

    initialize_session_state()
    inject_custom_css()

    st.title("Spool")
    render_sidebar()

    video_title = get_video_title(st.session_state.video_id)
    render_video_banner(st.session_state.video_id, video_title)

    retriever, chain = initialize_pipeline(st.session_state.video_id)

    render_chat_history()

    user_input = st.chat_input("Ask something about the video...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(
                f'<div class="user-message"></div>{user_input}',
                unsafe_allow_html=True,
            )

        with st.chat_message("assistant"):
            with st.spinner(""):
                docs: list[Document] = retriever.invoke(user_input)
                context = "\n".join(doc.page_content for doc in docs)

                response = chain.invoke(
                    {
                        "context": context,
                        "chat_history": st.session_state.chat_history,
                        "user_message": user_input,
                    }
                )
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

        if "does not contain information" not in response:
            st.session_state.chat_history.append(HumanMessage(content=user_input))
            st.session_state.chat_history.append(AIMessage(content=response))

        if len(st.session_state.chat_history) > 10:
            st.session_state.chat_history = st.session_state.chat_history[-10:]


if __name__ == "__main__":
    main()
