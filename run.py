from dotenv import load_dotenv
import os

load_dotenv()

from game import app

app.debug = os.getenv("DEBUG", "False") == "True"

if __name__ == "__main__":
    app.run(debug=True)
