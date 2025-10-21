"""
POWERRBI_METADATA
"""

#!/usr/bin/env python
# coding: utf-8

# In[3]:


import shutil
import os
import json

def extract_metadata(pbix_path):
    # Renombrar el archivo .pbix a .zip
    zip_path = pbix_path.replace('.pbix', '.zip')
    shutil.copyfile(pbix_path, zip_path)

    # Crear un directorio temporal para extraer los archivos
    temp_dir = 'temp_extracted_files'
    os.makedirs(temp_dir, exist_ok=True)

    # Extraer el archivo .zip
    shutil.unpack_archive(zip_path, temp_dir)

    # Leer el archivo metadata.json
    metadata_file = os.path.join(temp_dir, 'Metadata', 'metadata.json')
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        shutil.rmtree(temp_dir)
        os.remove(zip_path)
        return metadata
    else:
        shutil.rmtree(temp_dir)
        os.remove(zip_path)
        return "Metadata file not found in the .pbix archive."

# Path to your .pbix file
pbix_path = r"C:\Users\HP\Downloads\Examen 1-SEM 17.pbix"
metadata = extract_metadata(pbix_path)

# Print extracted metadata
print(json.dumps(metadata, indent=4))



# In[7]:


import zipfile
import os
import json

def extract_pbix_metadata(pbix_file_path):
    if not os.path.exists(pbix_file_path):
        raise FileNotFoundError(f"The file {pbix_file_path} does not exist.")

    # Create a directory to extract the PBIX contents
    extract_dir = pbix_file_path + "_extracted"
    os.makedirs(extract_dir, exist_ok=True)

    # Extract the PBIX file (which is a ZIP file)
    with zipfile.ZipFile(pbix_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    # Read the metadata file (typically the metadata is stored in a JSON file within the PBIX)
    metadata_file_path = os.path.join(extract_dir, 'Report', 'Layout')
    if not os.path.exists(metadata_file_path):
        raise FileNotFoundError(f"The metadata file was not found in the extracted PBIX contents.")

    # Read the file content as bytes
    with open(metadata_file_path, 'rb') as file:
        file_content = file.read()

    # Try decoding the content with different encodings
    for encoding in ['utf-8', 'utf-8-sig', 'utf-16', 'utf-16le', 'utf-16be']:
        try:
            metadata_str = file_content.decode(encoding)
            metadata_json = json.loads(metadata_str)
            break
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue
    else:
        raise ValueError("The metadata file could not be decoded with common encodings.")

    # Extract relevant metadata
    metadata = {
        "name": metadata_json.get("name"),
        "description": metadata_json.get("description"),
        "tables": []
    }

    for table in metadata_json.get("model", {}).get("tables", []):
        table_info = {
            "name": table.get("name"),
            "columns": []
        }
        for column in table.get("columns", []):
            column_info = {
                "name": column.get("name"),
                "data_type": column.get("dataType"),
                "is_hidden": column.get("isHidden", False)
            }
            table_info["columns"].append(column_info)

        metadata["tables"].append(table_info)

    return metadata


# Example usage
pbix_file_path =  r"C:\Users\HP\Downloads\Examen 1-SEM 17.pbix"
metadata = extract_pbix_metadata(pbix_file_path)
print(metadata)


# In[ ]:






if __name__ == "__main__":
    pass
