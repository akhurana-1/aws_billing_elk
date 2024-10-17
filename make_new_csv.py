import csv

def transform_csv(header, input_file, output_file):
    """Transform the input CSV file and write to the output CSV file."""
    
    # Read the CSV and write to the output file
    with open(input_file, mode='r') as csvfile, open(output_file, mode='w', newline='') as f:
        reader = csv.reader(csvfile)
        writer = csv.writer(f)

        # Write the header for the output file
        writer.writerow(header)
        
        # Skip the header from input CSV
        input_header = next(reader)

        # Iterate through each row in the CSV
        for row in reader:
            service_name = row[0]  # First column is the service name
            prices = row[1:]  # The rest are the monthly prices
            
            # Iterate through prices and corresponding months
            for month, price in zip(input_header[1:], prices):  # Skip the first column in header
                # Remove quotes and commas from the price
                price_cleaned = price.replace('"', '').replace(',', '').strip()
                writer.writerow([service_name, month, price_cleaned])

    print(f"Data has been written to {output_file}!")

# AWS Summary
header = ["Service Name", "Month", "Price"]
input_file = 'input/aws_summary.csv'
output_file = 'modified_input/aws_summary.csv'
transform_csv(header, input_file, output_file)

# AWS Total Billing
header = ["Total Bill", "Month", "Total Price"]
input_file = 'input/aws_total_billing.csv'
output_file = 'modified_input/aws_total_billing.csv'
transform_csv(header, input_file, output_file)

# AWS Ec2 Summary
header = ["Ec2 Service Name", "Month", "Ec2 Service Price"]
input_file = 'input/ec2_summary.csv'
output_file = 'modified_input/ec2_summary.csv'
transform_csv(header, input_file, output_file)

# AWS Redshift Summary
header = ["Redshift Service Name", "Month", "Redshift Service Price"]
input_file = 'input/Redshiftsummery.csv'
output_file = 'modified_input/Redshiftsummery.csv'
transform_csv(header, input_file, output_file)

# AWS S3 Summary
header = ["S3 Resource Name", "Month", "S3 Resource Price"]
input_file = 'input/S3Cost.csv'
output_file = 'modified_input/S3Cost.csv'
transform_csv(header, input_file, output_file)