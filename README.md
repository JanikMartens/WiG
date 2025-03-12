This script provides an interactive command-line interface for searching and installing Windows packages using winget. It leverages fuzzy searching to match user queries against a pre-built package index stored in MessagePack files.

Features

Fuzzy search: Finds the best matches based on user input.

Interactive selection: Lists up to 20 results with package details.

Winget installation: Launches a new terminal window to install selected packages.

Requirements

Windows OS

Python 3.x

winget (Windows Package Manager) installed and available in system PATH

Required Python packages:

msgpack

fuzzywuzzy

Installation

Ensure you have the required dependencies installed:

pip install msgpack fuzzywuzzy

Usage

Prepare the data files: Ensure package_data.msgpack and index.msgpack exist in the script directory.

Run the script:

python script.py

Search for packages: Enter search terms when prompted.

Select a package to install: Enter the corresponding number to install a package.

Confirm installation: The script will launch a new terminal window to execute winget install.

Exit: Type q or quit at any prompt to exit.

File Structure

script.py - Main script file.

package_data.msgpack - Contains package metadata.

index.msgpack - Contains searchable package data.

Example Usage

Enter search terms (or 'quit' to exit): vscode

Found 2 results for 'vscode':
#   | Package Name                    | Package ID                     | Version         
--------------------------------------------------------------------------------
1   | Visual Studio Code              | Microsoft.VisualStudioCode      | 1.85.2          
2   | Visual Studio Code - Insiders   | Microsoft.VisualStudioCode.Insiders | 1.86.0

Enter number to install, 's' to search again, or 'q' to quit: 1
Install Microsoft.VisualStudioCode? (y/n): y
Installing: Microsoft.VisualStudioCode in a new terminal window...
✅ Installation of Microsoft.VisualStudioCode started in a new window.

Notes

The .Portable suffix in package identifiers is automatically removed before installation.

Ensure winget is installed and configured correctly for smooth operation.

License

This script is provided under the MIT License.
