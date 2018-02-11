from .date_and_time import DateAdapter, TimeAdapter, DatetimeAdapter, ConversionException
from datetime import date, time, datetime

conversions_dict = {"date": DateAdapter.from_dict,
			"time": TimeAdapter.from_dict,
			"datetime": DatetimeAdapter.from_dict}

def handle_type(value):
	if(isinstance(value, (str, int, float, bool, bytes))):
		return value
	if(isinstance(value, dict)):
		if(not "__type__" in value):
			raise ConversionException("missing __type__")
		if(not value["__type__"] in conversions_dict):
			raise ConversionException("unknow type: {}".format(value["__type__"]))
		return conversions_dict[value["__type__"]](value)
	raise ConversionException("Unsupported type: {}".format(type(value)))


def handle_types(dct):
	return {k: handle_type(v) for k,v in dct.items()}


def reverse_handle_type(value):
	if(isinstance(value, (str, int, float, bool, bytes))):
		return value
	if(isinstance(value, datetime)):
		return DatetimeAdapter.copy(value)
	if(isinstance(value, time)):
		return TimeAdapter.copy(value)
	if(isinstance(value, date)):
		return DateAdapter.copy(value)

