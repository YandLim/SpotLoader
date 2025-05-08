# Import the interface and .env
from interface import App
from dotenv import load_dotenv

load_dotenv(".env")

# Running the app
if __name__ == "__main__":
    app = App()
    app.mainloop()