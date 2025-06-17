from db.db_connection import MedsecureDBConnection
from env import host, user, password, database

# host = "localhost"
# user = "root"
# password = "Y@shtul9274"    
# database = "medsecure360"

reports = [
    {
        "desc": "Average Vitals per Department",
        "query": """
            SELECT 
            d.department,
            ROUND(AVG(vt.heart_rate), 1) AS avg_heart_rate,
            ROUND(AVG(vt.bp_systolic), 1) AS avg_bp_systolic,
            ROUND(AVG(vt.bp_diastolic), 1) AS avg_bp_diastolic,
            ROUND(AVG(vt.spo2), 1) AS avg_spo2
        FROM vitals vt
        JOIN visits vi ON vt.visit_id = vi.visit_id
        JOIN doctors d ON vi.doctor_id = d.doctor_id
        GROUP BY d.department
        ORDER BY d.department;
        """
    },
    {
        "desc": "Patient Count by Department",
        "query": """
            SELECT 
            d.department,
            COUNT(DISTINCT vi.patient_id) AS total_patients
        FROM visits vi
        JOIN doctors d ON vi.doctor_id = d.doctor_id
        GROUP BY d.department
        ORDER BY total_patients DESC;
        """
    },
    {
        "desc": "Anomaly Identification Heart rate < 50 or > 120 -- Systolic BP > 140 -- Diastolic BP > 90 -- SpO₂ < 92",
        "query": """
            SELECT 
            p.first_name,p.last_name,p.email,
            d.department,
            vt.heart_rate,vt.bp_systolic,vt.bp_diastolic,vt.spo2,vt.recorded_time
        FROM vitals vt
        JOIN visits vi ON vt.visit_id = vi.visit_id
        JOIN patients p ON vi.patient_id = p.patient_id
        JOIN doctors d ON vi.doctor_id = d.doctor_id
        WHERE 
            vt.heart_rate < 50 OR vt.heart_rate > 90 OR
            vt.bp_systolic >= 140 OR
            vt.bp_diastolic >= 90 OR
            vt.spo2 < 92
        ORDER BY vt.recorded_time DESC;
        """
    },
]

db_connection = MedsecureDBConnection(host, user, password, database)
db_connection.reinitialize_database()
db_connection.insert_patient(
    "Yash", "Tulsyan", "yashwardhan.tulsyan@example.com",
    "1234567890", "2220-09-24", "Male", "B+", 0, "Single"
)




# for report in reports:
#     print(report["desc"])
#     db_connection.print_output(query=report["query"])
#     print()

# while True:
#     print("Welcome to Medsecure360")
#     print("="*30)
#     print("\nChoose option:")
#     print("1. Enter patients data")
#     print("9. Exit")
#     option = input("Enter your option: ")
    
#     if option == 1:
#         print("Enter patients details: ")
#         first_name = input("Enter first name* :")
#         last_name = input("Enter last name* :")
#         email = input("Enter email* :")
#         phone_number = input("Enter phone number* :")
#         dob = input("Enter date of birth (yyyy-mm-dd)* :")
#         gender = input("Enter gender (m/f)* :")
#         blood_group = input("Enter blood group* :")
#         is_insured = input("Are You insured (y/n)* :")
#         if is_insured in ("Y", "y"):
#             insurance_provider = input("Enter your insurance provider* :")
        
        
#         allergies=None, existing_conditions=None, insurance_provider=None
#     break


