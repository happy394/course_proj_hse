import json
import os
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from huggingface_hub import login


def _load_paths():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.abspath(os.path.join(base_dir, '..', '..'))
    news_file = os.path.join(parent_dir, 'parsed', 'news.json')
    player_file = os.path.join(parent_dir, 'parsed', 'player_advanced.json')
    return news_file, player_file


def _load_data(news_file, player_file):
    with open(news_file, 'r', encoding='utf-8') as f:
        news_dict = json.load(f)
    with open(player_file, 'r', encoding='utf-8') as f:
        player_data = json.load(f)
    return news_dict, player_data


def _initialize_model():
    login(token="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")
    tokenizer = AutoTokenizer.from_pretrained("artem2284708/basketball2_checkpoints")
    model = AutoModelForSequenceClassification.from_pretrained("artem2284708/basketball2_checkpoints")
    return pipeline("text-classification", model=model, tokenizer=tokenizer, truncation=True)


def _prepare_dataframe(player_data):
    data_list = [{"Player": name, **stats} for name, stats in player_data.items()]
    df = pd.json_normalize(data_list)
    df['pos'] = 0
    df['neu'] = 0
    df['neg'] = 0
    return df


def _is_valid_mention(mentioned, player_data):
    return (
        sum(name in player_data for name in mentioned) == 1 and
        not any(word in ['Frivolities', 'Injuries', 'Trade'] for word in mentioned) and
        len(mentioned) < 5
    )


def _classify_and_update(news_dict, player_data, df, classifier):
    for _, news in news_dict.items():
        mentioned = news.get('mentioned', [])
        if _is_valid_mention(mentioned, player_data):
            result = classifier(news['text'])[0]['label'].upper()

            for name in mentioned:
                if name in player_data:
                    row_idx = df.index[df['Player'] == name].tolist()
                    if not row_idx:
                        continue
                    idx = row_idx[0]

                    if result == 'NEGATIVE':
                        df.at[idx, 'neg'] += 1
                    elif result == 'NEUTRAL':
                        df.at[idx, 'neu'] += 1
                    elif result == 'POSITIVE':
                        df.at[idx, 'pos'] += 1
    return df


def _save_results(df, player_file):
    reversed_data = {
        row['Player']: row.drop(labels='Player').to_dict()
        for _, row in df.iterrows()
    }
    with open(player_file, 'w', encoding='utf-8') as f:
        json.dump(reversed_data, f, ensure_ascii=False, indent=4)


def news_classifier():
    news_file, player_file = _load_paths()
    news_dict, player_data = _load_data(news_file, player_file)
    classifier = _initialize_model()
    df = _prepare_dataframe(player_data)
    df = _classify_and_update(news_dict, player_data, df, classifier)
    _save_results(df, player_file)
