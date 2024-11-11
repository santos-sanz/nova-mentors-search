import subprocess
import sys
import json
import time
from pathlib import Path

def format_execution_time(seconds):
    """Format execution time in minutes and seconds if over 60 seconds"""
    if seconds >= 60:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes} min {remaining_seconds:.2f} sec"
    return f"{seconds:.2f} seconds"

def run_script(script_name, description):
    """Execute a Python script and handle its result"""
    print(f"\n{'='*50}")
    print(f"Running {script_name}: {description}")
    print(f"{'='*50}\n")
    
    start_time = time.time()
    
    try:
        # Run the process with Python unbuffered mode
        process = subprocess.Popen(
            [sys.executable, "-u", script_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        # Print output in real-time
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip(), flush=True)

        # Get the return code
        return_code = process.poll()
        
        execution_time = time.time() - start_time
        print(f"\nExecution time for {script_name}: {format_execution_time(execution_time)}")
        
        # Check for errors
        if return_code != 0:
            _, stderr = process.communicate()
            print(f"Error executing {script_name}:")
            print(stderr)
            return False
            
        # Verify that expected output files exist after each step
        if script_name == 'evaluate_affinity.py':
            if not Path('affinity_scores.json').exists():
                print(f"Error: affinity_scores.json was not created by {script_name}")
                return False
            
        return True
        
    except Exception as e:
        print(f"Error executing {script_name}: {str(e)}")
        return False

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
    pipeline_start_time = time.time()
    
    # Define pipeline steps
    pipeline_steps = [
        ('extract_mentors.py', 'Extracting mentors data'),
        ('extract_keywords.py', 'Extracting keywords from input description'),
        ('evaluate_affinity.py', 'Evaluating mentor affinities'),
        ('merge_results.py', 'Merging results and calculating metrics')
    ]
    
    print("\nStarting mentorship matching pipeline...")
    
    pipeline_success = True
    for i, (script, description) in enumerate(pipeline_steps, 1):
        print(f"\nStep {i}/{len(pipeline_steps)}")
        
        if not Path(script).exists():
            print(f"Error: Script {script} not found!")
            pipeline_success = False
            break
        
        # Run the script
        if not run_script(script, description):
            print("\nPipeline failed! Stopping execution.")
            pipeline_success = False
            break
        
        # After extracting keywords, pause for review
        if script == 'extract_keywords.py':
            print("\nKeywords extraction completed.")
            if not review_keywords():
                print("\nPipeline failed during keywords review! Stopping execution.")
                pipeline_success = False
                break
            print("\nContinuing with pipeline execution...")
        
        # Add a small delay between steps
        time.sleep(1)
    
    total_execution_time = time.time() - pipeline_start_time
    
    if pipeline_success:
        print("\n✨ Pipeline completed successfully! ✨")
        print(f"Total execution time: {format_execution_time(total_execution_time)}")
        print("\nGenerated files:")
        print("- mentors.csv: Extracted mentor data")
        print("- extracted_keywords.json: Keywords from input description")
        print("- affinity_scores.json: Individual affinity scores")
        print("- mentors_with_affinities.csv: Final results with rankings")
    else:
        print("\nPipeline failed! Some steps were not completed successfully.")
        print(f"Time until failure: {format_execution_time(total_execution_time)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 