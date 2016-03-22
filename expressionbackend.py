# The expression backend code

class Add:
    def __init__(self,left,right):
        self.left = left
        self.right = right
        
    def eval(self):
        return self.left.eval() + self.right.eval()
    
    def __repr__(self):
        return "Add(" + repr(self.left) + "," + repr(self.right) + ")"
    
    
class Mul:
    def __init__(self,left,right):
        self.left = left
        self.right = right
        
    def eval(self):
        return self.left.eval() * self.right.eval()
    
    def __repr__(self):
        return "Mul(" + repr(self.left) + "," + repr(self.right) + ")"    
    
    
class Num:
    def __init__(self,number):
        self.num = number
        
    def eval(self):
        return int(self.num)
    
    def __repr__(self):
        return "Num(" + repr(self.num) + ")"    
    
#class Id:
#    def __init__(self,id):
#        self.id = id
#        
#    def eval(self):
#        raise Exception("not implemented")
    
