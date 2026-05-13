import streamlit as st
import pandas as pd
import smtplib
import requests
import urllib.parse
from email.mime.text import MIMEText
import random

# -----------------------------------------------------
# १. Mitradnya Publication - Setup
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
# २. वेबसाईट इंटरफेस
# -----------------------------------------------------
st.set_page_config(page_title="Mukesh Sir's Online Exam", page_icon="📝")
st.sidebar.title("📚 Mitradnya Publication's Mukesh Sir's Online Test Series")

if df is not None:
    chapters = df['No'].unique()
    selected_chapter = st.sidebar.selectbox("1. Select Chapter:", chapters)
    
    chapter_questions = df[df['No'] == selected_chapter]
    total_q = len(chapter_questions)
    
    st.sidebar.markdown("---")
    
    # २०-२० प्रश्नांचे भाग
    chunk_size = 20
    test_parts = []
    for i in range(0, total_q, chunk_size):
        test_parts.append(f"Test {i//chunk_size + 1}")
        
    selected_part = st.sidebar.radio("2. Select Test Part:", test_parts)
    
    part_index = test_parts.index(selected_part)
    start_idx = part_index * chunk_size
    end_idx = start_idx + chunk_size
    current_quiz_df = chapter_questions.iloc[start_idx:end_idx]
    
    st.title("📚 Mukesh Sir's Online Examination Portal")
    st.subheader(f"Topic: {selected_chapter}")
    st.write(f"**{selected_part} (20 Marks)**")
    
    student_name = st.text_input("👤 Full Name:")
    student_div = st.text_input("🏫 Division (A/B/C):")
    student_roll = st.text_input("🔢 Roll No:")
    student_email = st.text_input("📧 Email ID:")
    st.markdown("---")
    
    user_answers = []
    for idx, (i, row) in enumerate(current_quiz_df.iterrows(), 1):
        st.write(f"**Q: {idx}. {row['Question']}**")
        
        raw_options = [str(row['Option A']), str(row['Option B']), str(row['Option C']), str(row['Option D'])]
        
        # --- Duplicate Options Fix (सारखे पर्याय दुरुस्त करणे) ---
        unique_options = []
        for opt in raw_options:
            while opt in unique_options:
                opt += " "  # Duplicate असल्यास एक space वाढवणे
            unique_options.append(opt)
        
        options = unique_options
        
        # --- पर्याय शफल (Shuffle) ---
        random.seed(i)
        random.shuffle(options)
        random.seed()
        
        ans = st.radio("Options:", options, key=f"q_{i}", index=None, label_visibility="collapsed")
        user_answers.append(ans)
        st.write("")

    if st.button("🚀 Submit Exam"):
        if student_name and student_div and student_roll and None not in user_answers:
            score = 0
            detailed_report_text = ""
            correct_answers = current_quiz_df['Correct Answer (Full Text)'].astype(str).str.strip().values
            
            for idx, (i, row) in enumerate(current_quiz_df.iterrows()):
                user_ans = str(user_answers[idx]).strip()
                correct_ans = str(correct_answers[idx]).strip()
                
                if user_ans == correct_ans:
                    score += 1
                    status = "✅ Correct"
                else:
                    status = f"❌ Wrong (Correct: {correct_ans})"
                detailed_report_text += f"Q: {row['Question']}\nYour Ans: {user_ans}\nStatus: {status}\n\n"
            
            st.success(f"🎉 Result: {score}/{len(current_quiz_df)}")
            
            # Google Sheet Update
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
                    if res.status_code == 200:
                        st.info("📊 तुमचा निकाल Excel मध्ये जतन झाला आहे.")
                    else:
                        st.error("⚠️ Excel मध्ये सेव्ह करताना अडचण आली.")
                except Exception as e:
                    st.error(f"⚠️ Excel Connection Error: {e}")
            
            # Send Emails
            send_detailed_email(TEACHER_EMAIL, student_name, student_div, student_roll, score, len(current_quiz_df), selected_chapter, selected_part, detailed_report_text, True)
            
            if student_email:
                send_detailed_email(student_email, student_name, student_div, student_roll, score, len(current_quiz_df), selected_chapter, selected_part, detailed_report_text, False)
                st.info(f"📧 Detailed report sent to {student_email}")
            
            st.markdown("---")
            st.markdown("### 📊 Detailed Performance:")
            for idx, (i, row) in enumerate(current_quiz_df.reset_index().iterrows()):
                if str(user_answers[idx]).strip() == correct_answers[idx]:
                    st.success(f"Q: {row['Question']}\n\n✅ Your Ans: {user_answers[idx]}")
                else:
                    st.error(f"Q: {row['Question']}\n\n❌ Your Ans: {user_answers[idx]}\n\n🎯 Correct: {correct_answers[idx]}")
        else:
            st.warning("⚠️ Please fill all details and answer all questions.")
