import kagglehub
import shutil
import os

print("Downloading dataset...")
path = kagglehub.dataset_download("rwilliams7653/dna-methylome-of-idiopathic-pulmonary-fibrosis")
print("Path to dataset files:", path)

# Copy to local workspace for easier access
dest = os.path.join(os.getcwd(), "idiopathic_data")
if os.path.exists(dest):
    shutil.rmtree(dest)
shutil.copytree(path, dest)
print(f"Copied to {dest}")
