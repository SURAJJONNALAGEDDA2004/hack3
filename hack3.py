import csv
import os

DRUGS_FILE = 'drugs.csv'
TRANSFERS_FILE = 'transfers.csv'

# Initialize CSV files if they don't exist
def init_files():
    if not os.path.exists(DRUGS_FILE):
        with open(DRUGS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Batch Number', 'Name', 'Manufacturer', 'Manufactured Date', 'Current Holder'])

    if not os.path.exists(TRANSFERS_FILE):
        with open(TRANSFERS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Batch Number', 'From', 'To', 'Transfer Date'])

# Register a new drug
def register_drug(batch_number, name, manufacturer, manufactured_date, current_holder):
    with open(DRUGS_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([batch_number, name, manufacturer, manufactured_date, current_holder])
    print(f'Drug {name} registered successfully.')

# Transfer drug ownership
def transfer_drug(batch_number, to_holder, transfer_date):
    drugs = []
    drug_found = False

    # Read all drugs and update the current holder for the specified batch number
    with open(DRUGS_FILE, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        for row in reader:
            if row[0] == batch_number:
                drug_found = True
                from_holder = row[4]
                row[4] = to_holder
                drugs.append(row)
                # Log the transfer
                with open(TRANSFERS_FILE, 'a', newline='') as t_file:
                    t_writer = csv.writer(t_file)
                    t_writer.writerow([batch_number, from_holder, to_holder, transfer_date])
                print(f'Drug ownership transferred from {from_holder} to {to_holder}.')
            else:
                drugs.append(row)

    if not drug_found:
        print(f'Batch number {batch_number} not found.')

    # Write the updated data back to the CSV
    with open(DRUGS_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(drugs)

# Track drug details and transfer history
def track_drug(batch_number):
    drug_found = False
    with open(DRUGS_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == batch_number:
                drug_found = True
                print(f"Batch Number: {row[0]}, Name: {row[1]}, Manufacturer: {row[2]}, Manufactured Date: {row[3]}, Current Holder: {row[4]}")

    if not drug_found:
        print(f'Batch number {batch_number} not found.')
        return

    print('Transfer History:')
    with open(TRANSFERS_FILE, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        history_found = False
        for row in reader:
            if row[0] == batch_number:
                print(f"From: {row[1]} To: {row[2]} Date: {row[3]}")
                history_found = True

        if not history_found:
            print('No transfer history found for this drug.')

# Initialize the CSV files
init_files()

# Example usage
register_drug('BATCH001', 'Paracetamol', 'PharmaCorp', '2024-08-20', 'PharmaCorp Warehouse')
register_drug('BATCH002', 'Ibuprofen', 'MediLife', '2024-08-21', 'MediLife Warehouse')

transfer_drug('BATCH001', 'Distributor Inc.', '2024-08-22')
transfer_drug('BATCH002', 'PharmaDistributor', '2024-08-23')

track_drug('BATCH001')
track_drug('BATCH002')
