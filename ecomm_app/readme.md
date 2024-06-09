# E-commerce Web Application

This project is an e-commerce web application that tracks user interactions with various products and stores clickstream data in AWS DynamoDB. It utilizes AWS Kinesis for data streaming and AWS Lambda for processing the data.

## Table of Contents
- [Introduction](#introduction)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [AWS Configuration](#aws-configuration)
  - [Deploying the Application](#deploying-the-application)
- [Usage](#usage)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Introduction

This application allows users to browse and view details of various products. It tracks the click counts for each product and identifies the most viewed product. The tracked data is sent to an AWS Kinesis stream, processed by a Lambda function, and stored in DynamoDB.

## Architecture

The architecture consists of the following components:
- **Streamlit App**: Front-end application where users interact with the products.
- **AWS Kinesis**: Data stream service used to collect and process clickstream data in real-time.
- **AWS Lambda**: Serverless compute service that processes data from Kinesis and updates DynamoDB.
- **AWS DynamoDB**: NoSQL database used to store the product click counts.

## Setup Instructions

### Prerequisites

Ensure you have the following tools installed:
- Python 3.x
- AWS CLI
- AWS SAM CLI
- Streamlit (Python library for building web applications)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/RiyaMary1512/EcommerceApp.git
    ```
2. Navigate to the Project Directory: 

All the code relevant to this ecommerce app & integration with AWS services are found inside ecomm_app folder.

Once cloned, navigate to the project directory:
    ```sh
    cd ecomm_app
    cd ecomm_web-app
    ```
3. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

### AWS Configuration

To deploy and run TrendAnalyzerApp, you'll need an AWS account and appropriate permissions. Here's what you need to do:

1. **Create an AWS Account**: If you don't already have one, sign up for an AWS account at [aws.amazon.com](https://aws.amazon.com).
2. **Configure AWS CLI**: Set up the AWS Command Line Interface (CLI) with your AWS credentials:
    ```bash
    aws configure
    ```
3. **Configure AWS SAM**: Set up the AWS Serverless Application Model Command Line Interface (AWS SAM CLI) using below command:
    ```bash
    sam init
    ```

### Deploying the Application

Ready to deploy Ecommerce App? Follow these steps to deploy the application:

1. **Build the Code**: The necessary AWS configurations have been given in 'template.yaml' file. Navigate to ecomm_web-app directory inside ecomm_app folder & build the code using sam:
    ```bash
    sam build
    ```
2. **Deploy the Code**: Once the code is build successfully, deploy the code using sam. Make your own choices for the prompted questions during guided deployment:
    ```bash
    sam deploy --guided
    ```

3. **Deploy Streamlit Application:**
   - Ensure you have Streamlit installed: `pip install streamlit`
   - Navigate back to ecomm_app directory.
   - Images required for the app UI is sstored in folder named 'images'. 
   - Run the Streamlit app:
     ```sh
     streamlit run streamlit_ecomm.py
     ```

## Usage

- **Home Page**: Displays a list of products. Users can click the "View Details" button to see more information about a product. Clicking this button also increments the product's click count and sends this data to AWS Kinesis.
- **Most Viewed Products**: Clicking this button fetches and displays the product with the highest click count from DynamoDB.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## Acknowledgements

We'd like to express our gratitude to the following:

- **Streamlit**: For providing an intuitive framework for building web applications with Python.
- **Amazon Web Services (AWS)**: For offering robust cloud infrastructure services that power TrendAnalyzerApp.
- **Open Source Community**: For their continuous support and contributions to the world of technology.
