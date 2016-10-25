
/* For each occourance count how many are in file */
CREATE TABLE 'thesis'(
    id INTEGER NOT NULL,
    thesis_type_id INTEGER,
    key VARCHAR(50),
    mdate DATE,
    title VARCHAR(300),              /* jest 5306116 */
    year INTEGER,                   /* jest 3515191 */
    PRIMARY KEY (id)
);

CREATE TABLE 'thesis_type'(
    id INTEGER NOT NULL,
    type_name VARCHAR(20) UNIQUE,
    /*
        This is enum implementation for sqlite
        article         - 0
        inproceedings   - 1
        proceedings     - 2
        book            - 3
        incollection    - 4
        phdthesis       - 5
        mastersthesis   - 6
        www             - 7
        data            - 8
    */
    PRIMARY KEY(id)
);

CREATE TABLE 'thesis_crossref'(
    thesis_id INTEGER NOT NULL,
    crossref_id INTEGER NOT NULL,
    PRIMARY KEY(thesis_id, crossref_id)
);

CREATE TABLE 'crossref'(
    /*
        possible values:        32911
        occurence:              1873183
        max value length:       59
    */
    id INTEGER NOT NULL,
    crossref VARCHAR(50),
    PRIMARY KEY(id)
);

CREATE TABLE 'thesis_booktitle'(
    thesis_id INTEGER NOT NULL,
    booktitle_id INTEGER NOT NULL,
    PRIMARY KEY(thesis_id, booktitle_id)
);

CREATE TABLE 'booktitle'(
    /*
        possible values:        6471
        occurence:              1946438
        max value length:       107
    */
    id INTEGER NOT NULL,
    booktitle VARCHAR(150),
    PRIMARY KEY(id)
);

CREATE TABLE 'thesis_number'(
    thesis_id INTEGER NOT NULL,
    number_id INTEGER NOT NULL,
    PRIMARY KEY(thesis_id, number_id)
);

CREATE TABLE 'number'(
    /*
        possible values:        616
        occurence:              1266449
        max value length:       29
    */
    id iNTEGER NOT NULL,
    number VARCHAR(40),
    PRIMARY KEY(id)
);

CREATE TABLE 'thesis_pages'(
    id INTEGER NOT NULL,
    thesis_id INTEGER NOT NULL,
    pages VARCHAR(40),
    PRIMARY KEY(id)
);

CREATE TABLE 'thesis_volume'(
    thesis_id INTEGER NOT NULL,
    volume_id INTEGER NOT NULL,
    PRIMARY KEY(thesis_id, volume_id)
);

CREATE TABLE 'volume'(
    /*
        possible values:        122684
        occurence:              1540783
        max value length:       39
    */
    id iNTEGER NOT NULL,
    volume VARCHAR(50),
    PRIMARY KEY(id)
);

CREATE TABLE 'thesis_journal'(
    thesis_id INTEGER NOT NULL,
    journal_id INTEGER NOT NULL,
    PRIMARY KEY(thesis_id, journal_id)
);

CREATE TABLE 'journal'(
    /*
        possible values:        765
        occurence:              1523881
        max value length:       31
    */
    id INTEGER NOT NULL,
    journal VARCHAR(40),
    PRIMARY KEY(id)
);

CREATE TABLE 'thesis_url'(
    /*
        occurene:               3513007
    */
    id INTEGER NOT NULL,
    thesis_id INTEGER NOT NULL,
    url VARCHAR(100),
    PRIMARY KEY(id)
);

CREATE TABLE 'thesis_ee'(
    id INTEGER NOT NULL,
    thesis_id INTEGER NOT NULL,
    ee VARCHAR(100),
    PRIMARY KEY(id)
);

CREATE TABLE 'thesis_extra_info'(
    id INTEGER NOT NULL,
    thesis_id INTEGER NOT NULL,
    key VARCHAR(20),
    value VARCHAR(100),
    /*

        Here should be put values of very low level of occurence:

        publtype VARCHAR(30)             150658
        cdate DATE,                      0
        month INTEGER,                   2481
        cdrom VARCHAR(20),               12977
        isbn VARCHAR(30),                45461
        chapter INTEGER,                 2
        school VARCHAR(50),              33242
        series VARCHAR(50),              20739
        layout UNKNOWN                   0
        ref UNKNOWN                      0
        note_ VARCHAR(50)                47312
        publisher VARCHAR(40)
        cite                             172689
        address                          3
        reviewid VARCHAR(50),            63
        rating VARCHAR(10),              61

    */
    PRIMARY KEY(id)
);

CREATE TABLE 'thesis_author'(
    /*
        many to many relation implementation
    */
    thesis_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    PRIMARY KEY(thesis_id, person_id)
);

CREATE TABLE 'thesis_editor'(
    /*
        many to many relation implementation
    */
    thesis_id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    PRIMARY KEY(thesis_id, person_id)
);

CREATE TABLE 'person'(
    /*
        0 occurence in xml file
        table for thesis editors and authors
    */
    id INTEGER NOT NULL,
    name VARCHAR(40),
    PRIMARY KEY (id)
);

CREATE TABLE 'person_extra_info'(
    id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    key VARCHAR(20),
    value VARCHAR(100),
    PRIMARY KEY (id)
);
