#!/usr/bin/env python3
"""
Script to generate comprehensive runs.json with complete file contents and accurate counts.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def count_words(text):
    """Count words in text."""
    return len(text.split())

def count_characters(text):
    """Count characters in text."""
    return len(text)

def read_file_content(filepath):
    """Read complete file content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return ""

def process_run(run_path, run_name):
    """Process a single run directory and extract all data."""
    run_data = {
        "name": run_name,
        "description": "",
        "files": {},
        "totals": {}
    }
    
    # Read details.txt for description
    details_path = run_path / "details.txt"
    if details_path.exists():
        run_data["description"] = read_file_content(details_path).strip()
    
    # Process each file type
    file_types = ["system-prompt.md", "user-prompt.md", "output.md"]
    
    total_prompt_words = 0
    total_prompt_chars = 0
    total_output_words = 0
    total_output_chars = 0
    
    for file_type in file_types:
        file_path = run_path / file_type
        if file_path.exists():
            content = read_file_content(file_path)
            word_count = count_words(content)
            char_count = count_characters(content)
            
            # Determine file category
            if "prompt" in file_type:
                total_prompt_words += word_count
                total_prompt_chars += char_count
                category = "prompt"
            elif "output" in file_type:
                total_output_words += word_count
                total_output_chars += char_count
                category = "output"
            else:
                category = "other"
            
            run_data["files"][file_type.replace('.md', '').replace('-', '_')] = {
                "filename": file_type,
                "category": category,
                "word_count": word_count,
                "character_count": char_count,
                "content": content
            }
    
    # Calculate totals
    run_data["totals"] = {
        "prompt_words": total_prompt_words,
        "prompt_characters": total_prompt_chars,
        "output_words": total_output_words,
        "output_characters": total_output_chars,
        "total_words": total_prompt_words + total_output_words,
        "total_characters": total_prompt_chars + total_output_chars
    }
    
    return run_data

def calculate_analysis(runs_data):
    """Calculate comparative analysis between runs."""
    control = runs_data["control"]["totals"]
    optimised = runs_data["optimised"]["totals"]
    raw = runs_data["raw"]["totals"]
    
    analysis = {
        "prompt_progression": {
            "control_to_optimised": {
                "word_increase": optimised["prompt_words"] - control["prompt_words"],
                "character_increase": optimised["prompt_characters"] - control["prompt_characters"],
                "percentage_increase_words": f"{((optimised['prompt_words'] - control['prompt_words']) / control['prompt_words'] * 100):.1f}%",
                "percentage_increase_characters": f"{((optimised['prompt_characters'] - control['prompt_characters']) / control['prompt_characters'] * 100):.1f}%"
            },
            "optimised_to_raw": {
                "word_increase": raw["prompt_words"] - optimised["prompt_words"],
                "character_increase": raw["prompt_characters"] - optimised["prompt_characters"],
                "percentage_increase_words": f"{((raw['prompt_words'] - optimised['prompt_words']) / optimised['prompt_words'] * 100):.1f}%",
                "percentage_increase_characters": f"{((raw['prompt_characters'] - optimised['prompt_characters']) / optimised['prompt_characters'] * 100):.1f}%"
            },
            "control_to_raw": {
                "word_increase": raw["prompt_words"] - control["prompt_words"],
                "character_increase": raw["prompt_characters"] - control["prompt_characters"],
                "percentage_increase_words": f"{((raw['prompt_words'] - control['prompt_words']) / control['prompt_words'] * 100):.1f}%",
                "percentage_increase_characters": f"{((raw['prompt_characters'] - control['prompt_characters']) / control['prompt_characters'] * 100):.1f}%"
            }
        },
        "output_progression": {
            "control_to_optimised": {
                "word_increase": optimised["output_words"] - control["output_words"],
                "character_increase": optimised["output_characters"] - control["output_characters"],
                "percentage_increase_words": f"{((optimised['output_words'] - control['output_words']) / control['output_words'] * 100):.1f}%",
                "percentage_increase_characters": f"{((optimised['output_characters'] - control['output_characters']) / control['output_characters'] * 100):.1f}%"
            },
            "optimised_to_raw": {
                "word_increase": raw["output_words"] - optimised["output_words"],
                "character_increase": raw["output_characters"] - optimised["output_characters"],
                "percentage_increase_words": f"{((raw['output_words'] - optimised['output_words']) / optimised['output_words'] * 100):.1f}%",
                "percentage_increase_characters": f"{((raw['output_characters'] - optimised['output_characters']) / optimised['output_characters'] * 100):.1f}%"
            },
            "control_to_raw": {
                "word_increase": raw["output_words"] - control["output_words"],
                "character_increase": raw["output_characters"] - control["output_characters"],
                "percentage_increase_words": f"{((raw['output_words'] - control['output_words']) / control['output_words'] * 100):.1f}%",
                "percentage_increase_characters": f"{((raw['output_characters'] - control['output_characters']) / control['output_characters'] * 100):.1f}%"
            }
        },
        "key_insights": {
            "prompt_optimization_effectiveness": f"The optimised run produced {((optimised['output_words'] - control['output_words']) / control['output_words'] * 100):.1f}% more detailed output compared to the control.",
            "diminishing_returns": f"While the raw prompt was {((raw['prompt_words'] - control['prompt_words']) / control['prompt_words'] * 100):.0f}% longer than control, it only produced {((raw['output_words'] - control['output_words']) / control['output_words'] * 100):.0f}% more output, suggesting diminishing returns.",
            "optimal_sweet_spot": f"The optimised approach appears effective - {((optimised['prompt_words'] - control['prompt_words']) / control['prompt_words'] * 100):.0f}% longer prompt resulted in {((optimised['output_words'] - control['output_words']) / control['output_words'] * 100):.0f}% more comprehensive output."
        }
    }
    
    return analysis

def main():
    """Main function to generate runs.json."""
    base_path = Path("/home/daniel/repos/github/Long-Prompting-Simple-Demo")
    runs_path = base_path / "experiment-results" / "runs" / "text"
    
    # Initialize the main data structure
    runs_json = {
        "metadata": {
            "created": datetime.now().isoformat(),
            "description": "AI experiment runs comparing different prompt optimization approaches for voice-generated prompts",
            "total_runs": 3,
            "script_version": "1.0"
        },
        "runs": {}
    }
    
    # Process each run
    run_names = ["control", "optimised", "raw"]
    for run_name in run_names:
        run_path = runs_path / run_name
        if run_path.exists():
            print(f"Processing {run_name} run...")
            runs_json["runs"][run_name] = process_run(run_path, run_name)
        else:
            print(f"Warning: {run_name} directory not found")
    
    # Calculate analysis
    if len(runs_json["runs"]) == 3:
        print("Calculating comparative analysis...")
        runs_json["analysis"] = calculate_analysis(runs_json["runs"])
    
    # Write the JSON file
    output_path = base_path / "runs.json"
    print(f"Writing complete runs.json to {output_path}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(runs_json, f, indent=2, ensure_ascii=False)
    
    print("✓ Complete runs.json generated successfully!")
    
    # Print summary
    print("\nSummary:")
    for run_name, run_data in runs_json["runs"].items():
        totals = run_data["totals"]
        print(f"  {run_name}: {totals['prompt_words']} prompt words → {totals['output_words']} output words")

if __name__ == "__main__":
    main()
