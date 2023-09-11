from parsers.teammates_parser import TeammatesParser
from src.parsers.player_id_parser import PlayerIdParser

if __name__ == "__main__":
    player_parser = PlayerIdParser()
    letters = "abcdefghijklmnopqrstuvwxyz"
    player_counter = 0
    for letter in letters:
        player_parser.parse(letter)
        player_counter += len(player_parser.get_data())

    print(f"Found {player_counter} players")

