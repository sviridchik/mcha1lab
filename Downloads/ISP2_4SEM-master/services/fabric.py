from serializations import JsonClass, TomlClass as t, YamlClass as y, PickleClass as p


def fabrica(s):
    if s == 'json':
        return JsonClass.JsonClassMy()
    elif s == 'pickle':
        return p.PickleClassMy()
    elif s == 'toml':
        return t.TomlClassMy()
    elif s == 'yaml':
        return y.YamlClassMy()

