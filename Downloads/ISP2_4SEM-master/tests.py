import os
import unittest
from serializations import *
from services.ordinary_types import *
from services.fabric import *
import math


def p(c):
    return "the res is {}".format(c)


def summ(a=9, b=1):
    return p(a + b)


def out_func(x):
    return math.cos(x)


data_etalon = {'__closure__': None,
               '__code__': {'co_argcount': 2,
                            'co_cellvars': [],
                            'co_code': [116, 0, 124, 0, 124, 1, 23, 0, 131, 1, 83, 0],
                            'co_consts': [None],
                            'co_filename': '/Users/victoriasviridchik/PycharmProjects/isp_4sem_2/tests.py',
                            'co_firstlineno': 7,
                            'co_flags': 67,
                            'co_freevars': [],
                            'co_kwonlyargcount': 0,
                            'co_lnotab': [0, 1],
                            'co_name': 'summ',
                            'co_names': ['p'],
                            'co_nlocals': 2,
                            'co_posonlyargcount': 0,
                            'co_stacksize': 3,
                            'co_varnames': ['a', 'b']},
               '__defaults__': (9, 1),
               '__globals__': {'p': {'__closure__': None,
                                     '__code__': {'co_argcount': 1,
                                                  'co_cellvars': [],
                                                  'co_code': [100,
                                                              1,
                                                              160,
                                                              0,
                                                              124,
                                                              0,
                                                              161,
                                                              1,
                                                              83,
                                                              0],
                                                  'co_consts': [None, 'the res is {}'],
                                                  'co_filename': '/Users/victoriasviridchik/PycharmProjects/isp_4sem_2/tests.py',
                                                  'co_firstlineno': 4,
                                                  'co_flags': 67,
                                                  'co_freevars': [],
                                                  'co_kwonlyargcount': 0,
                                                  'co_lnotab': [0, 1],
                                                  'co_name': 'p',
                                                  'co_names': ['format'],
                                                  'co_nlocals': 1,
                                                  'co_posonlyargcount': 0,
                                                  'co_stacksize': 3,
                                                  'co_varnames': ['c']},
                                     '__defaults__': None,
                                     '__globals__': {},
                                     '__name__': 'p'}},
               '__name__': 'summ'}


class TestSer(unittest.TestCase):
    def test_atom(self):
        a_int = prepare_data(9)
        a_float = prepare_data(3.14)
        self.assertEqual(a_int, 9)
        self.assertEqual(a_float, 3.14)

    def test_simplices(self):
        list_data = [1, 2, 3]
        a_list = prepare_data(list_data)
        dict_data = {'data': [{'vbh': bytes([6, 9, 123]), 'y': ('x', 5), 'o': {8, 'z'}}]}
        a_dict = prepare_data(dict_data)
        a_exp = {'data': [{'o': [8, 'z'], 'vbh': [6, 9, 123], 'y': ['x', 5]}]}
        self.assertEqual(a_list, list_data)
        self.assertEqual(a_dict, a_exp)

    def test_func(self):
        a_func = prepare_data(summ)
        self.assertEqual(de_prepare_data(a_func)(2), "the res is 3")
        # self.assertEqual(a_dict, a_exp)

    def test_dumps_loads(self):
        data = {"I am tired HELP": ["very"], 'float': 3.14, 'bool': True, 'unbool': False}
        # a_dict = prepare_data(data)
        # a_expp_json = {"I am tired HELP": ["very"]}
        # a_expp_pickle =bytes("I am tired HELP")
        # print(a_expp)
        res = fabrica('json').dumps(data)
        res_pickle = fabrica('pickle').dumps(data)
        res_toml = fabrica('toml').dumps(data)
        res_yaml = fabrica('yaml').dumps(data)
        # print(a_expp)
        # print(res)
        # self.assertEqual(res,a_expp_json)
        self.assertEqual(fabrica('json').loads(res), data)
        self.assertEqual(fabrica('pickle').loads(res_pickle), data)
        self.assertEqual(fabrica('toml').loads(res_toml), data)
        self.assertEqual(fabrica('yaml').loads(res_yaml), data)

    def test_loads_dumps_json(self):
        full_json_str = '{"name": "Viktor", "age": 30, "married": true, "divorced": false, "children": ["Anna", ["Alex", "Nikita"], "Bogdan"], "pets": null, "cars": [{"model": "BMW 230", "mpg": 27.5}, {"model": "Ford Edge", "mpg": 24.1}]}'
        res = fabrica('json').loads(full_json_str)
        self.assertEqual(fabrica('json').dumps(res), full_json_str)

    def test_dump_load(self):
        data = {"I am tired HELP": ["very"]}
        # a_dict = prepare_data(data)
        # with open('data_json', 'w'):
        fabrica('json').dump(data, 'data_json')
        self.assertEqual(fabrica('json').load('data_json'), data)
        # with open('data_toml', 'w'):
        fabrica('toml').dump(data, 'data_toml')
        self.assertEqual(fabrica('toml').load('data_toml'), data)
        # with open('data_yaml', 'w'):
        fabrica('yaml').dump(data, 'data_yaml')
        self.assertEqual(fabrica('yaml').load('data_yaml'), data)
        # with open('pickle_data', 'wb'):
        fabrica('pickle').dump(data, 'pickle_data')
        self.assertEqual(fabrica('pickle').load('pickle_data'), data)
        os.remove('data_json')
        os.remove('data_toml')
        os.remove('data_yaml')
        os.remove('pickle_data')

    def test_func_with_out_import(self):
        data = out_func

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('json').dump(data, 'data_json')
        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('toml').dump(data, 'data_toml')
        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('yaml').dump(data, 'data_yaml')
        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('pickle').dump(data, 'pickle_data')

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('json').dumps(data)

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('toml').dumps(data)

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('yaml').dumps(data)

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('pickle').dumps(data)

    def test_func_ser(self):
        data = summ

        fabrica('json').dump(data, 'data_json')

        fabrica('toml').dump(data, 'data_toml')

        fabrica('yaml').dump(data, 'data_yaml')

        fabrica('pickle').dump(data, 'pickle_data')

        res = fabrica('json').dumps(data)
        fabrica('json').loads(res)

        res = fabrica('toml').dumps(data)
        fabrica('toml').loads(res)

        fabrica('yaml').dumps(data)

        res = fabrica('pickle').dumps(data)
        fabrica('pickle').loads(res)


class TestDeSer(unittest.TestCase):
    def test_atom(self):
        a_int = de_prepare_data(prepare_data(9))
        a_float = de_prepare_data(prepare_data(3.14))
        self.assertEqual(a_int, 9)
        self.assertEqual(a_float, 3.14)

    def test_simplices(self):
        list_data = [1, 2, 3]
        a_list = de_prepare_data(prepare_data(list_data))
        dict_data = {'data': [{'vbh': bytes([6, 9, 123]), 'y': ('x', 5), 'o': {8, 'z'}}]}
        a_dict = de_prepare_data(prepare_data(dict_data))
        a_exp = {'data': [{'o': [8, 'z'], 'vbh': [6, 9, 123], 'y': ['x', 5]}]}
        self.assertEqual(a_list, list_data)
        self.assertEqual(a_dict, a_exp)

    def test_func(self):
        a_func = de_prepare_data(prepare_data(summ))
        self.assertEqual(a_func(3), "the res is 4")
        # self.assertEqual(a_dict, a_exp)


class CustomExceptionTest(unittest.TestCase):
    def test_loads(self):
        data = {'data': {'asd': [1, 2, 3]}}
        res_json = fabrica('json').dumps(data)
        res_pickle = fabrica('pickle').dumps(data)
        res_toml = fabrica('toml').dumps(data)
        res_yaml = fabrica('yaml').dumps(data)
        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            res_pickle = res_pickle[:len(res_json) // 2]
            fabrica('pickle').loads(res_pickle)

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            res_json = res_json[:len(res_json) // 2]
            fabrica('json').loads(res_json)

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            res_toml = res_toml[:len(res_toml) // 2]
            fabrica('toml').loads(res_toml)

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            res_yaml = '\x09'
            fabrica('yaml').loads(res_yaml)

    def test_load(self):
        data = {"I am tired HELP": ["very"], 'tired_koef': 100500}
        # a_dict = prepare_data(data)

        fabrica('json').dump(data, 'data_json')
        with open('data_json', 'a') as fp:
            fp.seek(3)
            fp.write('hhr"en"hr')

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('json').load('data_json')

        fabrica('yaml').dump(data, 'data_yaml')
        with open('data_yaml', 'a') as fp:
            fp.seek(3)
            fp.write('hhr"en"hr')

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('yaml').load('data_yaml')

        # fabrica('pickle').dump(data, 'data_pickle')
        with open('data_pickle', 'wb') as fp:
            # fp.seek(10)
            fp.write(b'hhr"en"hsaf;;lmr')

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            fabrica('pickle').load('data_pickle')

        fabrica('toml').dump(data, 'data_toml')
        with open('data_toml', 'w') as fp:
            # fp.seek(10, os.SEEK_CUR)
            fp.write('hhr"en"hsaf;;lmr')

        with self.assertRaises(Exceptions.InvalidTypeSourceException):
            res = fabrica('toml').load('data_toml')
            fabrica('toml').load('data_toml')

        os.remove('data_json')
        os.remove('data_toml')
        os.remove('data_yaml')
        os.remove('data_pickle')


if __name__ == '__main__':
    unittest.main()
