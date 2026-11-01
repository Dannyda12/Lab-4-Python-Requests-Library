import json
import logging
import sys
from pathlib import Path

import requests

# Find the Lab 4 project folder
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Add this script's activity to the lab log
logging.basicConfig(
    filename=LOG_DIR / "lab4.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    force=True,
)


def main():
    try:
        response = requests.get(
            "https://icanhazdadjoke.com/",
            headers={"Accept": "application/json"},

            timeout=10,
        )
        if response.status_code != 200:
            logging.error("LAB4_ERR HTTP status: %s", response.status_code)
            sys.exit(1)

        logging.info("LAB4_JOKE_HTTP_OK")
        
        joke_data = response.json()
        joke = joke_data.get("joke")
        logging.info("LAB4_JOKE_JSON_OK")
        
        if not joke:
            logging.error("LAB4_ERR Missing joke in response")
            sys.exit(1)


        # Save the complete API response and the joke text
        with open(DATA_DIR / "joke.json", "w", encoding="utf-8") as file:
            json.dump(joke_data, file, indent=2)
         
        with open(DATA_DIR / "joke.txt", "w", encoding="utf-8") as file:
            file.write(joke + "\n")

           
        # Print only the joke to standard output
        print(joke)
        logging.info("LAB4_JOKE_PRINTED")

    except (requests.RequestException, ValueError, OSError) as error:
        logging.error("LAB4_ERR %s", error)
        print("Could not retrieve or save the joke.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    logging.info("LAB4_START")
    main()

   





            

           




