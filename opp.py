import streamlit as st
import pandas as pd
import smtplib
import requests
import urllib.parse
from email.mime.text import MIMEText

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
        # आधी utf-8 तपासून पाहू, एरर आला तर Windows च्या (cp1252) फॉरमॅटमध्ये वाचू
        try:
            df = pd.read_csv('All in one.csv', encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv('All in one.csv', encoding='cp1252')
            
        # रिकाम्या जागा भरून काढण्यासाठी
        df.fillna("None", inplace=True) 
        return df
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

df = load_data()

def send_score_to_teacher(student_name, div, roll, score, total, chapter, test_name):
    msg_content = f"📚 Result Alert!\n\nStudent: {student_name}\nDiv: {div}\nRoll: {roll}\nChapter: {chapter}\nTest: {test_name}\nScore: {score}/{total}"
    msg = MIMEText(msg_content)
    msg['Subject'] = f"Exam Result: {student_name} ({div}) score {score}/{total}"
    msg['From'] = TEACHER_NAME
    msg['To'] = TEACHER_EMAIL
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(TEACHER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(TEACHER_EMAIL, TEACHER_EMAIL, msg.as_string())
        server.quit()
        return True
    except:
        return False

# शिक्षक आणि विद्यार्थ्याला ईमेल पाठवण्यासाठी फंक्शन
def send_detailed_email(receiver_email, student_name, div, roll, score, total, chapter, test_name, report_content, is_teacher=True):
    if is_teacher:
        subject = f"New Result: {student_name} ({div}-{roll}) - {score}/{total}"
        body = f"📚 Result Alert for Mukesh Sir!\n\nStudent: {student_name}\nDivision: {div}\nRoll No: {roll}\nChapter: {chapter}\nTest: {test_name}\nScore: {score}/{total}\n\n--- Detailed Report ---\n{report_content}"
    else:
        subject = f"Your Online Exam Result (Mitradnya Publication's) ({score}/{total})"
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
    except:
        return False

# -----------------------------------------------------
# २. वेबसाईट इंटरफेस
# -----------------------------------------------------
st.set_page_config(page_title="Mukesh Sir's Online Exam", page_icon="📝")
st.sidebar.title("📚 Mitradnya Publication's (Mukesh Sir's) Online Test")

if df is not None:
    chapters = df['No'].unique()
    selected_chapter = st.sidebar.selectbox("1. Select Chapter:", chapters)
    
    chapter_questions = df[df['No'] == selected_chapter]
    total_q = len(chapter_questions)
    
    st.sidebar.markdown("---")
    
    # २०-२० प्रश्नांचे भाग (२० च्या गटात विभागणी)
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
    st.write(f"**Test: {selected_part} (20 Marks)**")
    
    student_name = st.text_input("👤 Enter Your Full Name:")
    student_div = st.text_input("🏫 Enter Your Division (e.g., A, B, C):")
    student_roll = st.text_input("🔢 Enter Your Roll No:")
    student_email = st.text_input("📧 Enter Your Email ID (To Receive Result):")
    st.markdown("---")
    
    user_answers = []
    for idx, (i, row) in enumerate(current_quiz_df.iterrows(), 1):
        # इथे आपण 'Q' आणि आपोआप येणारा नंबर जोडला आहे, सोबत एक छान चिन्ह दिले आहे
        st.write(f"**Q. {idx}. {row['Question']}**")
        
        options = [str(row['Option A']), str(row['Option B']), str(row['Option C']), str(row['Option D'])]
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
            
            st.success(f"🎉 Exam Submitted! Score: {score}/{len(current_quiz_df)}")
            
            # १. Google Sheet अपडेट (शिक्षक अहवालासाठी)
            GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbw7BoAF9_uf5pp1kM7XhpsIGb7zfMeX708BAFTjuoDLCUK4Yhpm-kbX2TevEeB_K5Yq/exec"
            safe_name = urllib.parse.quote(student_name)
            final_test_name = urllib.parse.quote(f"{selected_chapter}-{selected_part}")
            requests.get(f"{GOOGLE_SHEET_URL}?name={safe_name}&div={student_div}&roll={student_roll}&test={final_test_name}&score={score}")
            
            # २. शिक्षकाला सविस्तर रिपोर्ट पाठवणे
            send_detailed_email(receiver_email=TEACHER_EMAIL, student_name=student_name, div=student_div, roll=student_roll, score=score, total=len(current_quiz_df), chapter=selected_chapter, test_name=selected_part, report_content=detailed_report_text, is_teacher=True)
            
            # ३. विद्यार्थ्याला सविस्तर रिपोर्ट पाठवणे
            if student_email:
                send_detailed_email(receiver_email=student_email, student_name=student_name, div=student_div, roll=student_roll, score=score, total=len(current_quiz_df), chapter=selected_chapter, test_name=selected_part, report_content=detailed_report_text, is_teacher=False)
                st.info(f"📧 Detailed report sent to {student_email}")
            
            # ४. स्क्रीनवर सविस्तर निकाल दाखवणे
            st.markdown("---")
            st.markdown("### 📊 Your Detailed Performance:")
            for idx, (i, row) in enumerate(current_quiz_df.reset_index().iterrows()):
                if user_answers[idx] == correct_answers[idx]:
                    st.success(f"Q: {row['Question']}\n\n✅ Your Ans: {user_answers[idx]}")
                else:
                    st.error(f"Q: {row['Question']}\n\n❌ Your Ans: {user_answers[idx]}\n\n🎯 Correct: {correct_answers[idx]}")
        else:
            st.warning("⚠️ कृपया सर्व माहिती भरा आणि सर्व प्रश्न सोडवा.")
