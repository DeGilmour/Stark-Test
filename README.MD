# Stark WebHook

This project is a Flask-based web application that handles invoice creation and transfer processing.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setting Up the Environment](#setting-up-the-environment)
- [Running the Flask App](#running-the-flask-app)
- [Running Tests](#running-tests)
- [Environment Variables](#environment-variables)
## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.10
- Pip (Python package installer)

You can install the required Python packages using:

    
    pip install -r requirements.txt
    

## Setting Up the Environment

You need to set up several environment variables for the Flask app to run correctly. Create a `.env` file in the root directory of the project and add the following variables:

    
    PEM_PATH=path/to/your/pem/file.pem
    PROJECT_ID=your_project_id
    TRANSFER_PATH=path/to/transfer/details.json

    # Account vars
    TAX_ID=your_tax_id
    NAME=your_bank_name
    BANK_CODE=your_bank_code
    BRANCH_CODE=your_branch_code
    ACCOUNT_NUMBER=your_account_number
    ACCOUNT_TYPE=your_account_type
    

Make sure to replace the placeholders with your actual values.

## Running the Flask App

To start the Flask application, use the following command:

    
    python invoice.py
    

The Flask app will run on [http://0.0.0.0:8080](http://0.0.0.0:8080) by default. You can access the endpoints at:

- **Start Invoice Creation**: `POST /start-invoices`
- **Create Transfer**: `POST /create-transfer`

## Running Tests

To ensure everything is working as expected, you can run the tests using pytest. First, make sure pytest is installed:

    
    pip install pytest
    

Then, run the tests with the following command:

    
    pytest
    
## Environment Variables

Here is a description of each environment variable:

- **`PEM_PATH`**: Path to the PEM file containing the private key for Stark Bank authentication.
- **`PROJECT_ID`**: Your Stark Bank project ID.
- **`TRANSFER_PATH`**: Path to the JSON file containing transfer details.
- **`TAX_ID`**: Tax ID used for transfers.
- **`NAME`**: Name of the bank account used for transfers.
- **`BANK_CODE`**: Bank code for the transfer.
- **`BRANCH_CODE`**: Branch code for the transfer.
- **`ACCOUNT_NUMBER`**: Account number for the transfer.
- **`ACCOUNT_TYPE`**: Type of account for the transfer (e.g., checking).

Ensure all these environment variables are set correctly for both development and testing environments.
