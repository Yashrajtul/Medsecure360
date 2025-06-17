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
# for report in reports:
#     print(report["desc"])
#     db_connection.print_output(query=report["query"])
#     print()