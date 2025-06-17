# # import pandas as pd
# # from datetime import datetime
# # import os

# # class WearableVitalsETL:
# #     def __init__(self, input_path, output_path):
# #         self.input_path = input_path
# #         self.output_path = output_path
# #         self.data = None

# #     def extract(self):
# #         """Extract data from CSV."""
# #         try:
# #             self.data = pd.read_csv(self.input_path)
# #             print(f"[Extract] {len(self.data)} records loaded from {self.input_path}")
# #         except Exception as e:
# #             raise RuntimeError(f"[Extract] Failed to read file: {e}")

# #     def transform(self):
# #         """Clean and validate the vitals data."""
# #         if self.data is None:
# #             raise RuntimeError("[Transform] No data to transform. Run extract() first.")

# #         print("[Transform] Starting data validation and cleanup...")

# #         self.data['Timestamp'] = pd.to_datetime(self.data['Timestamp'], errors='coerce')

# #         # Drop invalid or null entries
# #         self.data.dropna(subset=[
# #             'Timestamp', 'Heart_Rate', 'BP_Systolic', 'BP_Diastolic', 'SpO2'
# #         ], inplace=True)

# #         # Convert to integer types
# #         for col in ['Heart_Rate', 'BP_Systolic', 'BP_Diastolic', 'SpO2']:
# #             self.data[col] = pd.to_numeric(self.data[col], errors='coerce').astype('Int64')

# #         # Filter out unrealistic values
# #         self.data = self.data[
# #             (self.data['Heart_Rate'].between(40, 180)) &
# #             (self.data['BP_Systolic'].between(90, 200)) &
# #             (self.data['BP_Diastolic'].between(50, 120)) &
# #             (self.data['SpO2'].between(85, 100))
# #         ]

# #         print(f"[Transform] Data cleaned. Remaining records: {len(self.data)}")

# #     def load(self):
# #         """Save the cleaned data to a new CSV file."""
# #         if self.data is None or self.data.empty:
# #             raise RuntimeError("[Load] No data available to load.")

# #         os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
# #         self.data.to_csv(self.output_path, index=False)
# #         print(f"[Load] Cleaned data saved to {self.output_path}")

# #     def run(self):
# #         """Run the ETL process."""
# #         print("🔄 Running ETL process...")
# #         self.extract()
# #         self.transform()
# #         self.load()
# #         print("✅ ETL process completed successfully.")


# # # Example usage:
# # if __name__ == "__main__":
# #     etl = WearableVitalsETL(
# #         input_path=os.path.join("data","wearable_vitals.csv"),
# #         output_path=os.path.join("cleaned_data","cleaned_wearable_vitals.csv")
# #     )
# #     etl.run()

# from db_connection import MedsecureDBConnection
# import pandas as pd
# import os
# # from datetime import datetime

# class WearableVitalsETL:
#     def __init__(self, input_path, db_connection: MedsecureDBConnection):
#         self.input_path = input_path
#         self.data = None
#         self.db = db_connection

#     def extract(self):
#         """Extract data from CSV."""
#         try:
#             self.data = pd.read_csv(self.input_path)
#             print(f"[Extract] Loaded {len(self.data)} records.")
#         except Exception as e:
#             raise RuntimeError(f"[Extract] Failed: {e}")

#     def transform(self):
#         """Clean and validate the vitals data."""
#         if self.data is None:
#             raise RuntimeError("[Transform] No data to transform.")

#         print("[Transform] Cleaning data...")
#         self.data['Timestamp'] = pd.to_datetime(self.data['Timestamp'], errors='coerce')
#         self.data.dropna(subset=['Timestamp', 'Heart_Rate', 'BP_Systolic', 'BP_Diastolic', 'SpO2'], inplace=True)

#         for col in ['Heart_Rate', 'BP_Systolic', 'BP_Diastolic', 'SpO2']:
#             self.data[col] = pd.to_numeric(self.data[col], errors='coerce').astype('Int64')

#         self.data = self.data[
#             (self.data['Heart_Rate'].between(40, 180)) &
#             (self.data['BP_Systolic'].between(90, 200)) &
#             (self.data['BP_Diastolic'].between(50, 120)) &
#             (self.data['SpO2'].between(85, 100))
#         ]

#         print(f"[Transform] Cleaned data: {len(self.data)} records.")

#     def load(self):
#         """Load cleaned data into database."""
#         if self.data is None or self.data.empty:
#             raise RuntimeError("[Load] No valid data to load.")
#         self.db.insert_vitals(self.data)

#     def run(self):
#         """Run the ETL process."""
#         print("🔄 Starting ETL process...")
#         self.extract()
#         self.transform()
#         self.load()
#         print("✅ ETL process finished.")


# # --- Example execution ---

# host = "localhost"
# user = "root"
# password = "Y@shtul9274"    
# database = "medsecure360"


# if __name__ == "__main__":
#     input_path = os.path.join("data", "wearable_vitals.csv")
#     db_connection = MedsecureDBConnection(host, user, password, database)
#     etl = WearableVitalsETL(input_path, db_connection)
#     etl.run()
