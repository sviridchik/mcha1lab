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

import re


# import json


class JsonClassMy(SerBase.SerBaseClass):
    def dump(self, obj, fp):
        """сериализует Python объект в файл"""
       # prep_obj = prepare_data(obj)
        with open(fp, 'w') as fp_prep:
            return fp_prep.write(self.dumps(obj))

    def dumps(self, obj):
        """сериализует Python объект в строку"""

        def dumps_prepared(prep_obj):
            return str(prep_obj).replace("'", '"').replace('None', 'null').replace(
                'True', 'true').replace('False', 'false').replace('(', '[').replace(')', ']')

        prep_obj = prepare_data(obj)
        return dumps_prepared(prep_obj)

    def load(self, fp):
        """десериализует Python объект из файла"""
        # fp_prep = open(fp, 'w')
        with open(fp, 'r') as fp_prep:
            prep_obj = self.loads(fp_prep.read())
            # try:
            #     prep_obj = de_prepare_data(json.load(fp_prep))
            # except json.JSONDecodeError as e:
            #     raise InvalidTypeSourceException(e)
            return prep_obj

    def loads(self, s):
        """десериализует Python объект из строки"""

        # try:
        #     prep_obj = de_prepare_data(json.loads(s))
        # except json.JSONDecodeError as e:
        #     raise InvalidTypeSourceException(e)
        # return prep_obj

        def loads_prep(s: str):
            def find_list_end(data, i):
                if data[i].strip()[-1] == ']':
                    return 0
                j = i
                open_count = 0
                while open_count or j == i:
                    open_count += data[j].count('[')
                    open_count -= data[j].count(']')
                    j += 1
                return j

            def find_dict_end(data, i):
                if data[i].strip()[-1] == '}':
                    return 0
                j = i
                open_count = 0
                while open_count or j == i:
                    open_count += data[j].count('{')
                    open_count -= data[j].count('}')
                    # if data[j].strip()[-1] == '}':
                    #     open_count -= 1
                    # elif data[j].strip()[0] == '{':
                    #     open_count += 1
                    j += 1
                return j

            s = s.strip()

            if s[0] == '{' and s[-1] == '}':
                # dict
                res = {}
                data = s[1:len(s) - 1].split(',')
                if len(data) == 1 and data[0].strip() == '':
                    return {}
                skip_count = 0
                for i in range(len(data)):
                    if skip_count:
                        skip_count -= 1
                        continue
                    # for key_value in s[1:len(s) - 1].split(','):
                    key, value = data[i].split(':', 1)
                    if value.strip()[0] == '[':
                        j = find_list_end(data, i)
                        if j != 0:
                            value = ','.join([value] + data[i + 1:j])
                            skip_count = j - i - 1

                    if value.strip()[0] == '{':
                        j = find_dict_end(data, i)
                        if j != 0:
                            value = ','.join([value] + data[i + 1:j])
                            skip_count = j - i - 1

                    res[loads_prep(key)] = loads_prep(value)
                return res
            elif s[0] == '"' and s[-1] == '"':
                # str
                return str(s[1:len(s) - 1])
            elif s == 'null':
                return None
            elif s == 'true':
                return True
            elif s == 'false':
                return False
            elif s[0] == '[' and s[-1] == ']':
                res = []
                data = s[1:len(s) - 1].split(',')
                if len(data) == 1 and data[0].strip() == '':
                    return []
                skip_count = 0
                for i in range(len(data)):
                    if skip_count:
                        skip_count -= 1
                        continue
                    value = data[i]
                    if value.strip()[0] == '[':
                        j = find_list_end(data, i)
                        if j != 0:
                            value = ','.join([value] + data[i + 1:j])
                            skip_count = j - i - 1

                    if value.strip()[0] == '{':
                        j = find_dict_end(data, i)
                        if j != 0:
                            value = ','.join([value] + data[i + 1:j])
                            skip_count = j - i - 1

                    res.append(loads_prep(value))
                return res
            elif re.fullmatch(r"[-+]?\d+", s):
                return int(s)
            elif re.fullmatch(r"[-+]?\d+\.\d*", s):
                return float(s)
            else:
                raise InvalidTypeSourceException(f'Wrong json type near {s}')

        prep_obj = de_prepare_data(loads_prep(s))
        return prep_obj