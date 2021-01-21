from .. import config

from sqlalchemy import (Boolean, Column, Date, ForeignKey, Integer,
                        LargeBinary, Text, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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
    supervisor = Column('supervisor', Integer,  ForeignKey('Users.userID'))
    # a pound.
    poundID = Column('poundID', Integer, ForeignKey('Pounds.poundID'))
    # The rescue that the animal is going to
    rescueID = Column('rescueID', Integer, ForeignKey('Rescues.rescueID'))
    # The stage that animal is in throughout the rescue process
    stage = Column('stage', Integer, nullable=False)
    # The date started this stage
    stageDate = Column("stageDate", Date)
    # The type of animal this record refers to
    animalType = Column('animalType', Text, nullable=False)
    # The name of the animal
    name = Column("name", Text)
    # The pound that the animal came from, if it came from
    notes = Column('notes', Text)
    #Relationships
    stageInfo = relationship("StageInfo", cascade="all, delete")
    radioAnswers = relationship("IntakeRadioAnswers", cascade="all, delete")
    checkBoxAnswers = relationship("IntakeCheckboxAnswers", cascade="all, delete")
    textAnswers = relationship("IntakeTextAnswers", cascade="all, delete")    
    files = relationship("Files", cascade="all, delete")
    
class StageInfo(Base):
    """
    This class is the stages table, which represents a date and note for each
    animal going through the substage. It is normalized, so one animal can 
    belong to many rows in this table.
    """
    __tablename__ = "StageInfo"
    animalID = Column('animalID', Integer, ForeignKey('Animals.animalID'),
                      nullable=False, primary_key=True)
    stageNum = Column("stageNum", Integer, primary_key=True, nullable=False)
    substageNum = Column("substageNum", Integer, primary_key=True, nullable=False)
    completionDate = Column("completionDate", Date, nullable=False)
    note = Column("note", Text)


class IntakeRadioAnswers(Base):
    """
    This class is the Intake Radio Answers Table, which represents all the
    questions asked in the forms that use a radio styled button. Radio style
    answers stores as an integer. It is normalized, so one animal can 
    belong to many rows in this table.
    """
    __tablename__ = "IntakeRadioAnswers"
    animalID = Column('animalID', Integer, ForeignKey('Animals.animalID'),
                      nullable=False, primary_key=True)
    questionName = Column("questionName", Text, primary_key=True, nullable=False)
    answer = Column("answer", Integer, nullable=False)


class IntakeTextAnswers(Base):
    """
    This class is the Intake Text Answers Table, which represents all the
    questions asked in the forms that use a text box style. Text style
    answers stores as text. It is normalized, so one animal can 
    belong to many rows in this table.
    """
    __tablename__ = "IntakeTextAnswers"
    animalID = Column('animalID', Integer, ForeignKey('Animals.animalID'),
                      nullable=False, primary_key=True)
    questionName = Column("questionName", Text, primary_key=True, nullable=False)
    answer = Column("answer", Text, nullable=False)


class IntakeCheckboxAnswers(Base):
    """
    This class is the Intake Checkbox Answers Table, which represents all the
    questions asked in the forms that use a check box style. Text style
    answers stores as boolean for each individual box in the question. 
    It is normalized, so one animal can belong to many rows in this table.
    """
    __tablename__ = "IntakeCheckboxAnswers"
    animalID = Column('animalID', Integer, ForeignKey('Animals.animalID'),
                      nullable=False, primary_key=True)
    subQuesitonName = Column("subQuestionName", Text, primary_key=True, nullable=False)
    answer = Column("answer", Boolean, nullable=False)


class Files(Base):
    """
    This class is the files table, which represents locations for each file.
    """
    __tablename__ = "Files"
    fileID = Column('fileID', Integer, primary_key=True,
                    autoincrement=True, unique=True, nullable=False)
    animalID = Column('animalID', Integer, ForeignKey(
        'Animals.animalID'), nullable=False)
    fileName = Column('name', Text, nullable=False)


class Pounds(Base):
    """
    This class is the pounds table, which represents information for each pound.
    """
    __tablename__ = "Pounds"
    poundID = Column('poundID', Integer, primary_key=True,
                     autoincrement=True, unique=True, nullable=False)
    poundName = Column('poundName', Text, nullable=False)
    # Some users are accounts tied to a specific pound
    users = relationship("Users", cascade="all, delete")


class Rescues(Base):
    """
    This class is the rescues table, which represents infromation for each rescue.
    """
    __tablename__ = "Rescues"
    rescueID = Column('rescueID', Integer, primary_key=True,
                      autoincrement=True, unique=True, nullable=False)
    rescueName = Column('rescueName', Text, nullable=False)
    # Some users are accounts tied to a specific rescue
    users = relationship("Users", cascade="all, delete")


class Users(Base):
    """
    This class is the users table, which represents information for each user.
    """
    __tablename__ = "Users"
    userID = Column('userID', Integer, primary_key=True,
                      autoincrement=True, unique=True, nullable=False)    
    username = Column('username', Text, unique=True, nullable=False)
    password = Column('password', LargeBinary, nullable=False)
    # 0 = Admin, 1 = NPLB user, 2 = SudoPound, 3 = Pound, 4 = SudoRescue, 5 = Rescue
    # SudoPound + SudoRescue both have ability to create new pound/rescue users.
    userLVL = Column('userLVL', Integer, nullable=False)
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
