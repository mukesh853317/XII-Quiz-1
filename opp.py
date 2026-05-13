import streamlit as st
import smtplib
import requests
from email.mime.text import MIMEText

# -----------------------------------------------------
# १. Mitradnya Publication - Email Setup
# -----------------------------------------------------
TEACHER_EMAIL = "vidyarthi.mitradnyapublications@gmail.com" 
EMAIL_PASSWORD = "vhoc lltr ejwu qomk"   
TEACHER_NAME = "Mukesh Sir"

def send_score_to_teacher(student_name, div, roll, score, total, test_name):
    msg_content = f"📚 Online Exam's Result Alert 📚!\n\nStudent Name: {student_name}\nDivision: {div}\nRoll No: {roll}\nTopic: Partnership Final Accounts\nTest: {test_name}\nScore: {score}/{total}"
    msg = MIMEText(msg_content)
    msg['Subject'] = f"New Quiz Result: {student_name} ({div}-{roll}) scored {score}/{total} in {test_name}"
    msg['From'] = TEACHER_NAME
    msg['To'] = TEACHER_NAME

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
# २. सर्व १०० प्रश्नांचा मास्टर डेटाबेस (Select काढलेले आहेत)
# -----------------------------------------------------
quiz_data = [
    # --- Basic 50 Questions ---
    {"q": "1. The Indian Partnership Act was passed in the year:", "options": ["1923", "1932", "1956", "2013"], "ans": "1932"},
    {"q": "2. The liability of partners in a standard partnership firm is:", "options": ["Limited", "Unlimited", "Zero", "Joint only"], "ans": "Unlimited"},
    {"q": "3. The document containing the terms of the partnership agreement is called:", "options": ["Partnership Deed", "Prospectus", "Articles", "Memorandum"], "ans": "Partnership Deed"},
    {"q": "4. In the absence of a Partnership Deed, profits and losses are shared:", "options": ["In Capital Ratio", "In Time Ratio", "Equally", "As per work"], "ans": "Equally"},
    {"q": "5. Registration of a Partnership Firm is compulsory in the state of:", "options": ["Gujarat", "Maharashtra", "Delhi", "Goa"], "ans": "Maharashtra"},
    {"q": "6. In the absence of an agreement, interest on partner's loan is allowed at:", "options": ["5% p.a.", "6% p.a.", "8% p.a.", "10% p.a."], "ans": "6% p.a."},
    {"q": "7. Closing stock is always valued at Cost Price or Market Price, whichever is:", "options": ["Higher", "Lower", "Equal", "None"], "ans": "Lower"},
    {"q": "8. Wages and Salaries appearing in the Trial Balance are shown in:", "options": ["Trading A/c", "Profit & Loss A/c", "Balance Sheet", "Capital A/c"], "ans": "Trading A/c"},
    {"q": "9. Salaries and Wages appearing in the Trial Balance are shown in:", "options": ["Trading A/c", "Profit & Loss A/c", "Balance Sheet", "Capital A/c"], "ans": "Profit & Loss A/c"},
    {"q": "10. Carriage Inward is debited to:", "options": ["Trading A/c", "Profit & Loss A/c", "Partners' Capital A/c", "Balance Sheet"], "ans": "Trading A/c"},
    {"q": "11. Carriage Outward is debited to:", "options": ["Trading A/c", "Profit & Loss A/c", "Partners' Capital A/c", "Balance Sheet"], "ans": "Profit & Loss A/c"},
    {"q": "12. Return Outward is deducted from:", "options": ["Sales", "Purchases", "Capital", "Debtors"], "ans": "Purchases"},
    {"q": "13. Return Inward is deducted from:", "options": ["Sales", "Purchases", "Capital", "Debtors"], "ans": "Sales"},
    {"q": "14. Prepaid expenses are shown on the:", "options": ["Asset side", "Liability side", "Debit of P&L", "Credit of Trading"], "ans": "Asset side"},
    {"q": "15. Outstanding expenses are shown on the:", "options": ["Asset side", "Liability side", "Debit of Trading", "Credit of P&L"], "ans": "Liability side"},
    {"q": "16. Bad debts are written off against:", "options": ["Creditors", "Bills Receivable", "Debtors", "Cash"], "ans": "Debtors"},
    {"q": "17. Provision for doubtful debts (RDD) is calculated on:", "options": ["Creditors", "Net Sales", "Debtors", "Bills Payable"], "ans": "Debtors"},
    {"q": "18. Depreciation is a charge against:", "options": ["Assets", "Liabilities", "Capital", "Cash"], "ans": "Assets"},
    {"q": "19. Depreciation is shown on the debit side of:", "options": ["Trading A/c", "Profit & Loss A/c", "Balance Sheet", "Partners A/c"], "ans": "Profit & Loss A/c"},
    {"q": "20. Goods distributed as free samples are credited to:", "options": ["Trading A/c", "Profit & Loss A/c", "Capital A/c", "Balance Sheet"], "ans": "Trading A/c"},
    {"q": "21. Goods distributed as free samples are debited to P&L A/c as:", "options": ["Purchases", "Advertisement", "Charity", "Discount"], "ans": "Advertisement"},
    {"q": "22. Goods withdrawn by a partner for personal use is called:", "options": ["Capital", "Drawings", "Investment", "Salary"], "ans": "Drawings"},
    {"q": "23. Interest on drawings is a/an ________ for the partnership firm.", "options": ["Expense", "Income", "Asset", "Liability"], "ans": "Income"},
    {"q": "24. Interest on capital is a/an ________ for the partnership firm.", "options": ["Expense", "Income", "Asset", "Liability"], "ans": "Expense"},
    {"q": "25. If there are Fixed Capital Accounts, all adjustments are made in:", "options": ["Capital A/c", "Current A/c", "Suspense A/c", "Loan A/c"], "ans": "Current A/c"},
    {"q": "26. If the Capital method is Fluctuating, all adjustments are made in:", "options": ["Capital A/c", "Current A/c", "Suspense A/c", "Cash A/c"], "ans": "Capital A/c"},
    {"q": "27. Gross Profit is transferred to the ________ side of the Profit & Loss A/c.", "options": ["Debit", "Credit", "Asset", "Liability"], "ans": "Credit"},
    {"q": "28. Net Profit is transferred to the ________ of Partners' Capital/Current A/c.", "options": ["Debit", "Credit", "Asset", "Liability"], "ans": "Credit"},
    {"q": "29. The debit balance of the Trading Account indicates:", "options": ["Gross Profit", "Gross Loss", "Net Profit", "Net Loss"], "ans": "Gross Loss"},
    {"q": "30. The credit balance of the Profit & Loss Account indicates:", "options": ["Gross Profit", "Gross Loss", "Net Profit", "Net Loss"], "ans": "Net Profit"},
    {"q": "31. Bills Receivable discounted but dishonoured is added to:", "options": ["Debtors", "Creditors", "Cash", "Capital"], "ans": "Debtors"},
    {"q": "32. Interest on Partner's Loan is debited to:", "options": ["Trading A/c", "Profit & Loss A/c", "Capital A/c", "Asset"], "ans": "Profit & Loss A/c"},
    {"q": "33. Unrecorded purchases are added to Purchases and:", "options": ["Debtors", "Creditors", "Bills Payable", "Capital"], "ans": "Creditors"},
    {"q": "34. Unrecorded sales are added to Sales and:", "options": ["Debtors", "Creditors", "Cash", "Stock"], "ans": "Debtors"},
    {"q": "35. Goods destroyed by fire (fully insured), the insurance claim is an:", "options": ["Expense", "Asset", "Liability", "Income"], "ans": "Asset"},
    {"q": "36. Royalty paid on production is debited to:", "options": ["Trading A/c", "Profit & Loss A/c", "Balance Sheet", "Capital A/c"], "ans": "Trading A/c"},
    {"q": "37. Royalty paid on sales is debited to:", "options": ["Trading A/c", "Profit & Loss A/c", "Balance Sheet", "Capital A/c"], "ans": "Profit & Loss A/c"},
    {"q": "38. Commission received in advance is a/an:", "options": ["Asset", "Liability", "Income", "Expense"], "ans": "Liability"},
    {"q": "39. Income accrued but not received is shown on the:", "options": ["Asset side", "Liability side", "Debit of P&L", "Credit of Trading"], "ans": "Asset side"},
    {"q": "40. Bank Overdraft is shown under:", "options": ["Fixed Assets", "Current Liabilities", "Current Assets", "Investments"], "ans": "Current Liabilities"},
    {"q": "41. Goodwill is an example of a/an:", "options": ["Tangible Asset", "Intangible Asset", "Fictitious Asset", "Current Asset"], "ans": "Intangible Asset"},
    {"q": "42. Patents and Trademarks appear on which side of the Balance Sheet?", "options": ["Asset", "Liability", "Both", "None"], "ans": "Asset"},
    {"q": "43. Provident Fund contribution by the employer is debited to:", "options": ["Trading A/c", "Profit & Loss A/c", "Capital A/c", "Balance Sheet"], "ans": "Profit & Loss A/c"},
    {"q": "44. Cash in hand is a/an:", "options": ["Current Asset", "Fixed Asset", "Intangible Asset", "Liability"], "ans": "Current Asset"},
    {"q": "45. Discount allowed is shown on the debit side of:", "options": ["Trading A/c", "Profit & Loss A/c", "Capital A/c", "Balance Sheet"], "ans": "Profit & Loss A/c"},
    {"q": "46. Partners share profit/loss in their _________ ratio.", "options": ["Capital", "Sacrifice", "Profit Sharing", "Gain"], "ans": "Profit Sharing"},
    {"q": "47. Balance Sheet is a statement showing:", "options": ["Income & Expenses", "Financial Position", "Cash flow", "Production"], "ans": "Financial Position"},
    {"q": "48. Factory lighting is debited to:", "options": ["Trading A/c", "Profit & Loss A/c", "Capital A/c", "Balance Sheet"], "ans": "Trading A/c"},
    {"q": "49. Office lighting is debited to:", "options": ["Trading A/c", "Profit & Loss A/c", "Capital A/c", "Balance Sheet"], "ans": "Profit & Loss A/c"},
    {"q": "50. An amount which cannot be recovered from Debtors is called:", "options": ["Discount", "Bad Debts", "Drawings", "Charity"], "ans": "Bad Debts"},

    # --- Advanced 51 to 100 Questions ---
    {"q": "51. If 'Rent (for 10 months) ₹10,000' is given in the Trial Balance, what is the Outstanding Rent amount and for how many months?", "options": ["2 months, ₹2,000", "1 month, ₹1,000", "2 months, ₹1,000", "No Outstanding"], "ans": "2 months, ₹2,000"},
    {"q": "52. If 'Insurance (paid for 15 months w.e.f. 1st April) ₹15,000' is given (Accounting year ends 31st March), what is the Prepaid Insurance?", "options": ["₹5,000", "₹3,000", "₹12,000", "₹1,000"], "ans": "₹3,000"},
    {"q": "53. If 'Advertisement (for 3 years) ₹30,000' is given, what amount will be charged to the Profit & Loss A/c for the current year?", "options": ["₹30,000", "₹15,000", "₹10,000", "₹20,000"], "ans": "₹10,000"},
    {"q": "54. If '10% Bank Loan ₹50,000' is taken on 1st Oct and the year ends on 31st March, what will be the Outstanding Interest?", "options": ["₹5,000", "₹2,500", "₹1,250", "No Interest"], "ans": "₹2,500"},
    {"q": "55. Where is the second effect of 'Accrued Interest on 12% Government Bonds' recorded?", "options": ["P&L Debit side", "Balance Sheet Liability", "Balance Sheet Asset side", "Trading Credit side"], "ans": "Balance Sheet Asset side"},
    {"q": "56. If goods worth ₹5,000 are destroyed by fire and the insurance company admits a claim of ₹3,000, what amount of loss is shown on the P&L Debit side?", "options": ["₹5,000", "₹3,000", "₹2,000", "₹8,000"], "ans": "₹2,000"},
    {"q": "57. What are the two effects of Uninsured goods stolen?", "options": ["Trading Cr. & Asset", "Trading Cr. & P&L Dr.", "Trading Cr. & Liability", "P&L Dr. & Asset"], "ans": "Trading Cr. & P&L Dr."},
    {"q": "58. Under which expense head are 'Goods distributed as free samples' recorded on the P&L Debit side?", "options": ["Advertisement", "Sales", "Purchases", "Charity"], "ans": "Advertisement"},
    {"q": "59. What is the second effect if a partner withdraws goods for personal use?", "options": ["P&L Debit", "Partners Capital/Current Cr.", "Partners Capital/Current Dr.", "Asset side"], "ans": "Partners Capital/Current Dr."},
    {"q": "60. Closing Stock is always valued at:", "options": ["Cost Price", "Market Price", "Cost Price or Market Price, whichever is LESS", "Cost Price or Market Price, whichever is HIGHER"], "ans": "Cost Price or Market Price, whichever is LESS"},
    {"q": "61. On which amount is 'New RDD' calculated?", "options": ["Gross Debtors", "Net Debtors (After deducting new bad debts)", "Creditors", "Sales"], "ans": "Net Debtors (After deducting new bad debts)"},
    {"q": "62. How are 'Unrecorded Sales' treated before calculating RDD?", "options": ["Added to Debtors", "Deducted from Debtors", "Ignored", "Debited to P&L"], "ans": "Added to Debtors"},
    {"q": "63. What is the effect of 'Bills Receivable dishonoured'?", "options": ["Add to Debtors & Deduct from Bills Receivable", "Deduct from Debtors", "Add to Creditors", "P&L Debit"], "ans": "Add to Debtors & Deduct from Bills Receivable"},
    {"q": "64. If the total of P&L Debit (Old Bad debts + New Bad debts + New RDD) is LESS than Old RDD, where is the balance shown?", "options": ["P&L Debit side", "P&L Credit side", "Asset side", "Liability side"], "ans": "P&L Credit side"},
    {"q": "65. When is the 'Reserve for discount on Debtors' calculated?", "options": ["At the very beginning", "After deducting New Bad debts and New RDD", "Only on Gross Debtors", "On Sales"], "ans": "After deducting New Bad debts and New RDD"},
    {"q": "66. What are the two effects of 'Unrecorded Purchases'?", "options": ["Add to Purchases & Add to Debtors", "Add to Purchases & Add to Creditors", "Deduct from Purchases", "Trading Cr. & Asset"], "ans": "Add to Purchases & Add to Creditors"},
    {"q": "67. What is the effect of 'Bills Payable dishonoured'?", "options": ["Add to Creditors & Deduct from Bills Payable", "Deduct from Creditors", "P&L Credit", "Add to Debtors"], "ans": "Add to Creditors & Deduct from Bills Payable"},
    {"q": "68. Where is the 'Reserve for discount on Creditors' shown?", "options": ["P&L Debit & Deduct from Debtors", "P&L Credit & Deduct from Creditors", "Trading Debit", "Add to Creditors"], "ans": "P&L Credit & Deduct from Creditors"},
    {"q": "69. What is 'Return Outward' and from what is it deducted?", "options": ["Sales Return (Deduct from Sales)", "Purchase Return (Deduct from Purchases)", "Bad debts", "Discount"], "ans": "Purchase Return (Deduct from Purchases)"},
    {"q": "70. What is 'Return Inward'?", "options": ["Purchase Return", "Sales Return", "Carriage", "Freight"], "ans": "Sales Return"},
    {"q": "71. Under the Fixed Capital Method, where are all adjustments (like Interest, Salary, Drawings) recorded?", "options": ["Capital Account", "Current Account", "Suspense Account", "Loan Account"], "ans": "Current Account"},
    {"q": "72. Is a Current Account opened under the Fluctuating Capital Method?", "options": ["Yes, it is opened", "No, all entries are made in the Capital Account", "Only for profit", "Sometimes"], "ans": "No, all entries are made in the Capital Account"},
    {"q": "73. If the date of drawings is not given, for how many months is 'Interest on Drawings' charged?", "options": ["12 months", "3 months", "6 months", "No interest is charged"], "ans": "6 months"},
    {"q": "74. If not mentioned in the deed, what is the rate of 'Interest on Partner's Loan' and where is it recorded?", "options": ["6% p.a. (P&L Debit)", "5% p.a. (P&L Credit)", "10% p.a. (Trading Debit)", "Not Allowed"], "ans": "6% p.a. (P&L Debit)"},
    {"q": "75. 'Interest on Capital' is a/an ________ for the partnership firm.", "options": ["Income", "Asset", "Expense", "Liability"], "ans": "Expense"},
    {"q": "76. Where are 'Wages paid for installation of Machinery' recorded?", "options": ["Trading Debit (Added to Wages)", "P&L Debit", "Balance Sheet Asset (Added to Machinery)", "Capital Account"], "ans": "Balance Sheet Asset (Added to Machinery)"},
    {"q": "77. If 'Wages and Salaries' is given in the Trial Balance, where is it recorded?", "options": ["Trading A/c Debit", "Profit & Loss A/c Debit", "Partners Current A/c", "Balance Sheet"], "ans": "Trading A/c Debit"},
    {"q": "78. If 'Salaries and Wages' is given in the Trial Balance, where is it recorded?", "options": ["Trading A/c Debit", "Profit & Loss A/c Debit", "Partners Capital A/c", "Balance Sheet"], "ans": "Profit & Loss A/c Debit"},
    {"q": "79. If only 'Trade Expenses' are given (without General Expenses), where are they recorded?", "options": ["Trading A/c Debit", "Profit & Loss A/c Debit", "Asset Side", "Liability Side"], "ans": "Profit & Loss A/c Debit"},
    {"q": "80. If 'Trade Expenses' are given along with 'General/Office Expenses', where are the 'Trade Expenses' recorded?", "options": ["Trading A/c Debit", "Profit & Loss A/c Debit", "Asset Side", "Liability Side"], "ans": "Trading A/c Debit"},
    {"q": "81. Where is 'Carriage Inward' debited?", "options": ["Trading A/c", "Profit & Loss A/c", "Capital A/c", "Asset"], "ans": "Trading A/c"},
    {"q": "82. Where is 'Carriage Outward' debited?", "options": ["Trading A/c", "Profit & Loss A/c", "Capital A/c", "Liability"], "ans": "Profit & Loss A/c"},
    {"q": "83. Where is 'Royalty on Production/Purchase' debited?", "options": ["Profit & Loss A/c", "Trading A/c", "Capital A/c", "Asset"], "ans": "Trading A/c"},
    {"q": "84. Where is 'Royalty on Sales' debited?", "options": ["Profit & Loss A/c", "Trading A/c", "Capital A/c", "Asset"], "ans": "Profit & Loss A/c"},
    {"q": "85. Where are 'Import Duty' and 'Export Duty' recorded respectively?", "options": ["Both in Trading A/c", "Both in P&L A/c", "Import (Trading Dr.) & Export (P&L Dr.)", "Export (Trading Dr.) & Import (P&L Dr.)"], "ans": "Import (Trading Dr.) & Export (P&L Dr.)"},
    {"q": "86. 'Pre-received Income' (Income received in advance) is a/an ________ for the firm.", "options": ["Asset", "Liability", "Expense", "Income"], "ans": "Liability"},
    {"q": "87. Where is 'Income Receivable' (Income earned but not received) shown?", "options": ["Asset Side", "Liability Side", "Trading Debit", "P&L Debit"], "ans": "Asset Side"},
    {"q": "88. What are the two effects of 'Outstanding Expenses'?", "options": ["Add to Exp (P&L/Trading Dr.) & Asset", "Add to Exp (P&L/Trading Dr.) & Liability", "Deduct from Exp & Asset", "Deduct from Exp & Liability"], "ans": "Add to Exp (P&L/Trading Dr.) & Liability"},
    {"q": "89. What are the two effects of 'Prepaid Expenses'?", "options": ["Add to Exp & Liability", "Deduct from Exp (P&L/Trading Dr.) & Liability", "Deduct from Exp (P&L/Trading Dr.) & Asset", "Add to Exp & Asset"], "ans": "Deduct from Exp (P&L/Trading Dr.) & Asset"},
    {"q": "90. If 'Loss on sale of Furniture' is given on the debit side of the Trial Balance, where will it go?", "options": ["Trading Dr.", "P&L Dr.", "Balance Sheet Liability", "Balance Sheet Asset"], "ans": "P&L Dr."},
    {"q": "91. What is the formula for 'Cost of Goods Sold'?", "options": ["Sales - Closing Stock", "Opening Stock + Purchases + Direct Exp - Closing Stock", "Purchases + Sales - Closing Stock", "Opening Stock - Purchases"], "ans": "Opening Stock + Purchases + Direct Exp - Closing Stock"},
    {"q": "92. How is 'Gross Profit' calculated?", "options": ["Net Sales - Cost of Goods Sold", "Purchases - Sales", "Opening Stock + Purchases", "Net Profit - Indirect Expenses"], "ans": "Net Sales - Cost of Goods Sold"},
    {"q": "93. What is the formula to calculate 'Operating Profit'?", "options": ["Gross Profit - Operating Expenses", "Net Sales - Gross Profit", "Net Profit + Income", "Cost of Goods Sold + Expenses"], "ans": "Gross Profit - Operating Expenses"},
    {"q": "94. If a partner is to be given a 5% commission on 'Net Profit', on which side of the P&L is it recorded?", "options": ["Credit side", "Debit side", "Trading Credit", "Balance Sheet Asset"], "ans": "Debit side"},
    {"q": "95. Is 'Depreciation' calculated on Current Assets (like Debtors, Cash)?", "options": ["Yes", "No, only on Fixed Assets", "Only on Cash", "Only on Debtors"], "ans": "No, only on Fixed Assets"},
    {"q": "96. In which year was the Indian Partnership Act passed?", "options": ["1956", "1932", "2013", "1881"], "ans": "1932"},
    {"q": "97. If the 'Partnership Deed' is silent on the profit-loss sharing ratio, how are profits shared?", "options": ["In Capital Ratio", "According to age", "Equally", "According to work"], "ans": "Equally"},
    {"q": "98. If there is no provision in the 'Partnership Deed', what percentage of 'Interest on Capital' is allowed?", "options": ["5%", "6%", "10%", "Not Allowed"], "ans": "Not Allowed"},
    {"q": "99. As per the Companies Act, 2013, what is the maximum number of partners allowed in a partnership firm?", "options": ["20", "50", "100", "Unlimited"], "ans": "50"},
    {"q": "100. 'Goodwill' is an example of which type of asset?", "options": ["Tangible Asset", "Intangible Asset", "Current Asset", "Fictitious Asset"], "ans": "Intangible Asset"}
]

# -----------------------------------------------------
# ३. वेबसाईटचे डिझाईन आणि मेनू बार (Menu Bar)
# -----------------------------------------------------
st.set_page_config(page_title="Mukesh Sir's Online Exam", page_icon="📝")

st.sidebar.title("📚 Mitradnya Publication's (Mukesh Sir's) Online Exam 📚")
st.sidebar.markdown("---")
st.sidebar.subheader("Select Your Exam:")
test_choice = st.sidebar.radio("Choose a Test Part:", [
    "Test 1: Basics & Theory (Q1-Q25)",
    "Test 2: Trading & P&L (Q26-Q50)",
    "Test 3: Adjustments & Rules (Q51-Q75)",
    "Test 4: Advanced Concepts (Q76-Q100)"
])
st.sidebar.markdown("---")
st.sidebar.info("Developed by Mukesh Sir (9130103386)")

if test_choice == "Test 1: Basics & Theory (Q1-Q25)":
    current_quiz = quiz_data[0:25]
    topic_name = "Part 1: Basics & Theory"
elif test_choice == "Test 2: Trading & P&L (Q26-Q50)":
    current_quiz = quiz_data[25:50]
    topic_name = "Part 2: Trading & P&L Concepts"
elif test_choice == "Test 3: Adjustments & Rules (Q51-Q75)":
    current_quiz = quiz_data[50:75]
    topic_name = "Part 3: Adjustments & Rules"
else:
    current_quiz = quiz_data[75:100]
    topic_name = "Part 4: Advanced Concepts"

st.title("📚 Mukesh Sir's - Online Exam 📚")
st.subheader("Subject: Book-Keeping & Accountancy")
st.markdown(f"**Topic: Partnership Final Accounts - {topic_name} (25 Marks)**")

st.markdown("---")
student_name = st.text_input("👤 Enter Your Full Name:")
student_division = st.text_input("🏫 Enter Your Division (e.g., A, B, C):")
student_roll_no = st.text_input("🔢 Enter Your Roll No:")
student_email = st.text_input("📧 Enter Your Email ID (To Get Result on Mail):") # <-- हा बदल केला आहे
st.markdown("---")

user_answers = []

# येथे 'index=None' टाकले आहे जेणेकरून कोणताही पर्याय आधीपासून निवडलेला नसेल
for index, item in enumerate(current_quiz):
    st.markdown(f"**{item['q']}**")
    ans = st.radio("Options:", item['options'], key=f"test_{test_choice}_q_{index}", label_visibility="collapsed", index=None)
    user_answers.append(ans)
    st.markdown("<br>", unsafe_allow_html=True)

st.markdown("---")

# सबमिट बटण आणि तपासणी
if st.button("🚀 Submit Exam"):
    if student_name == "" or student_division == "" or student_roll_no == "":
        st.warning("⚠️ Please enter your Name, Division, and Roll No first!")
    elif None in user_answers:
        st.warning("⚠️ Please answer all questions before submitting!")
    else:
        score = 0
        total_questions = len(current_quiz)
        report_text = "" 
        
        for i in range(total_questions):
            if user_answers[i] == current_quiz[i]['ans']:
                score += 1
                
        # १. मुख्य निकाल दाखवणे
        st.success(f"🎉 Exam Submitted! Dear {student_name}, your Score is {score}/{total_questions}")
        
        # २. Google Sheet मध्ये डेटा पाठवणे (येथे तुमची लिंक अगदी बरोबर टाकली आहे)
        with st.spinner("Saving data to Mitradnya Excel..."):
            GOOGLE_SHEET_URL = "https://script.google.com/macros/s/AKfycbw7BoAF9_uf5pp1kM7XhpsIGb7zfMeX708BAFTjuoDLCUK4Yhpm-kbX2TevEeB_K5Yq/exec"
            
            data_to_send = {
                "name": student_name,
                "div": student_division,
                "roll": student_roll_no,
                "test": topic_name,
                "score": f"{score}/{total_questions}"
            }
            try:
                requests.get(GOOGLE_SHEET_URL, params=data_to_send)
                st.info("📊 Data successfully added to your Excel report.")
            except:
                st.error("Data saving failed, but email will be sent.")

        st.markdown("---")
        st.markdown("### 📊 तुमचा सविस्तर निकाल (Detailed Report):")
       
        # ३. लाल आणि हिरव्या रंगात उत्तरे दाखवणे
        for i in range(total_questions):
            user_ans = user_answers[i]
            correct_ans = current_quiz[i]['ans']
            question_text = current_quiz[i]['q']
            
            if user_ans == correct_ans:
                st.success(f"**{question_text}**\n\n✅ Your Ans: {user_ans}")
                report_text += f"{question_text}\n✅ Your Ans: {user_ans} (Correct)\n\n"
            else:
                st.error(f"**{question_text}**\n\n❌ Your Ans: {user_ans} \n\n🎯 Correct Ans: {correct_ans}")
                report_text += f"{question_text}\n❌ Your Ans: {user_ans} \n🎯 Correct Ans: {correct_ans}\n\n"
        
        # ४. ईमेल पाठवण्याची सिस्टीम
        with st.spinner("Saving Result..."):
            send_score_to_teacher(student_name, student_division, student_roll_no, score, total_questions, topic_name, detailed_report)
            
            if student_email != "":
                try:
                    student_msg = MIMEText(f"Dear {student_name},\n\nYour Score for {topic_name} is {score}/{total_questions}.\n\nBelow is your detailed report:\n\n{report_text}\n\nKeep Studying!\n- Mukesh Arvind Amrutkar (9130103386)")
                    student_msg['Subject'] = f"Your Online Exam Result (Mitradnya Publications) ({score}/{total_questions})"
                    student_msg['From'] = TEACHER_NAME
                    student_msg['To'] = student_email
                    
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(TEACHER_EMAIL, EMAIL_PASSWORD)
                    server.sendmail(TEACHER_EMAIL, student_email, student_msg.as_string())
                    server.quit()
                    st.info(f"📧 Your Detail Report {student_email} mail on this id.")
                except Exception as e:
                    st.error("ईमेल पाठवण्यात तांत्रिक अडचण आली.")
