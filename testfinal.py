import re
import sys 
# from mem import Memory #memory(2) name wasn't recognized


def com(ii8, n):
    x = len(ii8)
    if x == n:
        return ii8
    else:
        m = ii8[::-1]
        # i=0
        for y in range(0, n-x):
            m = m + '0'
        m = m[::-1]
        return m


class Memory:
    data = {}
    text = []
    stack = []
    pointer = 268435456

    def add_data_at(self, add, val):
        # add = hex(add).zfill(8)
        add = '0x'+(hex(add)[2::].zfill(8))
        self.data[add] = hex(int(val, 2)).replace('0x', '').zfill(2)
        

    def add_data(self, type, val):
        if(type != '.asciiz'):
            val = val.replace(",", ' ')
        arr = val.split(' ')
        myreturnvalue = len(self.data)
        if(type == '.byte'):
            ret_value = self.pointer
            for x in arr:
                if(len(x) > 1):  # NO need to convert if passed value is already in hex
                    if (x[0] == '0' and x[1] == 'x'):
                        if(len(x) <= 4):
                            ok = com(x[2:], 2)
                            self.data[hex(self.pointer)] = ok
                            self.pointer += 1
                            print("to")
                        else:
                            print("can't store value because",x, "is too large")
                            self.data[hex(self.pointer)] = (x[2:])[-2:]
                            self.pointer+=1
                    else:
                        y = hex(int(x) & 0xff)[2::].zfill(2)
                        if(len(hex(int(x))) <= 4):
                            self.data[hex(self.pointer)] = y
                            self.pointer += 1
                        else:
                            print("can't store", x, "in a byte, because value is too large. truncating the value and storing 1 least significant nibble")
                            y=y[-2:]
                            self.data[hex(self.pointer)] = y
                            self.pointer += 1
                else:  # not a hex
                    self.data[hex(self.pointer)] = (com(hex(int(x))[2::], 2))
                    self.pointer += 1
            return hex(ret_value)

        elif(type == '.word'):
            ret_value = self.pointer
            for x in arr:
                if(len(x) > 1):  # NO need to convert if passed value is already in hex
                    if(x[0] == '0' and x[1] == 'x'):
                        if(len(x) <= 10):
                            y = com(x[2::], 8)
                        else:
                            print("value", x, " too large to fit in a word, storing 4 least sign. bytes")
                            y=x[2::][-8:]
                    else:  # not hex
                        y = hex(int(x) & 0xffffffff)[2::].zfill(8)
                        # print(y)
                        if(len(y) <= 8):
                            y = com(y, 8)
                        else:
                            print("can't store", x, "in a word, because value is too large. truncating the value and storing 4 least significant bytes")
                            y = y[-8:]
                else:  # length <=1
                    y = hex(int(x.strip()))[2::]
                    y = com(y, 8)
                y1 = y[0:2]
                y2 = y[2:4]
                y3 = y[4:6]
                y4 = y[6:8]
                self.data[hex(self.pointer)] = (y4)
                self.pointer += 1
                self.data[hex(self.pointer)] = (y3)
                self.pointer += 1
                self.data[hex(self.pointer)] = (y2)
                self.pointer += 1
                self.data[hex(self.pointer)] = (y1)
                self.pointer += 1  
            return hex(ret_value)   
        
        elif(type == '.halfword'):
            ret_value = self.pointer
            for x in arr:
                if(len(x) > 1):  # NO need to convert if passed value is already in hex
                    if(x[0] == '0' and x[1] == 'x'):
                        if(len(x)<=6):
                        	y = com(x[2::], 4)
                        else:
                            print("can't store value",x,"in halfword as its too large,truncating and storing 2 least significant bytes")
                            y= (x[2::])[-4]
                    else:  # not a hex
                        y = hex(int(x) & 0xffff)[2::].zfill(4)
                        # y = hex(int(x))[2::]
                        if(len(y) <= 4):
                            y = com(y, 4)
                        else:
                            print("can't store", x, "in a halfword, because value is too large, truncating and storing 2 least significant bytes")
                            y = y[-4:]
                else:  # length <=1
                    y = hex(int(x))[2::]
                    y = com(y, 4)
                y1 = y[0:2]
                y2 = y[2:4]
                self.data[hex(self.pointer)] = (y2)
                self.pointer += 1
                self.data[hex(self.pointer)] = (y1)
                self.pointer += 1  
            return hex(ret_value)
        
        elif(type == '.dword'):
            ret_value = self.pointer
            for x in arr:
                if(len(x) > 1):  # NO need to convert if passed value is already in hex
                    if(x[0] == '0' and x[1] == 'x' ):
                        if(len(x) <= 18):
                        	y = com(x[2::], 16)
                        else:
                            print("couldn't store", x, 'in a doubleword, as value is too large, truncating and storing 8 least significant bytes')
                            y = (x[2::])[-16:]
                    else:    # not a hex
                        y = hex(int(x) & 0xffffffffffffffff)[2::].zfill(16)
                        if(len(y) <= 16):
                            y = com(y, 16)
                        else:
                            print("couldn't store", x, 'in a doubleword, as value is too large, truncating and storing 8 least significant bytes')
                            y = y[-16:]
                else:  # length <=1
                    y = str(hex(int(x)))[2:]
                    y = com(y, 16)
                y1 = y[0:2]
                y2 = y[2:4]
                y3 = y[4:6]
                y4 = y[6:8]
                y5 = y[8:10]
                y6 = y[10:12]
                y7 = y[12:14]
                y8 = y[14:16]
                self.data[hex(self.pointer)]=(y8)
                self.pointer+=1
                self.data[hex(self.pointer)]=(y7)
                self.pointer+=1
                self.data[hex(self.pointer)]=(y6)
                self.pointer+=1
                self.data[hex(self.pointer)]=(y5)
                self.pointer+=1
                self.data[hex(self.pointer)]=(y4)
                self.pointer+=1
                self.data[hex(self.pointer)]=(y3)
                self.pointer+=1
                self.data[hex(self.pointer)]=(y2)
                self.pointer+=1
                self.data[hex(self.pointer)]=(y1)
                self.pointer+=1
            return hex(ret_value)
        
        elif(type == '.asciiz'):
            ret_value = self.pointer
            for x in range(len(val)):
                self.data[hex(self.pointer)] = (hex(ord(val[x]))[2::])
                self.pointer+=1
            self.data[hex(self.pointer)] = '00'
            self.pointer+=1
            return hex(ret_value)
        else:
            print("Unrecognized datatype directive",type)
            return
        	# print(val,"stored at =" ,hex(myreturnvalue+268435456))
        	# print(self.data)
        	# return hex(int(myreturnvalue+268435456))
		
    def get_data_at(self, add ):
        # x=int(0x10000000)
        # y=int(add)
        # z=y-x
        # print (self.data[hex(add & 0xffffffff).zfill(8)])
        try:
            return self.data[hex(add & 0xffffffff).zfill(8)]
        except:
            return '00'
    
    def add_text(self, val):
        self.text.append(val)

    def show_Memory(self):
        print("data segment---------------------------------------------------------------------------------------------------------\n", self.data)
        data_out = []
        '''
        for x in range(len(self.data)):
            # print(hex(268435456 + x)," ",self.data[x])
            data_out.append( str(hex(268435456 + x))+ " : " + str(self.data[x]) )
        '''
        print("text segment"+"("+str(len(self.text))+")",
              "---------------------------------------------------------------------------------------------------------\n", self.text, "\n\n")
        return data_out



dict3 = {
    "add": "000", "and": "111", "or": "110", "sll": "001", "slt": "010", "sra": "101", "srl": "101", "sub": "000", "xor": "100", "mul": "000", "div": "100", "rem": "110",
    "addi": "000", "andi": "111", "ori": "110", "lb": "000", "lh": "001", "lw": "010", "jalr": "000",
    "sb": "000", "sw": "010", "sh": "001",
    "beq": "000", "bne": "001", "bge": "101", "blt": "100",
    "auipc": "", "lui": "",
    "jal": ""
}

dict7 = {
    "add": "0000000", "and": "0000000", "or": "0000000", "sll": "0000000", "slt": "0000000", "sra": "0100000", "srl": "0000000", "sub": "0100000", "xor": "0000000",
    "mul": "0000001", "div": "0000001", "rem": "0000001"
}

dictionary_format = {
    'add': 'r', 'and': 'r', 'or': 'r', 'srl': 'r', 'sll': 'r', 'slt': 'r', 'sra': 'r', 'sub': 'r', 'xor': 'r', 'mul': 'r', 'div': 'r', 'rem': 'r',
    'addi': 'i', 'andi': 'i', 'ori': 'i', 'lb': 'i', 'lh': 'i', 'lw': 'i', 'jalr': 'i',
    'sb': 's', 'sw': 's', 'sh': 's',
    'beq': 'sb', 'bne': 'sb', 'bge': 'sb', 'blt': 'sb',
    'auipc': 'u', 'lui': 'u',
    'jal': 'uj'
}

dictionary_opcode = {
    'add': '0110011', 'and': '0110011', 'or': '0110011', 'srl': '0110011', 'sll': '0110011', 'slt': '0110011', 'sra': '0110011', 'sub': '0110011', 'xor': '0110011','mul': '0110011', 'div': '0110011', 'rem': '0110011',
    'addi': '0010011', 'andi': '0010011', 'ori': '0010011', 
    'lb': '0000011', 'lh': '0000011', 'lw': '0000011', 
    'jalr': '1100111',
    'sb': '0100011', 'sw': '0100011', 'sh': '0100011',
    'beq': '1100011', 'bne': '1100011', 'bge': '1100011', 'blt': '1100011',
    'auipc': '0010111', 'lui': '0110111', 'jal': '1101111'
}

# dict_labels = {}


def get_register(string):
    if (string[0] == 'x'):
        s1 = int(string[1::])
        if (-1 < s1 and s1 < 32 ):
            return format(s1, '05b')
        else:
            print ("Register not Identified {only 32 registers available}. Assuming the register to be x0\n")
            return -1
    elif (string[0] == 'a'):
        s1 = int(string[1::])
        if ( -1 < s1 and s1 < 8):
            return format(s1+10, '05b')
        else:
            print ("Register not Identified. Assuming the register to be a0\n")
            return -1
    else:
        print ("Register not Identified. Assuming the register to be x0\n")
        return -1


def immediate12bit(string):
    #print(string)
    if(len(string) > 1):
        if(string[0] == '0' and string[1] == 'x'):
            if(len(string) > 5):
                print ("Immediate value out of range, must be 12 bit wide {Range: [-2048,2047]}. Assuming the Immediate value as zero\n")
                return ("000000000000")
            else:
                return bin(int(string[2::], 16))[2::].zfill(12)  # 33333
    # elif (string[0]=='0' and string[1]=='x'): #being a hexadecimal number we need to convert it to a 12 bit value
    #	n = int(string) - 2**12
        elif (string[0] == '-'):  # eg.  -16
            n = int(string[1::])
            if (n<2049):
                n = 2**12 - n
                return (format(n, '012b'))
            else:
                print ("Immediate value out of range, must be 12 bit wide {Range: [-2048,2047]}. Assuming the Immediate value as zero\n")
                return ("000000000000")
        else:
            mike_check = int(string)
            if (mike_check < 2048):
                return (format(int(string), '012b'))
            else:
                print ("Immediate value out of range, must be 12 bit wide {Range: [-2048,2047]}. Assuming the Immediate value as zero\n")
                return ("000000000000")
    else:
        if (len(string) == 1):
            if (string[0] != '0' and string[0] != '1' and string[0] != '2' and string[0] != '3' and string[0] != '4' and string[0] != '5' and string[0] != '6' and string[0] != '7' and string[0] != '8' and string[0] != '9'):
                print ("Immediate value must be a digit {Range: [-2048,2047]}. Assuming the Immediate value as zero\n")
                return ("000000000000")
        mike_check = int(string)
        if (mike_check < 2048):
            return (format(int(string), '012b'))
        else:
            print ("Immediate value out of range, must be 12 bit wide {Range: [-2048,2047]}. Assuming the Immediate value as zero\n")
            return ("000000000000")


def immediate20bit(string):
    if(len(string) > 1):
        if(string[0] == '0' and string[1] == 'x'):
            if(len(string) > 7):
                return ("Immediate value of range, must be 20 bit wide {Range: [-524288,524287]}. Assuming the Immediate value as zero\n")
                return ("00000000000000000000")
            else:  # return  as it is
                return bin(int(string[2::], 16))[2::].zfill(20)
        elif(string[0] == '-'):
            n = int(string[1::])
            if (n < 524289):
                n = 2**20 - n
                return format(n, '020b')
            else:
                return ("Immediate value of range, must be 20 bit wide {Range: [-524288,524287]}. Assuming the Immediate value as zero\n")
                return ("00000000000000000000")
        else:
            bigmike_check = int(string)
            if (bigmike_check < 524288):
                return format(int(string), '020b')
            else:
                print ("Immediate value of range, must be 20 bit wide {Range: [-524288,524287]}. Assuming the Immediate value as zero\n")
                return ("00000000000000000000")
    else:
        if (len(string) == 1):
            if (string[0] != '0' and string[0] != '1' and string[0] != '2' and string[0] != '3' and string[0] != '4' and string[0] != '5' and string[0] != '6' and string[0] != '7' and string[0] != '8' and string[0] != '9'):
                print ("Immediate value must be a digit {Range: [-524288,524287]}. Assuming the Immediate value as zero\n")
                return ("00000000000000000000")
        bigmike_check = int(string)
        if (bigmike_check < 524288):
            return format(int(string), '020b')
        else:
            print ("Immediate value of range, must be 20 bit wide {Range: [-524288,524287]}. Assuming the Immediate value as zero\n")
            return ("00000000000000000000")


def get_mc(l, pc, labels,data):
    if(dictionary_format.get(l[0],-1)==-1):
        print("incorrect command",l[0],end='')
        return -2,-2,''
    elif dictionary_format[l[0]] == 'r':
        #checking if we got enough values {mc1,mc2 will be returned as -2,-2 if not}
        exp = 4
        land = len(l)
        if (land != exp):
            print ("Expected",exp - 1,"arguments but received",land - 1,end='')
            return -2,-2,''
        #continue making mc
        f7 = dict7[l[0]]
        f3 = dict3[l[0]]
        rd = get_register(l[1])
        rs1 = get_register(l[2])
        rs2 = get_register(l[3])
        if(rd==-1 or rs1==-1 or rs2==-1):
            print("Error: Undefined register in R-format instruction",l[0])
            sys.exit()
        opcode = dictionary_opcode[l[0]]
        # print(f7,rs2,rs1,f3,rd,opcode)
        mc = f7 + rs2 + rs1 + f3 + rd + opcode
        # print(mc,'0x'+'%.*x'%(8,int('0b'+mc,0)), format(int(mc,2),"#010x"))
        return '%#010x' % (int('0b'+mc, 0)),-1,l[0]+" "+l[1]+" "+l[2]+" "+l[3]+"   "
    if(dictionary_format[l[0]] == 'i'):
        opcode = dictionary_opcode[l[0]]
        rd = get_register(l[1])
        f3 = dict3[l[0]]
        if(opcode !='0000011'): #not a load instruction
            rs1 = get_register(l[2])
            if(rs1==-1 or rd==-1):
                print("Error: undefined register in load instruction",l[0])
                sys.exit()
            imm = immediate12bit(l[3])
        else: #load instruction
            # print(l)
            if(len(l)==4): #simple register available
                rs1 = get_register(l[2])
                if(rs1==-1 or rd==-1):
                    print("Error: undefined register in",l[0])
                    sys.exit()
                imm = immediate12bit(str(l[3]))
            elif(len(l)==3 and data.get(l[2],-1)!=-1): #load of a variable and variable is defined
                new_l = ['auipc',l[1],'0x10000']
                # print(new_l,pc)
                mc1 = get_mc(new_l,pc,labels,data)
                print(mc1[2])
                pc+=4
                print("value",data[l[2]])
                new_l = [l[0],l[1],l[1],int(data[l[2]],16) - 268435456 - pc + 4] # load x1 , x1 , offset and offset = data[l[2]] - int(0x10000000) - pc 
                # print(new_l,pc)
                # print(int(data[l[2]],16) - 268435456 - pc + 4)
                mc2 = get_mc(new_l,pc,labels,data)
                # print(l)
                return mc1[0],mc2[0],mc1[2]+" $ "+l[0]+" "+ l[1]+" " + str(int(data[l[2]],16) - 268435456 - pc + 4) +"("+l[1]+")"
            else:
                print("incorrect format for the instruction. either",l[2],"not defined, or more than expected number of parameters passed")
        # print(imm,rs1,f3,rd,opcode)
        mc = imm + rs1 + f3 + rd + opcode
        rep = str(l[0]) +" "+ str(l[1])+ " " +str(l[2])+ " " +str(l[3])+ "   "
        if(opcode=='0000011'):
            rep = str(l[0])+" "+str(l[1])+" "+str(l[3])+"("+l[2]+")   "
        # print(mc,'0x'+'%.*x'%(8,int('0b'+mc,0)), format(int(mc,2),"#010x"))
        return '%#010x' % (int('0b'+mc, 0)),-1,rep
    if(dictionary_format[l[0]] == 's'):
        #checking if we got enough values {mc1,mc2 will be returned as -2,-2 if not}
        exp = 4
        land = len(l)
        if (land != exp):
            print ("Expected",exp - 1,"arguments but received",land - 1,end='')
            return -2,-2,''
        #continue making mc
        #print(l)
        imm = immediate12bit(l[3])
        rs1 = get_register(l[2])
        rs2 = get_register(l[1])
        if(rs1==-1 or rs2==-2):
            print("Error: undefined register in Store instruction",l[0])
            sys.exit()
        f3 = dict3[l[0]]
        opcode = dictionary_opcode[l[0]]
        #print(imm[0:7:],rs2,rs1,f3,imm[7::],opcode)
        mc = imm[0:7:] + rs2 + rs1 + f3 + imm[7::] + opcode
        #print(mc)
        return '%#010x' % (int('0b'+mc, 0)),-1,l[0] + " "+l[1]+" "+l[3]+"("+l[2]+")   "
    elif(dictionary_format[l[0]] == 'sb'):
        #checking if we got enough values {mc1,mc2 will be returned as -2,-2 if not}
        exp = 4
        land = len(l)
        if (land != exp):
            print ("Expected",exp - 1,"arguments but received",land - 1,end='')
            return -2,-2,''
        #continue making mc
        # print(labels)
        # print()
        imm = int((labels[l[3]]*4 - pc)/2)
        rs1 = get_register(l[1])
        rs2 = get_register(l[2])
        if(rs1==-1 or rs2==-2):
            print("Error: undefined register in Branch instruction",l[0])
            sys.exit()
        f3 = dict3[l[0]]
        opcode = dictionary_opcode[l[0]]
        # print("immiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii = ", (labels[l[3]]*4 - pc))
        if(str(imm)[0] != '-'):
            imm = format(int(imm), '#014b')[2::]
        else:
            imm = format(2**12 - abs(int(imm)), '#014b')[2::]
        # print(2**12 - abs(int(imm)))
        # print(imm[0],imm[2:8:],imm[8::],imm[1])  # , rs2, rs1, f3, imm[7::], opcode)
        mc = imm[0] + imm[2:8:] + rs2 + rs1 + f3 + imm[8::] + imm[1] + opcode
        # print(mc,'%#010x'%(int('0b'+mc,0)))#, format(int(mc,2),"#010x"))
        return '%#010x' % (int('0b'+mc, 0)),-1,l[0]+" "+l[1]+" "+l[2]+" "+str((labels[l[3]]*4 - pc))+"   "
    if(dictionary_format[l[0]] == 'u'):
        #checking if we got enough values {mc1,mc2 will be returned as -2,-2 if not}
        exp = 3
        land = len(l)
        if (land != exp):
            print ("Expected",exp - 1,"arguments but received",land - 1,end='')
            return -2,-2,''
        #continue making mc
        imm = immediate20bit(l[2])
        rd = get_register(l[1])
        if(rd==-1):
            print("Error: undefined register in instruction",l[0])
            sys.exit()
        opcode = dictionary_opcode[l[0]]
        #print(l,imm,rd,opcode)
        mc = imm+rd+opcode
        tttt = l[2]
        if(l[2][0]=='0' and l[2][1]=='x'):
            tttt = int(l[2],16)
        # print(tttt)
        return '%#010x' % (int('0b'+mc, 0)),-1,l[0]+" "+l[1]+" "+str(tttt)+"  "
    if(dictionary_format[l[0]] == 'uj'):  # jal x1,label
        #checking if we got enough values {mc1,mc2 will be returned as -2,-2 if not}
        exp = 3
        land = len(l)
        if (land != exp):
            print ("Expected",exp - 1,"arguments but received",land - 1,end='')
            return -2,-2,''
        #continue making mc
        opcode = dictionary_opcode[l[0]]
        rd = get_register(l[1])
        if(rd==-1):
            print("Error: Undefined register in jal instruction")
            sys.exit()
        #print("label[l[2]] =", labels[l[2]], "current pc =", pc)
        imm = int(labels[l[2]])*4 - pc
        # print("imm = ", imm)
        tttt = imm
        # imm = "11111111111111111111" #relative value from address of current instructionAddress of label - PC(considerin PC is at current instruction)
        if(str(imm)[0] != '-'):
            imm = format(imm, "#022b")[2::]
        else:
            imm = format(2**20 - abs(imm), '#022b')[2::]
        #print(imm,rd,opcode)
        # because jal takes imm[20:1] ignores the first bit(0 index) as all instruction jumps are a multiple of 4 and 2 thus reducing redundancy
        imm = imm[0] + imm[0:19]
        imm = imm[0] + imm[10::] + imm[9] + imm[1:9:]
        #print(imm)
        mc = str(imm) + rd + opcode
        return '%#010x' % (int('0b'+mc, 0)),-1,l[0]+" "+l[1]+" "+str(tttt)+"   "


def convertToMC(instruction, labels,datas,data_out):
    # print(instruction)
    # print(labels)
    # print(datas,"\nshindeiru")
    writefile = open("out.mc", "w")
    write2 = open('outfile.mc','w')
    writefile.write("TEXT_SEGMENT_OF_MCFILE\n\n")
    instructionAddress = 0
    for x in instruction:
        # this flag is for switching format in case of {jalr x0,0(x1)} equating {jalr x0 x1 0}
        flag = False
        # print(x)
        if(x.strip("\r\n") == "" or x.strip()==''):
            print("no instruction here, a empty line encountered!")
            continue
        
        s = str(x)
        s = s.strip("\r\n")
        s = s.strip()
        l = []
        s = s.replace(",", " ")
        s = s.replace(":", " ")
        if (s.count('(') != 0):
            flag = True
            s = s.replace("(", " ")
            s = s.replace(")", "")
        # print(s)
        l = s.split()
        if (flag == True and len(l)==4) :
            l[2], l[3] = l[3], l[2]
            s = l[0]+" " + l[1] + " " + l[2] + " " + l[3]
        
        # print("nextInstruction = ",l)
        machineCode1,machineCode2,basicCode = get_mc(l, instructionAddress, labels,datas)
        #print(machineCode1,machineCode2) ###################3
        #if mc1,mc2 is -2,-2 that means we recieved less arguments, so we skip mc writing
        if (machineCode1 == -2 and machineCode2 == -2):
            machineCode1 = machineCode2
            msg = ''
            for x in l:
                msg = msg + x+" " 
            print(", in the instruction",msg)
            sys.exit()
        else:
            # print(l)
            writefile.write(hex(instructionAddress) + "  \t:\t"+machineCode1 + "\n")
            write2.write(hex(instructionAddress) +" "+machineCode1+" "+basicCode[:basicCode.find("$")].strip()+"\n")
            M.add_text(machineCode1)
            instructionAddress += 4
            if(machineCode2!=-1):
                writefile.write(hex(instructionAddress) + "  \t:\t"+machineCode2 + "\n")
                write2.write(hex(instructionAddress) + " "+machineCode2+" "+basicCode[basicCode.find("$")+1:].strip() + "\n")
                M.add_text(machineCode2)
                instructionAddress+=4
        
    writefile.write("\n\nDATA_SEGMENT_OF_MCFILE\n{only the contents of memory locations that were explicity set by the program are shown}\n\n")
    # for ke in datas:
    #     writefile.write(str(ke)+"\t:\t"+str(datas[ke])+"\n")
    for k in range(len(data_out)):
        writefile.write(data_out[k]+"\n")
    writefile.close()


def getDirectives():
    rf = open("t.asm", "r")
    file = rf.read()
    s = ''
    ins = []
    textsegment = True
    labels = {}
    data = {}
    tocheck = []
    for x in file:
        if(x == '\n'):
            if(s.strip(" \r\n") != '' or s.strip()!=''):
                # ins.append(s)
                #print("line :", s)
                # print("textsegment=", textsegment)
                if(s.find("#")!=-1):
                    s=s[0:s.find('#'):]
                if(s.strip() == '.data'):
                    textsegment = False
                    #ins.append(s)
                elif(s.strip()== '.text'):
                    textsegment = True
                    #ins.append(s)
                elif(s.find(":") != -1 and textsegment == True):
                    # cuu = s[0:s.find(":"):].replace('\t', 'aa')
                #    print("wooohooo", cuu)
                    labels[s[0: s.find(":"):].strip()] = len(ins)
                    if(s[s.find(":")+1::].strip().replace(" ", "") != ''):
                        ins.append(s[s.find(":")+1::])
                elif(textsegment==True):
                    ins.append(s)
                    y = s
                    y = y.replace(",",' ')
                    y = y.strip()
                    yy = y.split()
                    if(len(yy)==3 and data.get(yy[2],-1)!=-1):
                        tocheck.append(len(ins))
                elif(textsegment==False):
                    s=s.strip()
                    dd = s.split(":")
                    dd[0]=dd[0].strip()
                    dd[1]=dd[1].strip()
                    dd.append(dd[1][dd[1].find(" ")::].strip())
                    
                    dd[1] = dd[1][:dd[1].find(" "):].strip()
                    dd[2] = dd[2].replace('"','')
                    #print(dd)
                    data[dd[0]] = dd[1],dd[2]
                    #print(data)
                    address_for_stored_variable = M.add_data(data[dd[0]][0],data[dd[0]][1])
                    data[dd[0]] = address_for_stored_variable
                    #print(data)
            s = ''
        else:
            s += x
    #s=s.replace(" ",'')
    # print("last=",s.strip("\r\n"),sep="")
    if(s.strip("\r\n") != '' or s.strip()!=''):  #this segment is in case final character is not a new line and process the last line irrespective of that
        # print("line :", s)
        # print("textsegment=", textsegment)
        s=s.strip()
        if(textsegment == False and s.find(':')!=-1 and s.strip('\r\n')!='.data' and s.strip('\r\n')!='.text'):
            s=s.strip()
            dd = s.split(":")
            dd[0]=dd[0].strip()
            dd[1]=dd[1].strip()
            dd.append(dd[1][dd[1].find(" ")::].strip())
            dd[1] = dd[1][:dd[1].find(" "):].strip()
            dd[2] = dd[2].replace('"','')
            #print(dd)
            data[dd[0]] = dd[1],dd[2]
            #print(data)
            address_for_stored_variable = M.add_data(data[dd[0]][0],data[dd[0]][1])
            data[dd[0]] = address_for_stored_variable
            # ins.append(s)
        elif(textsegment == True and s.find(':')==-1 and s.strip('\r\n')!='.data' and s.strip('\r\n')!='.text'):
            ins.append(s)
        elif(s.find(":") != -1 and textsegment == True and s.strip('\r\n')!='.data' and s.strip('\r\n')!='.text'):
        #    print("wooohooo", s[s.find(":")+1::])
            labels[s[0: s.find(":"):].replace(" ",'')] = len(ins)
            if(s[s.find(":")+1::].strip("\r\n").replace(" ","")!=''):
                ins.append(s[s.find(":")+1::])
            
    #print(ins)
    #print(labels)
    # print(len(ins))
    rf.close()
    
    # print(ins)
    for o in tocheck:
        for k in labels.keys():
            # print(o,k,labels[k])
            if((labels[k])>=o):
                labels[k]+=1
                # print(o,k,labels[k])
    
    
    return ins, labels , data

M = Memory()
instructions, labela,dataa = getDirectives() # returns list of instructions , labels , data (containing variable with address they point to)
# print(dataa)
data_out = M.show_Memory()
convertToMC(instructions, labela,dataa,data_out)
# M.show_Memory()

