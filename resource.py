import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from pypdf import PdfReader
import os

# -------------------------
# LOAD ENV
# -------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(
    page_title="PDF Summarizer AI",
    page_icon="📄",
    layout="wide"
)

# -------------------------
# CSS
# -------------------------

st.markdown("""
<style>

.title{
text-align:center;
font-size:40px;
font-weight:bold;
color:#2563eb;
}

.box{
background-color:#f5f5f5;
padding:20px;
border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# TITLE
# -------------------------

st.markdown(
"<p class='title'>📄 AI PDF Summarizer</p>",
unsafe_allow_html=True
)

st.write(
"Upload a PDF, generate a summary, and create questions."
)

st.divider()

# -------------------------
# PDF UPLOAD
# -------------------------

uploaded_file = st.file_uploader(
"Upload PDF",
type=["pdf"]
)

summary_length = st.selectbox(
"Select Summary Length",
[
100,
200,
300,
500,
700
]
)

# -------------------------
# EXTRACT PDF TEXT
# -------------------------

def extract_pdf_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text

# -------------------------
# GENERATE SUMMARY
# -------------------------

if uploaded_file:

    pdf_text = extract_pdf_text(uploaded_file)

    st.success("PDF Uploaded Successfully")

    if st.button("Generate Summary"):

        with st.spinner("Generating Summary..."):

            prompt = f"""
            Summarize the following PDF content.

            Limit summary to approximately
            {summary_length} words.

            Content:

            {pdf_text[:12000]}
            """

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            )

            summary = response.choices[0].message.content

            st.session_state["summary"] = summary

# -------------------------
# DISPLAY SUMMARY
# -------------------------

if "summary" in st.session_state:

    st.subheader("📌 Summary")

    st.markdown(
        st.session_state["summary"]
    )

    st.download_button(
        "Download Summary",
        st.session_state["summary"],
        file_name="summary.txt"
    )

# -------------------------
# GENERATE QUESTIONS
# -------------------------

if "summary" in st.session_state:

    if st.button("Generate Questions"):

        with st.spinner("Generating Questions..."):

            prompt = f"""
            Based on the following content,
            create exactly 5 questions.

            Content:

            {st.session_state["summary"]}
            """

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            )

            questions = response.choices[0].message.content

            st.session_state["questions"] = questions

# -------------------------
# DISPLAY QUESTIONS
# -------------------------

if "questions" in st.session_state:

    st.subheader("❓ Questions")

    st.markdown(
        st.session_state["questions"]
    )