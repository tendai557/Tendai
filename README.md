🧾 Automated Payroll Processing System
This Python script automates the generation and email distribution of employee payslips. It reads data from an Excel file, generates personalized PDF payslips, and sends them to each employee via email.

📦 Features
✅ Reads employee data from an Excel sheet

✅ Calculates net salary using basic salary, allowances, and deductions

✅ Generates professional-looking PDF payslips using FPDF

✅ Sends payslips via email to each employee using smtplib

✅ Prints detailed logs for monitoring the process

🛠 Requirements
Install the dependencies using pip:

bash
Copy
Edit
pip install pandas fpdf openpyxl
📁 File Structure
bash
Copy
Edit
.
├── employees.xlsx         # Excel file with employee data
├── payslips/              # Folder where PDFs will be saved
├── payroll_script.py      # Main script
└── README.md              # This file
📄 Excel Format (employees.xlsx)
The Excel file must include the following columns:

Employee ID

Name

Email

Basic Salary

Allowances

Deductions

Example:

Employee ID	Name	Email	Basic Salary	Allowances	Deductions
101	John Doe	john@example.com	1000	200	100
⚙️ Configuration
Edit these values at the top of the script:

python
Copy
Edit
SENDER_EMAIL = "your gmail.com"       # Replace with your Gmail address
EMAIL_PASSWORD = "your password"      # Use an App Password for Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
⚠️ Important: Use a Gmail App Password instead of your regular password.

🚀 How to Run
Place the Excel file (employees.xlsx) in the same directory and run:

bash
Copy
Edit
python payroll_script.py
📬 Email Output
Each employee will receive an email with a subject line:

Your Payslip for This Month

And a PDF attachment named like: 101_payslip.pdf

🧯 Error Handling
The script includes basic error handling for:

Reading Excel files

PDF generation

Email sending

Errors are printed to the console, and a final summary report is shown at the end.

📌 Notes
You can customize the layout of the payslip inside generate_payslip_pdf().

Modify email content and formatting in the send_email() function.

All generated payslips are saved in a folder named payslips/.

📝 License
This project is open-source and free to use. Attribution appreciated. 🙌


