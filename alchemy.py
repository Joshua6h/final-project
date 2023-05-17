import sqlalchemy as sqla
from sqlalchemy.orm import declarative_base, sessionmaker
import parsestats
import linear_weights_constants

Base = declarative_base()
filename = 'player_data.db3'


def createSession():
    try:
        engine = sqla.create_engine(f'sqlite:///{filename}')
        Session = sessionmaker(bind=engine)
        return Session()
    except:
        raise ConnectionError('Bad stuff happened')
    

class Players(Base):
    __tablename__ = "player"
    id = sqla.Column(name='id', type_=sqla.Integer, nullable=False, primary_key=True)
    name = sqla.Column(name='name', type_=sqla.Text, nullable=False)
    league = sqla.Column(name='league', type_=sqla.Text, nullable=False)
    at_bats = sqla.Column(name='at_bats', type_=sqla.Integer, nullable=False)
    singles = sqla.Column(name='singles', type_=sqla.Integer, nullable=False)
    doubles = sqla.Column(name='doubles', type_=sqla.Integer, nullable=False)
    triples = sqla.Column(name='triples', type_=sqla.Integer, nullable=False)
    hrs = sqla.Column(name='hrs', type_=sqla.Integer, nullable=False)
    walks = sqla.Column(name='walks', type_=sqla.Integer, nullable=False)
    RAA = sqla.Column(name='RAA', type_=sqla.Double, nullable=True)
    wOBA = sqla.Column(name='wOBA', type_=sqla.Double, nullable=True)

    def writeData(self, player, league):
        session = createSession()

        new_row = Players(id=player.id, name=player.name,league=league, at_bats=player.at_bats, 
                          singles=player.singles, doubles=player.doubles, triples=player.triples, 
                          hrs=player.home_runs, walks=player.walks, RAA=player.RAA, wOBA=player.wOBA)
        session.add(new_row)
        session.commit()
        session.close()


    def readData(self, league_filter=None, order_by="ab", ascdesc="desc", name_filter="", ab_min=0, ab_max=10000):
        session = createSession()

        result = None
        
        # set order
        order_dic = {"ab": Players.at_bats, "singles": Players.singles, "doubles": Players.doubles, "triples": Players.triples,
                     "home runs": Players.hrs, "walks": Players.walks, "raa": Players.RAA, "woba": Players.wOBA}

        order = order_dic[order_by]

        if ascdesc == "asc":
            order = order.asc()
        else:
            order = order.desc()
        
        
        if league_filter:
             result = session.query(Players).filter(Players.league == league_filter).\
                filter(Players.name.like(name_filter)).filter(Players.at_bats >= ab_min).\
                    filter(Players.at_bats <= ab_max).order_by(order).all()
        else:
            result = session.query(Players).\
                filter(Players.name.like(name_filter)).filter(Players.at_bats > ab_min).\
                    filter(Players.at_bats < ab_max).order_by(order).all()

        session.close()
        return result
    

    def readLeagueWideStats(self, league_name):
        session = createSession()
        result = session.query(sqla.func.sum(Players.at_bats), sqla.func.sum(Players.singles), sqla.func.sum(Players.doubles), sqla.func.sum(Players.triples), sqla.func.sum(Players.hrs), sqla.func.sum(Players.walks)).filter(Players.league == league_name)
        return result.first()
    
def getMaxId():
    session = createSession()
    result = session.query(Players).order_by(Players.id.desc())
    return result.first().id
    
def add_league_players(league_name):
    players = parsestats.parse_data(league_name + ".csv")
    player_table = Players()
    for player in players:
        player_table.writeData(player, league_name)

def get_all_league_players(league_name):
    players_table = Players()
    db_players = players_table.readData(league_filter=league_name)
    all_players = []
    for row in db_players:
        new_player = parsestats.Player(row.name, row.at_bats, row.singles + row.doubles + row.triples + row.hrs, 
                                       row.doubles, row.triples, row.hrs, row.walks, RAA=row.RAA, wOBA=row.wOBA, 
                                       hit_by_pitches=0, id=row.id)
        all_players.append(new_player)
    return all_players

def delete_league(league_name):
    with createSession() as session:
            session.query(Players).\
                filter(Players.league == league_name).delete()
            session.commit()

def update_player_RAA(player):
    engine = sqla.create_engine("sqlite:///player_data.db3")
    conn = engine.connect()
    metadata = sqla.MetaData()
    players = sqla.Table('player', metadata, autoload_with=engine)
    query = sqla.update(players).values(RAA = player.RAA).where(players.columns.id == player.id)
    conn.execute(query)
    conn.commit()

def update_player_wOBA(player):
    engine = sqla.create_engine("sqlite:///player_data.db3")
    conn = engine.connect()
    metadata = sqla.MetaData()
    players = sqla.Table('player', metadata, autoload_with=engine)
    query = sqla.update(players).values(wOBA = player.wOBA).where(players.columns.id == player.id)
    conn.execute(query)
    conn.commit()

def get_filtered_sorted_players(league_name, order="woba", ascdesc="desc", name_filter="", ab_min=0, ab_max=10000):
    name_filter = "%" + name_filter + "%"
    players_table = Players()
    db_players = players_table.readData(league_name, order, ascdesc, name_filter, ab_min, ab_max)
    filtered_players = []
    for row in db_players:
        new_player = parsestats.Player(row.name, row.at_bats, row.singles + row.doubles + row.triples + row.hrs, 
                                       row.doubles, row.triples, row.hrs, row.walks, RAA=row.RAA, wOBA=row.wOBA, 
                                       hit_by_pitches=0, id=row.id)
        filtered_players.append(new_player)
    return filtered_players

def get_league_stats(league_name):
        """Creates a season environment using all the players in a given table"""
        players = Players()

        output = players.readLeagueWideStats(league_name)

        probabilities = linear_weights_constants.create_season(output[0], output[1], output[2], output[3], output[4], output[5])


        return probabilities

if __name__ == "__main__":
    delete_league("rock_2022")
    print("Players: ")
    players = get_all_league_players("rock_2022")
    print(players)
    add_league_players("rock_2022")
    players = get_filtered_sorted_players("rock_2022", name_filter="", ab_min=35)
    print(players)
