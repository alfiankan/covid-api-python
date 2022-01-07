-- SQLite
CREATE TABLE covid_cases(
    key INT PRIMARY KEY NOT NULL,
    positive INT DEFAULT 0,
    recovered INT DEFAULT 0,
    death INT DEFAULT 0,
    active INT DEFAULT 0
)
