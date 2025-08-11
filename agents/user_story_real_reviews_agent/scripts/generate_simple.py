#!/usr/bin/env python3
"""
Simple User Story Generator Script from Customer Reviews (No external dependencies)

This script reads customer review CSV files, combines them with system prompts and examples,
then uses Claude API to generate detailed user personas based on real customer experiences.
"""

import json
import os
import sys
import urllib.request
import urllib.parse
import csv
from datetime import datetime
from pathlib import Path

def load_config():
    """Load configuration from config.json"""
    config_path = Path(__file__).parent.parent / "config.json"
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("Error: config.json not found. Please create it with your API key.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: config.json is not valid JSON.")
        sys.exit(1)

def load_file(file_path):
    """Load content from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def load_csv_reviews(file_path):
    """Load and parse CSV review file"""
    try:
        reviews = []
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                reviews.append(row)
        return reviews
    except FileNotFoundError:
        print(f"Error: CSV file not found: {file_path}")
        return []
    except Exception as e:
        print(f"Error reading CSV {file_path}: {e}")
        return []

def load_all_reviews(input_dir):
    """Load all CSV review files from input directory"""
    all_reviews = {
        'positive': [],
        'negative': [],
        'mixed': []
    }
    
    csv_files = list(input_dir.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {input_dir}")
        return all_reviews
    
    for csv_file in csv_files:
        print(f"Loading reviews from: {csv_file.name}")
        reviews = load_csv_reviews(csv_file)
        
        # Categorize reviews by filename or star rating
        if 'positive' in csv_file.name.lower():
            all_reviews['positive'].extend(reviews)
        elif 'negative' in csv_file.name.lower():
            all_reviews['negative'].extend(reviews)
        else:
            # Categorize by star rating if filename doesn't indicate sentiment
            for review in reviews:
                try:
                    stars = int(review.get('Stars', 0))
                    if stars >= 4:
                        all_reviews['positive'].append(review)
                    elif stars <= 2:
                        all_reviews['negative'].append(review)
                    else:
                        all_reviews['mixed'].append(review)
                except (ValueError, TypeError):
                    all_reviews['mixed'].append(review)
    
    return all_reviews

def format_reviews_for_prompt(reviews_data):
    """Format review data for Claude prompt"""
    formatted_content = "**CUSTOMER REVIEW DATA:**\n\n"
    
    # Positive Reviews Section
    if reviews_data['positive']:
        formatted_content += "### **POSITIVE REVIEWS (4-5 Stars):**\n\n"
        for i, review in enumerate(reviews_data['positive'][:15], 1):  # Limit to avoid token limits
            formatted_content += f"**Review {i}:**\n"
            formatted_content += f"- Username: {review.get('Username', 'Anonymous')}\n"
            formatted_content += f"- Stars: {review.get('Stars', 'N/A')}\n"
            formatted_content += f"- Location: {review.get('Area', 'Unknown')}\n"
            formatted_content += f"- Content: \"{review.get('Review Content', '')}\"\n\n"
    
    # Negative Reviews Section
    if reviews_data['negative']:
        formatted_content += "### **NEGATIVE REVIEWS (1-3 Stars):**\n\n"
        for i, review in enumerate(reviews_data['negative'][:15], 1):  # Limit to avoid token limits
            formatted_content += f"**Review {i}:**\n"
            formatted_content += f"- Username: {review.get('Username', 'Anonymous')}\n"
            formatted_content += f"- Stars: {review.get('Stars', 'N/A')}\n"
            formatted_content += f"- Location: {review.get('Area', 'Unknown')}\n"
            formatted_content += f"- Content: \"{review.get('Review Content', '')}\"\n\n"
    
    # Mixed Reviews Section (if any)
    if reviews_data['mixed']:
        formatted_content += "### **MIXED REVIEWS (3 Stars):**\n\n"
        for i, review in enumerate(reviews_data['mixed'][:10], 1):  # Limit to avoid token limits
            formatted_content += f"**Review {i}:**\n"
            formatted_content += f"- Username: {review.get('Username', 'Anonymous')}\n"
            formatted_content += f"- Stars: {review.get('Stars', 'N/A')}\n"
            formatted_content += f"- Location: {review.get('Area', 'Unknown')}\n"
            formatted_content += f"- Content: \"{review.get('Review Content', '')}\"\n\n"
    
    # Summary Statistics
    total_positive = len(reviews_data['positive'])
    total_negative = len(reviews_data['negative'])
    total_mixed = len(reviews_data['mixed'])
    total_reviews = total_positive + total_negative + total_mixed
    
    formatted_content += f"### **REVIEW SUMMARY:**\n"
    formatted_content += f"- Total Reviews: {total_reviews}\n"
    formatted_content += f"- Positive (4-5 stars): {total_positive}\n"
    formatted_content += f"- Negative (1-2 stars): {total_negative}\n"
    formatted_content += f"- Mixed (3 stars): {total_mixed}\n\n"
    
    return formatted_content

def load_example_from_json():
    """Load the example from labeled JSON for system prompt"""
    example_path = Path(__file__).parent.parent / "5_labeled_json"
    
    # Look for any JSON file in the labeled directory
    try:
        json_files = list(example_path.glob("*.json"))
        if not json_files:
            print("Warning: No example JSON files found in 5_labeled_json/")
            return "No example available."
        
        # Use the first JSON file found
        with open(json_files[0], 'r', encoding='utf-8') as f:
            example_data = json.load(f)
        
        # Extract the user stories content for the prompt
        content = example_data['user_stories_content']
        
        example_text = f"""
**EXAMPLE OF 8.5/10 QUALITY USER PERSONAS FROM REVIEWS:**

{content['generated_personas']}

---

This example demonstrates the quality, depth, and emotional authenticity we're targeting. Notice how personas are grounded in real customer language, specific demographic details, and authentic emotional experiences.
"""
        return example_text
        
    except Exception as e:
        print(f"Warning: Could not load example from JSON: {e}")
        return "No example available."

def call_claude_api(prompt, config):
    """Call Claude API using urllib"""
    try:
        # Prepare the request
        url = "https://api.anthropic.com/v1/messages"
        
        data = {
            "model": config['model'],
            "max_tokens": config['max_tokens'],
            "temperature": config['temperature'],
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Convert to JSON
        json_data = json.dumps(data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        req.add_header('x-api-key', config['anthropic_api_key'])
        req.add_header('anthropic-version', '2023-06-01')
        
        print("Calling Claude API...")
        
        # Make the request
        with urllib.request.urlopen(req, json_data) as response:
            response_data = json.loads(response.read().decode('utf-8'))
            
        # Extract the content
        if 'content' in response_data and len(response_data['content']) > 0:
            return response_data['content'][0]['text']
        else:
            print("Error: Unexpected API response format")
            print("Response:", response_data)
            return None
            
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        error_body = e.read().decode('utf-8')
        print(f"Error details: {error_body}")
        return None
    except Exception as e:
        print(f"Error calling Claude API: {e}")
        return None

def generate_user_stories(reviews_content, system_prompt, example, config):
    """Generate user stories using Claude API"""
    # Construct the full prompt
    full_prompt = f"""
{system_prompt}

{example}

---

{reviews_content}

---

**INSTRUCTIONS:**
Transform the above customer review data into detailed user personas following the exact structure and quality demonstrated in the example. Extract authentic customer psychology, real pain points, genuine benefits, and actual demographics from the review language. Create 5-7 personas that represent different customer segments and experiences reflected in the review data.

Generate the user personas now:
"""

    return call_claude_api(full_prompt, config)

def save_output(content, output_dir):
    """Save generated content to unlabeled folder"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"userstories_reviews_{timestamp}.md"
    output_path = output_dir / filename
    
    try:
        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"User stories saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving output: {e}")
        return None

def get_project_paths(config_file="config.json"):
    """Get project-specific paths from configuration"""
    config_path = Path(__file__).parent.parent / config_file
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        project = config.get("current_project", None)
        
        if project:
            # New project-based structure
            return {
                "input_dir": Path(__file__).parent.parent / "1_input" / project,
                "system_assets_dir": Path(__file__).parent.parent / "2_system_assets" / project,
                "output_dir": Path(__file__).parent.parent / "3_unlabeled" / project
            }
        else:
            # Legacy structure (backward compatibility)
            return {
                "input_dir": Path(__file__).parent.parent / "1_input",
                "system_assets_dir": Path(__file__).parent.parent / "2_system_assets",
                "output_dir": Path(__file__).parent.parent / "3_unlabeled"
            }
    except:
        # Fallback to legacy structure
        return {
            "input_dir": Path(__file__).parent.parent / "1_input",
            "system_assets_dir": Path(__file__).parent.parent / "2_system_assets",
            "output_dir": Path(__file__).parent.parent / "3_unlabeled"
        }

def main():
    """Main execution function"""
    print("User Story Real Reviews Generator Starting...")
    
    # Get project-aware paths
    paths = get_project_paths()
    input_dir = paths["input_dir"]
    system_assets_dir = paths["system_assets_dir"]
    output_dir = paths["output_dir"]
    
    system_prompt_file = system_assets_dir / "system_prompt.md"
    
    # Check if input directory has CSV files
    csv_files = list(input_dir.glob("*.csv"))
    if not csv_files:
        print(f"Error: No .csv files found in {input_dir}")
        print("Please place customer review CSV files in 1_input/")
        sys.exit(1)
    
    print(f"Found {len(csv_files)} CSV file(s):")
    for file in csv_files:
        print(f"  - {file.name}")
    
    # Load configuration
    print("Loading configuration...")
    config = load_config()
    
    # Load reviews
    print("Loading customer reviews...")
    reviews_data = load_all_reviews(input_dir)
    
    total_reviews = len(reviews_data['positive']) + len(reviews_data['negative']) + len(reviews_data['mixed'])
    if total_reviews == 0:
        print("Error: No valid reviews found in CSV files")
        sys.exit(1)
    
    print(f"Loaded {total_reviews} total reviews:")
    print(f"  - Positive: {len(reviews_data['positive'])}")
    print(f"  - Negative: {len(reviews_data['negative'])}")
    print(f"  - Mixed: {len(reviews_data['mixed'])}")
    
    # Format reviews for prompt
    reviews_content = format_reviews_for_prompt(reviews_data)
    
    print("Loading system prompt...")
    system_prompt = load_file(system_prompt_file)
    if not system_prompt:
        sys.exit(1)
    
    print("Loading example...")
    example = load_example_from_json()
    
    # Generate user stories
    print("Generating user stories from reviews...")
    generated_content = generate_user_stories(reviews_content, system_prompt, example, config)
    if not generated_content:
        sys.exit(1)
    
    # Save output
    print("Saving output...")
    output_path = save_output(generated_content, output_dir)
    if not output_path:
        sys.exit(1)
    
    print(f"""
SUCCESS! User stories generated from customer reviews.

Input: {len(csv_files)} CSV file(s) with {total_reviews} reviews
Output: {output_path.name}
Location: 3_unlabeled/

Next steps:
1. Review the generated user stories in 3_unlabeled/
2. Evaluate and score them using scripts/evaluate.py
3. Move to 5_labeled_json/ when reviewed for system learning
""")

if __name__ == "__main__":
    main()