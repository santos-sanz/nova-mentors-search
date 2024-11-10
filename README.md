# Nova Mentors Search

A Python-based tool that extracts mentor information from Nova's mentoring platform and performs AI-powered affinity analysis.

## Description

This tool processes local HTML files from Nova's mentoring platform and performs the following functions:

1. Extracts key mentor information:
   - Name
   - Position
   - Location
   - Description

2. Uses GPT to:
   - Extract keywords from search descriptions
   - Evaluate affinity between mentors and keywords
   - Generate compatibility scores

3. Generates CSV reports with sorted results

## File Structure

```
nova-mentors-search/
├── README.md                    # Main documentation
├── requirements.txt             # Python dependencies
├── extract_mentors.py          # Mentor data extractor
├── extract_keywords.py         # GPT-powered keyword extractor
├── evaluate_affinity.py        # GPT-powered affinity evaluator
├── merge_results.py           # Results merger
├── prompts.py                 # GPT prompt templates
├── run_pipeline.py            # Main pipeline script
└── .gitignore                 # Git ignored files
```

## Prerequisites

- Python 3.x
- OpenAI API key
- beautifulsoup4 (4.12.3 or later)
- pandas
- python-dotenv

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nova-mentors-search.git
cd nova-mentors-search/scripts
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file with:
```
OPENAI_API_KEY=your_api_key
MODEL_KEYWORDS=gpt-4
MODEL_AFFINITY=gpt-4
MAX_RETRIES_KEYWORDS=3
MAX_RETRIES_AFFINITY=3
BATCH_SIZE=20
```

## Usage

1. Save mentors page as HTML:
   - Open your browser
   - Go to https://digital-agent.novatalent.net
   - Login with your Nova credentials
   - Navigate to mentoring section
   - Save page as "Nova - Mentoring.html"

2. Run the complete pipeline:
```bash
python run_pipeline.py
```

The pipeline will execute:
- Mentor data extraction
- Keyword extraction
- Affinity evaluation
- Results merging

## Generated Files

- `mentors.csv`: Extracted mentor data
- `extracted_keywords.json`: Extracted keywords
- `affinity_scores.json`: Affinity scores
- `mentors_with_affinities.csv`: Final sorted results

## Key Components

### Mentor Extractor
- Processes HTML using BeautifulSoup4
- Cleans and formats mentor information
- Saves structured data to CSV

### Keyword Extractor
- Uses GPT to analyze input descriptions
- Extracts relevant keywords
- Supports manual review and editing

### Affinity Evaluator
- Evaluates semantic relationships
- Processes mentors in batches
- Generates numerical affinity scores

### Results Merger
- Combines all data sources
- Calculates final rankings
- Generates sorted output

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Create Pull Request

## Error Handling

The system includes comprehensive error handling:
- Logging to file and console
- Retry mechanisms for API calls
- Detailed error messages
- Input validation

## Configuration

Key configuration options in `.env`:
- API model selection
- Retry attempts
- Batch processing size
- Logging levels

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainer.

## Acknowledgments

- Nova platform for mentoring service
- OpenAI for GPT API
- BeautifulSoup4 for HTML parsing capabilities
- Python community for documentation and support