import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile
import os

# ---------------------------
# LOAD ENV
# ---------------------------
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="AI Course Platform",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------
# CUSTOM CSS
# ---------------------------
st.markdown("""
<style>

.main{
    padding:20px;
}

.title{
    text-align:center;
    font-size:45px;
    font-weight:bold;
    color:#1f77b4;
}

.course-box{
    background:#f5f5f5;
    padding:20px;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# TITLE
# ---------------------------
st.markdown(
    "<p class='title'>🎓 AI Course Application Platform</p>",
    unsafe_allow_html=True
)

st.write("---")

# ---------------------------
# COURSE SELECTION
# ---------------------------
courses = [
    "Python Programming",
    "Data Science",
    "Machine Learning",
    "Artificial Intelligence",
    "Web Development",
    "Cyber Security",
    "Cloud Computing"
]

course = st.selectbox(
    "📚 Select Course",
    courses
)

difficulty = st.selectbox(
    "🎯 Select Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

timeline = st.selectbox(
    "📅 Select Timeline",
    [
        "7 Days",
        "15 Days",
        "30 Days",
        "45 Days",
        "60 Days"
    ]
)

# ---------------------------
# AI COURSE DETAILS
# ---------------------------
if st.button("Generate Course Details"):

    prompt = f"""
    Generate professional details for:

    Course: {course}
    Difficulty: {difficulty}
    Timeline: {timeline}

    Include:
    1. Overview
    2. Skills Learned
    3. Daily Learning Plan
    4. Career Opportunities

    Keep response structured.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    course_details = response.choices[0].message.content

    st.session_state["course_details"] = course_details

# ---------------------------
# SHOW DETAILS
# ---------------------------
if "course_details" in st.session_state:

    st.subheader("📖 Course Details")

    st.markdown(
        f"""
        <div class="course-box">
        {st.session_state['course_details']}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------
# APPLICATION FORM
# ---------------------------
st.write("---")
st.header("📝 Apply For Course")

name = st.text_input("Full Name")

email = st.text_input("Email")

phone = st.text_input("Phone Number")

# ---------------------------
# PDF FUNCTION
# ---------------------------
def generate_pdf(
    name,
    email,
    phone,
    course,
    difficulty,
    timeline
):

    file_path = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ).name

    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Course Application Summary",
            styles["Title"]
        )
    )

    content.append(Spacer(1,12))

    content.append(
        Paragraph(
            f"<b>Name:</b> {name}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Email:</b> {email}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Phone:</b> {phone}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Course:</b> {course}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Difficulty:</b> {difficulty}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Timeline:</b> {timeline}",
            styles["BodyText"]
        )
    )

    if "course_details" in st.session_state:

        content.append(Spacer(1,20))

        content.append(
            Paragraph(
                "AI Generated Course Details",
                styles["Heading2"]
            )
        )

        content.append(
            Paragraph(
                st.session_state["course_details"],
                styles["BodyText"]
            )
        )

    doc.build(content)

    return file_path

# ---------------------------
# APPLY BUTTON
# ---------------------------
if st.button("🚀 Apply Now"):

    if not name or not email:

        st.error(
            "Please enter Name and Email"
        )

    else:

        pdf_file = generate_pdf(
            name,
            email,
            phone,
            course,
            difficulty,
            timeline
        )

        st.success(
            "Course Applied Successfully!"
        )

        with open(pdf_file, "rb") as f:

            st.download_button(
                label="📄 Download PDF",
                data=f,
                file_name="course_application.pdf",
                mime="application/pdf"
            )