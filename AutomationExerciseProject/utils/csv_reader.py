import csv
import os
from typing import List, Dict

def read_login_data_csv(file_path: str) -> List[Dict[str, str]]:
    """
    Reads login credentials and expected results from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        List[Dict[str, str]]: List of dictionaries containing email, password, and expected_result.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found at path: {file_path}")
        
    required_columns = {"email", "password", "expected_result"}
    login_data = []
    
    with open(file_path, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        # Check if CSV has required headers
        fieldnames = set(reader.fieldnames or [])
        if not required_columns.issubset(fieldnames):
            missing = required_columns - fieldnames
            raise ValueError(f"CSV file is missing required columns: {missing}")
            
        for row in reader:
            # Skip empty or whitespace-only rows
            if not row or not any(row.values()):
                continue
                
            email = row.get("email", "").strip()
            password = row.get("password", "").strip()
            expected_result = row.get("expected_result", "").strip()
            
            if email and password and expected_result:
                login_data.append({
                    "email": email,
                    "password": password,
                    "expected_result": expected_result
                })
                
    return login_data
