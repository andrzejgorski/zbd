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


thesis_crossref = Table(
    'thesis_crossref',
    Base.metadata,
    Column('thesis_id', ForeignKey('thesis.id'), primary_key=True),
    Column('crossref_id', ForeignKey('crossref.id'), primary_key=True),
)


thesis_booktitle = Table(
    'thesis_booktitle',
    Base.metadata,
    Column('thesis_id', ForeignKey('thesis.id'), primary_key=True),
    Column('booktitle_id', ForeignKey('booktitle.id'), primary_key=True),
    Column('pages', String),
)


thesis_number = Table(
    'thesis_number',
    Base.metadata,
    Column('thesis_id', ForeignKey('thesis.id'), primary_key=True),
    Column('number_id', ForeignKey('number.id'), primary_key=True),
)


thesis_volume = Table(
    'thesis_volume',
    Base.metadata,
    Column('thesis_id', ForeignKey('thesis.id'), primary_key=True),
    Column('volume_id', ForeignKey('volume.id'), primary_key=True),
)


thesis_journal = Table(
    'thesis_journal',
    Base.metadata,
    Column('thesis_id', ForeignKey('thesis.id'), primary_key=True),
    Column('journal_id', ForeignKey('journal.id'), primary_key=True),
)


thesis_author = Table(
    'thesis_author',
    Base.metadata,
    Column('thesis_id', ForeignKey('thesis.id'), primary_key=True),
    Column('person_id', ForeignKey('person.id'), primary_key=True),
)


thesis_editor = Table(
    'thesis_editor',
    Base.metadata,
    Column('thesis_id', ForeignKey('thesis.id'), primary_key=True),
    Column('person_id', ForeignKey('person.id'), primary_key=True),
)


class DataBase(object):
    def __init__(self, db_url):
        self.engine = create_engine(db_url, echo=True)
        self.session_class = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session_class()


class Thesis(Base):
    __tablename__ = 'thesis'

    id = Column(Integer, Sequence('thesis_id_seq'), primary_key=True)
    thesis_type_id = Column(Integer, ForeignKey('thesis_type.id'))
    key = Column(String)
    mdate = Column(Date)
    title = Column(String)
    year = Column(Integer)

    crossrefs = relationship('Crossref', secondary=thesis_crossref)
    booktitle = relationship('BookTitle', secondary=thesis_booktitle)
    number = relationship('Number', secondary=thesis_number)
    volume = relationship('Volume', secondary=thesis_volume)
    journal = relationship('Journal', secondary=thesis_journal)

    thesis_type = relationship('ThesisType')
    urls = relationship('ThesisUrl', back_populates='thesis')
    ees = relationship('ThesisEE', back_populates='thesis')
    extra_infos = relationship('ThesisExtraInfo')
    authors = relationship('Person', secondary=thesis_author)
    editors = relationship('Person', secondary=thesis_editor)


class ThesisType(Base):
    __tablename__ = 'thesis_type'

    id = Column(Integer, Sequence('thesis_type_id_seq'), primary_key=True)
    type_name = Column(String(20))


class Crossref(Base):
    __tablename__ = 'crossref'

    id = Column(Integer, Sequence('crossref_id_seq'), primary_key=True)
    crossref = Column(String(50))


class BookTitle(Base):
    __tablename__ = 'booktitle'

    id = Column(Integer, Sequence('booktitle_id_seq'), primary_key=True)
    booktitle = Column('booktitle', String(150))


class Number(Base):
    __tablename__ = 'number'

    id = Column(Integer, Sequence('number_id_seq'), primary_key=True)
    number = Column(String(40))


class Volume(Base):
    __tablename__ = 'volume'

    id = Column(Integer, Sequence('volume_id_seq'), primary_key=True)
    volume = Column(String(50))


class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, Sequence('journal_id_seq'), primary_key=True)
    journal = Column(String(40))


class ThesisUrl(Base):
    __tablename__ = 'thesis_url'

    id = Column(Integer, Sequence('thesis_url_id_seq'), primary_key=True)
    thesis_id = Column(Integer, ForeignKey('thesis.id'))
    thesis = relationship('Thesis', back_populates='urls')
    url = Column(String(100))


class ThesisEE(Base):
    __tablename__ = 'thesis_ee'

    id = Column(Integer, Sequence('thesis_ee_id_seq'), primary_key=True)
    thesis_id = Column(Integer, ForeignKey('thesis.id'))
    thesis = relationship('Thesis', back_populates='ees')
    ee = Column(String(100))


class ThesisExtraInfo(Base):
    __tablename__ = 'thesis_extra_info'

    id = Column(Integer, Sequence('thesis_extra_info_id_seq'), primary_key=True)
    thesis_id = Column(Integer, ForeignKey('thesis.id'))
    key = Column(String(20))
    value = Column(String(100))


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    name = Column(String(20))
    mdate = Column(Date)
    cdata = Column(String(40))


# Test code


def db_test():
    db_url = 'sqlite:///%s' % 'baza_dblp.sqlite3'
    db = DataBase(db_url)
    Base.metadata.create_all(db.engine)

    article = ThesisType(type_name='article')

    dummy_thesis = Thesis(
       key='dummy_key2', thesis_type=article, mdate=None, title='title', year=4)
    crossref = Crossref(crossref='dummy crossref')
    booktitle = BookTitle(booktitle='dummy booktitle')
    number = Number(number='dummy number')
    volume = Volume(volume='dummy volume')
    journal = Journal(journal='dummy journal')

    url1 = ThesisUrl(url='dummy url1')
    url2 = ThesisUrl(url='dummy url2')

    ee1 = ThesisEE(ee='dummy ee1')
    ee2 = ThesisEE(ee='dummy ee2')

    extra_info = ThesisExtraInfo(key='extra', value='very extra info')

    person1 = Person(name='Adam')
    person2 = Person(name='Bartek')
    person3 = Person(name='Cezary')

    dummy_thesis.crossrefs.append(crossref)
    dummy_thesis.booktitle.append(booktitle)
    dummy_thesis.number.append(number)
    dummy_thesis.volume.append(volume)
    dummy_thesis.journal.append(journal)

    dummy_thesis.urls.append(url1)
    dummy_thesis.urls.append(url2)

    dummy_thesis.ees.append(ee1)
    dummy_thesis.ees.append(ee2)

    dummy_thesis.extra_infos.append(extra_info)

    dummy_thesis.editors.append(person1)
    dummy_thesis.editors.append(person2)

    dummy_thesis.authors.append(person2)
    dummy_thesis.authors.append(person3)

    session = db.get_session()
    session.add(dummy_thesis)
    session.commit()



# db_test()
