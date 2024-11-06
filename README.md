# Nova Mentors Search

A Python script to extract mentor information from Nova's mentoring platform HTML and save it to a CSV file.

## Description

This tool processes a local HTML file from Nova's mentoring platform and extracts key information about mentors, including:
- Name
- Position
- Location
- Description

The extracted data is cleaned (removing quotes, multiple spaces, and newlines) and saved to a CSV file for easy analysis.

## Prerequisites

- Python 3.x
- beautifulsoup4 (4.12.3 or later)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nova-mentors-search.git
cd nova-mentors-search
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Save the Nova mentoring page as HTML:
   - Open your browser
   - Go to https://digital-agent.novatalent.net
   - Login with your Nova credentials
   - Navigate to the mentoring section
   - Save the page as "Nova - Mentoring.html" in the project directory

2. Run the script:
```bash
python extract_mentors.py
```

3. The script will:
   - Process the HTML file
   - Extract mentor information
   - Save the data to `mentors.csv`

## Output Format

The script generates a CSV file (`mentors.csv`) with the following columns:
- `name`: Mentor's full name
- `position`: Current job position
- `location`: Geographic location
- `description`: Mentor's description or expertise


## File Structure

```
nova-mentors-search/
├── README.md
├── requirements.txt
├── extract_mentors.py
├── mentors.csv (generated)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License - see the LICENSE file for details.

## Acknowledgments

- Nova platform for providing the mentoring service
- BeautifulSoup4 for HTML parsing capabilities
- Python community for excellent documentation and support

## Support

For support, please open an issue in the GitHub repository or contact the maintainer.