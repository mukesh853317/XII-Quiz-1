import streamlit as st
import pandas as pd
import smtplib
import requests
import urllib.parse
from email.mime.text import MIMEText
import random
import streamlit.components.v1 as components
import re

# -----------------------------------------------------
# 1. Mitradnya Publication - Setup
# -----------------------------------------------------
TEACHER_EMAIL = "vidyarthi.mitradnyapublications@gmail.com" 
try:
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
except:
    EMAIL_PASSWORD = "" 

TEACHER_NAME = "Mukesh Sir"

# === Exam PIN ===
SECRET_EXAM_PIN = "MIT2026" 

@st.cache_data
def load_data():
    try:
        try:
            df = pd.read_csv('All in one.csv', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv('All in one.csv', encoding='cp1252')
        df.fillna("None", inplace=True) 
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

df = load_data()

def send_detailed_email(receiver_email, student_name, div, roll, score, total, chapter, test_name, report_content, is_teacher=True):
    if is_teacher:
        subject = f"New Result: {student_name} ({div}-{roll}) - {score}/{total}"
        body = f"📚 Result Alert for Mukesh Sir!\n\nStudent: {student_name}\nDivision: {div}\nRoll No: {roll}\nChapter: {chapter}\nTest: {test_name}\nScore: {score}/{total}\n\n--- Detailed Report ---\n{report_content}"
    else:
        subject = f"Your Exam Result - (Mitradnya Publication's) ({score}/{total})"
        body = f"Dear {student_name},\n\nYou have successfully completed the online test.\n\nChapter: {chapter}\nTest: {test_name}\nYour Score: {score}/{total}\n\n--- Detailed Performance ---\n{report_content}\n\nKeep Studying!\n- Mukesh Sir"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = TEACHER_NAME
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(TEACHER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(TEACHER_EMAIL, receiver_email, msg.as_string())
        server.quit()
        return True
    except: return False

# -----------------------------------------------------
# 2. Website Interface & Session State Initialization
# -----------------------------------------------------
st.set_page_config(page_title="📚 Mukesh Sir's Online Exam 📚", page_icon="📝", layout="centered")

# --- CUSTOM CSS (Dark/Light Mode Compatible) ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #E0E0E0; }
    h1 { color: #F1C40F; text-align: center; font-family: 'Arial Black', sans-serif; }
    div.stRadio > div { 
        background-color: #1E1E1E; 
        color: #FFFFFF;
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #F1C40F; 
        border: 1px solid #333333;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.5); 
        margin-bottom: 15px; 
    }
    div.stButton > button { 
        background-color: #F1C40F; color: #000000; font-size: 18px; 
        font-weight: bold; border-radius: 8px; width: 100%; 
    }
    div.stButton > button:hover { background-color: #D4AC0D; color: #000000; }
    </style>
    """, unsafe_allow_html=True)
# -------------------------------------------

st.sidebar.title("📚Mitradnya Publication's Online Test Series📚\n\n👨‍🏫Developed by: Mukesh Sir👨‍🏫")

if 'test_status' not in st.session_state:
    st.session_state.test_status = 'not_started' 

if df is not None:
    sidebar_disabled = st.session_state.test_status != 'not_started'
    
    chapters = df['No'].unique()
    selected_chapter = st.sidebar.selectbox("1. Select Chapter:", chapters, disabled=sidebar_disabled)
    
    chapter_questions = df[df['No'] == selected_chapter]
    total_q = len(chapter_questions)
    
    st.sidebar.markdown("---")
    
    chunk_size = 20
    test_parts = []
    for i in range(0, total_q, chunk_size):
        test_parts.append(f"Test {i//chunk_size + 1}")
        
    selected_part = st.sidebar.radio("2. Select Test Part:", test_parts, disabled=sidebar_disabled)
    
    part_index = test_parts.index(selected_part)
    start_idx = part_index * chunk_size
    end_idx = start_idx + chunk_size
    current_quiz_df = chapter_questions.iloc[start_idx:end_idx]
    
    st.title("📚 Mukesh Sir's Online Examination Portal 📚")
    st.subheader(f"Topic: {selected_chapter}")
    st.write(f"**{selected_part} (20 Marks / 20 Minutes)**")
    
    if st.session_state.test_status == 'not_started':
        st.info("⚠️ Instruction: Please enter your correct details and the Exam PIN provided by Mukesh Sir.")
        
    student_name = st.text_input("👤 Full Name (e.g., Rahul Patil):", disabled=sidebar_disabled)
    student_div = st.text_input("🏫 Division (A/B/C):", disabled=sidebar_disabled)
    student_roll = st.text_input("🔢 Roll No (Numbers Only):", disabled=sidebar_disabled)
    student_email = st.text_input("📧 Email ID (For Result):", disabled=sidebar_disabled)
    
    if st.session_state.test_status == 'not_started':
        exam_pin_input = st.text_input("🔑 Exam PIN (Secret Password):", type="password")
    
    st.markdown("---")

    if st.session_state.test_status == 'not_started':
        # Start Test बटण पूर्ण रुंदीचे 
        if st.button("🟢 Start Test", use_container_width=True):
            email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+$"
            is_valid_email = re.match(email_pattern, student_email)
            is_valid_roll = student_roll.isdigit()
            
            valid_domains = ["@gmail.com", "@yahoo.com", "@outlook.com", "@rediffmail.com"]
            is_real_domain = any(student_email.lower().endswith(d) for d in valid_domains)
            
            if not student_name or not student_div or not student_roll or not student_email or not exam_pin_input:
                st.warning("⚠️ Please fill in all the details, including the Exam PIN.")
            elif not is_valid_roll:
                st.error("❌ Invalid Roll No! Please enter numbers only (e.g., 15).")
            elif not is_valid_email or not is_real_domain:
                st.error("❌ Fake Email Detected! Please use a real valid email address (like @gmail.com or @yahoo.com).")
            elif exam_pin_input != SECRET_EXAM_PIN:
                st.error("❌ Incorrect Exam PIN! You cannot start the test without the correct password.")
            else:
                st.session_state.test_status = 'in_progress'
                st.rerun()

    elif st.session_state.test_status == 'in_progress':
        test_id = f"{selected_chapter}_{selected_part}".replace(" ", "_")
        
        # टायमर सुद्धा डार्क मोडमध्ये चांगला दिसेल असा
        timer_code = f"""
        <div style="background-color: var(--primary-color); color: white; padding:10px; border-radius:8px; text-align:center; font-size:22px; font-weight:bold; font-family:sans-serif; box-shadow: 2px 2px 5px rgba(0,0,0,0.2);">
            <span id="time">Loading Timer...</span>
        </div>
        <script>
            var testId = "{test_id}";
            var endTime = sessionStorage.getItem("examEndTime_" + testId);
            
            if (!endTime) {{
                endTime = new Date().getTime() + 20 * 60 * 1000; 
                sessionStorage.setItem("examEndTime_" + testId, endTime);
            }}
            
            var elem = document.getElementById('time');
            var timerId = setInterval(function() {{
                var now = new Date().getTime();
                var distance = endTime - now;
                
                if (distance <= 0) {{
                    clearInterval(timerId);
                    elem.innerHTML = "⚠️ Time Up! Please submit your exam immediately.";
                    elem.parentElement.style.backgroundColor = "#E74C3C";
                }} else {{
                    var m = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                    var s = Math.floor((distance % (1000 * 60)) / 1000);
                    elem.innerHTML = "⏱️ Time Remaining: " + m + " m " + s + " s";
                }}
            }}, 1000);
        </script>
        """
        components.html(timer_code, height=70)
        
        user_answers = []
        for idx, (i, row) in enumerate(current_quiz_df.iterrows(), 1):
            st.write(f"**Q {idx}. {row['Question']}**")
            
            raw_options = [str(row['Option A']), str(row['Option B']), str(row['Option C']), str(row['Option D'])]
            unique_options = []
            for opt in raw_options:
                while opt in unique_options:
                    opt += " "  
                unique_options.append(opt)
            options = unique_options
            
            random.seed(i)
            random.shuffle(options)
            random.seed()
            
            ans = st.radio("Options:", options, key=f"q_{i}", index=None, label_visibility="collapsed")
            user_answers.append(ans)
            st.write("")

        # Submit बटण अधिक आकर्षक आणि full width
        if st.button("🚀 Submit Exam", type="primary", use_container_width=True):
            if None not in user_answers:
                score = 0
                detailed_report_text = ""
                correct_answers = current_quiz_df['Correct Answer (Full Text)'].astype(str).str.strip().values
                results_list = []
                
                for idx, (i, row) in enumerate(current_quiz_df.iterrows()):
                    user_ans = str(user_answers[idx]).strip()
                    correct_ans = str(correct_answers[idx]).strip()
                    
                    if user_ans == correct_ans:
                        score += 1
                        status = "✅ Correct"
                        is_correct = True
                    else:
                        status = f"❌ Wrong (Correct: {correct_ans})"
                        is_correct = False
                        
                    detailed_report_text += f"Q: {row['Question']}\nYour Ans: {user_ans}\nStatus: {status}\n\n"
                    results_list.append({'q': row['Question'], 'user_ans': user_ans, 'correct_ans': correct_ans, 'is_correct': is_correct})
                
                with st.spinner("Saving data to Excel..."):
                    
                    GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbw3wvGw7hDYyAQIKBL1Rd-jTCP8DwzLzGGITCKTZwbCDMXaInzi3t2vyU4ipzz9SM9-/exec"
                    
                    safe_name = urllib.parse.quote(str(student_name))
                    safe_div = urllib.parse.quote(str(student_div))
                    safe_roll = urllib.parse.quote(str(student_roll))
                    safe_test = urllib.parse.quote(f"{selected_chapter} - {selected_part}")
                    safe_score = urllib.parse.quote(str(score))
                    safe_email = urllib.parse.quote(str(student_email))  
                    
                    final_url = f"{GOOGLE_SHEET_URL}?name={safe_name}&div={safe_div}&roll={safe_roll}&test={safe_test}&score={safe_score}&email={safe_email}"
                    
                    try:
                        res = requests.get(final_url)
                        sheet_success = (res.status_code == 200)
                    except Exception:
                        sheet_success = False
                
                send_detailed_email(TEACHER_EMAIL, student_name, student_div, student_roll, score, len(current_quiz_df), selected_chapter, selected_part, detailed_report_text, True)
                
                email_sent = False
                if student_email:
                    email_sent = send_detailed_email(student_email, student_name, student_div, student_roll, score, len(current_quiz_df), selected_chapter, selected_part, detailed_report_text, False)
                
                st.session_state.score = score
                st.session_state.total_questions = len(current_quiz_df)
                st.session_state.sheet_success = sheet_success
                st.session_state.email_sent = email_sent
                st.session_state.student_email = student_email
                
                st.session_state.test_status = 'submitted'
                st.rerun() 
            else:
                st.warning("⚠️ Please answer all questions before submitting.")

    elif st.session_state.test_status == 'submitted':
        test_id = f"{selected_chapter}_{selected_part}".replace(" ", "_")
        components.html(f"<script>sessionStorage.removeItem('examEndTime_{test_id}');</script>", height=0)
        
        st.success(f"🎉 Final Score: {st.session_state.score} / {st.session_state.total_questions}")
        
        if st.session_state.sheet_success:
            st.info("📊 Your result has been successfully saved in the system.")
            
        if st.session_state.student_email and st.session_state.email_sent:
            st.success(f"📧 The detailed Answer Key has been sent securely to your email: {st.session_state.student_email}")
            
        st.markdown("---")
        st.warning("🔒 **Strict Security Protocol:** Please check your registered email inbox to view your Detailed Result.")
        st.markdown("---")
        
        if st.button("🔄 Take Another Test", use_container_width=True):
            st.session_state.test_status = 'not_started'
            st.rerun()

    st.markdown("<br><hr><p style='text-align: center; color: var(--text-color); font-size: 16px;'>Developed with ❤️ by <b>Mukesh Sir (9130103386)</b></p>", unsafe_allow_html=True)
