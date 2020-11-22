from .. import config
from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(
    'postgressql://nplbam:{}@nplbam_db/nplbam'.format(config.DATABASE_KEY))


class Animals(Base):
    __tablename__ = "Animals"
    # Primary key for an animal
    animalID = Column('animalID', Integer, primary_key=True,
                      autoincrement=True, unique=True, nullable=False)
    # The stage that animal is in throughout the rescue process
    stage = Column('stage', Integer, nullable=False)
    # The type of animal this record refers to
    animalType = Column('animalType', Text, nullable=False)
    # The pound that the animal came from, if it came from
    # a pound.
    poundID = Column('poundID', Integer, nullable=False)
    # The rescue that the animal is going to
    rescueID = Column('rescueID', Integer)
    typeID = Column('typeID', Integer, nullable=False)
    # Entered the database
    stage0Finish = Column('stage0Finish', Date)
    # Stage 1
    stage1AFinish = Column('stage1AFinish', Date)
    stage1BFinish = Column('stage1BFinish', Date)
    stage1CFinish = Column('stage1CFinish', Date)
    stage1CNote = Column('stage1CNote', Text)
    stage1Finish = Column('stage1Finish', Date)
    # Stage 2
    stage2Finish = Column('stage2Finish', Date)
    stage2Note = Column('stage2Note', Text)
    # Stage 3
    stage3AFinish = Column('stage3AFinish', Date)
    stage3BFinish = Column('stage3BFinish', Date)
    stage3CFinish = Column('stage3CFinish', Date)
    stage3CNote = Column('stage3CNote', Text)
    stage3Finish = Column('stage3Finish', Date)
    # Stage 4
    stage4AFinish = Column('stage4AFinish', Date)
    stage4BFinish = Column('stage4BFinish', Date)
    stage4CFinish = Column('stage4CFinish', Date)
    stage4DFinish = Column('stage4DFinish', Date)
    stage4DNote = Column('stage4DNote', Text)
    stage4Finish = Column('stage4Finish', Date)
    # Stage 5
    stage5AFinish = Column('stage5AFinish', Date)
    stage5BFinish = Column('stage5BFinish', Date)
    stage5BNote = Column('stage5BNote', Text)
    stage5Finish = Column('stage5Finish', Date)
    # Stage 6
    stage6Finish = Column('stage6Finish', Date)
    stage6Note = Column('stage6Note', Text)
    # Stage 7
    stage7Finish = Column('stage7Finish', Date)
    stage7Note = Column('stage7Note', Text)
    # Stage 8
    stage8AFinish = Column('stage8AFinish', Date)
    stage8BFinish = Column('stage8BFinish', Date)
    stage8CFinish = Column('stage8CFinish', Date)
    stage8DFinish = Column('stage8DFinish', Date)
    stage8EFinish = Column('stage8EFinish', Date)
    stage8Finish = Column('stage8Finish', Date)


class Dog(Base):
    __tablename__ = "Dog"
    animalID = Column('animalID', Integer, ForeignKey(
        'Animals.animalID'), nullable=False, unique=True, primary_key=True)
    typeID = Column('typeID', Integer, nullable=False)
    poundID = Column('poundID', Integer, nullable=False)


def create_database_if_not_exists():
    """
    Build the above defined database
    """
    Base.metadata.create_all(bind=engine)


def get_db_engine():
    """
    Return the database engine
    """
    create_database_if_not_exists()
    return engine
