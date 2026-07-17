import streamlit as st


def inject_custom_css() -> None:
    """Read the CSS file, inject dynamic variables, and apply it to the Streamlit app."""
    thumbnail_url = (
        f"https://img.youtube.com/vi/{st.session_state.video_id}/maxresdefault.jpg"
    )

    with open("assets/style.css") as f:
        css_content = f.read().replace("{thumbnail_url}", thumbnail_url)

    st.markdown(f"<style>\n{css_content}\n</style>", unsafe_allow_html=True)


def render_sidebar() -> None:
    """Render the sidebar with video ID input and handle state reset on load."""
    with st.sidebar:
        st.header("Video ID")

        video_id_input = st.text_input(
            "YouTube Video ID",
            value=st.session_state.video_id,
            label_visibility="collapsed",
            placeholder="Enter YouTube Video ID",
        )

        if st.button("Load Video", use_container_width=True):
            st.session_state.video_id = video_id_input
            st.session_state.chat_history = []
            st.session_state.messages = []
            st.cache_resource.clear()
            st.cache_data.clear()
            st.rerun()


def render_video_banner(video_id: str, video_title: str) -> None:
    """Render the HTML video banner container with the video title."""
    st.markdown(
        f"""
        <a href="https://www.youtube.com/watch?v={video_id}" target="_blank" class="video-banner-link">
            <div class="video-banner-container">
                <div class="video-banner-bg"></div>
                <div class="video-banner-content">
                    <h3>{video_title}</h3>
                </div>
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )


def render_chat_history() -> None:
    """Iterate through stored messages and render them in the chat interface."""
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="user-message"></div>{msg["content"]}',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(msg["content"])
