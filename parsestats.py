import csv
import alchemy

class Player:
    """Class to keep track of an individual player and all pertinents stats of that player"""
    def __init__(self, name, at_bats, hits, doubles, triples, home_runs, walks, hit_by_pitches, RAA = 0, wOBA = 0, id = 0):
        self.name = name
        self.at_bats = int(at_bats)
        self.singles = int(hits) - int(doubles) - int(triples) - int(home_runs)
        self.doubles = int(doubles)
        self.triples = int(triples)
        self.home_runs = int(home_runs)
        self.walks = int(walks) + int(hit_by_pitches)
        self.RAA = RAA
        self.wOBA = wOBA
        self.id = id

    def __repr__(self):
        return  f"name: {self.name}, abs: {self.at_bats}, singles: {self.singles}, doubles: {self.doubles}, triples: {self.triples}, hrs: {self.home_runs}, walks: {self.walks}\n"


def parse_data(filename):
    """Function to parse a csv and return a list of player objects"""
    fields = []
    rows = []
    try:
        with open(filename, 'r') as csvfile:
            csvreader = csv.reader(csvfile)

            fields = next(csvreader)
            if fields[0] != "Player" or fields[1] != "AB" or fields[2] != "H" or fields[3] != "2B" or fields[4] != "3B" or fields[5] != "HR" or fields[6] != "BB" or fields[7] != "HBP":
                print("Invalid file format")
                return False

            for row in csvreader:
                rows.append(row)

            players = []
            i = alchemy.getMaxId() + 1
            for col in rows:
                new_player = Player(col[0], col[1], col[2], col[3], col[4], col[5], col[6], col[7], id = i)
                players.append(new_player)
                i += 1
    except:
        print("Error parsing file " + filename)
        return False


    return players

if __name__ == '__main__':
    parse_data("rock_2022.csv")