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
# import re as r
# pattern = '""(\w*[^""{}])"": {([^}]*)} ?'
# res = r.match(pattern,a)
# for r in res:
#     print(rim
from services.ordinary_types import *
from services import SerBase

#
# class YamlClassMyOld(SerBase.SerBaseClass):
#     def dump(self, obj, fp):
#         """сериализует Python объект в файл"""
#         prep_obj = prepare_data(obj)
#
#         with open(fp, 'w') as fp_prep:
#             try:
#                 return yaml.dump(prep_obj, fp_prep)
#             except yaml.YAMLError as e:
#                 raise InvalidTypeSourceException(e)
#
#     def dumps(self, obj):
#         """сериализует Python объект в строку"""
#         prep_obj = prepare_data(obj)
#         try:
#             return yaml.dump(prep_obj)
#         except yaml.YAMLError as e:
#             raise InvalidTypeSourceException(e)
#
#     def load(self, fp):
#         """десериализует Python объект из файла"""
#         # prep_obj = prepare_data(fp)
#         # fp_prep = open(fp, 'r')
#         with open(fp, 'r') as fp_prep:
#             try:
#                 prep_obj = de_prepare_data(yaml.load(fp_prep, Loader=yaml.FullLoader))
#             except yaml.YAMLError as e:
#                 raise InvalidTypeSourceException(e)
#             return prep_obj
#
#     def loads(self, s):
#         """десериализует Python объект из строки"""
#         try:
#             prep_obj = de_prepare_data(yaml.load(s, Loader=yaml.FullLoader))
#         except yaml.YAMLError as e:
#             raise InvalidTypeSourceException(e)
#         return prep_obj


tab_len = 2

gap_symbols = "\n\r\t "
COMPLEX_TYPES = [list, dict]


class YamlClassMy(SerBase.SerBaseClass):
    def dump(self, obj, fp):
        """сериализует Python объект в файл"""
        with open(fp, 'w') as fp_prep:
            return fp_prep.write(self.dumps(obj))

    def dumps(self, obj):
        """сериализует Python объект в строку"""
        prep_obj = prepare_data(obj)
        return self.__dumps(prep_obj, 0)

    def load(self, fp):
        """десериализует Python объект из файла"""
        with open(fp, 'r') as fp_prep:
            prep_obj = self.loads(fp_prep.read())
            return prep_obj

    def loads(self, s):
        """десериализует Python объект из строки"""
        prep_obj = de_prepare_data(self.loads_dict(s, 0, 0)[0])
        # prep_obj = self.loads_dict(s, 0, 0)[0]
        return prep_obj

    def __dumps(self, obj, depth):
        response = ""
        if type(obj) is dict:
            for key, value in obj.items():
                response += " " * tab_len * depth
                response += self.obj_to_str(key) + ": "
                if type(value) in COMPLEX_TYPES:
                    response += '\n'
                response += self.__dumps(value, depth + 1)
                if type(value) not in COMPLEX_TYPES:
                    response += '\n'
        elif type(obj) is list:
            for value in obj:
                response += " " * tab_len * (depth - 1) + '-'
                if type(value) not in COMPLEX_TYPES:
                    response += ' ' + self.__dumps(value, depth)
                else:
                    response += self.__dumps(value, depth)[tab_len * (depth - 1) + 1:]
                if type(value) not in COMPLEX_TYPES:
                    response += '\n'
        else:
            return self.obj_to_str(obj)
        return response

    def loads_dict(self, s, current, depth, flag=False):
        if not all([ord(c) <= 255 and c != '\t' and c != '"' for c in s]):
            raise InvalidTypeSourceException('not allowed character')
        response = {}
        while True:
            prev_current = current
            line, current = self.read_until_symbol(s, current, '\n')
            if current == len(s):
                return response, current
            if ':' not in line:
                return self.loads_list(s, prev_current, depth)
            key, value = line.split(':')
            if max(0, depth - 1) * tab_len < len(key) and key[max(0, depth - 1) * tab_len] == '-':
                if not flag:
                    return self.loads_list(s, prev_current, depth)
                else:
                    return response, prev_current

            if not self.get_spaces_count(key) == depth * tab_len:
                return response, prev_current

            key = self.str_to_obj(self.trim(key))
            value = self.trim(value)

            if len(value) > 0:
                response[key] = self.str_to_obj(value)
                current += 1
            else:
                response[key], current = self.loads_dict(s, current + 1, depth + 1)
                if flag:
                    return response, current
                continue

    def loads_list(self, s, current, depth):
        response = []
        while True:
            if current >= len(s):
                return response, current
            prev_current = current
            line, current = self.read_until_symbol(s, current, '\n')
            if '-' not in line:
                return response, prev_current
            if not line[max(0, (depth - 1)) * tab_len] == '-':
                return response, prev_current
            if ':' not in line:
                line = line[0:max(0, (depth - 1)) * tab_len] + ' ' + line[max(0, (depth - 1)) * tab_len + 1:]
                response.append(self.str_to_obj(self.trim(line)))
                current += 1
                continue

    def get_spaces_count(self, s):
        i = 0
        while i < len(s) and s[i] == ' ':
            i += 1
        return i

    def read_until_symbol(self, text, current, symbols):
        res = ""
        while len(text) > current and not text[current] in symbols:
            res += text[current]
            current += 1
        return res, current

    def trim(self, s):
        l, r = -1, 0
        for i in range(len(s)):
            if l == -1 and not s[i] in gap_symbols:
                l = i
            if not s[i] in gap_symbols:
                r = i + 1
        return s[l:r]

    def obj_to_str(self, obj):
        if type(obj).__name__ == 'str':
            return "\'" + str(obj) + "\'"
        if type(obj).__name__ == 'bool':
            return str(obj).lower()
        if obj is None:
            return "null"
        return str(obj)

    def str_to_obj(self, s):
        if s[0] == "'" and s[0] == s[-1]:
            return s[1:-1]
        if s == 'false':
            return False
        if s == 'true':
            return True
        if s == 'null':
            return None
        try:
            return int(s)
        except:
            return float(s)
