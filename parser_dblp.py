from datetime import datetime
import lxml.etree as etree
from sqlalchemy.exc import IntegrityError

from consts import (
    ConstsThesisTypes,
    thesis_types_map,
)
from db_connection import (
    DataBase,
    Thesis,
    ThesisType,
    Person,
    ThesisEE,
    ThesisUrl,
    Volume,
    Journal,
    Number,
)


class DBLP_DB_Parser(object):
    def __init__(self, xml_path='dblp.xml', db_path='baza_dblp.sqlite3'):
        self.iterator = etree.iterparse(
            xml_path,
            events=('start', 'end'),
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
            'author': self._dblp_handler,
            'title': self._title_handler,
            'pages': self._dblp_handler,
            'year': self._year_handler,
            'volume': self._dblp_handler,
            'journal': self._dblp_handler,
            'number': self._dblp_handler,
            'url': self._dblp_handler,
            'ee': self._dblp_handler,
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

    def _dblp_handler(self, event, elem, thesis):
        return thesis

    def _year_handler(self, event, elem, thesis):
        thesis.year = elem.text
        return thesis

    def _title_handler(self, event, elem, thesis):
        thesis.title = elem.text
        return thesis

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
