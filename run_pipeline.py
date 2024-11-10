import subprocess
import sys
import json
import time
from pathlib import Path

def run_script(script_name, description):
    """Execute a Python script and handle its result"""
    print(f"\n{'='*50}")
    print(f"Running {script_name}: {description}")
    print(f"{'='*50}\n")
    
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error executing {script_name}:")
        print(result.stderr)
        return False
    
    print(result.stdout)
    return True

def review_keywords():
    """Allow user to review and edit keywords in the file"""
    keywords_file = 'extracted_keywords.json'
    
    if not Path(keywords_file).exists():
        print(f"Error: {keywords_file} not found!")
        return False
        
    print("\nPlease review and edit the keywords directly in the file:")
    print(f"{keywords_file}")
    
    while True:
        choice = input("\nHave you finished reviewing the keywords? (yes/no): ").lower()
        if choice in ['yes', 'y']:
            try:
                with open(keywords_file, 'r', encoding='utf-8') as f:
                    keywords = json.load(f)
                print("\nUpdated keywords:")
                print(json.dumps(keywords, indent=2))
                return True
            except Exception as e:
                print(f"\nError reading file: {str(e)}")
                print("Please verify the file has valid JSON format")
                return False
        elif choice in ['no', 'n']:
            print("Please edit the file and try again")
        else:
            print("Please answer 'yes' or 'no'")

def main():
    # Define pipeline steps
    pipeline_steps = [
        ('extract_mentors.py', 'Extracting mentors data'),
        ('extract_keywords.py', 'Extracting keywords from input description'),
        ('evaluate_affinity.py', 'Evaluating mentor affinities'),
        ('merge_results.py', 'Merging results and calculating metrics')
    ]
    
    print("\nStarting mentorship matching pipeline...")
    
    # Execute each step
    for i, (script, description) in enumerate(pipeline_steps, 1):
        print(f"\nStep {i}/{len(pipeline_steps)}")
        
        if not Path(script).exists():
            print(f"Error: Script {script} not found!")
            sys.exit(1)
        
        # Run the script
        if not run_script(script, description):
            print("\nPipeline failed! Stopping execution.")
            sys.exit(1)
        
        # After extracting keywords, pause for review
        if script == 'extract_keywords.py':
            print("\nKeywords extraction completed.")
            if not review_keywords():
                print("\nPipeline failed during keywords review! Stopping execution.")
                sys.exit(1)
            print("\nContinuing with pipeline execution...")
        
        # Add a small delay between steps
        time.sleep(1)
    
    print("\n✨ Pipeline completed successfully! ✨")
    print("\nGenerated files:")
    print("- mentors.csv: Extracted mentor data")
    print("- extracted_keywords.json: Keywords from input description")
    print("- affinity_scores.json: Individual affinity scores")
    print("- mentors_with_affinities.csv: Final results with rankings")

if __name__ == "__main__":
    main() 