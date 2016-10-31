from sqlalchemy import create_engine
from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    Sequence,
    String,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker,
    relationship,
)


Base = declarative_base()


thesis_author = Table(
    'thesis_author',
    Base.metadata,
    Column('thesis_id', ForeignKey('thesis.id'), primary_key=True),
    Column('person_id', ForeignKey('person.id'), primary_key=True),
)


class DataBase(object):
    def __init__(self, db_url):
        self.engine = create_engine(db_url, echo=False)
        self.session_class = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session_class()


class Thesis(Base):
    __tablename__ = 'thesis'

    id = Column(Integer, Sequence('thesis_id_seq'), primary_key=True)
    thesis_type_id = Column(Integer, ForeignKey('thesis_type.id'))
    thesis_type = relationship('ThesisType')
    # title = Column(String)

    authors = relationship('Person', secondary=thesis_author)


class ThesisType(Base):
    __tablename__ = 'thesis_type'

    id = Column(Integer, Sequence('thesis_type_id_seq'), primary_key=True)
    type_name = Column(String(20))


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    name = Column(String(20))


# Test code
