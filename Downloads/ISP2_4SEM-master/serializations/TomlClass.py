from serializations.Exceptions import InvalidTypeSourceException

a = """{
  "AllData": {"ArchiveAndDearchieveConfiguration": {
      "Archieve": true,
      "DeArchieve": true
    },
    "FinderInfo": {
      "Coding": "utf8",
      "SourceDirectory": "/Users/victoriasviridchik/Desktop/lab2/SourceDir",
      "TargetDirectory": "/Users/victoriasviridchik/Desktop/lab2/TargetDir/",
      "LogPath": "/Users/victoriasviridchik/Desktop/zoo/templog.txt",
      "NeedToLog": true
    },
    "CompressingOptions": {
      "Compressing": false
    },
    "EncryptingAndDecriptingOptions": {
      "RandomKey": true,
      "Encrypt": false,
      "DEncrypt": false
    },

    "DataOptions": {
      "Server": "localhost\\SQLEXPRESS",
      "Database": "master",
      "Trusted_Connection": true
    }
  }
}"""

from services import SerBase
import inspect
import re
from pydoc import locate
from types import CodeType, FunctionType

FUNCTION_ATTRIBUTES = [
    "__code__",
    "__name__",
    "__defaults__",
    "__closure__"
]

CODE_OBJECT_ARGS = [
    'co_argcount',
    'co_posonlyargcount',
    'co_kwonlyargcount',
    'co_nlocals',
    'co_stacksize',
    'co_flags',
    'co_code',
    'co_consts',
    'co_names',
    'co_varnames',
    'co_filename',
    'co_name',
    'co_firstlineno',
    'co_lnotab',
    'co_freevars',
    'co_cellvars'
]


class TomlClassMy(SerBase.SerBaseClass):

    def dumps(self, obj) -> str:
        obj = Serializer.serialize(obj)
        return f"tuple = {serialize_toml(obj)}"

    def dump(self, obj, fp):
        with open(fp, 'w') as fp_prep:
            return fp_prep.write(self.dumps(obj))

    def loads(self, obj: str):
        obj = obj.split('=', 1)
        if len(obj) < 2:
            raise InvalidTypeSourceException()
        else:
            obj = obj[1]

        obj = deserialize_toml(obj.replace("\\n", "\n").strip())
        return Serializer.deserialize(obj)

    def load(self, fp):
        with open(fp, 'r') as fp_prep:
            prep_obj = self.loads(fp_prep.read())
        return prep_obj


class Serializer:

    @staticmethod
    def serialize(obj):
        ans = {}
        object_type = type(obj)
        if object_type == list:
            ans["type"] = "list"
            ans["value"] = tuple([Serializer.serialize(i) for i in obj])
        elif object_type == dict:
            ans["type"] = "dict"
            ans["value"] = {}

            for i in obj:
                key = Serializer.serialize(i)
                value = Serializer.serialize(obj[i])
                ans["value"][key] = value
            ans["value"] = tuple((k, ans["value"][k]) for k in ans["value"])
        elif object_type == tuple:
            ans["type"] = "tuple"
            ans["value"] = tuple([Serializer.serialize(i) for i in obj])
        elif object_type == bytes:
            ans["type"] = "bytes"
            ans["value"] = tuple([Serializer.serialize(i) for i in obj])
        elif obj is None:
            ans["type"] = "NoneType"
            ans["value"] = None
        elif inspect.isroutine(obj):
            ans["type"] = "function"
            ans["value"] = {}
            members = inspect.getmembers(obj)
            members = [i for i in members if i[0] in FUNCTION_ATTRIBUTES]
            for i in members:
                key = Serializer.serialize(i[0])
                if i[0] != "__closure__":
                    value = Serializer.serialize(i[1])
                else:
                    value = Serializer.serialize(None)
                ans["value"][key] = value
                if i[0] == "__code__":
                    key = Serializer.serialize("__globals__")
                    ans["value"][key] = {}
                    names = i[1].__getattribute__("co_names")
                    glob = obj.__getattribute__("__globals__")
                    globdict = {}
                    for name in names:
                        if name in glob and inspect.ismodule(glob[name]):
                            raise InvalidTypeSourceException
                        elif name == obj.__name__:
                            globdict[name] = obj.__name__
                        elif name in glob and not inspect.ismodule(name) and name not in __builtins__:
                            globdict[name] = glob[name]
                    ans["value"][key] = Serializer.serialize(globdict)
            ans["value"] = tuple((k, ans["value"][k]) for k in ans["value"])

        elif isinstance(obj, (int, float, complex, bool, str)):
            typestr = re.search(r"\'(\w+)\'", str(object_type)).group(1)
            ans["type"] = typestr
            ans["value"] = obj
        else:
            ans["type"] = "instance"
            ans["value"] = {}
            members = inspect.getmembers(obj)
            members = [i for i in members if not callable(i[1])]
            for i in members:
                key = Serializer.serialize(i[0])
                val = Serializer.serialize(i[1])
                ans["value"][key] = val
            ans["value"] = tuple((k, ans["value"][k]) for k in ans["value"])

        ans = tuple((k, ans[k]) for k in ans)
        return ans

    @staticmethod
    def deserialize(d):
        d = dict((a, b) for a, b in d)
        object_type = d["type"]
        ans = None
        if object_type == "list":
            ans = [Serializer.deserialize(i) for i in d["value"]]
        elif object_type == "dict":
            ans = {}
            if "value" not in d:
                raise InvalidTypeSourceException()
            for i in d["value"]:
                val = Serializer.deserialize(i[1])
                ans[Serializer.deserialize(i[0])] = val
        elif object_type == "tuple":
            ans = tuple([Serializer.deserialize(i) for i in d["value"]])
        elif object_type == "function":
            func = [0] * 4
            code = [0] * 16
            glob = {"__builtins__": __builtins__}
            for i in d["value"]:
                key = Serializer.deserialize(i[0])

                if key == "__globals__":
                    globdict = Serializer.deserialize(i[1])
                    for globkey in globdict:
                        glob[globkey] = globdict[globkey]
                elif key == "__code__":
                    val = i[1][1][1]
                    for arg in val:
                        codeArgKey = Serializer.deserialize(arg[0])
                        if codeArgKey != "__doc__":
                            codeArgVal = Serializer.deserialize(arg[1])
                            index = CODE_OBJECT_ARGS.index(codeArgKey)
                            code[index] = codeArgVal

                    code = CodeType(*code)
                else:
                    index = FUNCTION_ATTRIBUTES.index(key)
                    func[index] = (Serializer.deserialize(i[1]))

            func[0] = code
            func.insert(1, glob)

            ans = FunctionType(*func)
            if ans.__name__ in ans.__getattribute__("__globals__"):
                ans.__getattribute__("__globals__")[ans.__name__] = ans

        elif object_type == "NoneType":
            ans = None
        elif object_type == "bytes":
            ans = bytes([Serializer.deserialize(i) for i in d["value"]])
        else:
            if object_type == "bool":
                ans = d["value"] == "True"
            else:
                ans = locate(object_type)(d["value"])

        return ans


def serialize_toml(obj) -> str:
    if type(obj) == tuple:
        ans = ""
        for i in obj:
            ans += f"{serialize_toml(i)}, "
        return f"[ {ans[0:len(ans) - 1]}]"
    else:
        return f"\"{str(obj)}\"".replace("\n", "\\n")


def deserialize_toml(obj: str):
    if obj == '[]':
        return tuple()
    elif obj[0] == '[':
        obj = obj[1:len(obj) - 1]
        parsed = []
        depth = 0
        quote = False
        substr = ""
        for i in obj:
            if i == '[':
                depth += 1
            elif i == ']':
                depth -= 1
            elif i == '\"':
                quote = not quote
            elif i == ',' and not quote and depth == 0:
                parsed.append(deserialize_toml(substr))
                substr = ""
                continue
            elif i == ' ' and not quote:
                continue

            substr += i

        return tuple(parsed)
    else:
        return obj[1:len(obj) - 1]
