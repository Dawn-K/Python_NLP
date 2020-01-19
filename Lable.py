import re,random

class Lable:
    def __init__(self,name:str):
        self.name = name
        pass
    
class LablePool:
    def __init__(self,typ:str):
        self.pos = 0
        self.lable = []
        file_name = 'midTag'
        if typ == 'L1':
            file_name='endTag'
        with open(file_name,'r',encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n>').lstrip('<')
                self.lable.append(Lable(line))

        
    def getLable(self) -> Lable:
        res = self.lable[self.pos]
        
        return res