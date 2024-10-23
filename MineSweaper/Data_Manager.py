import json

class DataManager:
    def save(self, game_data):
        with open('data.json', 'w') as f:
            json.dump(game_data, f)
        return game_data

    def load(self):
        try:
            with open('data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
