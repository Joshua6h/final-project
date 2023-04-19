import sqlalchemy as sqla
from sqlalchemy.orm import declarative_base, sessionmaker

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
    RAA = sqla.Column(name='RAA', type_=sqla.DECIMAL, nullable=True)
    wOBA = sqla.Column(name='wOBA', type_=sqla.DECIMAL, nullable=True)

    def writeData(self, player, league):
        session = createSession()

        new_row = Players(name=player.name,league=league, at_bats=player.at_bats, singles=player.singles, doubles=player.doubles, triples=player.triples, hrs=player.home_runs, walks=player.walks, RAA=player.RAA, wOBA=player.wOBA)
        session.add(new_row)
        session.commit()
        session.close()


    def readData(self, lname_filter=None):
        session = createSession()

        result = None
        # if lname_filter:
        #     result = session.query(Players).filter(Players.lastName == lname_filter).first()
        # else:
        result = session.query(Players).all()

        session.close()
        return result
    