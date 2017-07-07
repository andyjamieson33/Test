import pymysql, random
from sqlalchemy import create_engine, Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, drop_database, create_database, analyze

# Set the db connection details

Base = declarative_base()
engine = create_engine('mysql+pymysql://pythontest:databaseaccess@localhost/dd')

# Set global variables

images_root="images"
images_monsters=(images_root + "/monsters")

# Drop the DB and re-create

def reset_db():
    if database_exists(engine.url):
        print('Dropping database')
        drop_database(engine.url)
        print('Database dropped')
        print('Creating database')
        create_database(engine.url)
        print('Database created')
    else:
        print('Creating database')
        create_database(engine.url)
        print('Database created')

# Add the monsters in to the DB

def bootstrap_monsters():
    class Monsters(Base):
        __tablename__ = 'monsters'
        id = Column(Integer, primary_key=True)
        level = Column(Integer)
        name = Column(String(20))
        rogue = Column(Integer)
        cleric = Column(Integer)
        fighter = Column(Integer)
        wizard = Column(Integer)
        fireball = Column(Integer)
        lightning = Column(Integer)
        image = Column(String(20))

    print("Opening database session")
    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    s = session()

    print("Bootstrapping monsters")
    s.add(Monsters(level=1, name="Dire Rat", rogue=5, cleric=4, fighter=3, wizard=6, fireball=2, lightning=7, image="dire_rat"))
    s.add(Monsters(level=2, name="Giant Lizard", rogue=5, cleric=4, fighter=2, wizard=5, fireball=2, lightning=2, image="giant_lizard"))
    s.add(Monsters(level=3, name="Ogre", rogue=8, cleric=9, fighter=6, wizard=8, fireball=4, lightning=5, image="ogre"))
    s.add(Monsters(level=4, name="Troll", rogue=9, cleric=10, fighter=8, wizard=8, fireball=7, image="troll"))

    s.commit()
    print("Monsters bootstrapped")

    s.close()
    print("Closing database session")

# Role an X sided dice

def d_roll(sides):
    return random.randint(1,sides)

if __name__ == '__main__':
    reset_db()
    bootstrap_monsters()
