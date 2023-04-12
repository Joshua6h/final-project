import csv

class Player:
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
    fields = []
    rows = []

    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        fields = next(csvreader)

        for row in csvreader:
            rows.append(row)

        print("Total no. of rows: %d"%csvreader.line_num)
        print("Field names are:" + ', '.join(field for field in fields))
        print("First five rows are:\n")
        for row in rows[:5]:
            for col in row:
                print(col),
            print('\n')

        players = []
        for col in rows:
            new_player = Player(col[0], col[1], col[2], col[3], col[4], col[5], col[6], col[7])
            players.append(new_player)

        for player in players[:5]:
            print(player)

    return players

if __name__ == '__main__':
    parse_data("rock_2022.csv")