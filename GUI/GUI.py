
import customtkinter
from PIL import Image
import os
from word2number import w2n
from datetime import date
import json

from Sheet.google_sheet import GoogleSheet
from game_search import GameSearch

FILE_PATH = "GUI/data.json"
IMG_PATH = "GUI/logo.png"

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

CONTAINER_COLOR = "#00ADB5"
BUTTON_COLOR = "#E13939"
TEXT_COLOR = "#1A1616"
SELECTION_BOX_COLOR = "#EEEEEE"

class GUI(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.game_manager = GameSearch()

        self.title("Gamico Track")
        self.geometry("620x620")
        self.resizable(False, False)

        self.email_var = customtkinter.StringVar()
        self.game_title_var = customtkinter.StringVar()
        self.target_price_var = customtkinter.StringVar()

        self.load_email()
        self.sheet_manager = None
        if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                saved_data = json.load(file)
                api_url = saved_data.get("api url", "")
                if api_url:
                    self.sheet_manager = GoogleSheet(api_url)

        self.interface()

    def trigger_popup(self,event):
        Popup(self)

    def interface(self):
        container = customtkinter.CTkFrame(self, corner_radius=20, fg_color=CONTAINER_COLOR)
        container.pack(fill="both",expand=True, padx=20, pady=20)

        logo = Image.open(IMG_PATH)
        logo_image = customtkinter.CTkImage(

            light_image=logo,
            dark_image=logo,
            size=(154,154),
        )

        logo_label = customtkinter.CTkLabel(container, text="", image=logo_image, cursor="hand2")
        logo_label.pack(pady=(20, 10))
        logo_label.bind("<Button-1>", self.trigger_popup)

        top_space = customtkinter.CTkLabel(container, text="")
        top_space.pack(pady=(20, 0))

        self.create_field(container, "Email", self.email_var)
        self.create_field(container, "Game Title", self.game_title_var)
        self.create_field(container, "Target Price ( ₹ )", self.target_price_var)

        save_button = customtkinter.CTkButton(

            container, text="Save",
            command=self.save_form,
            font=("Space mono", 14,),
            fg_color="transparent",
            text_color=TEXT_COLOR,
            hover_color=BUTTON_COLOR,
            border_color="black",
            border_width=2

        )
        save_button.pack(fill="none", pady=(12, 0), padx=0)

        self.status_label = customtkinter.CTkLabel(container, text="")
        self.status_label.pack(pady=(10, 0))

    def create_field(self, parent, label_text, variable):
        label = customtkinter.CTkLabel(

            parent, text=label_text, anchor="w",
            text_color=TEXT_COLOR,
            font=("", 14,"bold")

        )
        label.pack(fill="x", pady=(0, 4), padx=20)

        entry = customtkinter.CTkEntry(

            parent, textvariable=variable, height=37,
            fg_color=SELECTION_BOX_COLOR,
            text_color=TEXT_COLOR,
            justify="center",

        )
        entry.pack(fill="x", pady=(0, 12), padx=20)

    def save_email(self):
        with open(FILE_PATH, "r", encoding="utf-8") as file:
            save_email_data = json.load(file)
        save_email_data["email"] = self.email_var.get()
        with open(FILE_PATH, "w") as file:
            json.dump(save_email_data,file, indent=4)

    def load_email(self):
        if FILE_PATH:
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                saved_data = json.load(file)
                if isinstance(saved_data, dict):
                    self.email_var.set(saved_data.get("email", ""))


    def save_form(self):
        try:
            email = self.email_var.get().strip()
            game_title = self.game_title_var.get().strip()
            target_price = self.target_price_var.get().strip()

            if not email or not game_title or not target_price:
                raise ValueError("Kindly fill all details")

            if target_price.replace(".", "", 1).isdigit():
                price = float(target_price)
            else:
                try:
                    numeric_value = w2n.word_to_num(target_price)
                    price = float(numeric_value)
                except ValueError:
                    raise ValueError("Invalid input")


            game_data = {

                "game_title": game_title,
                "current_price": "",
                "target_price": price,
                "game_id": "",
                "date": date.today().strftime("%d/%m/%Y"),

            }

            self.save_email()

            self.game_manager.find_game_id(game_data)
            self.game_manager.steam_price(game_data)
            if self.sheet_manager is not None:
                self.sheet_manager.sheet(game_data)

            self.status_label.configure(text="Saved Successfully", text_color="dark green")
            self.status_label.after(3000, lambda:self.status_label.configure(text=""))

        except ValueError as error:
            self.status_label.configure(text=str(error), text_color="red")


class Popup(customtkinter.CTkToplevel):

    def __init__(self,parent):
        super().__init__(parent)
        self.title("Config")
        self.geometry("500x260")
        self.resizable(False, False)

        self.parent = parent

        self.sheety_api_url = customtkinter.StringVar()
        self.google_app_mail = customtkinter.StringVar()
        self.google_app_password = customtkinter.StringVar()

        self.popup_interface()

        self.attributes("-topmost", True)
        self.wait_visibility()
        self.grab_set()

        self.notification = None


    def popup_interface(self):
        container = customtkinter.CTkFrame(self, corner_radius=20, fg_color=CONTAINER_COLOR)
        container.pack(fill="both",expand=True, padx=20, pady=20)

        self.create_field(container, "API", self.sheety_api_url)
        self.create_field(container, "Email", self.google_app_mail)
        self.create_field(container, "Password", self.google_app_password)

        submit_button = customtkinter.CTkButton(

            container, text="Submit",
            command=self.submit_form,
            font=("Space mono", 14,),
            fg_color="transparent",
            text_color=TEXT_COLOR,
            hover_color=BUTTON_COLOR,
            border_color="black",
            border_width=2

        )
        submit_button.pack(fill="none", pady=(8, 0), padx=0)

        self.status_label = customtkinter.CTkLabel(container, text="")
        self.status_label.pack(pady=(10, 0))

    def create_field(self, parent, label_text, variable):

        row_frame = customtkinter.CTkFrame(parent, fg_color="transparent")
        row_frame.pack(fill="x", padx=25, pady=8)
        label = customtkinter.CTkLabel(

            row_frame,
            text=label_text,
            text_color=TEXT_COLOR,
            font=("", 14,"bold"),
            width=60,
            anchor="w"

        )
        label.pack(side="left", anchor="center")

        entry = customtkinter.CTkEntry(

            row_frame,
            textvariable=variable,
            height=30,
            fg_color=SELECTION_BOX_COLOR,
            text_color=TEXT_COLOR,
            width=280

        )
        entry.pack(pady=(0, 6), padx=20)

    def save_user_config(self):

        current_api_url = self.sheety_api_url.get()
        current_app_email = self.google_app_mail.get()
        current_app_password = self.google_app_password.get()

        data_format = {

            "app email":current_app_email,
            "api url":current_api_url,
            "app password":current_app_password

        }

        with open(FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data_format, file, indent=4)

    def submit_form(self):
        try:
            api_url = self.sheety_api_url.get().strip()
            app_email = self.google_app_mail.get().strip()
            app_password = self.google_app_password.get().strip()

            if not api_url or not app_email or not app_password:
                raise ValueError("Kindly fill all details")

            self.save_user_config()

            sheety_api = self.sheety_api_url.get()
            self.parent.sheet_manager = GoogleSheet(sheety_api)

            self.destroy()

        except ValueError as error:
            self.status_label.configure(text=str(error), text_color="red")


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
