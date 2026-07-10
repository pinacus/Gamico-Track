import smtplib
import requests
import json

from Sheet.google_sheet import GoogleSheet
from game_search import GameSearch

class NotificationManager:
    def __init__(self):
        with open("GUI/data.json", "r") as file:
            user_data = json.load(file)

        self.from_email = user_data.get("app email")
        self.from_email_password = user_data.get("app password")
        self.to_email = user_data.get("email")
        self.api_url = user_data.get("api url")

        self.steam_url = GameSearch().steam_price_url

        if self.api_url:
            self.check_deal = GoogleSheet(self.api_url)
        else:
            self.check_deal = None

    def send_email(self):
        if not self.check_deal:
            return

        games_sheet = self.check_deal.get_sheet_data()

        if games_sheet:
                for games_list in games_sheet:
                    steam_id = games_list.get("gameId")
                    row_id = games_list.get("id")
                    current_price = int(games_list.get("currentPrice"))
                    target_price = int(games_list.get("targetPrice"))

                    params = {

                        "appids":steam_id,
                        "cc":"in",
                        "filters":"price_overview"

                    }

                    response = requests.get(url=self.steam_url, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()

                    price_info = data.get(str(steam_id), {}).get("data", {}).get("price_overview")

                    new_deal_price = price_info["final"] / 100
                    self.check_deal.upload_new_deal(new_deal_price, row_id)

                    if current_price <= target_price:
                        game_title = games_list.get("gameTitle")
                        message_context = f"{game_title} is currently at you favored price right now at Rs.{current_price} on steam."

                        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                            connection.starttls()
                            connection.login(user=self.from_email, password=self.from_email_password)
                            connection.sendmail(

                                from_addr=self.from_email,
                                to_addrs=self.to_email,
                                msg=f"Subject:Time to buy that game!\n\n{message_context}"

                            )


if __name__ == "__main__":
    notification = NotificationManager()

    notification.send_email()
