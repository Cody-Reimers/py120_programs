
#~~~~SINGLE TYPE BOOLEAN-BASED CHECKING~~~~#

def is_int(obj):
    return isinstance(obj, int)

def is_float(obj):
    return isinstance(obj, float)

def is_string(obj):
    return isinstance(obj, str)

def is_list(obj):
    return isinstance(obj, list)

def is_tuple(obj):
    return isinstance(obj, tuple)

#~~~~SINGLE TYPE ERROR-BASED CHECKING~~~~#

def error_not_int(obj, ref="object"):
    if is_int(obj) is False:
        raise TypeError(f"{repr(ref)} must be an integer.")

def error_not_float(obj, ref="object"):
    if is_float(obj) is False:
        raise TypeError(f"{repr(ref)} must be a float.")

def error_not_string(obj, ref="object"):
    if is_string(obj) is False:
        raise TypeError(f"{repr(ref)} must be a string.")

def error_not_list(obj, ref="object"):
    if is_list(obj) is False:
        raise TypeError(f"{repr(ref)} must be a list.")

def error_not_tuple(obj, ref="object"):
    if is_tuple(obj) is False:
        raise TypeError(f"{repr(ref)} must be a tuple.")

#~~~~SINGLE TYPE TRY COERCION~~~~#

def try_to_int(data):
    try:
        return int(data)
    except (TypeError, ValueError):
        return data

def try_to_float(data):
    try:
        return float(data)
    except (TypeError, ValueError):
        return data

def try_to_string(data):
    try:
        return str(data)
    except (TypeError, ValueError):
        return data

#~~~~COMPARE TWO TYPES~~~~#

def error_not_isinstance(subject, test_type, ref="object"):
    if isinstance(subject, test_type) is False:
        raise TypeError(f"{repr(ref)} must be of type {test_type}.")

#~~~~MULTI-TYPE BOOLEAN-BASED CHECKING~~~~#

def is_int_or_float(obj):
    return is_int(obj) or is_float(obj)

def is_int_or_string(obj):
    return is_int(obj) or is_string(obj)

def is_list_or_tuple(obj):
    return is_list(obj) or is_tuple(obj)

#~~~~MULTI-TYPE ERROR-BASED CHECKING~~~~#

def error_not_int_or_float(obj, ref="object"):
    if is_int_or_float(obj) is False:
        raise TypeError(f"{repr(ref)} must be an integer or float.")

def error_not_int_or_string(obj, ref="object"):
    if is_int_or_string(obj) is False:
        raise TypeError(f"{repr(ref)} must be an integer or string.")

def error_not_list_or_tuple(obj, ref="object"):
    if is_list_or_tuple(obj) is False:
        raise TypeError(f"{repr(ref)} must be a list or tuple.")

#~~~~TESTING NUMBER PARITY~~~~#

def is_even(num):
    return num % 2 == 0

def is_odd(num):
    return num % 2 != 0

#~~~~TESTING IF COLLECTION IS EMPTY~~~~#

def is_empty_string(collection):
    return collection == ""

def is_empty_list(collection):
    return collection == list()

def is_empty_tuple(collection):
    return collection == tuple()

def is_empty_dictionary(collection):
    return collection == dict()

def is_empty_set(collection):
    return collection == set()

def is_empty_frozenset(collection):
    return collection == frozenset()
