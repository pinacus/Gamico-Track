import requests

class GoogleSheet:
    def __init__(self, sheety_api_url):
        self.endpoint_url = sheety_api_url
        self.api_header = "Bearer sdifwfndsnovslk"
        self.get_sheet_data()

    def sheet(self, game_data):

        header = {

            "Authorization": self.api_header

        }

        body = {

            "sheet1": {
                "date": game_data["date"],
                "gameTitle": game_data["game_title"],
                "targetPrice": game_data["target_price"],
                "currentPrice": game_data.get("current_price", ""),
                "gameId": game_data.get("game_id", ""),
            }

        }

        response = requests.post(url=self.endpoint_url, headers=header, json=body)
        response.raise_for_status()

    def get_sheet_data(self):
        if not self.endpoint_url:
            return []

        header = {

            "Authorization": self.api_header

        }

        response = requests.get(url=self.endpoint_url, headers=header)
        response.raise_for_status()

        self.google_sheet_data = response.json()

        return self.google_sheet_data.get("sheet1", [])


    def upload_new_deal(self, new_deal_price, row_id):

            put_url = f"{self.endpoint_url}/{row_id}"

            body = {
                "sheet1":{
                    "currentPrice": new_deal_price
                }
            }

            header = {

                "Authorization": self.api_header

            }

            response = requests.put(url=put_url, headers=header, json=body)
            response.raise_for_status()
