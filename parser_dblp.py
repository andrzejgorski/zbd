import xml.etree.ElementTree as etree


class Thesis(object):
    THESIS_TYPES = [
        'article', 'inproceedings', 'proceedings',
        'book', 'incollection', 'phdthesis',
        'mastersthesis', 'www', 'person', 'data'
    ]

    SPECIAL_ATTRIBUTES = [
        'author', 'editor', 'title', 'booktitle', 'ee',
        'crossref', 'number', 'volume', 'journal', 'url',
    ]

    attributes_handler = [

    ]

    def __init__(self, connection, thesis_type):
        self.connection = connection
        if thesis_type in self.THESIS_TYPES:
            self.thesis_type = thesis_type
        else:
            raise Exception('Unknown thesis type')
        self.attributes = dict()

    def add_attribute(self, attribute, value):
        if not attribute in self.SPECIAL_ATTRIBUTES:
            handler_name = 'default'
        self.attributes[attribute] = value

    def save(self):
        pass


class DBLP_DB_Parser(object):
    def __init__(self, xml_path='dblp.xml', db_path='baza_dblp.sqlite3'):
        self.iterator = etree.iterparse(
            xml_path,
            events=('start', 'end', 'start-ns', 'end-ns')
        )
        db_url = 'sqlite:///:memory'
        self.count = dict()

    def parse(self):
        for event, elem in self.iterator:
            pair = (event, elem)
            print pair
            if pair in self.count.keys():
                self.count[pair] = self.count[pair] + 1
            else:
                self.count[pair] = 1

        import ipdb; ipdb.set_trace()


db_url = 'sqlite:///%s' % 'baza_dblp.sqlite3'

if __name__ == "__main__":
    parser = DBLP_DB_Parser('dblp.xml', 'baza_dblp.sqlite3')
    parser.parse()
