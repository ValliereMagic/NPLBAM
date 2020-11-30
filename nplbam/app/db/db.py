from .. import config
from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey, \
    Date, ARRAY, Boolean, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine(
    'postgres://nplbam:{}@nplbam_db/nplbam'.format(config.DATABASE_KEY))


class Animals(Base):
    """
    This class is the animal table, which represents
    the basic information created by the system
    """
    __tablename__ = "Animals"
    # Primary key for an animal
    animalID = Column('animalID', Integer, primary_key=True,
                      autoincrement=True, unique=True, nullable=False)
    supervisor = Column('supervisor', Text,  ForeignKey('Users.userID'))
    # a pound.
    poundID = Column('poundID', Integer, ForeignKey('Pounds.poundID'))
    # The rescue that the animal is going to
    rescueID = Column('rescueID', Integer, ForeignKey('Rescues.rescueID'))

    # The stage that animal is in throughout the rescue process
    stage = Column('stage', Integer, nullable=False)
    # The type of animal this record refers to
    animalType = Column('animalType', Text, nullable=False)
    # The pound that the animal came from, if it came from

    notes = Column('notes', Text)
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
    """
    This class is the dog table, which represents the information given by the pounds for dogs.
    """
    __tablename__ = "Dog"
    animalID = Column('animalID', Integer, ForeignKey('Animals.animalID'),
                      nullable=False, unique=True, primary_key=True)
    poundID = Column('poundID', Integer, nullable=False)
    name = Column('name', Text)
    inDate = Column('inDate', Date)
    releaseDate = Column('releaseDate', Date)
    age = Column('age', Text)
    weight = Column('weight', Integer)
    breed = Column('breed', Text)
    colour = Column('colour', Text)
    markings = Column('markings', Text)
    # Visual Health of Animal
    visualFace = Column('visualFace', Text)
    visualNose = Column('visualNose', Text)
    visualTeeth = Column('visualTeeth', Text)
    visualEars = Column('visualEars', Text)
    visualEyes = Column('visualEyes', Text)
    visualNeck = Column('visualNeck', Text)
    visualAbdomen = Column('visualAbdomen', Text)
    visualTail = Column('visualTail', Text)
    visualLegs = Column('visualLegs', Text)
    visualPaws = Column('visualPaws', Text)
    visualNails = Column('visualNails', Text)
    visualCoat = Column('visualCoat', Text)
    visualOther = Column('visualOther', Text)
    notes = Column('notes', Text)
    #
    # Stored as int for as pseudo enum
    # 0 = Stray, 1 = Surrender
    status = Column('status', Integer)
    # 0 = Male, 1 = Female, 2 = IDK
    sex = Column('sex', Integer)
    # 0 = Male, 1 = Female, 2 = IDK
    sterilized = Column('sterilized', Integer)
    # 0 = Yes, 1 = No, 2 = IDK
    inHeat = Column('inHeat', Integer)
    # 0 = Yes, 1 = No, 2 = IDK
    visibleParasites = Column('visibleParasites', Integer)
    # 0 = Yes, 1 = No, 2 = IDK
    microChip = Column('microChip', Integer)
    # 0 = Yes, 1 = No, 2 = IDK
    cratedBarking = Column('cratedBarking', Integer)
    # 0 = Normal, 1 = Soft, 2 = Diarrhea, 3 = IDK
    stool = Column('stool', Integer)
    # 0 = Never, 1 = Hardly, 2 = Often, 3 = Constantly, 4 = IDK
    vocal = Column('vocal', Integer)
    # Using an array to store these fields as many of them may be chosen
    # [0]=Aggresive, [1]=Uneasy, [2]=Fearful, [3]=Tolerant, [4]=Relaxed, [5]=IDK
    temperamentPaw = Column('temperamentPaw', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Uneasy, [2]=Fearful, [3]=Tolerant, [4]=Relaxed, [5]=IDK
    temperamentAbdomen = Column('temperamentAbdomen', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Uneasy, [2]=Fearful, [3]=Tolerant, [4]=Relaxed, [5]=IDK
    temperamentFace = Column('temperamentFace', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Uneasy, [2]=Fearful, [3]=Tolerant, [4]=Relaxed, [5]=IDK
    temperamentNose = Column('temperamentNose', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Uneasy, [2]=Fearful, [3]=Tolerant, [4]=Relaxed, [5]=IDK
    temperamentEars = Column('temperamentEars', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Uneasy, [2]=Fearful, [3]=Tolerant, [4]=Relaxed, [5]=IDK
    temperamentHead = Column('temperamentHead', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Uneasy, [2]=Fearful, [3]=Tolerant, [4]=Relaxed, [5]=IDK
    temperamentNeck = Column('temperamentNeck', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Uneasy, [2]=Fearful, [3]=Tolerant, [4]=Relaxed, [5]=IDK
    temperamentHindQuarters = Column('temperamentHindQuarters', ARRAY(Boolean))
    # [0]=Growl, [1]=Bark, [2]=Calm, [3]=Fearful, [4]=Excited, [5]=IDK
    cratedGreeting = Column('cratedGreeting', ARRAY(Boolean))
    # [0]=Eats immediately, [1]=Eats off floor, [2]=Does not eat, [3]=IDK
    cratedFood = Column('cratedFood', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Dominant, [2]=Excited, [3]=Calm, [4]=Submissive, [5]=Polite,
    # [6]=Playful, [7]=IDK
    behaviourWithDogs = Column('behaviourWithDogs', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Fearful, [2]=Shy, [3]=Outgoing, [4]=IDK
    dispositionOverall = Column('dispositionOverall', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Fearful, [2]=Shy, [3]=Outgoing, [4]=Affectionate,
    # [5]=Independent, [6]=IDK
    dispositionStranger = Column('dispositionStranger', ARRAY(Boolean))
    # [0]=Aggresive, [1]=Glutton, [2]=Fussy, [3]=Nibbler, [4]=Protective, [5]=IDK
    dispositionFood = Column('dispositionFood', ARRAY(Boolean))
    # [0]=Selective, [1]=Playful, [2]=Destructive, [3]=Possessive, [4]=Uninterested
    # [5]=IDK
    dispositionToy = Column('dispositionToy', ARRAY(Boolean))
    # [0]=Pulls, [1]=Unfamiliar, [2]=Polite, [3]=Chews, [4]=IDK
    dispositionLeash = Column('dispositionLeash', ARRAY(Boolean))
    # [0]=Sit, [1]=Paw, [2]=Lie Down, [3]=Stay, [4]=IDK
    commands = Column('commands', ARRAY(Boolean))


class Files(Base):
    """
    This class is the files table, which represents locations for each file.
    """
    __tablename__ = "Files"
    fileID = Column('fileID', Integer, primary_key=True,
                    autoincrement=True, unique=True, nullable=False)
    animalID = Column('animalID', Integer, ForeignKey(
        'Animals.animalID'), nullable=False)
    fileName = Column('name', Text)


class Pounds(Base):
    """
    This class is the pounds table, which represents information for each pound.
    """
    __tablename__ = "Pounds"
    poundID = Column('poundID', Integer, primary_key=True,
                     autoincrement=True, unique=True, nullable=False)
    poundName = Column('poundName', Text)


class Rescues(Base):
    """
    This class is the rescues table, which represents infromation for each rescue.
    """
    __tablename__ = "Rescues"
    rescueID = Column('rescueID', Integer, primary_key=True,
                      autoincrement=True, unique=True, nullable=False)
    rescueName = Column('rescueName', Text)


class Users(Base):
    """
    This class is the users table, which represents information for each user.
    """
    __tablename__ = "Users"
    userID = Column('userID', Text, primary_key=True,
                    unique=True, nullable=False)
    password = Column('password', LargeBinary)
    # 0 = Admin, 1 = NPLB user, 2 = SudoPound, 3 = Pound, 4 = SudoRescue, 5 = Rescue
    # SudoPound + SudoRescue both have ability to create new pound/rescue users.
    userLVL = Column('userLVL', Integer)
    rescueID = Column('rescueID', Integer, ForeignKey('Rescues.rescueID'))
    poundID = Column('poundID', ForeignKey('Pounds.poundID'))


# Missing the Meta Table which represents quick information about the database.


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


create_database_if_not_exists()
