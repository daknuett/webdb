"""
File dispatchers for serving files for web applications.
"""

from abc import abstractmethod, ABCMeta

class AbstractFileDispatcher(metaclass = ABCMeta):
	@abstractmethod
	def dispatch_file(self, path, *args):
		"""
		Dispatch the file. This **must always** return 
		a ``FileOverlay``. Even if the file must not be accessed,
		or does not exist. In this case the ``modes`` must be emtpy.
		"""
		pass
	def cleanup_path(self, path):
		"""
		Clean up the path. Remove any ".."s and a leading "/".

		``dispatch_file`` **must** call this method before actually dispatching the
		file.
		"""
		if(path[0] == "/"):
			path = path[1:]
		return path.replace("..", "")


class UserFileDispatcher(AbstractFileDispatcher):
	"""
	This file dispatcher has a seperated path for
	every user. The user is allowed to do anything
	in this path (read, write, create, create parents).

	Only use this for "reliable" clients.
	"""
	def __init__(self, root):
		self._root = root

	def dispatch_file(self, path, username):
		path = cleanup_path(path)
		root = os.path.join(self._root, username)
		return FileOverlay(path, root, "rwcp", path)



class QuotaUserFileDispatcher(AbstractFileDispatcher):
	"""
	This file dispatcher has a seperated path for
	every user. The user is allowed to do anything
	in this path (read, write, create, create parents).

	Only use this for "semi reliable" clients.
	"""
