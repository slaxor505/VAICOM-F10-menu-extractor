import csv
import argparse
import os
import pyperclip
import tkinter as tk
from tkinter import messagebox
import re

def extract_f10_menu_items(csv_path):
    """
    Extract items from the F10 menu section of the CSV file and return them as a comma-separated string.
    The F10 menu section starts from the row where the 2nd column is "Imported F10 menu commands".

    Args:
        csv_path (str): Path to the CSV file

    Returns:
        str: Comma-separated string of F10 menu items
    """
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        rows = list(reader)

    f10_items = []
    in_f10_section = False

    for row in rows:
        if len(row) > 1:
            # Check if this is the start of the F10 menu section
            if row[0].strip() == "" and row[1].strip() == "Imported F10 menu commands":
                in_f10_section = True
                continue  # Skip the section header row

            # Check if we've reached the end of the F10 section (a new section starts)
            if in_f10_section and row[0].strip() == "" and row[1].strip() != "":
                break  # Exit the loop when we reach a new section

            # If we're in the F10 section and the row has data, extract the item
            if in_f10_section and row[0].strip() != "" and row[1].strip() != "":
                f10_items.append(row[1].strip())

    # Return the items as a comma-separated string
    return f10_items

def clean_text(text):
    """
    Clean the text by removing brackets and text in brackets, and removing new lines from the beginning and end.

    Args:
        text (str): The text to clean

    Returns:
        str: The cleaned text
    """
    # Remove brackets and text in brackets
    cleaned_text = re.sub(r'\[.*?\]', '', text)
    cleaned_text = re.sub(r'\(.*?\)', '', cleaned_text)
    cleaned_text = re.sub(r'\{.*?\}', '', cleaned_text)
    # Remove forward and backward slashes
    cleaned_text = cleaned_text.replace('/', '').replace('\\', '')

    # Remove new lines from the beginning and end
    cleaned_text = cleaned_text.strip()

    return cleaned_text

def add_to_keywords_txt(f10_items, txt_path):
    """
    Add F10 menu items to keywords.txt before "Mission;", following its structure.
    If F10 menu items already exist, they will be replaced.

    Args:
        f10_items (list): List of F10 menu items
        txt_path (str): Path to the keywords.txt file
    """
    # Format the F10 menu items as a simple semicolon-separated string
    f10_section = "; ".join(f10_items) + ";"

    # Read the entire file content
    with open(txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any existing F10 menu items
    # This is a simplified approach - we'll just check for a few key F10 items
    for item in f10_items[:5]:  # Use first few items as markers
        if item in content:
            # If we find these items, assume they're part of the F10 menu section
            # and remove them from the content
            start_idx = content.find(item)
            if start_idx > 0:
                # Find the end of this section (next semicolon after several items)
                end_idx = content.find(";", start_idx + 200)  # Look ahead for a semicolon
                if end_idx > 0:
                    content = content[:start_idx] + content[end_idx+1:]
                    break

    # Find the position of "Mission;" in the content
    mission_pos = content.find("Mission;")

    if mission_pos != -1:
        # Insert the F10 menu items before "Mission;"
        new_content = content[:mission_pos] + f10_section + "\n" + content[mission_pos:]

        # Write the updated content back to keywords.txt
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        # If "Mission;" is not found, add the new section at the end
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(content + "\n" + f10_section)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Extract F10 menu items from CSV and add to TXT file.')
    parser.add_argument('--source', '-s', help='Path to the source CSV file (default: keywords.csv)')
    parser.add_argument('--target', '-t', help='Path to the target TXT file (default: keywords.txt)')
    parser.add_argument('--no-clipboard', action='store_true', help='Disable copying to clipboard')
    parser.add_argument('--no-popup', action='store_true', help='Disable popup window')
    parser.add_argument('--save-to-file', action='store_true', help='Save to target file (by default, only copies to clipboard)')
    args = parser.parse_args()

    # Use provided paths or defaults (relative to current directory)
    csv_path = args.source if args.source else "keywords.csv"
    txt_path = args.target if args.target else "keywords.txt"

    print(f"Using source file: {csv_path}")
    print(f"Using target file: {txt_path}")

    # Get the F10 menu items
    f10_items = extract_f10_menu_items(csv_path)

    # Format the F10 menu items as a simple semicolon-separated string
    f10_section = "; ".join(f10_items) + ";"

    # Clean the F10 section text
    f10_section = clean_text(f10_section)

    # Try to read existing file if it exists
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the position of "Mission;" in the content
        mission_pos = content.find("Mission;")

        if mission_pos != -1:
            # Create the content with F10 menu items before "Mission;"
            keywords_content = content[:mission_pos] + f10_section + content[mission_pos:]
        else:
            # If "Mission;" is not found, add the new section at the end
            keywords_content = content + f10_section
    except FileNotFoundError:
        # If file doesn't exist, just use the F10 section
        keywords_content = f10_section

    # # Clean the final keywords content
    # keywords_content = clean_text(keywords_content)

    if args.save_to_file:
        # Save the prepared content to keywords.txt
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(keywords_content)
        print(f"Saved to {txt_path}")
    else:
        print(f"Clipboard-only mode: not saving to {txt_path}")

    # Copy to clipboard if not disabled
    if not args.no_clipboard:
        pyperclip.copy(keywords_content)
        print("Content of keywords.txt copied to clipboard")
    else:
        print("Clipboard copying disabled")

    print("Found F10 menu items:")
    print(", ".join(f10_items))

    # Show popup message if not disabled
    if not args.no_popup:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showinfo("Clipboard", "Keywords copied to clipboard. Paste into VoiceAttack profile.")
        root.destroy()
        print("Popup window displayed")
    else:
        print("Popup window disabled")
