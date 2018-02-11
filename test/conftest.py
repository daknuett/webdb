import pytest
import sqlite3

@pytest.fixture(scope = "session")
def sqlite3_db(tmpdir_factory):
	fn = tmpdir_factory.mktemp('data').join('test.db')

	return str(fn)


@pytest.fixture(scope = "session")
def sqlite3_db_default(tmpdir_factory):
	fn = tmpdir_factory.mktemp('data').join('test.db')

	con = sqlite3.connect(str(fn))
	cursor = con.cursor()

	cursor.execute("CREATE TABLE TEST(col_str TEXT, col_int INTEGER, col_float REAL)")
	con.commit()
	con.close()
	return str(fn)

