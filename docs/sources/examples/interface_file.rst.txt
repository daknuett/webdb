Example: File Interface
=======================


This example shows how to run a web application that serves
both calculated content under the ``/`` mount and file
content.

The ``/`` application handles the "login" in this case, the
``files`` application serves user files.

All files are placed in the directory ``root`` relative to
the current path.

.. code:: python

	from webdb.interface.file import FileInterface
	from webdb.files.dispatcher import UserFileDispatcher

	import cherrypy, logging

	cherrypy.config.update({'tools.sessions.on': True})
	dispatcher = UserFileDispatcher("root")

	class DummyApp(object):
		@cherrypy.expose
		def index(self):
			return "Hello, World!"
		@cherrypy.expose
		def login(self, name):
			cherrypy.session["name"] = name

		@cherrypy.expose
		def get_uname(self):
			return cherrypy.session["name"]

	dummy_app = DummyApp()
	interface = FileInterface(dispatcher, dummy_app.get_uname)
	cherrypy.tree.mount(interface, "/files", {"/": {"request.dispatch": cherrypy.dispatch.MethodDispatcher()}})

	cherrypy.quickstart(dummy_app, "/")


**Note**: The ``FileInterface`` requires the
``MethodDispatcher``.
