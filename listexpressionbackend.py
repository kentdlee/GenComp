# The expression backend code

class Append:
    def __init__(self,left,right):
        self.left = left
        self.right = right
        
    def eval(self):
        return self.left.eval() + self.right.eval()
    
    def __repr__(self):
        return "Append(" + repr(self.left) + "," + repr(self.right) + ")"
    
    

class Cons:
    def __init__(self,left,right):
        self.left = left
        self.right = right
        
    def eval(self):
        return [self.left.eval()] + self.right.eval()
    
    def __repr__(self):
        return "Cons(" + repr(self.left) + "," + repr(self.right) + ")"    
    
    
class Item:
    def __init__(self,number):
        self.num = number
        
    def eval(self):
        return int(self.num)
    
    def __repr__(self):
        return "Item(" + repr(self.num) + ")"    

class Nil:
    def __init__(self):
        pass

    def eval(self):
        return []

    def __repr__(self):
        return "Nil()"

class Num:
    def __init__(self,val):
        self.val = val

    def eval(self):
        return self.val 

    def __repr__(self):
        return "Num(" + str(self.val) + ")"
        
