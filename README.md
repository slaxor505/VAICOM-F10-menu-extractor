# VAICOM F10 Menu Extractor Project

## How to use:
- Drop exe file into VAICOM Export folder
- Export keywords files as per usual from VAICOM UI. "EXPORT" button.\
- Run the exe file - it will copy required keywords string for Voice Attack profile update.
- Update Voice Attack profile with the copied string as per usual.

## Overview
This project includes a tool that extracts F10 menu items from a specially formatted CSV file, adds them to a keywords.txt file, copies the content of keywords.txt to the Windows clipboard for easy pasting elsewhere, and displays a popup window confirming that the text has been copied to the clipboard.

The tool also cleans the extracted text by:
- Removing brackets and text in brackets (square brackets, parentheses, and curly braces)
- Removing new lines from the beginning and end of the text

## Requirements
- Python 3.x
- pyperclip (for clipboard functionality)

## Running the F10 Menu Extractor
You can run the F10 menu extractor in two ways:

### Using the Python Script
```
python extract_f10_menu.py [--source SOURCE_FILE] [--target TARGET_FILE] [--no-clipboard] [--no-popup] [--save-to-file]
```

Command-line options:
- `--source` or `-s`: Path to the source CSV file (default: keywords.csv in the current directory)
- `--target` or `-t`: Path to the target TXT file (default: keywords.txt in the current directory)
- `--no-clipboard`: Disable copying to clipboard
- `--no-popup`: Disable popup window
- `--save-to-file`: Save to target file (by default, only copies to clipboard)

After running the script, the content of the target file will be automatically copied to the Windows clipboard (unless disabled with `--no-clipboard`), allowing you to easily paste it elsewhere. A popup window will also appear to confirm that the text has been copied to the clipboard (unless disabled with `--no-popup`).

Examples:
```
# Use default files in the current directory
python extract_f10_menu.py

# Specify a custom source file
python extract_f10_menu.py --source custom_keywords.csv

# Specify a custom target file
python extract_f10_menu.py --target custom_output.txt

# Specify both custom source and target files
python extract_f10_menu.py -s custom_keywords.csv -t custom_output.txt

# Disable copying to clipboard
python extract_f10_menu.py --no-clipboard

# Disable popup window
python extract_f10_menu.py --no-popup

# Disable both clipboard copying and popup window
python extract_f10_menu.py --no-clipboard --no-popup

# Save to target file (by default, only copies to clipboard)
python extract_f10_menu.py --save-to-file
```

### Using the Windows Executable
You can use the executable in two ways:

#### Basic Usage
1. Make sure both `keywords.csv` and `keywords.txt` files are in the same directory as the executable
2. Double-click on `extract_f10_menu.exe` to run it
3. The program will process the files, copy the content of keywords.txt to the clipboard, display a popup window confirming that the text has been copied to the clipboard, and show a confirmation message in the console when complete

#### Command-line Usage
The executable supports the same command-line options as the Python script:

```
extract_f10_menu.exe [--source SOURCE_FILE] [--target TARGET_FILE] [--no-clipboard] [--no-popup] [--save-to-file]
```

Just like the Python script, the executable will automatically copy the content to the Windows clipboard after processing (unless disabled with `--no-clipboard`) and display a popup window confirming that the text has been copied to the clipboard (unless disabled with `--no-popup`). By default, it only copies to clipboard without saving to the target file. You can use the `--save-to-file` parameter to save to the target file as well.

Examples:
```
# Use default files in the current directory
extract_f10_menu.exe

# Specify a custom source file
extract_f10_menu.exe --source custom_keywords.csv

# Specify both custom source and target files
extract_f10_menu.exe -s custom_keywords.csv -t custom_output.txt

# Disable copying to clipboard
extract_f10_menu.exe --no-clipboard

# Disable popup window
extract_f10_menu.exe --no-popup

# Disable both clipboard copying and popup window
extract_f10_menu.exe --no-clipboard --no-popup

# Save to target file (by default, only copies to clipboard)
extract_f10_menu.exe --save-to-file
```

## Building the Executable
If you need to rebuild the executable, you can use PyInstaller. Make sure you have the required dependencies installed:

```
pip install pyinstaller
pip install pyperclip
pyinstaller --onefile extract_f10_menu.py
```

The executable will be created in the `dist` directory.

## File Structure
- keywords.csv – CSV input with command data.
- keywords.txt – Output text file (generated).
- extract_f10_menu.py – Script for extracting F10 menu items from the CSV file.
- dist/extract_f10_menu.exe – Windows executable for the F10 menu extractor.
- README.md – This documentation file.
