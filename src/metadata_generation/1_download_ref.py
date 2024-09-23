import os
import requests

# Define the URL of the reference genome
REFERENCE_GENOME = 'Homo_sapiens.GRCh38.103.gtf.gz'
REFERENCE_GENOME_URL = f'http://ftp.ensembl.org/pub/release-103/gtf/homo_sapiens/{REFERENCE_GENOME}'

# Define the directory to save the file relative to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(script_dir, '../../data/reference')

# Ensure the directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# If reference file already exists, say so and exit
gtf_file_path = os.path.join(DATA_DIR, REFERENCE_GENOME)

if os.path.exists(gtf_file_path):
    print(f"{REFERENCE_GENOME} already exists at {gtf_file_path}. Done.")
    exit(0)

print(f"Downloading reference from {REFERENCE_GENOME_URL} to {DATA_DIR}...")
# Download the file
response = requests.get(REFERENCE_GENOME_URL, stream=True)
response.raise_for_status()  # Check if the request was successful

# Save the file to the specified directory
with open(gtf_file_path, 'wb') as file:
    for chunk in response.iter_content(chunk_size=8192):
        file.write(chunk)

print(f"Downloaded {REFERENCE_GENOME}.gz to {gtf_file_path}")
