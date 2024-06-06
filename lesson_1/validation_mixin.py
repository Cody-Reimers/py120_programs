
class ValidationMixin:
#~~~~SINGULAR TYPE BOOLEAN-BASED CHECKING~~~~#

    @staticmethod
    def _is_int(obj):
        return isinstance(obj, int)

    @staticmethod
    def _is_str(obj):
        return isinstance(obj, str)

    @staticmethod
    def _is_float(obj):
        return isinstance(obj, float)

    @staticmethod
    def _is_list(obj):
        return isinstance(obj, list)

    @staticmethod
    def _is_tuple(obj):
        return isinstance(obj, tuple)

#~~~~SINGULAR TYPE ERROR-BASED CHECKING~~~~#

    @classmethod
    def _error_not_int(cls, obj, ref="object"):
        if cls._is_int(obj) is False:
            raise TypeError(f"{ref.title()} must be an integer.")

    @classmethod
    def _error_not_str(cls, obj, ref="object"):
        if cls._is_str(obj) is False:
            raise TypeError(f"{ref.title()} must be a string.")

    @classmethod
    def _error_not_float(cls, obj, ref="object"):
        if cls._is_float(obj) is False:
            raise TypeError(f"{ref.title()} must be a float.")

#~~~~MULTI-TYPE BOOLEAN-BASED CHECKING~~~~#

    @classmethod
    def _is_int_or_float(cls, obj):
        return cls._is_int(obj) or cls._is_float(obj)

    @classmethod
    def _is_list_or_tuple(cls, obj):
        return cls._is_list(obj) or cls._is_tuple(obj)

#~~~~MULTI-TYPE ERROR-BASED CHECKING~~~~#

    @classmethod
    def _error_not_int_or_float(cls, obj, ref="object"):
        if cls._is_int_or_float(obj) is False:
            raise TypeError(f"{ref.title()} must be an integer or float.")

    @classmethod
    def _error_not_list_or_tuple(cls, obj, ref="object"):
        if cls._is_list_or_tuple(obj) is False:
            raise TypeError(f"{ref.title()} must be a list or tuple.")
