import pandas as pd
from elasticsearch import Elasticsearch, helpers
import os

# Configuration
es_host = 'http://localhost:9200'  # Change this to your ES host
api_key = 'WEdudGlwSUJickVTMGMyZlprMGs6RHMyUWNoM3BSOC1QSlRGSWxDS0R4dw=='            # Replace with your actual API key
csv_file_paths = {
    'modified_input/aws_summary.csv': 'aws_costs_summary',
    'modified_input/aws_total_billing.csv': 'aws_total_costs',
    'modified_input/ec2_summary.csv': 'aws_ec2_summary',
    'modified_input/Redshiftsummery.csv': 'aws_redshift_summary',
    'modified_input/S3Cost.csv': 'aws_s3_summary'
}

# Initialize Elasticsearch client with API key
es = Elasticsearch(es_host, api_key=api_key)

def delete_existing_documents(index):
    """Delete all documents in the specified Elasticsearch index."""
    try:
        es.indices.delete(index=index, ignore=[400, 404])
        print(f'Deleted index: {index}')
    except Exception as e:
        print(f'Error deleting index: {e}')

def load_data_from_csv(file_path):
    """Load data from a CSV file into a DataFrame."""
    return pd.read_csv(file_path)

def index_data(data_frame, index):
    """Index the data from DataFrame into Elasticsearch."""
    actions = [
        {
            "_index": index,
            "_id": str(i),  # Optionally set an ID, or let Elasticsearch generate one
            "_source": row.to_dict(),
        }
        for i, row in data_frame.iterrows()
    ]
    helpers.bulk(es, actions)
    print(f'Indexed {len(actions)} documents into index: {index}')

def process_csv_file(file_path, index):
    """Process a single CSV file and index its data into Elasticsearch."""
    delete_existing_documents(index)  # Clear existing documents

    if os.path.exists(file_path):  # Check if the file exists
        data = load_data_from_csv(file_path)
        index_data(data, index)
    else:
        print(f'File not found: {file_path}')

def main():
    """Process all CSV files based on the provided mapping."""
    for file_path, index in csv_file_paths.items():
        process_csv_file(file_path, index)

if __name__ == '__main__':
    main()
