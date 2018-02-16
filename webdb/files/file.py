"""
File overlays for providing files to web applications.
"""
import os

class FileOverlay(object):
	"""
	This is the main file overlay providing methods on files 
	that are useful when operating over a remote connection.

	``path``
		relative path of the file
	``root``
		absolute path of the "root" directory for files,
		``os.path.join(root, path)`` must be the absolute path
		of the file
	``modes`` 
		string or list of characters: 

		- ``"r"`` readable
		- ``"w"`` writable
		- ``"c"`` file can be created
		- ``"p"`` also parent directories can be created.

	``nickname``
		the name of the file that the client knows.
	"""
	def __init__(self, path, root, modes, nickname, maxsize = float("inf")):
		self._path = path
		self._root = root
		self._modes = modes
		self._abspath = os.path.join(root, path)
		self._nickname = nickname
		self._maxsize = maxsize
		try:
			self._size = os.stat(self._abspath).st_size
		except:
			self._size = 0

	def get_file_part(self, offset, chunk_size):
		"""
		Return a ``FilePart`` of this file.
		"""
		if(not "r" in self._modes):
			raise IOError("file is not readable")
		if(not os.path.exists(self._abspath)):
			raise IOError("file does not exist")

		fout = open(self._abspath, "rb")
		return FilePart(fout, offset, chunk_size)

	def write_file_part(self, offset, chunk):
		"""
		Write a part of a file. If the file is not at least ``offset``
		bytes long, raise ``IndexError``. This is a protection against
		people that think it would be funny to fill the disk up with zeros.
		"""

		if(not "w" in self._modes):
			raise IOError("file is not writable")

		tail = offset - self._size + chunk_size
		if(tail + self._size > self._maxsize):
			raise IOError("maximum file size exceeded")

		if(not os.path.exists(self._abspath)):
			if(not "c" in self._modes):
				raise IOError("file does not exist")
			self.create_file(self)

		with open(self._abspath, "r+b") as fin:
			fin.seek(offset)
			if(fin.tell() < offset):
				raise IndexError("file size exceeded")
			fin.write(chunk)

	def truncate(self):
		if(not "w" in self._modes):
			raise IOError("file is not writable")

		if(not os.path.exists(self._abspath)):
			if(not "c" in self._modes):
				raise IOError("file does not exist")
			self.create_file(self)
			return

		open(self._abspath, "wb").close()

	def create_file(self):
		if(not "c" in self._modes):
			raise IOError("file ist not creatable")
		if(os.path.exists(self._abspath)):
			raise IOError("file does exist")

		if(not os.path.exists(os.path.dirname(self._abspath))):
			if(not "p" in self._modes):
				raise IOError("parent path cannot be created")
			os.makedirs(os.path.dirname(self._abspath))
		open(self._abspath, "wb").close()




class FilePart(object):
	"""
	This represents a readable file part.
	"""
	def __init__(self, file_, offset, chunk_size):
		self._file = file_
		self._offset = offset
		self._chunk_size = chunk_size
		self._cursor = offset
		self._file.seek(offset)

	def read(self, cnt = None):
		"""
		``read`` from the file. Do not read further than ``offset + chunk_size``.
		"""
		left = self._offset + self._chunk_size - self._cursor

		if(cnt == None):
			cnt = left

		if(cnt > left):
			cnt = left

		self._cursor += cnt
		return self._file.read(cnt)
	def close(self):
		"""
		Close the underlaying file.
		"""
		return self._file.close()
	def seekable(self):
		return False
	def writable(self):
		return False
	def readable(self):
		return True
