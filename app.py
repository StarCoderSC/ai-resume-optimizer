import streamlit as st
from resume_analyzer import ResumeAnalyzer
import time


st.info("🚀 Beta Version -- Free Resume Reviews for Early Users")

st.set_page_config(
    page_title="AI Resume Optimizer",
    page_icon="🚀",
    layout="centered"
)

st.title("AI Resume Analyzer")
st.markdown("### Optimize your resume for better job matches")
st.markdown("Upload your resume and job description to get instant insights.")


if "last_call" not in st.session_state:
    st.session_state.last_call = 0

if "ai_usage" not in st.session_state:
    st.session_state.ai_usage = 0

access_code = st.text_input("Enter Premium access code (if any)", type="password")
PREMIUM_CODES = st.secrets["PREMIUM_CODES"]

def can_use_ai():
    if access_code in PREMIUM_CODES:
        return True
    if st.session_state.ai_usage < 5:
        return True
    return False

st.divider()

resume_file = st.file_uploader("Upload Resume (.pdf or .txt)", type=["pdf", "txt"])
job_file = st.file_uploader("Upload Job Description (.pdf or .txt)", type=["pdf", "txt"])

if resume_file and job_file:
    resume_path = f"temp_resume.{resume_file.name.split('.')[-1]}"
    job_path = f"temp_job.{job_file.name.split('.')[-1]}"

    with open(resume_path, "wb") as f:
        f.write(resume_file.read())
    
    with open(job_path, "wb") as f:
        f.write(job_file.read())

    analyzer = ResumeAnalyzer(resume_path, job_path)
    analyzer.load_files()

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing resume..."):
            score, matched, missing = analyzer.calculate_basic_match()
        st.subheader("Match Score")
        st.progress(int(score))
        st.metric(label="Match Score", value=f"{score}%")

        st.subheader("Matched skills")
        st.write(",".join(sorted(matched)))

        st.subheader("Missing skills")
        st.write(",".join(sorted(missing)))
    
    if st.button("Get Full AI Review"):

        current_time = time.time()

        if not can_use_ai():
            st.warning("Free AI usage limit reached. Upgrade for Unlimited access.")
            
        elif current_time - st.session_state.last_call < 10:
            st.warning("Please wait a few seconds before trying again.")
        else:
            st.session_state.last_call = current_time
            st.session_state.ai_usage += 1

            with st.spinner("Generating full AI review..."):
                feedback = analyzer.analyze_resume_with_ai()

            st.subheader("AI Resume Review")
            st.markdown(feedback)

else:
    analyzer = ResumeAnalyzer("", "")


st.divider()

# ===== BULLET iMPROVEMENT =====
st.subheader("Improve Resume Bullet")

bullet = st.text_area("Paste a resume bullet")

if st.button("Improve Bullet"):
    if not bullet.strip():
        st.warning("Please enter a bullet point.`")
    else:
        current_time = time.time()

        if not can_use_ai():
            st.warning("Free AI usage limit reched. Upgrade for unlimited access.")
        elif current_time - st.session_state.last_call < 10:
            st.warning("Please wait a few seconds before trying again.")
        else:
            st.session_state.last_call = current_time
            st.session_state.ai_usage += 1

            with st.spinner("Improving bullet..."):
                improved = analyzer.improve_bullet_point(bullet)
            st.success("Improved Version:")
            st.write(improved)

st.divider()
st.markdown("###  Want Unlimited AI Reviews?")
st.markdown("Message me for premium access")
st.markdown("Contact: starcoder.dev@gmail.com | Linkedln: https://linkedin.com/in/starcoder-sc-8698893b2")