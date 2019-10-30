def _format(n, divisor, units):
	i = 0
	while n >= divisor and (i + 1) < len(units):
		n /= divisor
		i += 1

	if n == int(n):
		return "{} {}".format(int(n), units[i])
	else:
		return "{:.2f} {}".format(n, units[i])

def duration_short(t):
	return _format(t * 1e9, 1000, ("ns", "μs", "ms", "s", "ks"))

def file_size_1024(size):
	return _format(size, 1024, ("B", "KiB", "MiB", "GiB", "TiB", "PiB"))

def file_size(size):
	return _format(size, 1000, ("B", "kB", "MB", "GB", "TB", "PB"))

def duration(t):
	units_info = (
		("year",        "years",        60 * 60 * 24 * 365),
		("day",         "days",         60 * 60 * 24),
		("hour",        "hours",        60 * 60),
		("minute",      "minutes",      60),
		("second",      "seconds",      1),
		("millisecond", "milliseconds", 1e-3),
		("microsecond", "microseconds", 1e-6),
		("nanosecond",  "nanoseconds",  1e-9),
		("picosecond",  "picoseconds",  1e-12)
	)

	if t > (units_info[0][2] * 1e3):
		return "a very long time"
	elif t == 0:
		return "0 seconds"

	unit_info = None
	for unit_info in units_info:
		if t / unit_info[2] > 1:
			t /= unit_info[2]
			break

	if t == int(t):
		return "{} {}".format(int(t), unit_info[0] if t == 1 else unit_info[1])
	else:
		return "{:.2f} {}".format(t, unit_info[1])

def duration_verbose(t):
	units_info = (
		("galactic year",    "galactic years",    60 * 60 * 24 * 365 * 250e6),
		("Pu-239 half-life", "Pu-239 half-lives", 60 * 60 * 24 * 365 * 24110),
		("century",          "centuries",         60 * 60 * 24 * 365 * 100),
		("year",             "years",             60 * 60 * 24 * 365),
		("month",            "months",            60 * 60 * 24 * 30),
		("day",              "days",              60 * 60 * 24),
		("hour",             "hours",             60 * 60),
		("minute",           "minutes",           60),
		("second",           "seconds",           1),
		("millisecond",      "milliseconds",      1e-3),
		("microsecond",      "microseconds",      1e-6)
	)

	if t > (units_info[0][2] * 1e3):
		return "a very long time"
	elif t == 0:
		return "0 seconds"

	parts = []
	for unit_info in units_info:
		n = int(t / unit_info[2])

		if n > 0:
			parts.append("{} {}".format(n, unit_info[0] if n == 1 else unit_info[1]))
			t -= n * unit_info[2]

	if len(parts) == 1:
		return parts[0]
	else:
		last_part = parts.pop()
		return ", ".join(parts) + ", and " + last_part

def countdown(t):
	return "{:02d}:{:02d}.{:01d}".format(int(t / 60), int(t % 60), int(t % 1 * 10))
