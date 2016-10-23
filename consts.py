from db_connection import ThesisType


class ConstsThesisTypes(object):
    """
    This class is a namespace for thesis types loaded to database
    by default.
    """

    ARTICLE = 'article'
    INPROCEEDINGS = 'inproceedings'
    PROCEEDINGS = 'proceedings'
    BOOK = 'book'
    INCOLLECTION = 'incollection'
    PHDTHESIS = 'phdthesis'
    MASTERSTHESIS = 'mastersthesis'
    WWW = 'www'
    DATA = 'data'


thesis_types_map = {
    ConstsThesisTypes.ARTICLE: ThesisType(type_name='article'),
    ConstsThesisTypes.INPROCEEDINGS: ThesisType(type_name='inproceedings'),
    ConstsThesisTypes.PROCEEDINGS: ThesisType(type_name='proceedings'),
    ConstsThesisTypes.BOOK: ThesisType(type_name='book'),
    ConstsThesisTypes.INCOLLECTION: ThesisType(type_name='incollection'),
    ConstsThesisTypes.PHDTHESIS: ThesisType(type_name='phdthesis'),
    ConstsThesisTypes.MASTERSTHESIS: ThesisType(type_name='mastersthesis'),
    ConstsThesisTypes.WWW: ThesisType(type_name='www'),
    ConstsThesisTypes.DATA: ThesisType(type_name='data'),
}
