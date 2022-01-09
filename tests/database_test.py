import sqlite3

def testSqliteConnection():
    """[UNIT] test sqlite new connection return connection"""
    db = sqlite3.connect('covid_database.db')
    assert isinstance(db, sqlite3.Connection)
