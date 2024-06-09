import random
import requests
import time
import json
import logging
from datetime import datetime
from decimal import Decimal

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

truck_ids = ["TRK001", "TRK002", "TRK003"]

def convert_floats_to_strings(data):
    if isinstance(data, dict):
        return {k: convert_floats_to_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_floats_to_strings(item) for item in data]
    elif isinstance(data, float):
        return format(Decimal(data), '.10f')
    else:
        return data

def generate_random_data():
    data = {"trucks": []}
    current_timestamp = datetime.now().isoformat()
    for truck_id in truck_ids:
        truck_data = {
            "truck_id": truck_id,
            "timestamp": current_timestamp, 
            "gps_location": {
                "latitude": round(random.uniform(-90.0, 90.0), 6),
                "longitude": round(random.uniform(-180.0, 180.0), 6),
                "altitude": round(random.uniform(0, 1000), 1),
                "speed": round(random.uniform(0, 120), 1)
            },
            "vehicle_speed": round(random.uniform(0, 120), 1),
            "engine_diagnostics": {
                "engine_rpm": random.randint(500, 5000),
                "fuel_level": round(random.uniform(0, 100), 1),
                "temperature": round(random.uniform(-30, 120), 1),
                "oil_pressure": round(random.uniform(20, 80), 1),
                "battery_voltage": round(random.uniform(12, 15), 1)
            },
            "odometer_reading": round(random.uniform(0, 200000), 1),
            "fuel_consumption": round(random.uniform(5, 30), 1),
            "vehicle_health_and_maintenance": {
                "brake_status": random.choice(["Good", "Needs Inspection", "Replace"]),
                "tire_pressure": {
                    "front_left": round(random.uniform(30, 40), 1),
                    "front_right": round(random.uniform(30, 40), 1),
                    "rear_left": round(random.uniform(30, 40), 1),
                    "rear_right": round(random.uniform(30, 40), 1)
                },
                "transmission_status": random.choice(["Operational", "Needs Maintenance", "Faulty"])
            },
            "environmental_conditions": {
                "temperature": round(random.uniform(-50, 50), 1),
                "humidity": round(random.uniform(0, 100), 1),
                "atmospheric_pressure": round(random.uniform(950, 1050), 2)
            }
        }
        data["trucks"].append(truck_data)
    logging.debug(f"Generated data: {json.dumps(data, indent=2)}")
    return data

def send_data_to_api(data):
    url = "https://g7ypno4xsd.execute-api.ap-south-1.amazonaws.com/Prod/trucks"
    headers = {'Content-Type': 'application/json'}
    try:
        data_with_strings = convert_floats_to_strings(data)
        response = requests.post(url, data=json.dumps(data_with_strings), headers=headers)
        logging.info(f"Sent data to API: {data_with_strings}")
        logging.info(f"API Response: Status Code: {response.status_code}, Response Text: {response.text}")
        return response.status_code, response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error sending data to API: {e}")
        return None, str(e)

def main():
    while True:
        logging.info("Generating random data for trucks.")
        data = generate_random_data()
        logging.info("Sending data to API.")
        status_code, response_text = send_data_to_api(data)
        logging.info(f"API Response - Status Code: {status_code}, Response: {response_text}")
        logging.info("Sleeping for 60 seconds before next data generation.")
        time.sleep(60)

if __name__ == "__main__":
    main()
