import json

def load_language(lang):
    with open(f"{lang}.json", "r") as file:
        return json.load(file)