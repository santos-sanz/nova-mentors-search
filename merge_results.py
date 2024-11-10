import pandas as pd
import json
import numpy as np

def load_data():
    """Load data from mentors.csv and affinity_scores.json"""
    try:
        # Load mentors CSV
        mentors_df = pd.read_csv('mentors.csv')
        
        # Load affinity results
        with open('affinity_scores.json', 'r', encoding='utf-8') as f:
            affinity_scores = json.load(f)
            
        return mentors_df, affinity_scores
    except FileNotFoundError as e:
        raise Exception(f"Error loading files: {str(e)}")

def process_results(mentors_df, affinity_scores):
    """Process and combine results"""
    # Create DataFrame with affinity results
    affinity_df = pd.DataFrame(affinity_scores)
    
    # Convert affinities column from dict to new columns
    affinities_expanded = pd.json_normalize(affinity_df['affinities'])
    
    # Calculate average affinity for each mentor
    affinity_df['average_affinity'] = affinities_expanded.mean(axis=1)
    
    # Merge with original mentors DataFrame using name
    merged_df = mentors_df.merge(
        affinity_df[['mentor_name', 'affinities', 'average_affinity']], 
        left_on='name', 
        right_on='mentor_name', 
        how='left'
    )
    
    # Remove redundant mentor_name column from merge
    merged_df = merged_df.drop('mentor_name', axis=1)
    
    # Sort by average_affinity in descending order
    merged_df = merged_df.sort_values('average_affinity', ascending=False)
    
    return merged_df

def main():
    try:
        # Load data
        mentors_df, affinity_scores = load_data()
        
        # Process and combine results
        final_df = process_results(mentors_df, affinity_scores)
        
        # Save results
        output_file = 'mentors_with_affinities.csv'
        final_df.to_csv(output_file, index=False, encoding='utf-8')
        
        print(f"\nProcess completed successfully!")
        print(f"Results saved to: {output_file}")
        print(f"Total mentors processed: {len(final_df)}")
        print(f"Global average affinity: {final_df['average_affinity'].mean():.2f}")
        
        # Print top 3 mentors by affinity
        print("\nTop 3 mentors by affinity:")
        top_3 = final_df[['name', 'average_affinity']].head(3)
        for _, row in top_3.iterrows():
            print(f"{row['name']}: {row['average_affinity']:.2f}")
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main() 