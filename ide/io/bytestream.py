from io import BytesIO

from ide.bitconv import *


class BytesOutStream:
	def __init__(self, output = BytesIO()):
		self._data = output

	def getvalue(self):
		return self._data.getvalue()

	def close(self):
		self._data.close()

	def flush(self):
		self._data.flush()

	def seek(self, offset):
		self._data.seek(offset)

	def tell(self):
		return self._data.tell()

	def size(self):
		return len(self._data.getvalue())

	def bytes(self, data):
		return self._data.write(data)

	def uint(self, n: int, size_in_bytes: int):
		return self.bytes(pack_uint(n, size_in_bytes))

	def int(self, n: int, size_in_bytes: int):
		return self.bytes(pack_int(n, size_in_bytes))

	def uint8(self, n: int):
		return self.bytes(pack_uint8(n))

	def int8(self, n: int):
		return self.bytes(pack_int8(n))

	def uint16(self, n: int):
		return self.bytes(pack_uint16(n))

	def int16(self, n: int):
		return self.bytes(pack_int16(n))

	def uint32(self, n: int):
		return self.bytes(pack_uint32(n))

	def int32(self, n: int):
		return self.bytes(pack_int32(n))

	def uint64(self, n: int):
		return self.bytes(pack_uint64(n))

	def int64(self, n: int):
		return self.bytes(pack_int64(n))

	def float(self, n: float):
		return self.bytes(pack_float(n))

	def double(self, n: float):
		return self.bytes(pack_double(n))

	def uleb128(self, n: int):
		out = bytearray()
		while True:
			byte = n & 0x7f
			n >>= 7
			out.append(byte)
			if n:
				out[-1] |= 0x80
			else:
				break

		return self.bytes(out)

	def string(self, text: str, encoding = "utf-8"):
		data = bytes(text, encoding)
		self.uleb128(len(data))
		return self.bytes(data)


class BytesInStream:
	def __init__(self, data):
		self._data = data

	def close(self):
		self._data.close()

	def flush(self):
		self._data.flush()

	def seek(self, offset):
		self._data.seek(offset)

	def tell(self):
		return self._data.tell()

	def size(self):
		return len(self._data)

	def bytes(self, length):
		return self._data.read(length)

	def uint(self, size_in_bytes: int):
		return unpack_uint(self.bytes(size_in_bytes))

	def int(self, size_in_bytes: int):
		return unpack_int(self.bytes(size_in_bytes))

	def uint8(self):
		return unpack_uint8(self.bytes(1))

	def int8(self):
		return unpack_int8(self.bytes(1))

	def uint16(self):
		return unpack_uint16(self.bytes(2))

	def int16(self):
		return unpack_int16(self.bytes(2))

	def uint32(self):
		return unpack_uint32(self.bytes(4))

	def int32(self):
		return unpack_int32(self.bytes(4))

	def uint64(self):
		return unpack_uint64(self.bytes(8))

	def int64(self):
		return unpack_int64(self.bytes(8))

	def float(self):
		return unpack_float(self.bytes(4))

	def double(self):
		return unpack_double(self.bytes(8))

	def uleb128(self):
		value = 0
		shift = 0
		while not self.size() > self.tell():
			byte = self.bytes(1)[0]
			value |= (byte & 0x7f) << shift
			if byte & 0x80:
				shift += 7
			else:
				break

		return value

	def string(self, encoding = "utf-8"):
		length = self.uleb128()
		return self.bytes(length).decode(encoding)
