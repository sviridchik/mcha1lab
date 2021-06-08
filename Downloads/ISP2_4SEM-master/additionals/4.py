
class Vector(object):
    """creates vector"""

    def __init__(self,x=0,y=0):
        self.x,self.y = x,y

    def __str__(self):
        return "({},{})".format(self.x,self.y)

    def __add__(self, other):
        return Vector(self.x+other.x,self.y+other.y)

    def __sub__(self, other):
        return Vector(self.x-other.x,self.y-other.y)

    def __mul__(self, other):
        return Vector(self.x*other,self.y*other)

    def scalar(self,other):
        return Vector(self.x*other.x+self.x*other.x)

    def __len__(self):
        return ((self.x)**2+(self.y)**2)**(1/2)

    def __cmp__(self, other):
        """ self < other	отрицательное
            self == other	нуль
            self > other	положительное"""
        return (len(self) - len(other))


# class IndexIterable:
#     def __init__(self, obj):
#         self.obj = obj
#
#     def __getitem__(self, index):
#         return self.obj[index]
#
#
# for letter in IndexIterable('str'):
#     print(letter)

