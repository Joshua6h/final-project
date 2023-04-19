import parsestats
import alchemy

def create_league(league_name):
    players = parsestats.parse_data(league_name + '.csv')

    p = alchemy.Players()
    for player in players:
        p.writeData(player, league_name)


if __name__ == "__main__":
    create_league("rock_2022")