import json
import os
from datetime import datetime
import pandas as pd

def load_slang_data():
    df = pd.read_csv('slang_data/slang_list.csv')
    return df.to_dict(orient='records')  # [{...}, {...}, ...]

def load_user_history():
    if not os.path.exists('storage/user_history.json'):
        return {}
    with open('storage/user_history.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_user_history(history):
    with open('storage/user_history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def get_today_key():
    return datetime.now().strftime('%Y-%m-%d')
