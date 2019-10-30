from struct import pack as _pack, unpack_from as _unpack_from


def pack_uint(n: int, size_in_bytes: int):
	return bytearray((n >> (i * 8)) & 0xff for i in range(size_in_bytes))

def pack_int(n: int, size_in_bytes: int):
	k = 2 ** (size_in_bytes * 8)
	if n < (k / 2):
		n += k
	return pack_uint(n, size_in_bytes)

def unpack_uint(byte_iterable):
	n = 0
	i = 0
	for byte in byte_iterable:
		n += (byte << (i * 8))
		i += 1

	return n

def unpack_int(byte_iterable):
	n = unpack_uint(byte_iterable)
	k = 2 ** (len(byte_iterable) * 8)
	if n >= (k / 2):
		n -= k
	return n


def pack_uint8(n: int): return _pack("=B", n)
def pack_uint16(n: int): return _pack("=H", n)
def pack_uint32(n: int): return _pack("=I", n)
def pack_uint64(n: int): return _pack("=Q", n)
def pack_int8(n: int): return _pack("=b", n)
def pack_int16(n: int): return _pack("=h", n)
def pack_int32(n: int): return _pack("=i", n)
def pack_int64(n: int): return _pack("=q", n)
def pack_float(n: float): return _pack("=f", n)
def pack_double(n: float): return _pack("=d", n)

def pack_uint8_le(n: int): return _pack("<B", n)
def pack_uint16_le(n: int): return _pack("<H", n)
def pack_uint32_le(n: int): return _pack("<I", n)
def pack_uint64_le(n: int): return _pack("<Q", n)
def pack_int8_le(n: int): return _pack("<b", n)
def pack_int16_le(n: int): return _pack("<h", n)
def pack_int32_le(n: int): return _pack("<i", n)
def pack_int64_le(n: int): return _pack("<q", n)
def pack_float_le(n: float): return _pack("<f", n)
def pack_double_le(n: float): return _pack("<d", n)

def pack_uint8_be(n: int): return _pack(">B", n)
def pack_uint16_be(n: int): return _pack(">H", n)
def pack_uint32_be(n: int): return _pack(">I", n)
def pack_uint64_be(n: int): return _pack(">Q", n)
def pack_int8_be(n: int): return _pack(">b", n)
def pack_int16_be(n: int): return _pack(">h", n)
def pack_int32_be(n: int): return _pack(">i", n)
def pack_int64_be(n: int): return _pack(">q", n)
def pack_float_be(n: float): return _pack(">f", n)
def pack_double_be(n: float): return _pack(">d", n)


def unpack_uint8(packed_bytes: bytes, offset = 0): return _unpack_from("=B", packed_bytes, offset)[0]
def unpack_uint16(packed_bytes: bytes, offset = 0): return _unpack_from("=H", packed_bytes, offset)[0]
def unpack_uint32(packed_bytes: bytes, offset = 0): return _unpack_from("=I", packed_bytes, offset)[0]
def unpack_uint64(packed_bytes: bytes, offset = 0): return _unpack_from("=Q", packed_bytes, offset)[0]
def unpack_int8(packed_bytes: bytes, offset = 0): return _unpack_from("=b", packed_bytes, offset)[0]
def unpack_int16(packed_bytes: bytes, offset = 0): return _unpack_from("=h", packed_bytes, offset)[0]
def unpack_int32(packed_bytes: bytes, offset = 0): return _unpack_from("=i", packed_bytes, offset)[0]
def unpack_int64(packed_bytes: bytes, offset = 0): return _unpack_from("=q", packed_bytes, offset)[0]
def unpack_float(packed_bytes: bytes, offset = 0): return _unpack_from("=f", packed_bytes, offset)[0]
def unpack_double(packed_bytes: bytes, offset = 0): return _unpack_from("=d", packed_bytes, offset)[0]

def unpack_uint8_le(packed_bytes: bytes, offset = 0): return _unpack_from("<B", packed_bytes, offset)[0]
def unpack_uint16_le(packed_bytes: bytes, offset = 0): return _unpack_from("<H", packed_bytes, offset)[0]
def unpack_uint32_le(packed_bytes: bytes, offset = 0): return _unpack_from("<I", packed_bytes, offset)[0]
def unpack_uint64_le(packed_bytes: bytes, offset = 0): return _unpack_from("<Q", packed_bytes, offset)[0]
def unpack_int8_le(packed_bytes: bytes, offset = 0): return _unpack_from("<b", packed_bytes, offset)[0]
def unpack_int16_le(packed_bytes: bytes, offset = 0): return _unpack_from("<h", packed_bytes, offset)[0]
def unpack_int32_le(packed_bytes: bytes, offset = 0): return _unpack_from("<i", packed_bytes, offset)[0]
def unpack_int64_le(packed_bytes: bytes, offset = 0): return _unpack_from("<q", packed_bytes, offset)[0]
def unpack_float_le(packed_bytes: bytes, offset = 0): return _unpack_from("<f", packed_bytes, offset)[0]
def unpack_double_le(packed_bytes: bytes, offset = 0): return _unpack_from("<d", packed_bytes, offset)[0]

def unpack_uint8_be(packed_bytes: bytes, offset = 0): return _unpack_from(">B", packed_bytes, offset)[0]
def unpack_uint16_be(packed_bytes: bytes, offset = 0): return _unpack_from(">H", packed_bytes, offset)[0]
def unpack_uint32_be(packed_bytes: bytes, offset = 0): return _unpack_from(">I", packed_bytes, offset)[0]
def unpack_uint64_be(packed_bytes: bytes, offset = 0): return _unpack_from(">Q", packed_bytes, offset)[0]
def unpack_int8_be(packed_bytes: bytes, offset = 0): return _unpack_from(">b", packed_bytes, offset)[0]
def unpack_int16_be(packed_bytes: bytes, offset = 0): return _unpack_from(">h", packed_bytes, offset)[0]
def unpack_int32_be(packed_bytes: bytes, offset = 0): return _unpack_from(">i", packed_bytes, offset)[0]
def unpack_int64_be(packed_bytes: bytes, offset = 0): return _unpack_from(">q", packed_bytes, offset)[0]
def unpack_float_be(packed_bytes: bytes, offset = 0): return _unpack_from(">f", packed_bytes, offset)[0]
def unpack_double_be(packed_bytes: bytes, offset = 0): return _unpack_from(">d", packed_bytes, offset)[0]
