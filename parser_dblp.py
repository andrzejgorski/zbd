from datetime import datetime
import lxml.etree as etree
from sqlalchemy.exc import IntegrityError

from consts import (
    ConstsThesisTypes,
    thesis_types_map,
)
from db_connection import (
    BookTitle,
    Crossref,
    DataBase,
    Journal,
    Number,
    Person,
    Thesis,
    ThesisEE,
    ThesisPages,
    ThesisType,
    ThesisUrl,
    Volume,
)


def tag_handler(func):
    def wrapper(self, event, elem, thesis):
        if event == 'end':
            func(self, event, elem, thesis)
        return thesis
    return wrapper


class DBLP_DB_Parser(object):
    def __init__(self, xml_path='dblp.xml', db_path='baza_dblp.sqlite3'):
        self.iterator = etree.iterparse(
            xml_path,
            events=('start', 'end'),
            load_dtd=True,
        )
        db_url = 'sqlite:///%s' % db_path
        self.session = DataBase(db_url).get_session()
        self._prepare_handlers()
        self._add_thesis_types()
        self._update_thesis_type_map()

    def _add_thesis_types(self):
        if self.session.query(ThesisType).count() != 9:
            for thesis_type in thesis_types_map.values():
                self.session.add(thesis_type)
            self.session.commit()

    def _prepare_handlers(self):
        self.tag_handlers = {
            'dblp': self._dblp_handler,
            'author': self._author_handler,
            'title': self._title_handler,
            'pages': self._pages_handler,
            'year': self._year_handler,
            'volume': self._volume_handler,
            'journal': self._journal_hanlder,
            'number': self._number_handler,
            'url': self._url_handler,
            'ee': self._ee_handler,
            'editor': self._editor_handler,
            'crossref': self._crossref_handler,
            'booktitle': self._booktitle_handler,
            'isbn': self._dblp_handler,
            'series': self._dblp_handler,
            'publisher': self._dblp_handler,
        }
        thesis_keys = thesis_types_map.keys()
        for key in thesis_keys:
            self.tag_handlers[key] = self._thesis_handler

    def _update_thesis_type_map(self):
        thesis_keys = thesis_types_map.keys()
        for thesis_type in thesis_keys:
            thesis_types_map[thesis_type] = (
                self.session.query(ThesisType)
                .filter(ThesisType.type_name == thesis_type)
                .first()
            )

    def parse(self):
        thesis = None
        for event, elem in self.iterator:
            thesis = self.tag_handlers[elem.tag](event, elem, thesis)

        self.session.commit()
        self.session.close()

    @tag_handler
    def _dblp_handler(self, event, elem, thesis):
        pass

    def _get_person(self, name):
        person = (
            self.session.query(Person)
            .filter(Person.name == name)
            .first()
        )
        return person or Person(name=name)

    @tag_handler
    def _booktitle_handler(self, event, elem, thesis):
        booktitle = BookTitle(booktitle=elem.text)
        thesis.booktitle.append(booktitle)

    @tag_handler
    def _crossref_handler(self, event, elem, thesis):
        crossref = Crossref(crossref=elem.text)
        thesis.crossref.append(crossref)

    @tag_handler
    def _editor_handler(self, event, elem, thesis):
        person = self._get_person(elem.text)
        thesis.editors.append(person)

    @tag_handler
    def _author_handler(self, event, elem, thesis):
        person = self._get_person(elem.text)
        thesis.authors.append(person)

    @tag_handler
    def _pages_handler(self, event, elem, thesis):
        pages = ThesisPages(pages=elem.text)
        thesis.pages.append(pages)

    @tag_handler
    def _ee_handler(self, event, elem, thesis):
        ee = ThesisEE(ee=elem.text)
        thesis.ees.append(ee)

    @tag_handler
    def _url_handler(self, event, elem, thesis):
        url = ThesisUrl(url=elem.text)
        thesis.urls.append(url)

    @tag_handler
    def _number_handler(self, event, elem, thesis):
        number = Number(number=elem.text)
        thesis.number.append(number)

    @tag_handler
    def _journal_hanlder(self, event, elem, thesis):
        journal = Journal(journal=elem.text)
        thesis.journal.append(journal)

    @tag_handler
    def _volume_handler(self, event, elem, thesis):
        volume = Volume(volume=elem.text)
        thesis.volume.append(volume)

    @tag_handler
    def _year_handler(self, event, elem, thesis):
        thesis.year = elem.text

    @tag_handler
    def _title_handler(self, event, elem, thesis):
        thesis.title = elem.text

    def _get_thesis_attribs(self, elem):
        keys = ['key', 'mdate']
        result = {
            'key': elem.attrib['key'],
            'mdate': datetime.strptime(
                        elem.attrib['mdate'], '%Y-%m-%d').date(),
        }
        return result

    def _thesis_handler(self, event, elem, thesis):
        if event == 'start' and thesis is None:
            keys = self._get_thesis_attribs(elem)
            return Thesis(
                    thesis_type=thesis_types_map[elem.tag],
                    **keys
                )
        elif event == 'end' and thesis is not None:
            self.session.add(thesis)
            return None
        raise Exception('Error in thesis handler')


if __name__ == "__main__":
    parser = DBLP_DB_Parser('part.xml', 'baza_dblp.sqlite3')
    parser.parse()
