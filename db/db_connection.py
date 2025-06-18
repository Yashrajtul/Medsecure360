import atexit
import json
import os
import mysql.connector
import pandas as pd
from mysql.connector import Error

# Database connection class
# This class handles the connection to the MySQL database and provides methods to connect and disconnect.
# It also includes error handling for connection issues.
class MedsecureDBConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self._connect()
        atexit.register(self.disconnect)  # Ensure disconnection on exit

    # def __del__(self):
    #     self.disconnect()
        
    def _connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("✅ Connected to MySQL database")
                self.cursor = self.connection.cursor()
        except Error as e:
            print(f"❌ Error connecting to database: {e}")
            # throw exception for the ui    
            raise Exception(f"Error connecting to database: {e}")
            # return None

    def disconnect(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            print("✅ Disconnected from MySQL database")
    
    # Method to create the database and tables
    def create_tables(self):
        self.create_med_source_table()
        self.create_patients_table()
        self.create_doctors_table()
        self.create_visits_table()
        self.create_medications_table()
        self.create_vitals_table()
        self.create_diagnostics_table()
            
    def create_med_source_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS med_source (
                First_Name VARCHAR(50),
                Last_Name VARCHAR(50),
                Email VARCHAR(100),
                Phone_Number VARCHAR(15),
                Date_of_Birth DATE,
                Gender ENUM('Male', 'Female', 'Other'),
                Blood_Group VARCHAR(5),
                Allergies TEXT,
                Existing_Conditions TEXT,
                Insurance_Provider VARCHAR(100),
                Address TEXT,
                Marital_Status ENUM('Single', 'Married', 'Divorced', 'Widowed'),
                Is_Insured ENUM('Yes', 'No'),

                Doctor_Name VARCHAR(100),
                Specialization VARCHAR(100),
                Department VARCHAR(100),
                Doctor_Email VARCHAR(100),
                Doctor_Phone VARCHAR(15),

                Visit_Date DATE,
                Reason TEXT,

                Medication_Name VARCHAR(100),
                Dosage VARCHAR(50),
                Start_Date DATE,
                End_Date DATE,

                Heart_Rate INT,
                BP_Systolic INT,
                BP_Diastolic INT,
                SpO2 INT,
                Recorded_Time DATETIME,

                Test_Name VARCHAR(100),
                Test_Result TEXT
            );
            
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("✅ med_source table created successfully")
        except Error as e:
            print(f"❌ Error creating med_source table: {e}")
            raise Exception(f"Error creating med_source table: {e}")

    def create_patients_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INT PRIMARY KEY AUTO_INCREMENT,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                email VARCHAR(100) UNIQUE,
                phone_number VARCHAR(20),
                date_of_birth DATE,
                gender ENUM('Male', 'Female', 'Other'),
                blood_group VARCHAR(5),
                allergies VARCHAR(100),
                existing_conditions VARCHAR(100),
                insurance_provider VARCHAR(100),
                address TEXT,
                marital_status ENUM('Single', 'Married', 'Divorced', 'Widowed'),
                is_insured BOOLEAN
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("✅ patient table created successfully")
        except Error as e:
            print(f"❌ Error creating patient table: {e}")
            raise Exception(f"Error creating patient table: {e}")
    
    def create_doctors_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS doctors (
                doctor_id INT AUTO_INCREMENT PRIMARY KEY,
                doctor_name VARCHAR(100),
                specialization VARCHAR(100),
                department VARCHAR(100),
                doctor_email VARCHAR(100),
                doctor_phone VARCHAR(20)
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("✅ doctor table created successfully")
        except Error as e:
            print(f"❌ Error creating doctor table: {e}")
            raise Exception(f"Error creating doctor table: {e}")
        
    def create_visits_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS visits (
                visit_id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT,
                doctor_id INT,
                visit_date DATE,
                reason VARCHAR(255),
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
                FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("✅ visits table created successfully")
        except Error as e:
            print(f"❌ Error creating visits table: {e}")
            raise Exception(f"Error creating visits table: {e}")
        
    def create_medications_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS medications (
                medication_id INT AUTO_INCREMENT PRIMARY KEY,
                visit_id INT,
                medication_name VARCHAR(100),
                dosage VARCHAR(50),
                start_date DATE,
                end_date DATE,
                FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("✅ medications table created successfully")
        except Error as e:
            print(f"❌ Error creating medications table: {e}")
            raise Exception(f"Error creating medications table: {e}")
    
    def create_vitals_table(self):
        try:
            query = """
            CREATE TABLE vitals (
                vital_id INT AUTO_INCREMENT PRIMARY KEY,
                visit_id INT,
                heart_rate INT,
                bp_systolic INT,
                bp_diastolic INT,
                spo2 INT,
                recorded_time DATETIME,
                FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("✅ vitals table created successfully")
        except Error as e:
            print(f"❌ Error creating vitals table: {e}")
            raise Exception(f"Error creating vitals table: {e}")
            
    def create_diagnostics_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS diagnostics (
                diagnostic_id INT AUTO_INCREMENT PRIMARY KEY,
                visit_id INT,
                test_name VARCHAR(100),
                test_result TEXT,
                FOREIGN KEY (visit_id) REFERENCES visits(visit_id)
            );
            """
            self.cursor.execute(query)
            self.connection.commit()
            print("✅ diagnostics table created successfully")
        except Error as e:
            print(f"❌ Error creating diagnostics table: {e}")
            raise Exception(f"Error creating diagnostics table: {e}")
        
    # Initialize the tables
    def load_from_csv(self, csv_file_path):
        try:
            data = pd.read_csv(csv_file_path, encoding='latin1')  # or try 'ISO-8859-1'
            # Replace NaN with None (MySQL-compatible NULL)
            data = data.where(pd.notnull(data), None)
            data = data.astype(object) 
            query = """
            INSERT IGNORE INTO med_source (
                First_Name, Last_Name, Email, Phone_Number, Date_of_Birth, Gender, Blood_Group,
                Allergies, Existing_Conditions, Insurance_Provider, Address, Marital_Status, Is_Insured,
                Doctor_Name, Specialization, Department, Doctor_Email, Doctor_Phone, Visit_Date, Reason,
                Medication_Name, Dosage, Start_Date, End_Date, Heart_Rate, BP_Systolic, BP_Diastolic,
                SpO2, Recorded_Time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # self.cursor.executemany(query, [tuple(r) for r in data.to_records(index=False)])

            records = [tuple(row) for row in data.itertuples(index=False, name=None)]
            self.cursor.executemany(query, records)

            # for index, row in data.iterrows():
            #     self.cursor.execute(query, tuple(row))
            self.connection.commit()
            print("✅ Data loaded successfully from CSV")
        except Error as e:
            print(f"❌ Error loading data from CSV: {e}")
            raise Exception(f"Error loading data from CSV: {e}")
        
    def initialize_database(self):
        self.create_tables()
        
        # Load data from CSV file
        csv_file_path = "./data/medsecure360.csv"
        self.load_from_csv(csv_file_path)
        
        # initialize other tables from the swiggy_source table
        self.initialize_other_tables()
    
    def reinitialize_database(self):
        # Drop all tables
        self.drop_tables()
        
        # Recreate tables
        self.initialize_database()
    
    def initialize_other_tables(self):
        # initialize other tables from the swiggy_source table without using loop
        insert_queries = [
            # insert into patients table
            '''
            INSERT IGNORE INTO patients(first_name, last_name, email, phone_number, date_of_birth, gender, blood_group,
                allergies, existing_conditions, insurance_provider, address, marital_status, is_insured
            ) 
            SELECT DISTINCT
                First_Name, Last_Name, Email, Phone_Number, Date_of_Birth, Gender, Blood_Group,
                Allergies, Existing_Conditions, Insurance_Provider, Address, Marital_Status,
                CASE WHEN Is_Insured = 'Yes' THEN TRUE ELSE FALSE END
            FROM med_source;
            ''',
            
            # insert into doctors table
            '''
            INSERT IGNORE INTO doctors (
                doctor_name, specialization, department, doctor_email, doctor_phone
            )
            SELECT DISTINCT
                Doctor_Name, Specialization, Department, Doctor_Email, Doctor_Phone
            FROM med_source;
            ''',
            
            # insert into visits table
            '''
            INSERT IGNORE INTO visits (
                patient_id, doctor_id, visit_date, reason
            )
            SELECT
                p.patient_id,
                d.doctor_id,
                m.Visit_Date,
                m.Reason
            FROM med_source m
            JOIN patients p ON m.Email = p.email
            JOIN doctors d ON m.Doctor_Email = d.doctor_email;
            ''',
            
            # insert into medications table
            '''
            INSERT IGNORE INTO medications (
                visit_id, medication_name, dosage, start_date, end_date
            )
            SELECT
                v.visit_id,
                m.Medication_Name,
                m.Dosage,
                m.Start_Date,
                m.End_Date
            FROM med_source m
            JOIN patients p ON m.Email = p.email
            JOIN doctors d ON m.Doctor_Email = d.doctor_email
            JOIN visits v ON v.patient_id = p.patient_id AND v.doctor_id = d.doctor_id AND v.visit_date = m.Visit_Date;
            ''',
            
            # insert into vitals table
            '''
            INSERT IGNORE INTO vitals (
                visit_id, heart_rate, bp_systolic, bp_diastolic, spo2, recorded_time
            )
            SELECT
                v.visit_id,
                m.Heart_Rate,
                m.BP_Systolic,
                m.BP_Diastolic,
                m.SpO2,
                m.Recorded_Time
            FROM med_source m
            JOIN patients p ON m.Email = p.email
            JOIN doctors d ON m.Doctor_Email = d.doctor_email
            JOIN visits v ON v.patient_id = p.patient_id AND v.doctor_id = d.doctor_id AND v.visit_date = m.Visit_Date;
            '''
            # ,
            
            # # insert into diagnostics
            # '''
            # INSERT IGNORE INTO diagnostics (
            #     visit_id, test_name, test_result
            # )
            # SELECT
            #     v.visit_id,
            #     m.Test_Name,
            #     m.Test_Result
            # FROM med_source m
            # JOIN patients p ON m.Email = p.email
            # JOIN doctors d ON m.Doctor_Email = d.doctor_email
            # JOIN visits v ON v.patient_id = p.patient_id AND v.doctor_id = d.doctor_id AND v.visit_date = m.Visit_Date;
            # '''
        ]
        try:
            for query in insert_queries:
                self.cursor.execute(query)
                self.connection.commit()
            print("✅ Other tables initialized successfully")
            
        except Error as e:
            print(f"❌ Error initializing other tables: {e}")     
            raise Exception(f"Error initializing other tables: {e}")       
        
    # Drop all tables in the database
    def drop_tables(self):
        try:
            tables = [
                "med_source", "medications", "diagnostics", "vitals", "visits", "patients", "doctors", "medications"
            ]
            for table in tables:
                query = f"DROP TABLE IF EXISTS {table}"
                self.cursor.execute(query)
            self.connection.commit()
            print("✅ All tables dropped successfully")
        except Error as e:
            print(f"❌ Error dropping tables: {e}")
            raise Exception(f"Error dropping tables: {e}")
        
    def insert_diagnostics_from_json(self, json_path):
        try:
            with open(json_path, "r") as f:
                diagnotics_data = json.load(f)
            
            for entry in diagnotics_data:
                patient_email = entry["patient_email"]
                doctor_email = entry["doctor_email"]
                visit_date = entry["visit_date"]
                diagnostics = entry["diagnostics"]
                
                # Get visit_id using patient_email, doctor_email, visit_date
                self.cursor.execute("""
                    SELECT v.visit_id
                    FROM visits v
                    JOIN patients p ON v.patient_id = p.patient_id
                    JOIN doctors d ON v.doctor_id = d.doctor_id
                    WHERE p.email = %s AND d.doctor_email = %s AND v.visit_date = %s
                """, (patient_email, doctor_email, visit_date))
                result = self.cursor.fetchone()
                
                if not result:
                    print(f"Visit not found for {patient_email}, {doctor_email}, {visit_date}")
                    continue

                visit_id = result[0]

                # Insert diagnostics
                for diag in diagnostics:
                    test_name = diag["test_name"]
                    test_result = diag["test_result"]
                    self.cursor.execute("""
                        INSERT INTO diagnostics (visit_id, test_name, test_result)
                        VALUES (%s, %s, %s)
                    """, (visit_id, test_name, test_result))
        
            self.connection.commit()
            print("✅ Diagnostics inserted successfully.")
        except Error as e:
            print(f"❌ Error inserting diagnostics data: {e}")
        
    # def insert_vitals(self, df: pd.DataFrame):
    #     df = df.astype(object) 
    #     records = [tuple(row) for row in df.itertuples(index=False, name=None)]
    #     try:
    #         query = '''
    #             INSERT INTO wearable_vitals (Patient_ID, Timestamp, Heart_Rate, BP_Systolic, BP_Diastolic, SpO2)
    #             VALUES (?, ?, ?, ?, ?, ?)
    #         '''
    #         self.cursor.executemany(query, records)
    #         self.connection.commit()
    #         print(f"✅ [DB] Inserted {len(df)} records into the vitals table.")
    #     except Error as e:
    #         print(f"Error inserting vitals: {e}")
    #     pass
        
    # Select query methods
    def fetch_table_names(self):
        query = "SHOW TABLES"
        try:
            self.cursor.execute(query)
            tables = self.cursor.fetchall()
            return [table[0] for table in tables]
        except Error as e:
            print(f"❌ Error fetching table names: {e}")
            raise Exception(f"Error fetching table names: {e}")
            return None
        
    def fetch_table_columns(self, table_name): 
        query = f"SHOW COLUMNS FROM {table_name}"
        try:
            self.cursor.execute(query)
            columns = self.cursor.fetchall()
            return [column[0] for column in columns]
        except Error as e:
            print(f"❌ Error fetching columns for table {table_name}: {e}")
            raise Exception(f"Error fetching columns for table {table_name}: {e}")
            return None
        
    def fetch_table_description(self, table_name):
        query = f"DESCRIBE {table_name}"
        try:
            self.cursor.execute(query)
            description = self.cursor.fetchall()
            return description
        except Error as e:
            print(f"❌ Error describing table {table_name}: {e}")
            raise Exception(f"Error describing table {table_name}: {e}")
            return None
        
    def insert_patient(self, first_name, last_name, email, phone_number, dob, gender, blood_group, is_insured, marital_status="Single",
                    allergies=None, existing_conditions=None, insurance_provider=None, address=None):
        # Start building the query
        query = """INSERT INTO patients (first_name, last_name, email, phone_number, date_of_birth, gender, blood_group, is_insured, marital_status"""
        value_query = ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s"
        values = [first_name, last_name, email, phone_number, dob, gender, blood_group, is_insured, marital_status]

        if allergies is not None:
            query += ", allergies"
            value_query += ", %s"
            values.append(allergies)

        if existing_conditions is not None:
            query += ", existing_conditions"
            value_query += ", %s"
            values.append(existing_conditions)

        if insurance_provider is not None:
            query += ", insurance_provider"
            value_query += ", %s"
            values.append(insurance_provider)

        if address is not None:
            query += ", address"
            value_query += ", %s"
            values.append(address)

        query += value_query + ");"

        # Debug: print the final query and values
        # print("Final SQL Query:", query)
        # print("Values:", values)
        # print("Number of placeholders:", query.count('%s'))
        # print("Number of values:", len(values))

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("✅ Data inserted into patients table successfully")
        except Error as e:
            print(f"❌ Error inserting data into patients table: {e}")
            raise Exception(f"Error inserting data into patients table: {e}")

    def fetch_table_data(self, table_name, columns=None, where_clause=None, group_by=None, having=None, order_by=None, limit=None, offset=None):
        query = f"SELECT {', '.join(columns) if columns else '*'} FROM {table_name}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        if group_by:
            query += f" GROUP BY {group_by}"
        
        if having:
            query += f" HAVING {having}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" LIMIT {limit}"
        
        if offset:
            query += f" OFFSET {offset}"
        
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"❌ Error executing select query: {e}")
            raise Exception(f"Error executing select query: {e}")
            return None
        
    def fetch_query_result(self, query: str, values: tuple=None):
        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"❌ Error executing query: {e}")
            raise Exception(f"Error executing query: {e}")
            return None
        # try:
        #     self.cursor.execute(query)
        #     result = self.cursor.fetchall()
        #     columns = [desc[0] for desc in self.cursor.description]  # Get column names
        #     df = pd.DataFrame(result, columns=columns)               # Convert to DataFrame
        #     print("\n", df.to_string(index=False))                   # Print nicely
        #     return df
        # except Error as e:
        #     print(f"Error executing query: {e}")
        #     raise Exception(f"Error executing query: {e}")
        
    def print_query_result(self, query):
        result = self.fetch_query_result(query)
        columns = [desc[0] for desc in self.cursor.description]
        df = pd.DataFrame(result, columns=columns)
        print("\n", df.to_string(index=False)) 
        
    def print_output(self, query=None, table_name=None, columns=None, where_clause=None, group_by=None, having=None, order_by=None, limit=None, offset=None):
        if query:
            result = self.fetch_query_result(query)
        elif table_name:
            result = self.fetch_table_data(table_name, columns, where_clause, group_by, having, order_by, limit, offset)
        else:
            print("No query or table name provided")
            return
        
        if result:
            columns = [desc[0] for desc in self.cursor.description]
            df = pd.DataFrame(result, columns=columns)
            print("\n", df.to_string(index=False)) 
        else:
            print("No data found or error executing query")
            
    def print_results(self, results):
        if results:
            for row in results:
                print(row)
        else:
            print("No data found or error executing query")
        

