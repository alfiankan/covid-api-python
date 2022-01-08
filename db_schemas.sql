-- SQLite
CREATE TABLE covid_cases(
    key INT PRIMARY KEY NOT NULL,
    positive INT DEFAULT 0,
    recovered INT DEFAULT 0,
    death INT DEFAULT 0,
    active INT DEFAULT 0
)


CREATE TABLE vaccination(
    key INT PRIMARY KEY NOT NULL,
    first_vacc INT DEFAULT 0,
    second_vacc INT DEFAULT 0,
)

CREATE TABLE test(
    key INT PRIMARY KEY NOT NULL,
    pcr_tcm_specimen INT DEFAULT 0,
    antigen_specimen INT DEFAULT 0,
    antigen INT DEFAULT 0,
    pcr_tcm INT DEFAULT 0,
)
