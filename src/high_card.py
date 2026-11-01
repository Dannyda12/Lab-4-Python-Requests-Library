import json
import logging
import sys 
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "lab4.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    force=True,
)

def main():
    logging.info("LAB4_START")

    try:
        response = requests.get(
            "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1",
            timeout=10
        )
        response.raise_for_status()

        deck_data = response.json()
        deck_id = deck_data["deck_id"]
        logging.info("LAB4_DECK_CREATE_OK")

        players = int(input("How many players? (Minimum 2): "))

        if players < 2 or players > 52:
            raise ValueError("Choose between 2 and 52 players.")

        draw_response = requests.get(
            f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={players}",
            timeout=10
        )
 
        draw_response.raise_for_status()

        draw_data = draw_response.json()
        cards = draw_data["cards"]
        logging.info("LAB4_DRAW_OK")

        rounds = [draw_data]

        values = {
            **{str(number): number for number in range(2, 11)},
            "JACK": 11,
            "QUEEN": 12,
            "KING": 13,
            "ACE": 14,
        }
        active_players = list(range(1, players + 1)) 
        current_cards = cards

        while True:
            for card in current_cards:
                card["rank"] = values[card["value"]]

            for index, card in zip(active_players, current_cards):
                print(f"Player {index}: {card['code']}")

            highest = max(card["rank"] for card in current_cards)

            winners = [
                card for card in current_cards
                if card["rank"] == highest
            ]

            if len(winners) == 1:
                winner_index = active_players[
                    current_cards.index(winners[0])
                ]
                break

            print("It's a tie!")
            logging.info("LAB4_TIE_ROUND")

            active_players = [
                active_players[current_cards.index(card)]
                for card in winners
            ]
            
            tied_players = len(active_players)
            print(f"{tied_players} players will draw again!")
            draw_response = requests.get(
                f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={tied_players}",
                timeout=10
            )
            draw_response.raise_for_status()
            logging.info("LAB4_DRAW_OK")

            tie_data = draw_response.json()
            rounds.append(json.loads(json.dumps(tie_data)))
            current_cards = tie_data["cards"]

        print(f"Player {winner_index} wins!")

        with open(
            DATA_DIR / "high_card_rounds.json", 
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(rounds, file, indent=2)
        with open(
            DATA_DIR / "high_card_result.txt",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(f"Player {winner_index} wins!\n")

        logging.info("LAB4_GAME_END")

    except (
        requests.RequestException,
        ValueError,
        OSError,
        KeyError,
        TypeError,
    ) as error:
        logging.error("LAB4_ERR %s", error)
        print("The game could not be completed.", file=sys.stderr)
        sys.exit(1)

    finally:
        logging.info("LAB4_END")

if __name__ == "__main__":
    main()
    
            