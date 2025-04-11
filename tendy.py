import pandas as pd
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os

# ================== HARDCODED SETTINGS (REPLACE THESE!) ==================
SENDER_EMAIL = "tendaitasha557@gmail.com"     # Replace with your email
EMAIL_PASSWORD = "lfcxefcevwiskrpf"      # Replace with app password
SMTP_SERVER = "smtp.gmail.com"            # For Gmail
SMTP_PORT = 465                           # Gmail's SSL port
# ========================================================================

def read_employee_data(filepath):
    """Reads employee data from an Excel file."""
    print(f"\nReading Excel file: {filepath}")
    try:
        df = pd.read_excel(filepath)
        print(f"Successfully read Excel data, Found {len(df)} employees")
        return df
    except Exception as e:
        print(f"Failed to read Excel file: {str(e)}")
        return None

def calculate_net_salary(basic, allowances, deductions):
    """Calculate the net salary."""
    net = basic + allowances - deductions
    print(f"Salary Calculation: {basic} + {allowances} - {deductions} = {net}")
    return net

def generate_payslip_pdf(employee):
    """Generate a PDF payslip for an employee with improved layout."""
    print(f"\nProcessing employee: {employee['Name']} (ID: {employee['Employee ID']})")
    
    # Debug print before PDF generation
    print(f"Basic Salary: {employee['Basic Salary']}, Allowances: {employee['Allowances']}, Deductions: {employee['Deductions']}")
    
    pdf = FPDF()
    pdf.add_page()
    
    # Set fonts
    pdf.set_font("Arial", size=12)
    
    # Header: Company name and logo (if you have a logo, you can add it as well)
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, txt="Company Payroll System", ln=True, align="C")
    pdf.set_font("Arial", style='I', size=10)
    pdf.cell(200, 10, txt="------------------------------------------------------------", ln=True, align="C")
    
    # Employee Name and ID
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt=f"Payslip for: {employee['Name']}", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Employee ID: {employee['Employee ID']}", ln=True, align="L")
    pdf.cell(200, 10, ln=True)  # Blank line
    
    # Salary Details Section
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, txt="Salary Details", ln=True, align="L")
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Basic Salary:   ${employee['Basic Salary']}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Allowances:     ${employee['Allowances']}", ln=True, align="L")
    pdf.cell(200, 10, txt=f"Deductions:     ${employee['Deductions']}", ln=True, align="L")
    
    # Calculate and display net salary
    net_salary = calculate_net_salary(
        employee['Basic Salary'],
        employee['Allowances'],
        employee['Deductions']
    )
    pdf.cell(200, 10, txt=f"Net Salary:     ${net_salary}", ln=True, align="L")
    
    # Aesthetic Line for separation
    pdf.cell(200, 10, txt="------------------------------------------------------------", ln=True, align="L")
    
    # Footer Section: Company info and contact
    pdf.cell(200, 10, ln=True)  # Blank line
    pdf.set_font("Arial", size=8)
    pdf.cell(200, 10, txt="For queries, please contact HR at hr@company.com", ln=True, align="C")
    pdf.cell(200, 10, txt="Company Address: 123 Main St, City, Country", ln=True, align="C")
    
    # Save PDF
    os.makedirs("payslips", exist_ok=True)
    output_path = f"payslips/{employee['Employee ID']}_payslip.pdf"
    pdf.output(output_path)
    print(f"PDF generated at: {output_path}")
    return output_path

def send_email(recipient_email, pdf_path):
    """Sends an email with the payslip attachment."""
    print(f"\nAttempting to send email to: {recipient_email}")
    try:
        msg = EmailMessage()
        msg['Subject'] = "Your Payslip for This Month"
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        
        msg.set_content("""Dear Employee,\n\nPlease find your payslip attached.\n\nBest Regards,\nHR Team""")
        
        # Attach PDF
        with open(pdf_path, 'rb') as f:
            msg.add_attachment(f.read(), 
                             maintype='application', 
                             subtype='pdf', 
                             filename=os.path.basename(pdf_path))
        
        # Send email
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print(f"Successfully sent email to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"Email sending failed for {recipient_email}: {str(e)}")
        return False

def main():
    """Main function to process employee data and send payslips."""
    print("\nStarting payroll processing system")
    print("-------------------------------------")
    
    excel_file = "employees.xlsx"
    data = read_employee_data(excel_file)
    
    if data is None:
        print("No data found. Exiting program.")
        return
    
    total_employees = len(data)
    success_count = 0
    failure_count = 0
    
    print("\nProcessing employees:")
    for index, row in data.iterrows():
        try:
            print(f"\nProcessing employee #{index+1}/{total_employees}")
            pdf_path = generate_payslip_pdf(row)
            
            # Debug: Print PDF path
            print(f"PDF path: {pdf_path}")
            
            # Send email
            if send_email(row["Email"], pdf_path):
                success_count += 1
            else:
                failure_count += 1
                
        except Exception as e:
            print(f"Error processing Employee {row['Employee ID']}: {str(e)}")
            failure_count += 1
    
    print("\nFinal Report:")
    print(f"Payslips sent: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Total processed: {total_employees}")

if __name__ == "__main__":
    main()
    print("\nProgram execution completed")
