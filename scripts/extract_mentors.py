import csv
import os
import logging
from bs4 import BeautifulSoup
import re

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

def print_error(error_type, error_msg, error_trace=None):
    """Print error in a formatted way"""
    print("\n" + "="*50)
    print(f"ERROR TYPE: {error_type}")
    print(f"ERROR MESSAGE: {error_msg}")
    if error_trace:
        print("\nTRACEBACK:")
        print(error_trace)
    print("="*50 + "\n")

def clean_text(text):
    """Clean text by removing quotes, multiple spaces and newlines"""
    # Remove quotes
    text = text.replace('"', '')
    # Replace newlines and multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Strip leading/trailing spaces
    return text.strip()

def process_mentors_page(html_content):
    """
    Process the mentors page HTML and extract relevant information
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        print("\nExtracting mentors information...")
        
        mentors_data = []
        mentor_items = soup.find_all('li', {'data-testid': 'mentoring-user-list-item'})
        
        print(f"\nFound {len(mentor_items)} mentors")
        
        for item in mentor_items:
            try:
                # Extract basic information
                name = clean_text(item.find('p', class_='font-bold').text)
                
                # Get all text-nova-xs paragraphs
                info_paragraphs = item.find_all('p', class_='text-nova-grey-700 text-nova-xs')
                position = clean_text(info_paragraphs[0].text) if len(info_paragraphs) > 0 else ""
                location = clean_text(info_paragraphs[1].text) if len(info_paragraphs) > 1 else ""
                
                # Get description
                description = item.find('p', class_='text-nova-xs line-clamp-3')
                description_text = clean_text(description.text) if description else ""
                
                mentor_data = {
                    'name': name,
                    'position': position,
                    'location': location,
                    'description': description_text
                }
                
                mentors_data.append(mentor_data)
                print(f"Extracted data for mentor: {name}")
                
            except Exception as e:
                print(f"Error processing mentor item: {str(e)}")
                continue
        
        # Save data to CSV
        with open('mentors.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'position', 'location', 'description'])
            writer.writeheader()
            for mentor in mentors_data:
                writer.writerow(mentor)
        
        print(f"\nSuccessfully processed {len(mentors_data)} mentors and saved to mentors.csv")
        return mentors_data

    except Exception as e:
        print_error("PROCESSING ERROR", str(e))
        raise

def extract_mentors():
    """
    Extract mentors information from the HTML file
    """
    print("\nStarting mentor extraction process...")
    try:
        # Read the HTML file
        html_file_path = 'Nova - Mentoring.html'
        if not os.path.exists(html_file_path):
            raise Exception(f"HTML file not found: {html_file_path}")
        
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Process mentors data
        mentors_data = process_mentors_page(html_content)
        return mentors_data

    except Exception as e:
        print_error("EXTRACTION ERROR", str(e))
        raise

if __name__ == "__main__":
    try:
        extract_mentors()
    except Exception as e:
        print_error("FATAL ERROR", str(e))