# analyze_results.py
import json
import pandas as pd
from pathlib import Path

def analyze_failure_modes(experiments_dir="experiments/failure_modes"):
    """Analyze collected failure modes for research insights."""
    failures = []
    
    for file in Path(experiments_dir).glob("*.json"):
        with open(file) as f:
            failures.append(json.load(f))
    
    df = pd.DataFrame(failures)
    
    # Calculate failure rates
    failure_rates = df.groupby(['constraint_variant', 'model_size']).size()
    
    # Analyze failure modes
    failure_modes = df['verification_result'].apply(lambda x: x.get('failure_mode', 'unknown'))
    mode_distribution = failure_modes.value_counts()
    
    return {
        "total_failures": len(df),
        "failure_rates": failure_rates.to_dict(),
        "failure_mode_distribution": mode_distribution.to_dict(),
        "raw_data": df
    }

if __name__ == "__main__":
    results = analyze_failure_modes()
    print(f"Total failures recorded: {results['total_failures']}")
    print("\nFailure Rates by Constraint & Model Size:")
    print(results['failure_rates'])