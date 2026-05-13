import streamlit as st
import pandas as pd
import smtplib
import requests
import urllib.parse
from email.mime.text import MIMEText
import random
import streamlit.components.v1 as components

# -----------------------------------------------------
# 1. Mitradnya Publication - Setup
# -----------------------------------------------------
TEACHER_EMAIL = "vidyarthi.mitradnyapublications@gmail.com" 
try:
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]
except:
    EMAIL_PASSWORD = "" 

TEACHER_NAME = "Mukesh Sir"

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
st.set_page_config(page_title="Mukesh Sir's Online Exam", page_icon="📝")
st.sidebar.title("📚 Mitradnya Publication's Online Test Series")

# Initialize Session State for Test Locking
if 'test_status' not in st.session_state:
    st.session_state.test_status = 'not_started' # Options: 'not_started', 'in_progress', 'submitted'

if df is not None:
    # Disable sidebar selection if test is active to prevent cheating/changing chapters
    sidebar_disabled = st.session_state.test_status != 'not_started'
    
    chapters = df['No'].unique()
    selected_chapter = st.sidebar.selectbox("1. Select Chapter:", chapters, disabled=sidebar_disabled)
    
    chapter_questions = df[df['No'] == selected_chapter]
    total_q = len(chapter_questions)
    
    st.sidebar.markdown("---")
    
    # 20-20 Question Chunks
    chunk_size = 20
    test_parts = []
    for i in range(0, total_q, chunk_size):
        test_parts.append(f"Test {i//chunk_size + 1}")
        
    selected_part = st.sidebar.radio("2. Select Test Part:", test_parts, disabled=sidebar_disabled)
    
    part_index = test_parts.index(selected_part)
    start_idx = part_index * chunk_size
    end_idx = start_idx + chunk_size
    current_quiz_df = chapter_questions.iloc[start_idx:end_idx]
    
    st.title("📚 Mukesh Sir's Online Examination Portal")
    st.subheader(f"Topic: {selected_chapter}")
    st.write(f"**{selected_part} (20 Marks / 20 Minutes)**")
    
    # --- Student Information (Locks when test starts) ---
    if st.session_state.test_status == 'not_started':
        st.info("⚠️ Instruction: Please fill in your details first and click 'Start Test'. The timer will begin immediately.")
        
    student_name = st.text_input("👤 Full Name:", disabled=sidebar_disabled)
    student_div = st.text_input("🏫 Division (A/B/C):", disabled=sidebar_disabled)
    student_roll = st.text_input("🔢 Roll No:", disabled=sidebar_disabled)
    student_email = st.text_input("📧 Email ID:", disabled=sidebar_disabled)
    st.markdown("---")
    
    # =======================================================
    # STATE 1: Test Not Started
    # =======================================================
    if st.session_state.test_status == 'not_started':
        if st.button("🟢 Start Test"):
            if student_name and student_div and student_roll:
                st.session_state.test_status = 'in_progress'
                st.rerun() # Reloads page to lock inputs and show questions
            else:
                st.warning("⚠️ Please fill in your Full Name, Division, and Roll No to start the test.")

    # =======================================================
    # STATE 2: Test In Progress
    # =======================================================
    elif st.session_state.test_status == 'in_progress':
        test_id = f"{selected_chapter}_{selected_part}".replace(" ", "_")
        
        # English Timer (HTML/JS)
        timer_code = f"""
        <div style="background-color:#1B4F72; color:white; padding:10px; border-radius:8px; text-align:center; font-size:22px; font-weight:bold; font-family:sans-serif; border: 2px solid #AED6F1; box-shadow: 2px 2px 5px grey;">
            <span id="time">Loading Timer...</span>
        </div>
        <script>
            var testId = "{test_id}";
            var endTime = sessionStorage.getItem("examEndTime_" + testId);
            
            if (!endTime) {{
                endTime = new Date().getTime() + 20 * 60 * 1000; // 20 minutes
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
            st.write(f"**Q{idx}. 🔹 {row['Question']}**")
            
            raw_options = [str(row['Option A']), str(row['Option B']), str(row['Option C']), str(row['Option D'])]
            
            # --- Duplicate Options Fix ---
            unique_options = []
            for opt in raw_options:
                while opt in unique_options:
                    opt += " "  
                unique_options.append(opt)
            options = unique_options
            
            # --- Shuffle Options ---
            random.seed(i)
            random.shuffle(options)
            random.seed()
            
            ans = st.radio("Options:", options, key=f"q_{i}", index=None, label_visibility="collapsed")
            user_answers.append(ans)
            st.write("")

        if st.button("🚀 Submit Exam"):
            if None not in user_answers:
                score = 0
                detailed_report_text = ""
                correct_answers = current_quiz_df['Correct Answer (Full Text)'].astype(str).str.strip().values
                results_list = []
                
                # Check answers
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
                
                # Save Data processing logic safely
                with st.spinner("Saving data to Excel..."):
                    GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbzucsekDDlyax6P8ZUUZgSWYjX55P4n6jRKM6YzZe35wxQ0D5ldPLmTcYfkCMJOLlTV/exec"
                    safe_name = urllib.parse.quote(str(student_name))
                    safe_div = urllib.parse.quote(str(student_div))
                    safe_roll = urllib.parse.quote(str(student_roll))
                    safe_test = urllib.parse.quote(f"{selected_chapter} - {selected_part}")
                    safe_score = urllib.parse.quote(str(score))
                    
                    final_url = f"{GOOGLE_SHEET_URL}?name={safe_name}&div={safe_div}&roll={safe_roll}&test={safe_test}&score={safe_score}"
                    
                    try:
                        res = requests.get(final_url)
                        sheet_success = (res.status_code == 200)
                    except Exception:
                        sheet_success = False
                
                # Send Emails
                send_detailed_email(TEACHER_EMAIL, student_name, student_div, student_roll, score, len(current_quiz_df), selected_chapter, selected_part, detailed_report_text, True)
                
                email_sent = False
                if student_email:
                    email_sent = send_detailed_email(student_email, student_name, student_div, student_roll, score, len(current_quiz_df), selected_chapter, selected_part, detailed_report_text, False)
                
                # Store results in session state to show on the next page securely
                st.session_state.score = score
                st.session_state.total_questions = len(current_quiz_df)
                st.session_state.results_list = results_list
                st.session_state.sheet_success = sheet_success
                st.session_state.email_sent = email_sent
                st.session_state.student_email = student_email
                
                st.session_state.test_status = 'submitted'
                st.rerun() # Move to Result Page
            else:
                st.warning("⚠️ Please answer all questions before submitting.")

    # =======================================================
    # STATE 3: Test Submitted (Results Page)
    # =======================================================
    elif st.session_state.test_status == 'submitted':
        # Remove the timer token from browser
        test_id = f"{selected_chapter}_{selected_part}".replace(" ", "_")
        components.html(f"<script>sessionStorage.removeItem('examEndTime_{test_id}');</script>", height=0)
        
        st.success(f"🎉 Result: {st.session_state.score}/{st.session_state.total_questions}")
        
        if st.session_state.sheet_success:
            st.info("📊 Your result has been successfully saved in Excel.")
        else:
            st.error("⚠️ Error occurred while saving to Excel.")
            
        if st.session_state.student_email and st.session_state.email_sent:
            st.info(f"📧 Detailed report sent to {st.session_state.student_email}")
            
        st.markdown("---")
        st.markdown("### 📊 Detailed Performance:")
        
        for res in st.session_state.results_list:
            if res['is_correct']:
                st.success(f"Q: {res['q']}\n\n✅ Your Ans: {res['user_ans']}")
            else:
                st.error(f"Q: {res['q']}\n\n❌ Your Ans: {res['user_ans']}\n\n🎯 Correct: {res['correct_ans']}")
        
        st.markdown("---")
        if st.button("🔄 Take Another Test"):
            st.session_state.test_status = 'not_started'
            st.rerun()
