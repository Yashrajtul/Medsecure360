from db.db_connection import MedsecureDBConnection
from env import host, user, password, database

db_connection = MedsecureDBConnection(host, user, password, database)
# db_connection.reinitialize_database()
# db_connection.insert_patient(
#     "Yash", "Tulsyan", "yashwardhan.tulsyan@example.com",
#     "1234567890", "2220-09-24", "Male", "B+", 0, "Single"
# )


while True:
    print("\n--- MENU ---")
    print("1. Average Vitals per Department")
    print("2. Patient Count by Department")
    print("3. Anomaly Identification")
    print("4. Run a custom SQL query")
    print("0. Exit")
    choice = input("Enter your choice: ")

    if choice == '0':
        break

    elif choice == '1':
        avg_vitals = """
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
            ORDER BY d.department
            LIMIT 10;
        """
        db_connection.print_query_result(avg_vitals)

    elif choice == '2':
        pat_by_dept = """
            SELECT 
                d.department,
                COUNT(DISTINCT vi.patient_id) AS total_patients
            FROM visits vi
            JOIN doctors d ON vi.doctor_id = d.doctor_id
            GROUP BY d.department
            ORDER BY total_patients DESC
            LIMIT 10;
        """
        db_connection.print_query_result(pat_by_dept)

    elif choice == '3':
        anomly_identify = """
            SELECT 
                p.first_name, p.last_name, p.email,
                d.department,
                vt.heart_rate, vt.bp_systolic, vt.bp_diastolic, vt.spo2, vt.recorded_time
            FROM vitals vt
            JOIN visits vi ON vt.visit_id = vi.visit_id
            JOIN patients p ON vi.patient_id = p.patient_id
            JOIN doctors d ON vi.doctor_id = d.doctor_id
            WHERE 
                vt.heart_rate < 50 OR vt.heart_rate > 90 OR
                vt.bp_systolic >= 140 OR
                vt.bp_diastolic >= 90 OR
                vt.spo2 < 92
            ORDER BY vt.recorded_time DESC
            LIMIT 10;
        """
        db_connection.print_query_result(anomly_identify)

    elif choice == '4':
        user_query = input("Enter your SQL query:\n")
        db_connection.print_query_result(user_query)

    else:
        print("Invalid choice. Please try again.")




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










# def print_query_result(self, query):
#         results = self.fetch_query_result(query)
#         cursor_description = self.db_connection.cursor.description
#         columns = [desc[0] for desc in cursor_description] if cursor_description else [f"Column {i+1}" for i in range(len(results[0]))]
#         df = pd.DataFrame(results, columns=columns)               
#         print("\n", df.to_string(index=False))                   