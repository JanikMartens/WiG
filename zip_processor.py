import zipfile
import os
import requests
import yaml
import msgpack
from datetime import date, datetime

def get_appdata_path():
    """Get path to AppData/Local/wig directory, creating it if necessary."""
    appdata_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'wig')
    os.makedirs(appdata_dir, exist_ok=True)
    return appdata_dir

def download_winget_pkgs():
    """Download winget-pkgs ZIP from GitHub to script directory if it doesn’t exist."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(script_dir, "winget-pkgs-master.zip")
    
    if not os.path.exists(zip_path):
        url = "https://github.com/microsoft/winget-pkgs/archive/refs/heads/master.zip"
        response = requests.get(url)
        response.raise_for_status()
        with open(zip_path, 'wb') as f:
            f.write(response.content)
    return zip_path

def find_locale_files(zip_path):
    """Find unique locale.en-US.yaml files based on package name."""
    matching_files = []
    seen_packages = set()
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for file in zipf.namelist():
            if file.endswith("locale.en-US.yaml"):
                parts = file.split('/')
                filename = parts[-1]
                package_name = '.'.join(filename.split('.')[:-2])
                if package_name not in seen_packages:
                    seen_packages.add(package_name)
                    matching_files.append(file)
    return matching_files

def process_yaml_files(zip_path, file_list):
    """Process YAML files into a data dictionary and a searchable index with only specified fields."""
    data = {}
    index = {}
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for file_path in file_list:
            try:
                with zipf.open(file_path) as f:
                    content = f.read().decode('utf-8')
                    yaml_data = yaml.safe_load(content)
                    if 'PackageIdentifier' in yaml_data:
                        package_id = yaml_data['PackageIdentifier']
                        # Extract only the specified fields
                        filtered_data = {
                            'PackageIdentifier': package_id,
                            'PackageName': yaml_data.get('PackageName', ''),
                            'ShortDescription': yaml_data.get('ShortDescription', ''),
                            'Description': yaml_data.get('Description', '')
                        }
                        data[package_id] = filtered_data
                        
                        # Build searchable text for index using only the specified fields
                        searchable_text = (
                            package_id.lower() + " " +
                            filtered_data['PackageName'].lower() 
                            
                        ).strip()
                        index[package_id] = searchable_text
            except Exception:
                print(f"Error processing {file_path}")
                pass
    
    return data, index

def custom_encoder(obj):
    """Custom encoder for MessagePack to handle datetime objects."""
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError(f"Cannot serialize {type(obj)}")

# Main execution
appdata_dir = get_appdata_path()
zip_path = download_winget_pkgs()
locale_files = find_locale_files(zip_path)
data, index = process_yaml_files(zip_path, locale_files)

# Save full data
data_output_path = os.path.join(appdata_dir, "package_data.msgpack")
with open(data_output_path, 'wb') as f:
    msgpack.pack(data, f, default=custom_encoder, use_bin_type=True)
print(f"Full data saved to {data_output_path}")

# Save searchable index
index_output_path = os.path.join(appdata_dir, "index.msgpack")
with open(index_output_path, 'wb') as f:
    msgpack.pack(index, f, use_bin_type=True)
print(f"Searchable index saved to {index_output_path}")