import re
f=open("assemble.asm","r")
g=open("out.mc","w")
#s= str(f.readline())

def register_to_5bit(string,form):
	#print(string,form)
	if ((string[0] != '1') and (string[0] != '2') and (string[0] != '3') and (string[0] != '4') and (string[0] != '5') and (string[0] != '6') and (string[0] != '7') and (string[0] != '8')and(string[0] != '9')):
		s2 = int(string[1::])
		s5 = format(s2,'05b')
	else: #is a starting with a number
		if(form=="i" or form=='s' or form=='sb'):
			
			s2 = int(string)
			s5 = format(s2, '012b')
		#print(s5)
	return s5

dict3 = {
  	"add": "000", "and": "111", "or": "110", "sll": "001", "slt": "001", "sra": "101", "srl": "101", "sub": "000", "xor": "100", "mul": "000", "div": "100", "rem": "110",
  	"addi":"000", "andi":"111", "ori":"110", "lb":"000", "ld":"011", "lh":"001", "lw":"010", "jalr":"000",
  	"sb":"000", "sw":"010", "sd":"011", "sh":"001",
  	"beq":"000", "bne":"001", "bge":"101", "blt":"100",
  	"auipc":"", "lui":"",
  	"jal":""
}

dict7 = {
  	"add": "0000000", "and": "0000000", "or": "0000000", "sll": "0000000", "slt": "0000000", "sra": "0100000", "srl": "0000000", "sub": "0100000", "xor": "0000000", 
	"mul": "0000001", "div": "0000001", "rem": "0000001"
} 

dictionary_format = {
'add':'r','and':'r','or':'r','srl':'r','sll':'r','slt':'r','sra':'r','sub':'r','xor':'r','mul':'r','div':'r','rem':'r',
'addi':'i','andi':'i','ori':'i','lb':'i','ld':'i','lh':'i','lw':'i','jalr':'i',
'sb':'s','sw':'s','sh':'s',
'sd':'i',
'beq':'sb','bne':'sb','bge':'sb','blt':'sb',
'auipc':'u','lui':'u',
'jal':'uj'}

dictionary_opcode = {
'add':'0110011','and':'0110011','or':'0110011','srl':'0110011','sll':'0110011','slt':'0110011','sra':'0110011','sub':'0110011','xor':'0110011',
'mul':'0110011','div':'0110011','rem':'0110011',
'addi':'0010011','andi':'0010011','ori':'0010011','lb':'0000011','ld':'0000011','lh':'0000011','lw':'0000011','jalr':'1100111',
'sb':'0100011','sw':'0100011','sd':'0100011','sh':'0100011',
'beq':'1100011','bne':'1100011','bge':'1100011','blt':'1100011',
'auipc':'0010111','lui':'0110111','jal':'1101111'
}

for x in f:
	s=str(x)
	s=s.strip("\r\n")
	l=[]
	s=s.replace(","," ")
	s=s.replace(":"," ")
	print(s)
	l=s.split()
	#print(l)
	 #getting values converted from user
	rs1,rs2,rd,imm,f7,f3=(-1,-1,-1,-1,-1,-1)
	if dictionary_format[l[0]]=='r':
		f7=dict7[l[0]]
	if(dictionary_format[l[0]]=='r' or dictionary_format[l[0]]=='i'):
		rs1 = register_to_5bit(l[2],dictionary_format[l[0]])
		f3 = dict3[l[0]]
	if(dictionary_format[l[0]]=='r' or dictionary_format[l[0]]=='s' or dictionary_format[l[0]]=='sb'):
		rs2 = register_to_5bit(l[3],dictionary_format[l[0]])
	if(dictionary_format[l[0]]=='i'):
		imm = register_to_5bit(l[3],dictionary_format[l[0]])
	rd = register_to_5bit(l[1],dictionary_format[l[0]])
	#imm=
#	'''
	print("rd=",rd," rs1=",rs1," rs2=",rs2," imm=",imm," f7=",f7," f3=",f3,sep='')
	g.write(s)
	g.write("\n")
f.close()
g.close()



'''
0. handle directives
0.1 handle variables
0.2 handle labels
1. handling address conversion of variables starting with x

'''