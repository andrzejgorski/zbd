
/* For each occourance count how many are in file */
CREATE TABLE 'thesis'(
    id INTEGER NOT NULL,
    thesis_type_id INTEGER/* ,
    title VARCHAR(300) */
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

CREATE TABLE 'thesis_author'(
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
