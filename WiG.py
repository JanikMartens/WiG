import msgpack
from fuzzywuzzy import fuzz
from operator import itemgetter
import subprocess
import os
# Paths to the MessagePack files
appdata_dir = os.path.join(os.environ.get('LOCALAPPDATA'), 'wig')
data_path = os.path.join(appdata_dir, "package_data.msgpack")
index_path = os.path.join(appdata_dir, "index.msgpack")
# Load the data and index
with open(data_path, 'rb') as f:
    data = msgpack.unpack(f, raw=False)
with open(index_path, 'rb') as f:
    index = msgpack.unpack(f, raw=False)

def install_package(package_identifier):
    """Install package using winget in a new terminal window"""
    winget_id = package_identifier.replace(".Portable", "")
    
    # Command to open a new terminal window and run winget install
    command = f'start cmd /k "winget install --id {winget_id} --accept-source-agreements --accept-package-agreements"'
    
    print(f"\nInstalling: {winget_id} in a new terminal window...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ Installation of {winget_id} started in a new window.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching winget install in new terminal: {e}")
        return False

while True:
    search_input = input("\nEnter search terms (or 'quit' to exit): ").strip()
    if search_input.lower() in ('quit', 'q'):
        break
    if not search_input:
        continue

    search_terms = search_input.lower().split()
    matches = []
    
    # Perform search and scoring
    for package_id, searchable_text in index.items():
        if any(term in searchable_text for term in search_terms):
            max_score = max(fuzz.partial_ratio(term, searchable_text) for term in search_terms)
            matches.append((max_score, package_id, data[package_id]))
    
    # Sort and limit results
    matches = sorted(matches, key=itemgetter(0), reverse=True)[:20]
    
    if matches:
        print(f"\nFound {len(matches)} results for '{search_input}':")
        print(f"{'#':<3} | {'Package Name':<32} | {'Package ID':<32} | {'Version':<16}")
        print("-" * 96)
        for idx, (score, pkg_id, pkg_data) in enumerate(matches, 1):
            name = pkg_data.get("PackageName", "N/A")[:30]
            version = pkg_data.get("PackageVersion", "N/A")[:14]
            print(f"{idx:<3} | {name:<32} | {pkg_id:<32} | {version:<16}")
        
        # Selection handling
        while True:
            choice = input("\nEnter number to install, 's' to search again, or 'q' to quit: ").strip().lower()
            if choice in ('q', 's'):
                break
                
            if not choice.isdigit():
                print("❌ Please enter a valid number")
                continue
                
            num = int(choice)
            if 1 <= num <= len(matches):
                _, pkg_id, _ = matches[num-1]
                confirm = input(f"Install {pkg_id}? (y/n): ").strip().lower()
                if confirm == 'y':
                    install_package(pkg_id)
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(matches)}")
    else:
        print(f"🔍 No packages found matching '{search_input}'")