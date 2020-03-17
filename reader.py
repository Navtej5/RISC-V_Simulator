import re
from memory import Memory

dict3 = {
    "add": "000", "and": "111", "or": "110", "sll": "001", "slt": "001", "sra": "101", "srl": "101", "sub": "000", "xor": "100", "mul": "000", "div": "100", "rem": "110",
    "addi": "000", "andi": "111", "ori": "110", "lb": "000", "ld": "011", "lh": "001", "lw": "010", "jalr": "000",
    "sb": "000", "sw": "010", "sd": "011", "sh": "001",
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
    'addi': 'i', 'andi': 'i', 'ori': 'i', 'lb': 'i', 'ld': 'i', 'lh': 'i', 'lw': 'i', 'jalr': 'i',
    'sb': 's', 'sw': 's', 'sh': 's',
    'sd': 'i',
    'beq': 'sb', 'bne': 'sb', 'bge': 'sb', 'blt': 'sb',
    'auipc': 'u', 'lui': 'u',
    'jal': 'uj'
}

dictionary_opcode = {
    'add': '0110011', 'and': '0110011', 'or': '0110011', 'srl': '0110011', 'sll': '0110011', 'slt': '0110011', 'sra': '0110011', 'sub': '0110011', 'xor': '0110011',
    'mul': '0110011', 'div': '0110011', 'rem': '0110011',
    'addi': '0010011', 'andi': '0010011', 'ori': '0010011', 'lb': '0000011', 'ld': '0000011', 'lh': '0000011', 'lw': '0000011', 'jalr': '1100111',
    'sb': '0100011', 'sw': '0100011', 'sd': '0100011', 'sh': '0100011',
    'beq': '1100011', 'bne': '1100011', 'bge': '1100011', 'blt': '1100011',
    'auipc': '0010111', 'lui': '0110111', 'jal': '1101111'
}

dict_labels = {}


def get_register(string):
    s1 = int(string[1::])
    return format(s1, '05b')


def immediate12bit(string):
    if(len(string) > 1):
        if(string[0] == '0' and string[1] == 'x'):
            if(len(string) > 5):
                return "Immediate value out of range, must be 12 bit wide"
            else:
                return bin(int(string[2::], 16))[2::].zfill(12)  # 33333
            n = int(string)
            return (format(n, '012b'))
    # elif (string[0]=='0' and string[1]=='x'): #being a hexadecimal number we need to convert it to a 12 bit value
    #	n = int(string) - 2**12
        elif (string[0] == '-'):  # eg.  -16
            n = int(string[1::])
            n = 2**12 - n
            return (format(n, '012b'))
        else:
            return format(int(string), '012b')
    else:
        return (format(int(string), '012b'))


def immediate20bit(string):
    if(len(string) > 1):
        if(string[0] == '0' and string[1] == 'x'):
            if(len(string) > 7):
                return "Immediate value of range, must be 20 bit wide"
            else:  # return  as it is
                return bin(int(string[2::], 16))[2::].zfill(20)
        elif(string[0] == '-'):
            n = int(string[1::])
            n = 2**20 - n
            return format(n, '020b')
        else:
            return format(int(string), '020b')
    else:
        return format(int(string), '020b')


def get_mc(l, pc, labels,no_of_segmentflags):
    if dictionary_format[l[0]] == 'r':
        f7 = dict7[l[0]]
        f3 = dict3[l[0]]
        rd = get_register(l[1])
        rs1 = get_register(l[2])
        rs2 = get_register(l[3])
        opcode = dictionary_opcode[l[0]]
        # print(f7,rs2,rs1,f3,rd,opcode)
        mc = f7 + rs2 + rs1 + f3 + rd + opcode
        # print(mc,'0x'+'%.*x'%(8,int('0b'+mc,0)), format(int(mc,2),"#010x"))
        return '%#010x' % (int('0b'+mc, 0))
    if(dictionary_format[l[0]] == 'i'):
        rd = get_register(l[1])
        rs1 = get_register(l[2])
        opcode = dictionary_opcode[l[0]]
        f3 = dict3[l[0]]
        imm = immediate12bit(l[3])
        # print(imm,rs1,f3,rd,opcode)
        mc = imm + rs1 + f3 + rd + opcode
        # print(mc,'0x'+'%.*x'%(8,int('0b'+mc,0)), format(int(mc,2),"#010x"))
        return '%#010x' % (int('0b'+mc, 0))
    if(dictionary_format[l[0]] == 's' or dictionary_format[l[0]] == 'sb'):
        if(dictionary_format[l[0]] == 's'):
            imm = immediate12bit(l[3])
        else:  # sb format requires branch's label address
            imm = int(((labels[l[3]] - no_of_segmentflags)*4 - pc)/2)
        rs1 = get_register(l[1])
        rs2 = get_register(l[2])
        f3 = dict3[l[0]]
        opcode = dictionary_opcode[l[0]]
        #print("imm = ", imm,)
        if(str(imm)[0] != '-'):
            imm = format(int(imm), '#014b')[2::]
        else:
            imm = format(2**12 - abs(int(imm)), '#012b')[2::]
        # print(imm)
        # imm = imm[0] + imm[0:10:]
        # print(imm[0],imm[2:8:],imm[8::],imm[1])  # , rs2, rs1, f3, imm[7::], opcode)
        mc = imm[0] + imm[2:8:] + rs2 + rs1 + f3 + imm[8::] + imm[1] + opcode
        # print(mc,'%#010x'%(int('0b'+mc,0)))#, format(int(mc,2),"#010x"))
        return '%#010x' % (int('0b'+mc, 0))
    if(dictionary_format[l[0]] == 'u'):
        imm = immediate20bit(l[2])
        rd = get_register(l[1])
        opcode = dictionary_opcode[l[0]]
        # print(imm,rd,opcode)
        mc = imm+rd+opcode
        return '%#010x' % (int('0b'+mc, 0))
    if(dictionary_format[l[0]] == 'uj'):  # jal x1,label
        opcode = dictionary_opcode[l[0]]
        rd = get_register(l[1])
        #print("label[l[2]] =", labels[l[2]], "current pc =", pc)
        imm = (int(labels[l[2]]) - no_of_segmentflags)*4 - pc
        #print("imm = ", imm)
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
        return '%#010x' % (int('0b'+mc, 0))


def convertToMC(instruction, labels):
    # readingfile = open("assemble.asm", "r")
    writefile = open("out.mc", "w")
    instructionAddress = 0
    dataFlag = False  # True means this is a data segment and false means it is a text segment
    no_of_segment_flags=0
    for x in instruction:
        # this flag is for switching format in case of {jalr x0,0(x1)} equating {jalr x0 x1 0}
        flag = False
        # print(x)
        if(x.strip("\r\n") == ""):
            print("no instruction here, this is empty")
            continue
        elif(x.strip("\r\n").replace(" ","") == ".data"):
            dataFlag = True
            no_of_segment_flags+=1
            continue
        elif(x.strip("\r\n").replace(" ","") == ".text"):
            dataFlag = False
            no_of_segment_flags+=1
            continue
        # elif(x.find(":") != -1 and dataFlag == False):
        #     dict_labels[x[0:x.find(":"):]] = hex(instructionAddress)
        #     x = x[x.find(":")+1::]
        #     x = x.strip(" \r\n")
        #     print(dict_labels)
        #     # print("after this x is:",x,"[]")
        #     if(x == ""):
        #         # print("wubba lubaa dub dub")
        #         continue
        # elif(x.find(":")!=-1 and dataFlag==True): this will handle variables
        # 	dict_variables[] =
        if(dataFlag == False):
            s = str(x)
            s = s.strip("\r\n")
            l = []
            s = s.replace(",", " ")
            s = s.replace(":", " ")
            if (s.count('(') != 0):
                flag = True
                s = s.replace("(", " ")
                s = s.replace(")", "")
            # print(s)
            l = s.split()
            if flag == True:
                l[2], l[3] = l[3], l[2]
                s = l[0]+" " + l[1] + " " + l[2] + " " + l[3]
            machineCode = get_mc(l, instructionAddress, labels,no_of_segment_flags)
            writefile.write(hex(instructionAddress) + " "+machineCode + "\n")
            M.add_text(machineCode)
            instructionAddress += 4
        elif(dataFlag == True):  # this is data segment
            s = str(x)
            s = s.replace(":", " ")
            l = s.split()
            print(l)
    writefile.close()


def getDirectives():
    rf = open("t.asm", "r")
    file = rf.read()
    s = ''
    ins = []
    textsegment = True
    labels = {}
    data = {}
    for x in file:
        if(x == '\n'):
            if(s.strip(" \r\n") != ''):
                # ins.append(s)
                #print("line :", s)
                # print("textsegment=", textsegment)
                if(s.strip() == '.data'):
                    textsegment = False
                    ins.append(s)
                elif(s.strip()== '.text'):
                    textsegment = True
                    ins.append(s)
                elif(s.find(":") != -1 and textsegment == True):
                    cuu = s[0:s.find(":"):].replace('\t', 'aa')
                #    print("wooohooo", cuu)
                    labels[s[0: s.find(":"):].strip()] = len(ins)
                    if(s[s.find(":")+1::].strip().replace(" ", "") != ''):
                        ins.append(s[s.find(":")+1::])
                elif(textsegment==True):
                    ins.append(s)
                elif(textsegment==False):
                    s=s.strip()
                    dd = s.split(":")
                    dd[0]=dd[0].strip()
                    dd[1]=dd[1].strip()
                    dd.append(dd[1][dd[1].find(" ")::].strip())
                    dd[1] = dd[1][:dd[1].find(" "):].strip()
                    print(dd)
                    data[dd[0]] = dd[1],dd[2]
            s = ''
            #print(len(ins))
        else:
            s += x
    #s=s.replace(" ",'')
    #print("last=",s.strip("\r\n"),sep="")
    if(s.strip("\r\n") != ''):
        # print("line :", s)
        # print("textsegment=", textsegment)
        if(s.strip("\r\n") == '.data'):
            textsegment = False
            ins.append(s)
            # ins.append(s)
        elif(s.strip("\r\n") == '.text'):
            textsegment = True
            ins.append(s)
        elif(s.find(":") != -1 and textsegment == True):
        #    print("wooohooo", s[s.find(":")+1::])
            labels[s[0: s.find(":"):].replace(" ",'')] = len(ins)
            if(s[s.find(":")+1::].strip("\r\n").replace(" ","")!=''):
                ins.append(s[s.find(":")+1::])
        else:
            ins.append(s)
    #print(ins)
    #print(labels)
    # print(len(ins))
    print("YOOO\n",data)
    rf.close()
    return ins, labels

M = Memory()
instructions, labela = getDirectives()
convertToMC(instructions, labela)
M.show_Memory()

'''
0. handle directives
0.1 handle variables
0.2 handle labels
1. handling address conversion of variables starting with x

'''
