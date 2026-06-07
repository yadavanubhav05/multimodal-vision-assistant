import streamlit as st
import tempfile
import uuid
import pandas as pd
from pathlib import Path

from models.openai_model import ask_image_question
from evaluation.reports import save_report

st.set_page_config(
    page_title="Multimodal Vision Assistant",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "question" not in st.session_state:
    st.session_state.question = ""

if "image_name" not in st.session_state:
    st.session_state.image_name = ""

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:

    st.header("Example Questions")

    st.info("""
• What do you see in this image?

• Describe the main objects.

• Summarize the scene.

• What visual patterns stand out?

• Describe visible structures.
""")

# -----------------------------
# Title
# -----------------------------

st.title("👁️ Multimodal Vision Assistant")

st.caption(
    "GPT-4o Vision powered multimodal image understanding demo."
)

# -----------------------------
# Metrics
# -----------------------------

report_file = "outputs/evaluation_report.csv"

total_queries = 0
positive_feedback = 0

if Path(report_file).exists():

    try:

        df = pd.read_csv(report_file)

        total_queries = len(df)

        positive_feedback = len(
            df[df["feedback"] == "Helpful"]
        )

    except Exception:

        total_queries = 0
        positive_feedback = 0

m1, m2, m3 = st.columns(3)

m1.metric(
    "Questions Asked",
    total_queries
)

m2.metric(
    "Helpful Votes",
    positive_feedback
)

m3.metric(
    "Session ID",
    st.session_state.session_id
)

st.divider()

# -----------------------------
# Upload
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    col1, col2 = st.columns([1, 1])

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as tmp_file:

        tmp_file.write(
            uploaded_file.read()
        )

        image_path = tmp_file.name

    # -----------------------------
    # Image Preview
    # -----------------------------

    with col1:

        st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True
        )

    # -----------------------------
    # Question Box
    # -----------------------------

    with col2:

        question = st.text_area(
            "Ask a Question",
            placeholder="What do you see in this image?"
        )

        if st.button("Analyze"):

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "Analyzing image..."
                ):

                    answer = ask_image_question(
                        image_path,
                        question
                    )

                st.session_state.answer = answer
                st.session_state.question = question
                st.session_state.image_name = uploaded_file.name

                st.session_state.history.append(
                    {
                        "question": question,
                        "answer": answer
                    }
                )

        # -----------------------------
        # Response
        # -----------------------------

        if st.session_state.answer:

            st.subheader(
                "AI Analysis"
            )

            st.write(
                st.session_state.answer
            )

            c1, c2 = st.columns(2)

            with c1:

                if st.button(
                    "👍 Helpful"
                ):

                    save_report(
                        st.session_state.session_id,
                        st.session_state.image_name,
                        st.session_state.question,
                        st.session_state.answer,
                        "Helpful"
                    )

                    st.success(
                        "Feedback saved"
                    )

            with c2:

                if st.button(
                    "👎 Not Helpful"
                ):

                    save_report(
                        st.session_state.session_id,
                        st.session_state.image_name,
                        st.session_state.question,
                        st.session_state.answer,
                        "Not Helpful"
                    )

                    st.success(
                        "Feedback saved"
                    )

# -----------------------------
# Conversation History
# -----------------------------

if st.session_state.history:

    st.divider()

    st.subheader(
        "Conversation History"
    )

    for item in reversed(
        st.session_state.history
    ):

        st.markdown(
            f"**Q:** {item['question']}"
        )

        st.markdown(
            f"**A:** {item['answer']}"
        )

        st.divider()