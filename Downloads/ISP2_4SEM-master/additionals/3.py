import re
data = "0.123"
# data = "vic123@mail.com"
data1 = "https://example.com:8000/path/to/myfile.html?key1=value1&key2=value2"

def cheker(data:str)->None:
    """ ● валидации email-адреса
        ● валидации записи числа с плавающей строчкой
        ● получения отдельных частей URL (схема, хост, порт, путь,
параметры) с помощью механизма именованных групп"""
    pattern_float = "[+-]?([0-9]+[.][0-9]+)"
    pattern_email = r"([0-9A-Za-z!#$%&‘*+—=?^_`{|}~]+[@])([A-Za-z]+)[.]([a-z]{2,3})?"
    flag_float = 1
    flag_email = 0

    res = re.match(pattern_float, data)
    if res is None:
        res=re.match(pattern_email, data)
        flag_email = 1
        flag_float = 0
    if (res is not None) and res.span()[0] == 0 and res.span()[1] ==  len(data):
        if flag_float:
            print("It's a good float")
        elif flag_email:
            print("It's a good email")
    else:
        print("Nothing is found ,sorry ")


def getter(data:str)->None:
    pattern = r"(?P<scheme>[a-z]+[:])([/]{2})(?P<host>[a-z.]+)[:](?P<port>[0-9]+)[/](?P<path>[a-z/.]+)[?](?P<params>[a-z0-9=&]+)"
    if re.match(pattern,data) is not None:
        print("scheme : {}".format(re.match(pattern,data1).group('scheme')))
        print("host : {}".format(re.match(pattern,data1).group('host')))
        print("port : {}".format(re.match(pattern,data1).group('port')))
        print("params : {}".format(re.match(pattern,data1).group('params')))
    else:
        print("Nothing is found ,sorry ")

cheker(data)
getter(data1)