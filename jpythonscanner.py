from scanner import *
from state import *

#TOKEN Constants
TokenToIDMap = {'identifier':15,'integer':16,'>=':17,'<=':18,'==':19,'!=':20,'>':21,'<':22,'=':23,'(':24,')':25,'+':26,'-':27,'*':28,'/':29,'[':30,']':31,'{':32,'}':33,',':34,';':35,'stringconst':36,'comment':37,'endoffile':38}
IDToTokenMap = {15:'identifier',16:'integer',17:'>=',18:'<=',19:'==',20:'!=',21:'>',22:'<',23:'=',24:'(',25:')',26:'+',27:'-',28:'*',29:'/',30:'[',31:']',32:'{',33:'}',34:',',35:';',36:'stringconst',37:'comment',38:'endoffile'}

#KEYWORD Constants
False_keyword=14
None_keyword=9
True_keyword=13
and_keyword=4
decl_keyword=12
def_keyword=0
else_keyword=11
for_keyword=10
if_keyword=1
in_keyword=8
len_keyword=3
not_keyword=5
or_keyword=6
return_keyword=7
while_keyword=2

class jpythonScanner(Scanner):
	def __init__(self,instream):
		super().__init__(instream,0,{0: State(0,None,{';': 8, '>': 11, '!': 25, 'letter': 16, '[': 13, 'digit': 15, 'EOF': 12, '-': 6, ')': 2, ',': 5, '<': 9, 'quote': 27, '(': 1, ']': 14, '=': 10, '/': 7, '+': 4, '}': 19, 'doublequote': 26, 'pound': 17, '{': 18, '*': 3}), 1: State(1,24,{}), 2: State(2,25,{}), 3: State(3,28,{}), 4: State(4,26,{}), 5: State(5,34,{}), 6: State(6,27,{}), 7: State(7,29,{}), 8: State(8,35,{}), 9: State(9,22,{'=': 21}), 10: State(10,23,{'=': 22}), 11: State(11,21,{'=': 23}), 12: State(12,38,{}), 13: State(13,30,{}), 14: State(14,31,{}), 15: State(15,16,{'digit': 15}), 16: State(16,15,{'digit': 16, 'letter': 16}), 17: State(17,37,{'anycharbutnewline': 17}), 18: State(18,32,{}), 19: State(19,33,{}), 20: State(20,20,{}), 21: State(21,18,{}), 22: State(22,19,{}), 23: State(23,17,{}), 24: State(24,36,{}), 25: State(25,None,{'=': 20}), 26: State(26,None,{'doublequote': 24, 'anycharbutdoublequote': 26}), 27: State(27,None,{'anycharbutquote': 27, 'quote': 24})},{';': OrderedSet({59}), '/': OrderedSet({47}), '!': OrderedSet({33}), 'doublequote': OrderedSet({34}), 'anycharbutquote': OrderedSet({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255}), ',': OrderedSet({44}), 'anycharbutdoublequote': OrderedSet({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255}), 'EPSILON': OrderedSet(), 'digit': OrderedSet({48, 49, 50, 51, 52, 53, 54, 55, 56, 57}), 'EOF': OrderedSet({3}), 'letter': OrderedSet({65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122}), '-': OrderedSet({45}), ')': OrderedSet({41}), '[': OrderedSet({91}), '<': OrderedSet({60}), 'quote': OrderedSet({39}), ']': OrderedSet({93}), '=': OrderedSet({61}), '}': OrderedSet({125}), '(': OrderedSet({40}), '+': OrderedSet({43}), '>': OrderedSet({62}), 'anycharbutnewline': OrderedSet({0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255}), 'pound': OrderedSet({35}), '{': OrderedSet({123}), '*': OrderedSet({42})},{'True': 13, 'if': 1, 'while': 2, 'len': 3, 'for': 10, 'not': 5, 'else': 11, 'or': 6, 'in': 8, 'False': 14, 'def': 0, 'and': 4, 'None': 9, 'return': 7, 'decl': 12},15,True,37)

