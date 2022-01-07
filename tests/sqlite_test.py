import sqlite3

def testSqliteConnection():
    db = sqlite3.connect('covid_database.db')

    assert isinstance(db, sqlite3.Connection)

