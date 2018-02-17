import pytest
import sqlite3, os
from webdb.adapter.sqlite import SqliteDBMS

@pytest.fixture
def sqlite3_db(tmpdir_factory):
	fn = tmpdir_factory.mktemp('data').join('test.db')

	return str(fn)


@pytest.fixture
def sqlite3_db_default(tmpdir_factory):
	fn = tmpdir_factory.mktemp('data').join('test.db')

	con = sqlite3.connect(str(fn))
	cursor = con.cursor()

	cursor.execute("CREATE TABLE TEST(col_str TEXT, col_int INTEGER, col_float REAL)")
	con.commit()
	con.close()
	return str(fn)


@pytest.fixture
def sqlite_dbms_default(tmpdir_factory):
	path = str(tmpdir_factory.mktemp('data_dbms'))
	

	inject = lambda: "user1"
	inject_as = "username"

	db1 = "users"
	db2 = "logs"

	data1 = [("user1", "User Numer One", "password-hash1"),
		("user2", "User Number Two", "password-hash2")]

	data2 = [("user1", 1, "This is a log"),
		("user2", 2, "This is a log"),
		("user1", 3, "This is another log"),
		("user2", 4, "blablabla"),
		("user1", 5, "logout")]

	path1 = os.path.join(path, db1)
	path2 = os.path.join(path, db2)

	sqlite1 = sqlite3.connect(path1)
	sqlite2 = sqlite3.connect(path2)

	c = sqlite1.cursor()
	c.execute("CREATE TABLE users(username text, fullname text, passwd text)")
	c.executemany("INSERT INTO users VALUES(?, ?, ?)", data1)
	sqlite1.commit()
	c = sqlite2.cursor()
	c.execute("CREATE TABLE logs(username text, id integer, msg text)")
	c.executemany("INSERT INTO logs VALUES(?, ?, ?)", data2)
	sqlite2.commit()

	dbms = SqliteDBMS(path, [db1, db2], inject, inject_as)

	return (data1, data2, dbms)
