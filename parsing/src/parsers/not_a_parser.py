import json

def extract_mentions_with_news(data):
    mentions_dict = {}

    for timestamp, news in data.items():
        for mention in news["mentioned"]:
            if mention not in mentions_dict:
                mentions_dict[mention] = []
            mentions_dict[mention].append({
                "timestamp": timestamp,
                "source": news["source"],
                "text": news["text"]
            })

    return mentions_dict

def save_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Results successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving results: {e}")

def load_from_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return {}

# Load the existing news data from the specified file
news_data_file = "/Users/artem2284708/course_proj_hse/parsing/parsed/news_data.json"
news_data = load_from_json(news_data_file)

# Extract mentions from the loaded data
mentions_data = extract_mentions_with_news(news_data)

# Save the extracted mentions data to a new file
output_file = "~/course_proj_hse/parsing/parsed/mentions_data.json"
save_to_json(mentions_data, output_file)
