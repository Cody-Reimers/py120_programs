
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
        raise TypeError(f"{ref} must be an integer.")

def error_not_float(obj, ref="object"):
    if is_float(obj) is False:
        raise TypeError(f"{ref} must be a float.")

def error_not_string(obj, ref="object"):
    if is_string(obj) is False:
        raise TypeError(f"{ref} must be a string.")

def error_not_list(obj, ref="object"):
    if is_list(obj) is False:
        raise TypeError(f"{ref} must be a list.")

def error_not_tuple(obj, ref="object"):
    if is_tuple(obj) is False:
        raise TypeError(f"{ref} must be a tuple.")

#~~~~SINGLE TYPE TRY COERCION~~~~#

def try_to_int(data):
    try:
        return int(data)
    except:
        return data

def try_to_float(data):
    try:
        return float(data)
    except:
        return data

def try_to_string(data):
    try:
        return str(data)
    except:
        return data

#~~~~COMPARE TWO TYPES~~~~#

def other_is_same_type(test_type, subject):
    subject_type = type(subject)
    return test_type == subject_type

def error_not_same_type(test_type, subject, ref="object"):
    if other_is_same_type(test_type, subject) is False:
        raise TypeError(f"{ref} must be of type {test_type}.")

#~~~~MULTI-TYPE BOOLEAN-BASED CHECKING~~~~#

def is_int_or_float(obj):
    return isinstance(obj, int) or isinstance(obj, float)

def is_list_or_tuple(obj):
    return isinstance(obj, list) or isinstance(obj, tuple)

#~~~~MULTI-TYPE ERROR-BASED CHECKING~~~~#

def error_not_int_or_float(obj, ref="object"):
    if is_int_or_float(obj) is False:
        raise TypeError(f"{ref} must be an integer or float.")

def error_not_list_or_tuple(obj, ref="object"):
    if is_list_or_tuple(obj) is False:
        raise TypeError(f"{ref} must be a list or tuple.")
