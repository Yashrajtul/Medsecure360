from db_connection import MedsecureDBConnection
import pandas as pd
import os, sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from env import host, user, password, database


class WearableVitalsETL:
    def __init__(self, input_path, db_connection: MedsecureDBConnection):
        self.input_path = input_path
        self.data = None
        self.db = db_connection

    def extract(self):
        """Extract data from CSV."""
        try:
            self.data = pd.read_csv(self.input_path)
            print(f"[Extract] Loaded {len(self.data)} records.")
        except Exception as e:
            raise RuntimeError(f"[Extract] Failed: {e}")

    def transform(self):
        """Clean and validate the vitals data."""
        if self.data is None:
            raise RuntimeError("[Transform] No data to transform.")

        print("[Transform] Cleaning data...")

        # Rename for consistency
        self.data.rename(columns={
            "Patient_Email": "patient_email",
            "Timestamp": "recorded_time",
            "Heart_Rate": "heart_rate",
            "BP_Systolic": "bp_systolic",
            "BP_Diastolic": "bp_diastolic",
            "SpO2": "spo2"
        }, inplace=True)

        self.data['recorded_time'] = pd.to_datetime(self.data['recorded_time'], errors='coerce')
        self.data.dropna(subset=['patient_email', 'recorded_time', 'heart_rate', 'bp_systolic', 'bp_diastolic', 'spo2'], inplace=True)

        for col in ['heart_rate', 'bp_systolic', 'bp_diastolic', 'spo2']:
            self.data[col] = pd.to_numeric(self.data[col], errors='coerce').astype('Int64')

        self.data = self.data[
            (self.data['heart_rate'].between(40, 180)) &
            (self.data['bp_systolic'].between(90, 200)) &
            (self.data['bp_diastolic'].between(50, 120)) &
            (self.data['spo2'].between(85, 100))
        ]

        print(f"[Transform] Cleaned data: {len(self.data)} records.")

    def get_latest_visit_id(self, patient_email):
        """Fetch the latest visit_id for the given patient_email."""
        query = """
            SELECT v.visit_id
            FROM visits v
            JOIN patients p ON v.patient_id = p.patient_id
            WHERE p.email = %s
            ORDER BY v.visit_date DESC
            LIMIT 1
        """
        result = self.db.fetch_query_result(query, (patient_email,))
        return result[0][0] if result else None

    def load(self):
        """Load cleaned data into the database."""
        if self.data is None or self.data.empty:
            raise RuntimeError("[Load] No valid data to load.")

        insert_query = """
        INSERT INTO vitals (visit_id, heart_rate, bp_systolic, bp_diastolic, spo2, recorded_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = []
        skipped = 0

        for _, row in self.data.iterrows():
            visit_id = self.get_latest_visit_id(row['patient_email'])
            if not visit_id:
                print(f"[Load] Skipping {row['patient_email']}: No visit found.")
                skipped += 1
                continue
            values.append((
                visit_id,
                row['heart_rate'],
                row['bp_systolic'],
                row['bp_diastolic'],
                row['spo2'],
                row['recorded_time'].strftime('%Y-%m-%d %H:%M:%S')
            ))

        try:
            if values:
                self.db.cursor.executemany(insert_query, values)
                self.db.connection.commit()
                print(f"[Load] Inserted {len(values)} records.")
            else:
                print("[Load] No records inserted.")
        except Exception as e:
            self.db.connection.rollback()
            raise RuntimeError(f"[Load] Failed to insert data: {e}")

        if skipped:
            print(f"[Load] Skipped {skipped} records due to missing visit info.")

    def run(self):
        """Run the ETL pipeline."""
        print("🔄 Starting ETL process...")
        self.extract()
        self.transform()
        self.load()
        print("✅ ETL process finished.")


if __name__ == "__main__":
    input_path = os.path.join("data", "wearable_vitals.csv")
    db_connection = MedsecureDBConnection(host, user, password, database)
    etl = WearableVitalsETL(input_path, db_connection)
    etl.run()
