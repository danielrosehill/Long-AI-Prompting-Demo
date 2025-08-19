import json
import os

def count_words(text):
    """Counts the words in a given string."""
    return len(text.split())

def generate_runs_json(base_dir, output_file):
    """
    Generates a JSON file from the contents of subdirectories with word counts and ratios.

    Args:
        base_dir (str): The base directory containing the run subdirectories.
        output_file (str): The path to the output JSON file.
    """
    runs_data = []
    run_types = ['control', 'optimised', 'raw']

    for i, run_type in enumerate(run_types):
        run_path = os.path.join(base_dir, run_type)
        if not os.path.isdir(run_path):
            continue

        try:
            with open(os.path.join(run_path, 'details.txt'), 'r', encoding='utf-8') as f:
                description = f.read()
            with open(os.path.join(run_path, 'user-prompt.md'), 'r', encoding='utf-8') as f:
                user_prompt = f.read()
            with open(os.path.join(run_path, 'system-prompt.md'), 'r', encoding='utf-8') as f:
                system_prompt = f.read()
            with open(os.path.join(run_path, 'output.md'), 'r', encoding='utf-8') as f:
                ai_response = f.read()

            # Calculate word counts
            user_prompt_wc = count_words(user_prompt)
            system_prompt_wc = count_words(system_prompt)
            combined_prompt_wc = user_prompt_wc + system_prompt_wc
            output_wc = count_words(ai_response)
            ratio = round(output_wc / combined_prompt_wc, 4) if combined_prompt_wc > 0 else 0

            run_entry = {
                'run_number': i + 1,
                'run_name': run_type,
                'description': description.strip(),
                'user_prompt': user_prompt,
                'system_prompt': system_prompt,
                'ai_response': ai_response,
                'prompt_word_count_user': user_prompt_wc,
                'prompt_word_count_system': system_prompt_wc,
                'prompt_word_count_combined': combined_prompt_wc,
                'output_word_count': output_wc,
                'output_prompt_word_count_ratio': ratio
            }
            runs_data.append(run_entry)

        except FileNotFoundError as e:
            print(f"Warning: Could not process '{run_type}'. Missing file: {e.filename}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(runs_data, f, indent=4)

    print(f"Successfully generated {output_file} with new structure.")

if __name__ == "__main__":
    base_directory = 'experiment-results/runs/text/'
    output_json_file = 'runs.json'
    generate_runs_json(base_directory, output_json_file)
