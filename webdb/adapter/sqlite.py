import sqlite3
from .exceptions import DatabaseError
from .abstractsql import AbstractSQLDB

class SqliteDB(AbstractSQLDB):
	"""
	SQLite3 adapter.

	The constuctor requires the filename of the
	database file.
	"""
	def __init__(self, filename):
		AbstractSQLDB.__init__(self)
		self.filename = filename

	def open(self):
		self._con = sqlite3.connect(self.filename)
	def close(self):
		self._con.close()

	def get_column_names(self, table):
		if(not table in self.get_table_names()):
			raise DatabaseError("unknown table: {}".format(table))
		cursor = self._con.cursor()
		cursor.execute("PRAGMA table_info({})".format(table))
		return [row[1] for row in cursor.fetchall()]

	def get_table_names(self):
		cursor = self._con.cursor()
		cursor.execute("SELECT name FROM sqlite_master WHERE type = \"table\"")
		return [row[0] for row in cursor.fetchall()]
