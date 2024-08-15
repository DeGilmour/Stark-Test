from flask import Flask, request, jsonify
import threading
import time
from datetime import datetime, timedelta
import random as r
import starkbank
from cpf_generator import CPF
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

def get_vars():
	"""Retrieve environment variables."""
	pem_file_path = os.environ.get("PEM_PATH")
	project_id = os.environ.get("PROJECT_ID")
	transfer_path = os.environ.get("TRANSFER_PATH")
	
	# Account vars
	tax_id = os.environ.get("TAX_ID")  
	name = os.environ.get("NAME")
	bank_code = os.environ.get("BANK_CODE")
	branch_code = os.environ.get("BRANCH_CODE")
	account_number = os.environ.get("ACCOUNT_NUMBER")
	account_type = os.environ.get("ACCOUNT_TYPE")

	if not pem_file_path or not project_id or not transfer_path:
		raise Exception("Required environment variables are missing")

	if not tax_id or not name or not bank_code or not branch_code or not account_number or not account_type:
		raise Exception("Required account environment variables are missing")

	with open(pem_file_path, 'r') as pem_file:
		pem_data = pem_file.read()

	return {
		"pem_data": pem_data,
		"project_id": project_id,
		"transfer_path": transfer_path,
		"tax_id": tax_id,
		"name": name,
		"bank_code": bank_code,
		"branch_code": branch_code,
		"account_number": account_number,
		"account_type": account_type
	}


app = Flask(__name__)
app.config["DEBUG"] = True
env_vars = get_vars()

# Stark Bank user
user = starkbank.Project(
	environment="sandbox",
	id=env_vars['project_id'],
	private_key=env_vars['pem_data']
)

starkbank.user = user

@app.route('/start-invoices', methods=['POST'])
def create_invoices():
    """Creates a batch of invoices."""
    try:
        for _ in range(r.randint(8, 13)):
            amount = r.randint(10000, 50000)
            due_date = datetime.now() + timedelta(days=1)
            expiration = 2592000
            fine = 2.0
            interest = 1.0
            descriptions = [{"key": "Service", "value": "Random Service"}]
            discounts = []
            tags = ["Random Tag"]
            rules = []
            splits = []

            invoice = starkbank.Invoice(
                amount=amount,
                due=due_date,
                expiration=expiration,
                fine=fine,
                interest=interest,
                descriptions=descriptions,
                discounts=discounts,
                tags=tags,
                rules=rules,
                splits=splits,
                name=f"Random Person: {r.randint(1, 10000)}",
                tax_id=CPF.generate()
            )

            created_invoice = starkbank.invoice.create([invoice])
            logging.info(f'Created invoice: {created_invoice}')
        return jsonify({'status': 'success', 'message': 'Invoice creation started'}), 200

    except Exception as e:
        logging.error(f'Error creating invoices: {e}')


@app.route('/create-transfer', methods=['POST'])
def create_transfers():
	"""Creates the Transfers"""
	try:
		event = request.json.get("event")
		if not event:
			return jsonify({'status': 'error', 'message': "No event"}), 400

		if event['subscription'] == 'invoice':
			data = event['log'].get('invoice', {})
			amount_received = data.get('amount')
			fee = data.get('fee', 0) 

			if not amount_received:
				return jsonify({'status': 'error', 'message': "No Amount"}), 400

			transfer = starkbank.Transfer(
				amount=amount_received - fee,
				tax_id=env_vars['tax_id'],
				name=env_vars['name'],
				bank_code=env_vars['bank_code'],
				branch_code=env_vars['branch_code'],
				account_number=env_vars['account_number'],
				account_type=env_vars['account_type']
			)
			

			transfers = starkbank.transfer.create([transfer])
			logging.info(f'Transfer created: {transfers}')
			return jsonify({'status': 'success'}), 200

	except Exception as e:
		logging.error(f'Error handling webhook: {e}')
		return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)