from abc import ABCMeta, abstractmethod
from .exceptions import DatabaseError

class AbstractDBMS(metaclass = ABCMeta):
	apilevel = None
	threadsafety = None
	# paramstyle is undefined, as JSON objects will be 
	# used for requests.

	def __init__(self):
		self.inject = None
		self.inject_as = None

	@abstractmethod
	def connect(self, name, *args):
		pass

	@abstractmethod
	def dispatch_DB(self, db_name):
		pass
	
	def handle_request(self, request):
		db = self.dispatch_DB(request["database"])
		if(not db):
			raise DatabaseError()

		db.open()

		try:
			if(self.inject_as):
				result = db.handle_request(request["request"],
					inject = self.inject(),
					inject_as = self.inject_as
					)
			else:
				result = db.handle_request(request["request"])

		except BaseException as e:
			result = e
		finally:
			db.close()
		return result


class AbstractDB(metaclass = ABCMeta):
	@abstractmethod
	def open(self, *args):
		pass
	@abstractmethod
	def close(self, *args):
		pass

	@abstractmethod
	def handle_request(self, request, inject = None, inject_as = None):
		pass

