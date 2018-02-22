Guide
*****

.. toctree::
   :caption: Contents:

   examples/interface_file


How to use webdb
================

``webdb`` provides a simple way to expose your databases to
the web.

Authentication
--------------

``webdb`` **DOES NOT** provide a way to authenticate your
users. This **must** be done by a parent app or ``cherrypy``.
See the `docs
<http://docs.cherrypy.org/en/latest/basics.html#authentication>`_
on how to do that.

However one can isolate the users by injecting data into the
queries. This can be done easily using sessions: Just add
a ``username`` to the session, for instance in the
``checkpassword`` function and inject this data:

.. code:: python

	passwords = {"foo": "bar"}
	# XXX: do not actually use plaintext passwords.
	def check_password(realm, uname, passwd):
		if(uname in passwords and passwords[uname] == passwd):
			cherrypy.session["username"] = uname
			return True
		return False
	
	class WhateverServer(object):
		@cherrypy.expose
		def index(self):
			return "Foobar"
		def get_username(self):
			return cherrypy.session["username"]

	server = WhateverServer()
	dbms = SqliteDBMS("path/to/dbs", ["db1", "db2"],
			inject = server.get_username,
			inject_as = "username")

A database then will look like this:

.. code:: sql

	CREATE TABLE table1(username text, some_data text,
		more_data integer);



