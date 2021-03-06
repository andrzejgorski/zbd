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
    PersonExtraInfo,
    Person,
    Thesis,
    ThesisEE,
    ThesisExtraInfo,
    ThesisPages,
    ThesisType,
    ThesisUrl,
    Volume,
)


def tag_handler(func):
    def wrapper(self, event, elem, thesis):
        if event == 'start':
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
            'author': self._author_handler,
            'booktitle': self._booktitle_handler,
            'crossref': self._crossref_handler,
            'dblp': self._dblp_handler,
            'editor': self._editor_handler,
            'ee': self._ee_handler,
            'journal': self._journal_hanlder,
            'number': self._number_handler,
            'pages': self._pages_handler,
            'title': self._title_handler,
            'url': self._url_handler,
            'volume': self._volume_handler,
            'year': self._year_handler,

            # For extra infos
            'address': self._extra_info_handler,
            'cdrom': self._extra_info_handler,
            'chapter': self._extra_info_handler,
            'cite': self._extra_info_handler,
            'isbn': self._extra_info_handler,
            'month': self._extra_info_handler,
            'note': self._extra_info_handler,
            'publisher': self._extra_info_handler,
            'publnr': self._extra_info_handler,
            'school': self._extra_info_handler,
            'series': self._extra_info_handler,
            'sub': self._title_content_handler,
            'sup': self._title_content_handler,
            'i': self._title_content_handler,
            'tt': self._title_content_handler,
            'ref': self._title_content_handler,
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
            try:
                thesis = self.tag_handlers[elem.tag](event, elem, thesis)
            except Exception as e:
                if thesis:
                    thesis_repr = thesis.__dict__
                else:
                    thesis_repr = '< no thesis >'
                error = (
                    'Error while processing thesis: %s\n' % thesis_repr
                    + 'Error content:\n%s\n' % str(e)
                )
                print error
                with open("errors", "a") as errors_file:
                    errors_file.write(error)
                thesis = None

        self.session.close()

    @tag_handler
    def _dblp_handler(self, event, elem, thesis):
        pass

    @tag_handler
    def _extra_info_handler(self, event, elem, thesis):
        extra_info = ThesisExtraInfo(key=elem.tag, value=elem.text)
        thesis.extra_infos.append(extra_info)

    @tag_handler
    def _booktitle_handler(self, event, elem, thesis):
        booktitle = (
            self.session.query(BookTitle)
            .filter(BookTitle.booktitle == elem.text)
            .first()
        )
        booktitle = booktitle or BookTitle(booktitle=elem.text)
        thesis.booktitle.append(booktitle)

    @tag_handler
    def _crossref_handler(self, event, elem, thesis):
        crossref = (
            self.session.query(Crossref)
            .filter(Crossref.crossref == elem.text)
            .first()
        )
        crossref = crossref or Crossref(crossref=elem.text)
        thesis.crossref.append(crossref)

    def _get_person(self, name):
        person = (
            self.session.query(Person)
            .filter(Person.name == name)
            .first()
        )
        return person or Person(name=name)

    def _add_person_extra_infos(self, elem, person):
        for key in elem.attrib.keys():
            person.extra_infos.append(
                PersonExtraInfo(key=key, value=elem.attrib[key]))

    @tag_handler
    def _editor_handler(self, event, elem, thesis):
        person = self._get_person(elem.text)
        self._add_person_extra_infos(elem, person)
        thesis.editors.append(person)

    @tag_handler
    def _author_handler(self, event, elem, thesis):
        person = self._get_person(elem.text)
        self._add_person_extra_infos(elem, person)
        thesis.authors.append(person)

    @tag_handler
    def _pages_handler(self, event, elem, thesis):
        pages = (
            self.session.query(ThesisPages)
            .filter(ThesisPages.pages == elem.text)
            .first()
        )
        pages = pages or ThesisPages(pages=elem.text)
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
        number = (
            self.session.query(Number)
            .filter(Number.number == elem.text)
            .first()
        )
        number = number or Number(number=elem.text)
        thesis.number.append(number)

    @tag_handler
    def _journal_hanlder(self, event, elem, thesis):
        journal = (
            self.session.query(Journal)
            .filter(Journal.journal == elem.text)
            .first()
        )
        journal = journal or Journal(journal=elem.text)
        thesis.journal.append(journal)

    @tag_handler
    def _volume_handler(self, event, elem, thesis):
        volume = (
            self.session.query(Volume)
            .filter(Volume.volume == elem.text)
            .first()
        )
        volume = volume or Volume(volume=elem.text)
        thesis.volume.append(volume)

    @tag_handler
    def _year_handler(self, event, elem, thesis):
        thesis.year = elem.text

    @tag_handler
    def _title_handler(self, event, elem, thesis):
        thesis.title = elem.text
        if not thesis.title:
            thesis.title = ''

    @tag_handler
    def _title_content_handler(self, event, elem, thesis):
        text = elem.text or ''
        thesis.title += text

    def _get_thesis_attrs(self, elem):
        thesis_attrs = {
            'key': elem.attrib.get('key'),
            'mdate': datetime.strptime(
                        elem.attrib.get('mdate'), '%Y-%m-%d').date(),
        }
        return thesis_attrs

    def _get_thesis_extra_infos(self, elem):
        attrs_keys = ['key', 'mdate']
        extra_infos = list()
        for key in list(set(elem.attrib.keys()) - set(attrs_keys)):
            extra_infos.append(ThesisExtraInfo(key=key, value=elem.attrib[key]))
        return extra_infos

    def _thesis_handler(self, event, elem, thesis):
        if event == 'start' and thesis is None:
            keys = self._get_thesis_attrs(elem)
            thesis = Thesis(thesis_type=thesis_types_map[elem.tag], **keys)
            for extra_info in self._get_thesis_extra_infos(elem):
                thesis.extra_infos.append(extra_info)
            return thesis
        elif event == 'end' and thesis is not None:
            self.session.add(thesis)
            self.session.commit()
            return None
        raise Exception('Error in thesis handler')


if __name__ == "__main__":
    parser = DBLP_DB_Parser('dblp.xml', 'baza_dblp.sqlite3')
    parser.parse()
