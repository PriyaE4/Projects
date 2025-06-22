CREATE DATABASE Library;
Use Library ;
CREATE TABLE IF NOT EXISTS voterss (
    student_id VARCHAR(50),
    book_id INT CHECK (book_id IN (1, 2, 3,4,5,6)), -- Ensuring book_id can only be 1, 2, or 3
    PRIMARY KEY (student_id, book_id) -- Composite primary key to prevent duplicate entries
) ;
SELECT * FROM LIBRARY_DETAILS ;
