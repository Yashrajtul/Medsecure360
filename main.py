from db.db_connection import MedsecureDBConnection
from env import host, user, password, database

db_connection = MedsecureDBConnection(host, user, password, database)
db_connection.reinitialize_database()
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
            ORDER BY d.department;
        """
        result = db_connection.fetch_query_result(avg_vitals)
        print(result)

    elif choice == '2':
        pat_by_dept = """
            SELECT 
                d.department,
                COUNT(DISTINCT vi.patient_id) AS total_patients
            FROM visits vi
            JOIN doctors d ON vi.doctor_id = d.doctor_id
            GROUP BY d.department
            ORDER BY total_patients DESC;
        """
        result = db_connection.fetch_query_result(pat_by_dept)
        print(result)

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
            ORDER BY vt.recorded_time DESC;
        """
        result = db_connection.fetch_query_result(anomly_identify)
        print(result)

    elif choice == '4':
        user_query = input("Enter your SQL query:\n")
        result = db_connection.fetch_query_result(user_query)
        print(result)

    else:
        print("Invalid choice. Please try again.")


