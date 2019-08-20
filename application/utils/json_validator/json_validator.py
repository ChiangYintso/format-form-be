# -*- coding: utf-8 -*-

import abc
from re import fullmatch


class BaseValidator(metaclass=abc.ABCMeta):
    def __init__(self, required: bool = True):
        self.required = required
        if type(required) is not bool:
            raise TypeError(('Error in {}: '
                            'argument \'required\' should be <class \'bool\'>')
                            .format(self.__class__))

    @abc.abstractmethod
    def validate(self, value) -> bool:
        pass


class IntegerValidator(BaseValidator):
    def __init__(self,
                 required: bool = True,
                 max_value: int = float('inf'),
                 min_value: int = float('-inf')):
        if max_value != float('inf') and type(max_value) is not int:
            raise TypeError('Error in <class \'IntegerValidator\'>: '
                            'argument \'max_value\' should be <class \'int\'>')
        if min_value != float('-inf') and type(min_value) is not int:
            raise TypeError('Error in <class \'IntegerValidator\'>: '
                            'argument \'min_value\' should be <class \'int\'>')
        if max_value < min_value:
            raise ValueError('Error in <class \'IntegerValidator\'>: '
                             '\'min_value\' should not be larger than \'min_value\'')
        super().__init__(required)
        self.__max_value = max_value
        self.__min_value = min_value

    def validate(self, value: int) -> bool:
        if type(value) is not int:
            print('Error in <class \'IntegerValidator\'>: '
                  'argument \'value\' should be <class \'int\'>')
            return False
        if self.__min_value <= value <= self.__max_value:
            return True
        print('[json_validator warning]', type(self), value)
        return False


class StringValidator(BaseValidator):
    def __init__(self,
                 required=True,
                 max_length: int = 1000000000,
                 min_length: int = 0,
                 re: str = ''):
        if type(max_length) is not int:
            raise TypeError('Error in <class \'StringValidator\'>: '
                            'argument \'max_length\' should be <class \'int\'>')
        if type(min_length) is not int:
            raise TypeError('Error in <class \'StringValidator\'>: '
                            'argument \'min_length\' should be <class \'int\'>')
        if max_length > 1000000000 or min_length < 0 or max_length < min_length:
            raise ValueError('Error in <class \'StringValidator\'>: '
                             'invalid argument')
        if type(re) is not str:
            raise TypeError('Error in <class \'StringValidator\'>: '
                            'argument \'re\' should be <class \'str\'>')
        super().__init__(required)
        self.__max_length = max_length
        self.__min_length = min_length
        self.__re = re

    def validate(self, value: str) -> bool:
        if self.__min_length <= len(value) <= self.__max_length:
            if self.__re:
                if fullmatch(self.__re, value):
                    return True
                else:
                    print('[json_validator warning] value mismatch regular expression')
                    return False
            else:
                return True
        else:
            print('[json_validator warning] invalid length')
            return False


class ArrayValidator(BaseValidator):
    def __init__(self,
                 arr_temp,
                 required: bool = True,
                 enable_extra_element: bool = True):
        """
        :param arr_temp: validator template, accept list or subclass
                         of `BaseValidator`.
        """
        if type(arr_temp) is list:
            for i in arr_temp:
                if not issubclass(type(i), BaseValidator):
                    raise TypeError('Error in <class \'ArrayValidator\'>: '
                                    'element of \'arr_temp\' should be '
                                    '<class \'BaseValidator\'>')
        elif not issubclass(type(arr_temp), BaseValidator):
            raise TypeError('Error in  <class \'ArrayValidator\'>: '
                            'argument \'arr_temp\' should be '
                            '<class \'BaseValidator\'> or <class \'list\'>')
        if type(enable_extra_element) is not bool:
            raise TypeError('Error in  <class \'ArrayValidator\'>: '
                            'argument \'enable_extra_element\' should be'
                            '<class \'bool\'>')
        self.__arr_temp = arr_temp
        self.__enable_extra_element = enable_extra_element
        super().__init__(required)

    def validate(self, value: (list, BaseValidator)) -> bool:
        if issubclass(type(self.__arr_temp), BaseValidator):
            for i in value:
                if not self.__arr_temp.validate(i):
                    print('[json_validator warning] ArrayValidator '
                          'mismatched type')
                    return False
        else:
            if len(value) != len(self.__arr_temp):
                print('[json_validator warning] ArrayValidator '
                      'mismatched length')
                raise False
            for i in range(len(value)):
                if not self.__arr_temp[i].validate(value[i]):
                    print('[json_validator warning] ArrayValidator '
                          'mismatched type')
                    return False
        return True


class JsonValidator(BaseValidator):
    def __init__(self,
                 validator: dict,
                 required: bool = True,
                 enable_extra_key: bool = False):
        """
        :param validator: a template for validating json. For example:
            validator = JsonValidator({
                "key1": StringValidator(required=True),
                "key2": IntegerValidator(required=False),
                "key3": JsonValidator(required=True)
            })
        :param enable_extra_key: allow key not in "validator".
        """
        if type(enable_extra_key) is not bool:
            raise TypeError('Error in <class \'JsonValidator\'>: '
                            'argument \'enable_extra_key should be <class \'bool\'>')
        if type(validator) is not dict:
            raise TypeError('Error in <class \'JsonValidator\'>: '
                            'argument \'validator\' should be <class \'dict\'>')
        super().__init__(required)
        self.__enable_extra_key = enable_extra_key
        self.__validator = validator
        self.__validate_kv()

    def __validate_kv(self):
        for k, v in self.__validator.items():
            if type(k) is not str:
                raise TypeError('Error in <class \'JsonValidator\'>: '
                                'key of \'validator\' should be'
                                '<class \'str\'>')
            if not issubclass(type(v), BaseValidator):
                raise TypeError('Error in <class \'JsonValidator\'>: '
                                'value of \'validator\' should be '
                                '<class \'BaseValidator\'>')

    def validate(self, value: dict) -> bool:
        """
        :param value: data in JSON type to validate.
        """
        if not self.__enable_extra_key:
            for k in value.keys():
                if k not in self.__validator.keys():
                    if type(k) is not str:
                        print('Error in method JsonValidator.validate(): '
                              'key of argument \'value\' should be '
                              '<class \'str\'>')
                        return False
                    print('[json_validator warning]', type(self), value)
                    return False
        for k in self.__validator.keys():
            if self.__validator[k].required:
                if k not in value.keys():
                    print('[json_validator warning] require argument {}'.format(k))
                    return False
                if not self.__validator[k].validate(value[k]):
                    return False
        return True


if __name__ == '__main__':
    score_validator_temp = {
        'subject': StringValidator(),
        'score': IntegerValidator(min_value=0, max_value=100)
    }
    validator_temp = {
        'name': IntegerValidator(),
        'id': IntegerValidator(max_value=20),
        'score': ArrayValidator([JsonValidator(score_validator_temp),
                                 JsonValidator(score_validator_temp)])
    }
    json_validator = JsonValidator(validator_temp)
    data = {
        'name': 34,
        'id': 20,
        'score': [{
            'subject': 'Chinese',
            'score': 100
        }, {
            'subject': 'Math',
            'score': 99
        }]
    }
    if json_validator.validate(data):
        print('yes')
    else:
        print('no')
