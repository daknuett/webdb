from webdb.adapter.sqlite import SqliteDB

def test_sqlite(sqlite3_db_default):
	data = [("test", 1, 0.5),
		("foo", 3, 0.4), 
		("bar", 2, 1.1)]

	db = SqliteDB(sqlite3_db_default)
	db.open()

	for row in data:
		db.handle_request({"operation": "INSERT", 
				"table": "TEST", 
				"parameters": {
					"col_str": row[0],
					"col_int": row[1],
					"col_float": row[2]
					}})
		
	assert db.handle_request({"operation": "SELECT", 
				"table": "TEST",
				"parameters": {
					"what": {},
					"where": {}
					}}) == data

	db.handle_request({"operation": "UPDATE", 
				"table": "TEST",
				"parameters": {
					"set": {"col_int": 2},
					"where": {"col_str": "foo"}
					}
				})

	assert db.handle_request({"operation": "SELECT",
				"table": "TEST",
				"parameters": {
					"what": ["col_str"],
					"where": {"col_int": 2}
					}
				}) == [("foo", ), ("bar", )]

