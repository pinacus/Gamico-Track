import json
import requests

class GameSearch:
    def __init__(self):
        self.games_url = "https://www.cheapshark.com/api/1.0/games"
        self.steam_price_url = "https://store.steampowered.com/api/appdetails"
        self.game_id = ""
        self.deal_price = ""
        self.steam_id = ""

        with open("src/GUI/data.json", "r") as file:
            user_data = json.load(file)

        self.api_url = user_data.get("api url")

    def find_game_id(self, game_data):
        game_title = game_data.get("game_title", "").strip()

        params = {

            "title": game_title,
            "limit":1,

        }

        response = requests.get(url=self.games_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data:
            raise ValueError("Game not found")

        self.game_id = data[0]["gameID"]
        game_data["game_id"] = self.game_id

        self.steam_id = data[0]["steamAppID"]

        return self.game_id

    def steam_price(self, game_data):
        params = {

            "appids": self.steam_id,
            "cc": "in",
            "filters": "price_overview"

        }

        response = requests.get(url=self.steam_price_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        steam_data = data.get(str(self.steam_id), {})
        price_info = steam_data["data"]["price_overview"]

        self.deal_price = price_info["final"] / 100
        game_data["current_price"] = self.deal_price

        return self.deal_price
