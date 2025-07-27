import streamlit as st
import fitz  # PyMuPDF for PDF reading
import docx
import re

# ----------- Helper Functions -----------

# Function to read DOCX file
def read_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to read PDF file
def read_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

# ----------- Streamlit UI -----------

st.title("💼 AI Resume Analyzer & Job Fit Recommender")

st.subheader("📄 Upload Your Resume (PDF or DOCX)")
uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"])

if uploaded_file is not None:
    st.success(f"✅ Uploaded: {uploaded_file.name}")

    # Extract resume text based on file type
    if uploaded_file.name.endswith(".pdf"):
        resume_text = read_pdf(uploaded_file)
    else:
        resume_text = read_docx(uploaded_file)

    # Display extracted text
    st.subheader("📝 Resume Content:")
    st.text_area("Extracted Text", resume_text, height=300)

    # ----------- Extract Key Details -----------

    # Extract email
    email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", resume_text)
    email = email[0] if email else "Not found"

    # Extract phone number
    phone = re.findall(r"\+?\d[\d\s\-]{8,14}\d", resume_text)
    phone = phone[0] if phone else "Not found"

    # Display extracted info
    st.subheader("🔍 Extracted Details:")
    st.markdown(f"**📧 Email:** {email}")
    st.markdown(f"**📱 Phone:** {phone}")

    # ----------- Extract Skills -----------

    skill_keywords = [
        "python", "java", "c++", "sql", "machine learning", "deep learning",
        "nlp", "html", "css", "javascript", "excel", "power bi", "tableau",
        "pandas", "numpy", "tensorflow", "keras", "git", "github"
    ]

    resume_lower = resume_text.lower()
    extracted_skills = [skill for skill in skill_keywords if skill in resume_lower]

    st.markdown(f"**🛠️ Skills:** {', '.join(extracted_skills) if extracted_skills else 'Not found'}")

    # ----------- Recommend Job Roles Based on Skills -----------

    job_roles = {
        "Data Analyst": ["excel", "sql", "tableau", "power bi", "python"],
        "Web Developer": ["html", "css", "javascript", "git", "github"],
        "ML Engineer": ["python", "machine learning", "tensorflow", "keras", "pandas", "numpy"],
        "Backend Developer": ["python", "java", "sql", "git"],
    }

    recommended_roles = []
    for role, skills_required in job_roles.items():
        matched = [skill for skill in skills_required if skill in extracted_skills]
        if len(matched) >= 2:  # at least 2 skills match
            recommended_roles.append(role)

    st.subheader("🎯 Recommended Job Roles:")
    if recommended_roles:
        for role in recommended_roles:
            st.markdown(f"✅ {role}")
    else:
        st.warning("No strong role match found. Try improving your skill set!")

else:
    st.info("Please upload a resume to continue.")


