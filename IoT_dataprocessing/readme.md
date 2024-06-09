# IoT Truck Data Monitoring System

This project involves monitoring and analyzing real-time telemetry data from a fleet of delivery trucks using IoT sensors installed in each vehicle. The data helps in optimizing routes, reducing fuel consumption, proactively addressing maintenance issues, and ensuring the safety and reliability of delivery operations.

## Overview

The system comprises:
- Python script to generate random data simulating truck telemetry.
- AWS Lambda function to process incoming data and store it in DynamoDB.
- AWS CloudFormation template to set up the necessary AWS resources.

## Features

- Real-time telemetry data collection for each truck.
- API endpoint to receive truck data.
- Data stored in DynamoDB using Type 2 SCD (Slowly Changing Dimensions) schema to maintain historical data.
- Periodic data generation and transmission every minute.

## Data Schema

For each truck, the following data is collected:
- **Truck ID**: Unique identifier for the truck.
- **Timestamp**: Time of data collection.
- **GPS Location**: Latitude, Longitude, Altitude, Speed.
- **Vehicle Speed**: Real-time speed of the vehicle.
- **Engine Diagnostics**: Engine RPM, Fuel Level, Temperature, Oil Pressure, Battery Voltage.
- **Odometer Reading**: Total distance traveled.
- **Fuel Consumption**: Fuel usage over time.
- **Vehicle Health and Maintenance**: Brake status, Tire pressure, Transmission status.
- **Environmental Conditions**: Temperature, Humidity, Atmospheric Pressure.

## Project Structure

- `truck_data_api.py`: Python script to generate and send random truck data to the API.
- `app.py`: AWS Lambda function code to process and store data in DynamoDB.
- `template.yaml`: AWS CloudFormation template to create necessary AWS resources.

## Getting Started

### Prerequisites

- Python 3.x
- AWS CLI configured with appropriate permissions.
- AWS SAM CLI for deployment.
- Streamlit (Python library for building web applications)

### Setup Instructions

1. **Clone the repository**
    ```sh
    git clone https://github.com/RiyaMary1512/EcommerceApp.git
    ```

2. **Navigate to the Project Directory** 
    ```sh
    cd IoT_dataprocessing
    cd IoT-data
    ```

3. **Install the required Python packages**
    ```sh
    pip install -r requirements.txt
    ```

4. **Deploy AWS Resources**
    Use the AWS SAM CLI to deploy the CloudFormation stack which includes DynamoDB, Lambda function, and API Gateway.
    ```bash
    sam build
    sam deploy --guided
    ```
    Follow the prompts to provide stack name, AWS region, and other parameters.

5. **Generate Random Truck Data**

    The Python script `truck_data_api.py` generates random telemetry data for three trucks and sends it to the API every minute.
    ```bash
    python truck_data_api.py
    ```

### Configuration

- **DynamoDB Table**: The table `TruckData` stores the telemetry data with a composite primary key (truck_id, timestamp).
- **API Endpoint**: The API Gateway endpoint URL for data submission is output after deployment.

### Lambda Function

The Lambda function processes the incoming truck data and stores it in DynamoDB. The function is triggered by API Gateway when data is received.

### CloudFormation Template

The CloudFormation template `template.yaml` defines all the necessary AWS resources:
- DynamoDB Table
- Lambda Function
- API Gateway
- IAM Roles and Policies

## Logging and Monitoring

- **CloudWatch Logs**: All Lambda function executions are logged to AWS CloudWatch for monitoring and troubleshooting.
- **API Gateway Logs**: API Gateway request and response logs for auditing.

## Future Enhancements

- Implement real-time analytics and alerting.
- Add more detailed monitoring and reporting.
- Integrate with other AWS services for enhanced data processing.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## Acknowledgements

We'd like to express our gratitude to the following:

- **Streamlit**: For providing an intuitive framework for building web applications with Python.
- **Amazon Web Services (AWS)**: For offering robust cloud infrastructure services that power TrendAnalyzerApp.
- **Open Source Community**: For their continuous support and contributions to the world of technology.

