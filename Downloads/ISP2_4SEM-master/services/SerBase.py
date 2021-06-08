from abc import ABC,abstractmethod,ABCMeta
# @abstractclass
class SerBaseClass:
    __metaclass__ = ABCMeta
    @abstractmethod
    def dump(self,obj,fp):
        pass

    @abstractmethod
    def dumps(self,obj):
        pass

    @abstractmethod
    def load(self,fp):
        pass

    @abstractmethod
    def loads(self,s):
        pass


