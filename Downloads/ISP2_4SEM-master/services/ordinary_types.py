import types
# import json
# import yaml
import inspect
from serializations.Exceptions import InvalidTypeSourceException


# from services.fabric import fabrica

def prepare_data(raw_data):
    simplicies = [list, tuple, set, bytes]
    atom = [str, int, float, bool, type(None)]
    etalon = type(raw_data)
    if etalon in simplicies:
        res = []
        for el in raw_data:
            res.append(prepare_data(el))
        return res
    elif etalon in atom:
        return raw_data
    elif etalon == types.FunctionType:
        funct_res = {}
        # tmp_data = inspect.getmembers(raw_data)
        my_code = raw_data.__code__.co_names
        my_code_tmp = prepare_data(raw_data.__code__)
        funct_res["__code__"] = my_code_tmp

        my_globals = raw_data.__globals__
        my_globals_res = {}
        for k in my_code:
            if k in my_globals and inspect.isbuiltin(my_globals[k]) is False:
                if inspect.ismodule(my_globals[k]):
                    raise InvalidTypeSourceException
                my_globals_res[k] = prepare_data(my_globals[k])
        funct_res["__globals__"] = my_globals_res

        # my_globals = set(my_code).intersection(set(my_globals))
        my_name = raw_data.__name__
        my_argdefs = raw_data.__defaults__
        my_closure = raw_data.__closure__
        funct_res["__name__"] = my_name
        funct_res["__defaults__"] = my_argdefs
        funct_res["__closure__"] = my_closure

        return funct_res
        # types.CodeType()
        # types.FunctionType()
    elif etalon == dict:
        res = {}
        for k, v in raw_data.items():
            kk = prepare_data(k)
            vv = prepare_data(v)
            res[kk] = vv
        return res
    else:

        tmp_data = inspect.getmembers(raw_data)
        res = {}
        tmp_data_res = []
        needed = ['co_argcount', 'co_cellvars', 'co_code', 'co_consts', 'co_filename', 'co_firstlineno', 'co_flags',
                  'co_freevars', 'co_kwonlyargcount', 'co_lnotab', 'co_name', 'co_names', 'co_nlocals', 'co_stacksize',
                  'co_varnames', 'co_posonlyargcount']
        if type(raw_data) == types.CodeType:
            for el in tmp_data:
                if el[0] in needed:
                    tmp_data_res.append((el[0], el[1]))
            tmp_data = tmp_data_res.copy()
            flag_pos = False
            for el in tmp_data:
                if el[0] == 'co_posonlyargcount':
                    flag_pos = True
            if flag_pos is False:
                tmp_data.append(('co_posonlyargcount', 0))
        for el in tmp_data:
            kk = prepare_data(el[0])
            vv = prepare_data(el[1])
            res[kk] = vv
        return res


# 5 cases (atom simple dict func class)


def de_prepare_data(not_raw_data):
    simplicies = [list, tuple]
    func_evidence = ['__code__', '__globals__', '__name__', '__defaults__', '__closure__']
    atom = [str, int, float, bool, type(None)]
    etalon = type(not_raw_data)
    # либо дикт либо класс либо функ
    if etalon == dict:
        kk = []
        for k in not_raw_data.keys():
            kk.append(k)
        if set(kk) == set(func_evidence):
            code_templates = {}
            # полный трындец
            ttmp = not_raw_data['__code__']
            code_templates['argcount'] = ttmp['co_argcount']
            code_templates['posonlyargcount'] = ttmp['co_posonlyargcount']
            code_templates['kwonlyargcount'] = ttmp['co_kwonlyargcount']
            code_templates['nlocals'] = ttmp['co_nlocals']
            code_templates['stacksize'] = ttmp['co_stacksize']
            code_templates['flags'] = ttmp['co_flags']
            code_templates['codestring'] = bytes(ttmp['co_code'])
            code_templates['constants'] = tuple(ttmp['co_consts'])
            code_templates['names'] = tuple(ttmp['co_names'])
            code_templates['varnames'] = tuple(ttmp['co_varnames'])
            code_templates['filename'] = ttmp['co_filename']
            code_templates['name'] = ttmp['co_name']
            code_templates['firstlineno'] = ttmp['co_firstlineno']
            code_templates['lnotab'] = bytes(ttmp['co_lnotab'])
            code_templates['freevars'] = tuple(ttmp['co_freevars'])
            code_templates['cellvars'] = tuple(ttmp['co_cellvars'])
            #
            tmp_code = types.CodeType(*code_templates.values())
            tmp_globals = de_prepare_data(not_raw_data["__globals__"])
            tmp_name = not_raw_data["__name__"]
            if not_raw_data['__defaults__'] is not None:
                my_argdefs = tuple(de_prepare_data(not_raw_data['__defaults__']))
            else:
                my_argdefs = None
            if not_raw_data['__closure__'] is not None:
                my_closure = tuple(de_prepare_data(not_raw_data['__closure__']))
            else:
                my_closure = None
            # my_closure = tuple(de_prepare_data(not_raw_data['__closure__']))

            my_func = types.FunctionType(tmp_code, tmp_globals, tmp_name, my_argdefs, my_closure)
            return my_func
            # # my_name = raw_data.__name__
            # my_argdefs = raw_data.__defaults__
            # my_closure = raw_data.__closure__

        else:
            res = {}
            for k, v in not_raw_data.items():
                kk = de_prepare_data(k)
                vv = de_prepare_data(v)
                res[kk] = vv
            return res

    # ok
    elif etalon in atom:
        return not_raw_data
    elif etalon in simplicies:
        res = []
        for el in not_raw_data:
            res.append(de_prepare_data(el))
        return res


def p(c):
    return "the res is {}".format(c)


def summ(a=9, b=1):
    return p(a + b)


class Man():
    def __init__(self, name, age=19):
        self.name = name
        self.age = age


# print(set([1,2]) == set([2,1]))
dct = {'vikusha': [{'vbh': bytes([6, 9, 123]), 'y': ('x', 5), 'o': {8, 'z'}}]}
# res_ser = prepare_data(dct)
# print(res_ser)
# print(yaml.dump(res_ser))
# res_deser = de_prepare_data(res_ser)
# print(res_deser)
# print(res_deser(3))
# fedia = Man("fedia")
# print(prepare_data(fedia))
# fabrica('json').dump(prepare_data(summ))
