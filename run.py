from game import app
from dotenv import load_dotenv
import os

load_dotenv()

app.debug = os.getenv("DEBUG", "False") == "True"
if __name__ == "__main__":
    app.run(debug=True)

import game.routes