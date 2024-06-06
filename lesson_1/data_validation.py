
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
