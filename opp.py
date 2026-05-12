import streamlit as st
import smtplib
from email.mime.text import MIMEText

# -----------------------------------------------------
# -----------------------------------------------------
# (येथे तुमचा खरा ईमेल आणि Gmail App Password टाका)
TEACHER_EMAIL = "mukeshamrutkar.shm@gmail.com" 
EMAIL_PASSWORD = "Mukesh@9991"   

def send_score_to_teacher(student_name, score, total):
    msg_content = f"Mukesh Amrutkar's Quiz!\n\nStudent Name: {student_name}\nTopic: Partnership Final Accounts\nScore: {score}/{total}"
    msg = MIMEText(msg_content)
    msg['Subject'] = f"New Quiz Result: {student_name} scored {score}/{total}"
    msg['From'] = TEACHER_EMAIL
    msg['To'] = TEACHER_EMAIL

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(TEACHER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(TEACHER_EMAIL, TEACHER_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False

# -----------------------------------------------------
# २. सर्व ५० प्रश्नांचा डेटाबेस (Python List of Dictionaries)
# -----------------------------------------------------
quiz_data = [
    {"q": "1. The Indian Partnership Act was passed in the year:", "options": ["Select", "1923", "1932", "1956", "2013"], "ans": "1932"},
    {"q": "2. The liability of partners in a standard partnership firm is:", "options": ["Select", "Limited", "Unlimited", "Zero", "Joint only"], "ans": "Unlimited"},
    {"q": "3. The document containing the terms of the partnership agreement is called:", "options": ["Select", "Partnership Deed", "Prospectus", "Articles", "Memorandum"], "ans": "Partnership Deed"},
    {"q": "4. In the absence of a Partnership Deed, profits and losses are shared:", "options": ["Select", "In Capital Ratio", "In Time Ratio", "Equally", "As per work"], "ans": "Equally"},
    {"q": "5. Registration of a Partnership Firm is compulsory in the state of:", "options": ["Select", "Gujarat", "Maharashtra", "Delhi", "Goa"], "ans": "Maharashtra"},
    {"q": "6. In the absence of an agreement, interest on partner's loan is allowed at:", "options": ["Select", "5% p.a.", "6% p.a.", "8% p.a.", "10% p.a."], "ans": "6% p.a."},
    {"q": "7. Closing stock is always valued at Cost Price or Market Price, whichever is:", "options": ["Select", "Higher", "Lower", "Equal", "None"], "ans": "Lower"},
    {"q": "8. Wages and Salaries appearing in the Trial Balance are shown in:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Balance Sheet", "Capital A/c"], "ans": "Trading A/c"},
    {"q": "9. Salaries and Wages appearing in the Trial Balance are shown in:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Balance Sheet", "Capital A/c"], "ans": "Profit & Loss A/c"},
    {"q": "10. Carriage Inward is debited to:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Partners' Capital A/c", "Balance Sheet"], "ans": "Trading A/c"},
    {"q": "11. Carriage Outward is debited to:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Partners' Capital A/c", "Balance Sheet"], "ans": "Profit & Loss A/c"},
    {"q": "12. Return Outward is deducted from:", "options": ["Select", "Sales", "Purchases", "Capital", "Debtors"], "ans": "Purchases"},
    {"q": "13. Return Inward is deducted from:", "options": ["Select", "Sales", "Purchases", "Capital", "Debtors"], "ans": "Sales"},
    {"q": "14. Prepaid expenses are shown on the:", "options": ["Select", "Asset side", "Liability side", "Debit of P&L", "Credit of Trading"], "ans": "Asset side"},
    {"q": "15. Outstanding expenses are shown on the:", "options": ["Select", "Asset side", "Liability side", "Debit of Trading", "Credit of P&L"], "ans": "Liability side"},
    {"q": "16. Bad debts are written off against:", "options": ["Select", "Creditors", "Bills Receivable", "Debtors", "Cash"], "ans": "Debtors"},
    {"q": "17. Provision for doubtful debts (RDD) is calculated on:", "options": ["Select", "Creditors", "Net Sales", "Debtors", "Bills Payable"], "ans": "Debtors"},
    {"q": "18. Depreciation is a charge against:", "options": ["Select", "Assets", "Liabilities", "Capital", "Cash"], "ans": "Assets"},
    {"q": "19. Depreciation is shown on the debit side of:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Balance Sheet", "Partners A/c"], "ans": "Profit & Loss A/c"},
    {"q": "20. Goods distributed as free samples are credited to:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Capital A/c", "Balance Sheet"], "ans": "Trading A/c"},
    {"q": "21. Goods distributed as free samples are debited to P&L A/c as:", "options": ["Select", "Purchases", "Advertisement", "Charity", "Discount"], "ans": "Advertisement"},
    {"q": "22. Goods withdrawn by a partner for personal use is called:", "options": ["Select", "Capital", "Drawings", "Investment", "Salary"], "ans": "Drawings"},
    {"q": "23. Interest on drawings is a/an ________ for the partnership firm.", "options": ["Select", "Expense", "Income", "Asset", "Liability"], "ans": "Income"},
    {"q": "24. Interest on capital is a/an ________ for the partnership firm.", "options": ["Select", "Expense", "Income", "Asset", "Liability"], "ans": "Expense"},
    {"q": "25. If there are Fixed Capital Accounts, all adjustments are made in:", "options": ["Select", "Capital A/c", "Current A/c", "Suspense A/c", "Loan A/c"], "ans": "Current A/c"},
    {"q": "26. If the Capital method is Fluctuating, all adjustments are made in:", "options": ["Select", "Capital A/c", "Current A/c", "Suspense A/c", "Cash A/c"], "ans": "Capital A/c"},
    {"q": "27. Gross Profit is transferred to the ________ side of the Profit & Loss A/c.", "options": ["Select", "Debit", "Credit", "Asset", "Liability"], "ans": "Credit"},
    {"q": "28. Net Profit is transferred to the ________ of Partners' Capital/Current A/c.", "options": ["Select", "Debit", "Credit", "Asset", "Liability"], "ans": "Credit"},
    {"q": "29. The debit balance of the Trading Account indicates:", "options": ["Select", "Gross Profit", "Gross Loss", "Net Profit", "Net Loss"], "ans": "Gross Loss"},
    {"q": "30. The credit balance of the Profit & Loss Account indicates:", "options": ["Select", "Gross Profit", "Gross Loss", "Net Profit", "Net Loss"], "ans": "Net Profit"},
    {"q": "31. Bills Receivable discounted but dishonoured is added to:", "options": ["Select", "Debtors", "Creditors", "Cash", "Capital"], "ans": "Debtors"},
    {"q": "32. Interest on Partner's Loan is debited to:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Capital A/c", "Asset"], "ans": "Profit & Loss A/c"},
    {"q": "33. Unrecorded purchases are added to Purchases and:", "options": ["Select", "Debtors", "Creditors", "Bills Payable", "Capital"], "ans": "Creditors"},
    {"q": "34. Unrecorded sales are added to Sales and:", "options": ["Select", "Debtors", "Creditors", "Cash", "Stock"], "ans": "Debtors"},
    {"q": "35. Goods destroyed by fire (fully insured), the insurance claim is an:", "options": ["Select", "Expense", "Asset", "Liability", "Income"], "ans": "Asset"},
    {"q": "36. Royalty paid on production is debited to:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Balance Sheet", "Capital A/c"], "ans": "Trading A/c"},
    {"q": "37. Royalty paid on sales is debited to:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Balance Sheet", "Capital A/c"], "ans": "Profit & Loss A/c"},
    {"q": "38. Commission received in advance is a/an:", "options": ["Select", "Asset", "Liability", "Income", "Expense"], "ans": "Liability"},
    {"q": "39. Income accrued but not received is shown on the:", "options": ["Select", "Asset side", "Liability side", "Debit of P&L", "Credit of Trading"], "ans": "Asset side"},
    {"q": "40. Bank Overdraft is shown under:", "options": ["Select", "Fixed Assets", "Current Liabilities", "Current Assets", "Investments"], "ans": "Current Liabilities"},
    {"q": "41. Goodwill is an example of a/an:", "options": ["Select", "Tangible Asset", "Intangible Asset", "Fictitious Asset", "Current Asset"], "ans": "Intangible Asset"},
    {"q": "42. Patents and Trademarks appear on which side of the Balance Sheet?", "options": ["Select", "Asset", "Liability", "Both", "None"], "ans": "Asset"},
    {"q": "43. Provident Fund contribution by the employer is debited to:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Capital A/c", "Balance Sheet"], "ans": "Profit & Loss A/c"},
    {"q": "44. Cash in hand is a/an:", "options": ["Select", "Current Asset", "Fixed Asset", "Intangible Asset", "Liability"], "ans": "Current Asset"},
    {"q": "45. Discount allowed is shown on the debit side of:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Capital A/c", "Balance Sheet"], "ans": "Profit & Loss A/c"},
    {"q": "46. Partners share profit/loss in their _________ ratio.", "options": ["Select", "Capital", "Sacrifice", "Profit Sharing", "Gain"], "ans": "Profit Sharing"},
    {"q": "47. Balance Sheet is a statement showing:", "options": ["Select", "Income & Expenses", "Financial Position", "Cash flow", "Production"], "ans": "Financial Position"},
    {"q": "48. Factory lighting is debited to:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Capital A/c", "Balance Sheet"], "ans": "Trading A/c"},
    {"q": "49. Office lighting is debited to:", "options": ["Select", "Trading A/c", "Profit & Loss A/c", "Capital A/c", "Balance Sheet"], "ans": "Profit & Loss A/c"},
    {"q": "50. An amount which cannot be recovered from Debtors is called:", "options": ["Select", "Discount", "Bad Debts", "Drawings", "Charity"], "ans": "Bad Debts"}
]

# -----------------------------------------------------
# ३. वेबसाईटचे डिझाईन आणि सिस्टीम
# -----------------------------------------------------
st.set_page_config(page_title="Mitradnya Online Exam", page_icon="📝")

st.title("📚 Mitradnya Publication - Online Exam")
st.subheader("Subject: Book-Keeping & Accountancy")
st.markdown("**Topic: Partnership Final Accounts (50 Marks)**")
st.markdown("---")

student_name = st.text_input("👤 Enter Your Full Name:")
st.markdown("---")

# विद्यार्थ्यांची उत्तरे साठवण्यासाठी एक रिकामी यादी 
user_answers = []

# 'For Loop' वापरून सर्व ५० प्रश्न एकाच वेळी स्क्रीनवर आणण्याची पद्धत
for index, item in enumerate(quiz_data):
    st.markdown(f"**{item['q']}**")
    # प्रत्येक प्रश्नाला एक वेगळी ओळख (key) द्यावी लागते
    ans = st.radio("Options:", item['options'], key=f"q_{index}", label_visibility="collapsed")
    user_answers.append(ans)
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# सबमिट बटण आणि निकाल 
if st.button("🚀 Submit Exam"):
    if student_name == "":
        st.warning("⚠️ Please enter your name first!")
    else:
        score = 0
        total_questions = len(quiz_data)
        
        # उत्तरे तपासण्याची सिस्टीम
        for i in range(total_questions):
            if user_answers[i] == quiz_data[i]['ans']:
                score += 1
                
        st.success(f"🎉 Exam Submitted! Dear {student_name}, your Score is {score}/{total_questions}")
        
        # शिक्षकाला ईमेल पाठवणे
        with st.spinner("Sending report to Mukesh Sir..."):
            email_sent = send_score_to_teacher(student_name, score, total_questions)
            
        if email_sent:
            st.info("✅ Your official result has been emailed to the teacher.")
        else:
            st.error("❌ Note: Result calculated, but Email setup is not complete yet.")
