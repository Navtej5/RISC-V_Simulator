from testfinal import Memory
import math
import time
mem = Memory()
mem.show_Memory()

def printregisters():
    for i in [0,1,2,3,4,5,6,7,9,10,11,12,13,22,23,30,31]:
        print("x{}\t".format(i),'0x'+(hex(int(registers[i],2)).replace('0x','').zfill(8)))

def extractsignedvalue(binstring, n):
    # print("sss",binstring,len(binstring))
    if(len(binstring) == n):
        if(binstring[0] == '0'):
            return int(binstring, 2)
        else:
            return int(binstring, 2)-2**(n)
    else:
        return int(binstring, 2)

def converttosignedvalue(number,n): #decimal number in number and decimal unit in n
    pop = -1
    if(n==12):
        pop = 0xfff
    elif(n==4):
        pop=0xf
    elif(n==20):
        pop = 0xfffff
    elif( n ==32):
        pop = 0xffffffff
    ans = bin( number & pop).replace("0b",'').zfill(n)
    # print(number,ans,"poop",hex(pop))
    if(number<(-1)*(2**(n-1)) or number>2**(n-1) - 1):
        print("error: value overflow for number =",number)

    return ans

'''0:rs1 1:rs2 2:imm 3:rd 4:f3 5:f7 6:opcode 7:ir 8:pc 9:current_function '''
#carr_for_list=['00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000',
# '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000',
# '00000000000000000000000000000000'] #list of strings

# Initialised values of all the 32 registers in binary
registers=['00000000000000000000000000000000','00000000000000000000000000000000','01111111111111111111111111110000','00010000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000']

stack = {}

def com_8(i8):
    x = len(i8)
    if x==8:
        return i8
    else:
        m = i8[::-1]
        # i=0
        for y in range(0,8-x):
            m = m + '0'
        m = m[::-1]
        return m

def com_32(i32):
    x = len(i32)
    if x==32:
        return i32
    else:
        m = i32[::-1]
        # i=0
        for y in range(0,32-x):
            m = m + '0'
        m = m[::-1]
        return m

def getIR(file_name,pc):
    f = open(file_name,'r')
    i = 0
    for x in f:
        if i==pc:
            ins_a = x.split()
            ins_a[1]=ins_a[1].replace("0x","")
            res = "{0:32b}".format(int(ins_a[1], 16))
            res=res.replace(" ","0")
            #res=int(ins_a[1],16)
            #y = bin(res).replace("0b","")
            #print(res)
            return res
        i=i+4
    return -1

i_file = "outfile.mc" # give file name here

def fetch(carr_for_list):
    # print(carr_for_list[8])
    # print("befor fetch",carr_for_list[8])
    carr_for_list[7] = getIR(i_file,int(carr_for_list[8],2))
    if(carr_for_list[7]==-1):
        return "over"
    carr_for_list[8]=bin(int(carr_for_list[8],2)+4).replace("0b","").zfill(32)
    # print("after fetch",carr_for_list[8])
    return "continue"

'''0:rs1 1:rs2 2:imm 3:rd 4:f3 5:f7 6:opcode 7:ir 8:pc 9:current_function '''
def decode(carr_for_list):
    #print(carr_for_list)
    ins=carr_for_list[7]
    opcode = ins[25:32]
    carr_for_list[6]=opcode
    if(opcode=="0110011"):#r-format
        carr_for_list[5]=ins[0:7] #f7
        carr_for_list[1]=ins[7:12] #rs2
        carr_for_list[0]=ins[12:17] #rs1
        carr_for_list[4]=ins[17:20] #f3
        carr_for_list[3]=ins[20:25] #rd

        if carr_for_list[5]== "0000000": #f7 = 0000000
            if carr_for_list[4]=="000":
                carr_for_list[9]="add"

            elif carr_for_list[4]=="111":
                carr_for_list[9]="and"

            elif carr_for_list[4]=="110":
                carr_for_list[9]="or"

            elif carr_for_list[4]=="001":
                carr_for_list[9]="sll"

            elif carr_for_list[4]=="010":
                carr_for_list[9]="slt"

            elif carr_for_list[4]=="101":
                carr_for_list[9]="srl"

            elif carr_for_list[4]=="100":
                carr_for_list[9]="xor"

        elif carr_for_list[5]== "0100000":
            if carr_for_list[4]=="101":
                carr_for_list[9]="sra"

            elif carr_for_list[4]=="000":
                carr_for_list[9]="sub"

        elif carr_for_list[5]== "0000001":
            if carr_for_list[4]=="000":
                carr_for_list[9]="mul"

            elif carr_for_list[4]=="100":
                carr_for_list[9]="div"

            elif carr_for_list[4]=="110":
                carr_for_list[9]="rem"


    elif(opcode=="0100011"):# s-format
        carr_for_list[2]=ins[0:7]   #immediate value should take only starting 12 bits of this string
        carr_for_list[1]=ins[7:12] #rs2
        carr_for_list[0]=ins[12:17] #rs1
        carr_for_list[4]=ins[17:20] #f3
        carr_for_list[2]+=ins[20:25]
        # carr_for_list[2]+ins[20:25]
        if carr_for_list[4]=="000":
            carr_for_list[9]="sb"

        elif carr_for_list[4]=="010":
            carr_for_list[9]="sw"

        elif carr_for_list[4]=="011":
            carr_for_list[9]="sd"

        elif carr_for_list[4]=="001":
            carr_for_list[9]="sh"


            '''0:rs1 1:rs2 2:imm 3:rd 4:f3 5:f7 6:opcode 7:ir 8:pc 9:current_function '''
    elif(opcode=="1100011"):#sb

        #carr_for_list[2][11]=ins[0]
        #carr_for_list[2][4:10]=ins[1:7]
        carr_for_list[1]=ins[7:12]
        carr_for_list[0]=ins[12:17]
        carr_for_list[4]=ins[17:20]
        #carr_for_list[2][0:4]=ins[20:24]
        #carr_for_list[2][10]=ins[24]
        carr_for_list[2]=(ins[0]+ins[24]+ins[1:7]+ins[20:24]) #this still needs to be multiplied by 2 for execution
        if carr_for_list[4]=="000":
            carr_for_list[9]="beq"
            m=int(carr_for_list[0],2)
            n=int(carr_for_list[1],2)
            o=extractsignedvalue(carr_for_list[2],12)*2
            # print(carr_for_list[8],"inside beq function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
            if extractsignedvalue(registers[m],32)==extractsignedvalue(registers[n],32):
                # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
                if(o>0):
                    carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
                else:
                    carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")

        elif carr_for_list[4]=="001":
            carr_for_list[9]="bne"
            m=int(carr_for_list[0],2)
            n=int(carr_for_list[1],2)
            o=extractsignedvalue(carr_for_list[2],12)*2
            # print(carr_for_list[8],"inside beq function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
            if extractsignedvalue(registers[m],32)!=extractsignedvalue(registers[n],32):
                # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
                if(o>0):
                    carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
                else:
                    carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")

        elif carr_for_list[4]=="101":
            carr_for_list[9]="bge"
            m=int(carr_for_list[0],2)
            n=int(carr_for_list[1],2)
            o=extractsignedvalue(carr_for_list[2],12)*2
            # print(carr_for_list[8],"inside beq function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
            if extractsignedvalue(registers[m],32)>=extractsignedvalue(registers[n],32):
                # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
                if(o>0):
                    carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
                else:
                    carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")

        elif carr_for_list[4]=="100":
            carr_for_list[9]="blt"
            m=int(carr_for_list[0],2)
            n=int(carr_for_list[1],2)
            o=extractsignedvalue(carr_for_list[2],12)*2
            # print(carr_for_list[8],"inside beq function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
            if extractsignedvalue(registers[m],32)<extractsignedvalue(registers[n],32):
                # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
                if(o>0):
                    carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
                else:
                    carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")

    elif(opcode=="0000011"):#lb,lw,lh,ld
        carr_for_list[2]=ins[0:12]
        carr_for_list[0]=ins[12:17]
        carr_for_list[3]=ins[20:25]
        carr_for_list[4]=ins[17:20]

        if carr_for_list[4]=="000":
            carr_for_list[9]="lb"

        elif carr_for_list[4]=="001":
            carr_for_list[9]="lh"

        elif carr_for_list[4]=="010":
            carr_for_list[9]="lw"

        elif carr_for_list[4]=="011":
            carr_for_list[9]="ld"


    elif opcode=="0010111": #U-auipc
        carr_for_list[2]=ins[0:20]
        carr_for_list[3]=ins[20:25]
        carr_for_list[9]="auipc"

    elif opcode=="0110111": #U-lui
        carr_for_list[2]=ins[0:20]
        carr_for_list[3]=ins[20:25]
        carr_for_list[9]="lui"

    elif opcode=="0010011": #I-format   #andi ori addi
        carr_for_list[2]=ins[0:12]
        carr_for_list[0]=ins[12:17]
        carr_for_list[3]=ins[20:25]
        carr_for_list[4]=ins[17:20]

        if carr_for_list[4]=="110":
            carr_for_list[9]="ori"

        elif carr_for_list[4]=="111":
            carr_for_list[9]="andi"

        elif carr_for_list[4]=="000":
            carr_for_list[9]="addi"

    elif opcode=="1100111": #jalr
        carr_for_list[2]=ins[0:12]
        carr_for_list[0]=ins[12:17]
        carr_for_list[3]=ins[20:25]
        carr_for_list[4]=ins[17:20]
        carr_for_list[9]="jalr"

    elif opcode=="1101111": #jal
        # carr_for_list[2][0]=ins[0]
        # carr_for_list[2][1:9]=ins[12:20]
        # carr_for_list[2][10]=ins[11]
        carr_for_list[2]=ins[0]+ins[12:20]+ins[11]+ins[1:11]
        carr_for_list[3]=ins[20:25]
        carr_for_list[9]="jal"

def execute(carr_for_list,registers):
    fun_name=carr_for_list[9]
    if(fun_name=="add"):
        return add(carr_for_list)
    elif(fun_name=="and"):
        return and1(carr_for_list)
    elif(fun_name=="or"):
        return or1(carr_for_list)
    elif(fun_name=="sll"):
        return sll(carr_for_list)
    elif(fun_name=="slt"):
        return slt(carr_for_list)
    elif(fun_name=="sra"):
        return sra(carr_for_list)
    elif(fun_name=="srl"):
        return srl(carr_for_list)
    elif(fun_name=="sub"):
        return sub(carr_for_list)
    elif(fun_name=="xor"):
        return xor(carr_for_list)
    elif(fun_name=="mul"):
        return mul(carr_for_list)
    elif(fun_name=="div"):
        return div(carr_for_list)
    elif(fun_name=="rem"):
        return rem(carr_for_list)
    elif(fun_name=="addi"):
        return addi(carr_for_list)
    elif(fun_name=="andi"):
        return andi(carr_for_list)
    elif(fun_name=="ori"):
        return ori(carr_for_list)
    elif(fun_name=="lb"):
        return lb(carr_for_list)
    elif(fun_name=="lh"):
        return lh(carr_for_list)
    elif(fun_name=="lw"):
        return lw(carr_for_list)
    elif(fun_name=="jalr"):
        return jalr(carr_for_list)
    elif(fun_name=="sb"):
        return sb(carr_for_list)
    elif(fun_name=="sw"):
        return sw(carr_for_list)
    elif(fun_name=="sd"):
        return sd(carr_for_list)
    elif(fun_name=="sh"):
        return sh(carr_for_list)
    elif(fun_name=="beq"):
        return beq(carr_for_list)
    elif(fun_name=="bne"):
        return bne(carr_for_list)
    elif(fun_name=="bge"):
        return bge(carr_for_list)
    elif(fun_name=="blt"):
        return blt(carr_for_list)
    elif(fun_name=="auipc"):
        return auipc(carr_for_list)
    elif(fun_name=="lui"):
        return lui(carr_for_list)
    elif(fun_name=="jal"):
        return jal(carr_for_list)

#list_fun=[add, and1, or1, sll, slt, sra, srl, sub, xor, mul, div, rem,addi, andi, ori, lb, ld, lh, lw, jalr,sb, sw, sd, sh,beq, bne, bge, blt, auipc, lui,jal]


def add(carr_for_list):
    #print(carr_for_list)
    m=int(carr_for_list[0],2)#values in registers and carr_for_list are in binary format
    n=int(carr_for_list[1],2)
    x=extractsignedvalue(registers[m],32) + extractsignedvalue(registers[n],32)
    o=int(carr_for_list[3],2)
    # print(x,"herffffffffffffffffre")
    # registers[o]=converttosignedvalue(x,32)
    return converttosignedvalue(x,32),o,"R";
    # print("yo")
    #print(m)
    #print(n)
    #print(x)

def and1(carr_for_list):
    # print("yooooooo2")
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    # print(int(registers[m],2),int(registers[n],2))
    x = extractsignedvalue(registers[m],32) & extractsignedvalue(registers[n],32)
    # print(x,"ans")
    o=int(carr_for_list[3],2)
    return converttosignedvalue(x,32),o,"R";
    # print(o)
    # registers[o]=converttosignedvalue(x,32)
    # print(registers[o])

def or1(carr_for_list):
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    x = extractsignedvalue(registers[m],32) | extractsignedvalue(registers[n],32)
    o = int(carr_for_list[3],2)
    return converttosignedvalue(x,32),o,"R";
    # registers[o]=converttosignedvalue(x,32)

def slt(carr_for_list):
    # print("9999999999999999999999999999999999999999999999999")
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    o=int(carr_for_list[3],2)
    if extractsignedvalue(registers[m],32) < extractsignedvalue(registers[n],32):
        return converttosignedvalue(1,32),o,"R";
        # print('yessssssssssssssss')
        # registers[o]=converttosignedvalue(1,32)
    else:
        # registers[o]=converttosignedvalue(0,32)
        return converttosignedvalue(0,32),o,"R";

def sll(carr_for_list):
    m = int(carr_for_list[0],2) #rs1
    n = int(carr_for_list[1],2) #rs2
    if(extractsignedvalue(registers[n],32)<0):
        print("error: negative shift count not allowed")
        return "error: negative shift count not allowed"
    if(extractsignedvalue(registers[n],32)>32):
        x=0
    else:
        x = extractsignedvalue(registers[m],32) << extractsignedvalue(registers[n],32)
    # print(int(registers[m],2),int(registers[n],2))
    o=int(carr_for_list[3],2)
    # print(x)
    return converttosignedvalue(x,32),o,"R";
    # registers[o]=converttosignedvalue(x,32)
    # print(registers[o],"hererere")

def sra(carr_for_list):
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    if(extractsignedvalue(registers[n],32)<0):
        print("error: negative shift count not allowed")
        return "error: negative shift count not allowed"
    elif(extractsignedvalue(registers[n],32)<=32):
        x = extractsignedvalue(registers[m],32)>>extractsignedvalue(registers[n],32)
    else:
        x= -1
    # x = int(registers[m],2) >> int(registers[n],2)
    o = int(carr_for_list[3],2)
    # print(x)
    # registers[o]=converttosignedvalue(x,32)
    return converttosignedvalue(x,32),o,"R";
    # print(registers[o],"hererere",len(registers[o]))

def srl(carr_for_list):#Some understanding problem
    m = int(carr_for_list[0],2) #rs1
    n = int(carr_for_list[1],2) #rs2
    o = int(carr_for_list[3],2)
    if(extractsignedvalue(registers[n],32)<0):
        print("error: negative shift count not allowed")
        return "error: negative shift count not allowed"
    elif(extractsignedvalue(registers[n],32)<=32):
        v = registers[m]
        for _ in range(int(registers[n],2)):
            v = ('0'+v)[:32]
        #registers[o]=com_32(v)
        return com_32(v),o,"R";
    else:
        v=0
        return converttosignedvalue(v,32),o,"R";
        # registers[o]=converttosignedvalue(v,32)

def sub(carr_for_list):
    m=int(carr_for_list[0],2)
    n=int(carr_for_list[1],2)
    x=extractsignedvalue(registers[m],32) - extractsignedvalue(registers[n],32)
    o=int(carr_for_list[3],2)
    return converttosignedvalue(x,32),o,"R";
    # registers[o]=converttosignedvalue(x,32)
    # print("yo1")

def xor(carr_for_list):
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    x = extractsignedvalue(registers[m],32) ^ extractsignedvalue(registers[n],32)
    # print("iiiiiiiiiiiiiiiii",converttosignedvalue(extractsignedvalue(registers[m],32)^extractsignedvalue(registers[n],32),32))
    o=int(carr_for_list[3],2)
    return converttosignedvalue(x,32),o,"R";
    # registers[o]=converttosignedvalue(x,32)

def mul(carr_for_list):
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    x = extractsignedvalue(registers[m],32) * extractsignedvalue(registers[n],32)
    o=int(carr_for_list[3],2)
    return converttosignedvalue(x,32),o,"R";
    # registers[o]=converttosignedvalue(x,32)

def div(carr_for_list):
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    if(extractsignedvalue(registers[n],32)==0):
        print("division by zero not allowed")
        return "error : division by zero not allowed"
    x = int(extractsignedvalue(registers[m],32) / extractsignedvalue(registers[n],32))
    o=int(carr_for_list[3],2)
    return converttosignedvalue(x,32),o,"R";
    # registers[o]=converttosignedvalue(x,32)

def rem(carr_for_list):
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    x = extractsignedvalue(registers[m],32) % extractsignedvalue(registers[n],32)
    o=int(carr_for_list[3],2)
    return converttosignedvalue(x,32),o,"R";
    # registers[o]=converttosignedvalue(x,32)

def addi(carr_for_list):
    m = int(carr_for_list[0],2)
    n = str(carr_for_list[2])
    # print("immediate value =",n,extractsignedvalue(n,12))
    # print(registers[m],extractsignedvalue(registers[m],32))
    x = extractsignedvalue(registers[m],32) + extractsignedvalue(n,12)
    # print((x))
    # print(converttosignedvalue(x,32))
    o = int(carr_for_list[3],2)
    return converttosignedvalue(x,32),o,"I";
    # registers[o]=converttosignedvalue(x,32)

def andi(carr_for_list):
    # print(carr_for_list)
    m = int(carr_for_list[0],2)
    n = str(carr_for_list[2])
    # print("debug",m,n)
    x = extractsignedvalue(registers[m],32) & extractsignedvalue(n,12)
    o = int(carr_for_list[3],2)
    return converttosignedvalue(x,32),o,"I";
    # registers[o]=converttosignedvalue(x,32)

def ori(carr_for_list):
    m = int(carr_for_list[0],2)
    n = str(carr_for_list[2])
    x = extractsignedvalue(registers[m],32) | extractsignedvalue(n,12)
    o = int(carr_for_list[3],2)
    return converttosignedvalue(x,32),o,"I";
    # registers[o]=converttosignedvalue(x,32)

def lb(carr_for_list):
    m=extractsignedvalue(carr_for_list[2],12) #immediate value
    k=int(carr_for_list[0],2) #rs1
    n=m+extractsignedvalue(registers[k],32) #calculate r[rs1] + imm

    # print(hex(n),m,k)
    # if(n<500000000):
    #     # print("address",hex(n))
    #     x=mem.get_data_at(n)  #to be reviewed
    # else:
    #     try:
    #         x=stack[hex(n)]
    #     except:
    #         x='00'
    # print(x, converttosignedvalue( extractsignedvalue(bin(int('0x'+x,16))[2:],8),32 ) , 'oyoyoyoyoy')
    y=int(carr_for_list[3],2)
    return n,y,"LOADBYTE";
    # registers[y]=converttosignedvalue(extractsignedvalue(bin(int('0x'+x,16))[2:],8),32)

def lw(carr_for_list):
    # print("m=====",carr_for_list[2])
    m=extractsignedvalue(carr_for_list[2],12)
    # print(m)
    k=int(carr_for_list[0],2)
    # print("address in register ",hex(int(registers[k],2)))
    n=m+int(registers[k],2)
    # print("n=====",(n-268435456))
    # print(hex(n),n)
    y=int(carr_for_list[3],2)
    return n,y,"LOADWORD";

        # print("loaded value =",x)
    # print("mama mia",int('0x'+x,16),x)

def lh(carr_for_list):
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    # if(n+1<500000000):
    #     x1=mem.get_data_at(n)
    #     x2=mem.get_data_at(n+1)
    #     x=x2+x1
    # else:#they are in stack
    #     try:
    #         x2=stack[hex(n+1)]
    #     except:
    #         x2='00'
    #     try:
    #         x1=stack[hex(n)]
    #     except:
    #         x1='00'
    #     x = x2+x1
    y=int(carr_for_list[3],2)
    return n,y,"LOADHALF"
    #registers[y]=converttosignedvalue(extractsignedvalue(bin(int('0x'+x,16))[2:],16),32)

def sb(carr_for_list):
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    itit = registers[y]
    return n,itit,"S";
    #returning final address, register_to_access , "S"

def sw(carr_for_list):
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    # print(k,m,registers[k])
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    itit = registers[y]
    return n,itit,"S";
    #returning final address, register_to_access , "S"

def sh(carr_for_list):
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    itit = registers[y]
    return n,itit,"S";
    #returning final address, register_to_access , "S"

def sd(carr_for_list): #venus didn't overwrite upper 4 bytes to '00', thus this also works similarly
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    itit = registers[y]
    return n,itit,"S";
    #returning final address, register_to_access , "S"

def beq(carr_for_list):
    # m=int(carr_for_list[0],2)
    # n=int(carr_for_list[1],2)
    # o=extractsignedvalue(carr_for_list[2],12)*2
    # # print(carr_for_list[8],"inside beq function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
    # if extractsignedvalue(registers[m],32)==extractsignedvalue(registers[n],32):
    #     # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
    #     if(o>0):
    #         carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
    #     else:
    #         carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")
    #         # carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
    #     # else:
    #     #     carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")
    #     # print('pc changed to',carr_for_list[8])
    return 1,1,"SB";

def bge(carr_for_list):
    # m=int(carr_for_list[0],2)
    # n=int(carr_for_list[1],2)
    # o=extractsignedvalue(carr_for_list[2],12)*2
    # if extractsignedvalue(registers[m],32)>=extractsignedvalue(registers[n],32):
    #     # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
    #     if(o>0):
    #         carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
    #     else:
    #         carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")
    return 1,1,"SB";

def bne(carr_for_list):
    # m=int(carr_for_list[0],2)
    # n=int(carr_for_list[1],2)
    # o=extractsignedvalue(carr_for_list[2],12)*2
    # # print(carr_for_list[8],"inside BNE function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
    # if extractsignedvalue(registers[m],32)!=extractsignedvalue(registers[n],32):
    #     # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
    #     if(o>0):
    #         carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
    #     else:
    #         carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")
    return 1,1,"SB";

def blt(carr_for_list):
    # m=int(carr_for_list[0],2)
    # n=int(carr_for_list[1],2)
    # o=extractsignedvalue(carr_for_list[2],12)*2
    # if extractsignedvalue(registers[m],32)<extractsignedvalue(registers[n],32):
    #     # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
    #     if(o>0):
    #         carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
    #     else:
    #         carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")
    return 1,1,"SB";

def lui(carr_for_list):
    m=int(carr_for_list[2],2)
    n=int(carr_for_list[3],2)
    # print("ayeayeaye",bin(m).replace("0b",""))
    # registers[n]=bin(m).replace("0b","")+"000000000000"
    # registers[n]=com_32(registers[n])
    return com_32(bin(m).replace("0b","")+"000000000000"),n,"U";
    # print(n,(registers[n]))
    # print(registers)

def auipc(carr_for_list): #should add to register values given value + current pc
    m=int(carr_for_list[2],2) #current imm/given value
    n=int(carr_for_list[3],2)
    a = int(carr_for_list[8],2) #current pc
    x=bin(m).replace("0b","")+"000000000000"
    x=bin(int(x,2)+int(carr_for_list[8],2) - 4 ).replace("0b","")
    x = com_32(x)
    return x,n,"U";

def jal(carr_for_list):
    m=extractsignedvalue(carr_for_list[2],20)*2 #imm
    n=int(carr_for_list[3],2) #rd
    # print("jump from jal=",m,"pc before=",int(carr_for_list[8],2))
    temp = com_32(bin(int(carr_for_list[8],2)).replace("0b",""))#storing return address in register

    carr_for_list[8]=bin(int(carr_for_list[8],2)+m - 4).replace("0b","") #updating program counter
    # print("hoooooooooooooooooooooooooo   pc after=",int(carr_for_list[8],2))
    # print("after jal = register file is\n",printregisters())
    return temp,n,"J1";

def jalr(carr_for_list): #jalr x0,0(x1)
    m=extractsignedvalue(carr_for_list[2],12) #imm
    k=int(carr_for_list[0],2) #rs1
    n=m+int(registers[k],2) #relative address to load from memory
    o=int(carr_for_list[3],2)
    temp=com_32(bin(int(registers[8],2)+4).replace("0b",""))
    # carr_for_list[8]=bin(n).replace("0b","").zfill(32)
    carr_for_list[8] = converttosignedvalue(n,32)
    # print(carr_for_list[8])
    return temp,o,"J2";

def mem_access(carr_for_list,v1,v2,v3):
    ins_type = v3 # index where ins_type is stored
    if(ins_type == "R"):#do nothing
        return v1,v2,"R";
    elif(ins_type == "U"):#do nothing
        return v1,v2,"U";
    elif(ins_type == "I"):#do nothing
        return v1,v2,"I";
    elif(ins_type == "S"):
        fun_name = carr_for_list[9]
        if(fun_name=="sb"):
            n = v1 # index where final address is stored
            itit = v2 # index where itit is stored
            if(n<500000000):
                mem.add_data_at(n,itit[24:32])
            else:
                stack[hex(n)]=hex(int(itit[24:32],2))[2::].zfill(2)
            return 1,1,"S";
        elif(fun_name=="sw"):
            n = v1 # index where final address is stored
            itit = v2 # index where itit is stored
            # print(n+3,n+2,n+1,n,m)
            #itit = registers[y]
            add3,add2,add1,add0=hex(n+3),hex(n+2),hex(n+1),hex(n)
            val3,val2,val1,val0=hex(int(itit[0:8],2))[2::].zfill(2), hex(int(itit[8:16],2))[2::].zfill(2),hex(int(itit[16:24],2))[2::].zfill(2),hex(int(itit[24:],2))[2::].zfill(2)
            # print(add3,add2,add1,add0)
            if(n+3<500000000): #store in data segment and append the list
                mem.add_data_at(n+3,itit[0:8])
                mem.add_data_at(n+2,itit[8:16])
                mem.add_data_at(n+1,itit[16:24])
                mem.add_data_at(n,itit[24:32])
            if(int( add3 ,16)>0x7ffffff3):
                print("can't write in memory after 0x7ffffff3")
            else: #store in stack
                stack[add3]=val3
                stack[add2]=val2
                stack[add1]=val1
                stack[add0]=val0
                # print(stack)
            return 1,1,"S";
        elif(fun_name=="sh"):
            n = v1 # index where final address is stored
            itit = v2 # index where itit is stored
            add1,add0=hex(n+1),hex(n)
            val1,val0=hex(int(itit[16:24],2))[2::].zfill(2),hex(int(itit[24:],2))[2::].zfill(2)
            if(n+1<500000000):
                mem.add_data_at(n+1,itit[16:24])
                mem.add_data_at(n,itit[24:32])

            else:
                stack[add1]=val1
                stack[add0]=val0
            return 1,1,"S";

    elif(ins_type == "SB"):
        return 1,1,"SB";

    elif(ins_type == "LOADBYTE"):
        n = v1#index of address
        r_i = v2#index of register index
        if(n<500000000):
            # print("address",hex(n))
            x=mem.get_data_at(n)  #to be reviewed
        else:
            try:
                x=stack[hex(n)]
            except:
                x='00'
        a = converttosignedvalue(extractsignedvalue(bin(int('0x'+x,16))[2:],8),32)
        return a,r_i,"LOADBYTE";
    elif(ins_type == "LOADWORD"):
        n = v1#index of address
        r_i = v2#index of register index
        if(n+3<500000000):
            x1=mem.get_data_at(n)
            x2=mem.get_data_at(n+1)
            x3=mem.get_data_at(n+2)
            x4=mem.get_data_at(n+3)
            x=x4+x3+x2+x1
            # print("loaded value =",x)
        else:#they are in stack
            # print(hex(n),"address in the stack")
            try:#x4 from n+3 address
                x4=stack[hex(n+3)]
            except:
                x4='00'
            try:
                x3=stack[hex(n+2)]
            except:
                x3='00'
            try:
                x2=stack[hex(n+1)]
            except:
                x2='00'
            try:
                x1=stack[hex(n)]
            except:
                x1='00'
            x = x4+x3+x2+x1
        a = converttosignedvalue(extractsignedvalue(bin(int('0x'+x,16))[2:],32),32)
        # print("return value from memaccess of LOADWORD,",a,r_i,"LOADWORD")
        return a,r_i,"LOADWORD";
    elif(ins_type == "LOADHALF"):
        n = v1#index of address
        r_i = v2#index of register index
        if(n+1<500000000):
            x1=mem.get_data_at(n)
            x2=mem.get_data_at(n+1)
            x=x2+x1
        else:#they are in stack
            try:
                x2=stack[hex(n+1)]
            except:
                x2='00'
            try:
                x1=stack[hex(n)]
            except:
                x1='00'
            x = x2+x1
        a = converttosignedvalue(extractsignedvalue(bin(int('0x'+x,16))[2:],16),32)
        return a,r_i,"LOADHALF";
    elif(ins_type == "J1"):
        # o = v1
        # #c_pc = int(carr_for_list[8])+4
        # carr_for_list[8] = bin(int(carr_for_list[8],2)+o - 4).replace("0b","")
        # return com_32(bin(int(carr_for_list[8],2)).replace("0b","")),v2,"J1";
        return v1,v2,"J1";
    elif(ins_type == "J2"):
        # o = v1
        # #c_pc = int(carr_for_list[8])+4
        # carr_for_list[8] = bin(o).replace("0b","")
        # return com_32(bin(int(registers[8],2)+4).replace("0b","")),v2,"J2";
        return v1,v2,"J2";

def write(carr_for_list,registers,v1,v2,v3):
    ins_type = v3 # index where ins_type is stored
    index = v2 #index where index of destination register is stored
    result = v1 #index where result is stored
    # print(v3,v2,v1)
    if(ins_type == "R"):
        if index!=0:
            registers[index] = result
        # print("after write value of reg[",index,'] = ',registers[index])
    elif(ins_type == "I"):
        if index!=0:
            registers[index] = result
    elif(ins_type == "U"):
        if index!=0:
            registers[index] = result
    elif(ins_type == "S"):#do nothing
        nothingness = "sad"
    elif(ins_type == "SB"):#do nothing
        nothingness = "sad"
    elif(ins_type == "J1"):
        # nothingness = "sad"
        if index!=0:
            registers[index] = result
    elif(ins_type == "J2"):
        # nothingness = "sad"
        if index!=0:
            registers[index] = result
    elif(ins_type == "LOADBYTE"):
        if index!=0:
            registers[index] = result
    elif(ins_type == "LOADWORD"):
        if index!=0:
            registers[index] = result
    elif(ins_type == "LOADHALF"):
        if index!=0:
            registers[index] = result




def run(carr_for_list):
    start=time.time()
    elapsed=0
    count=0
    while elapsed < 4:
        #print(list[7])
        string=fetch(carr_for_list)
        #print(string)
        if string=="continue":
            count=count+1  #for GUI

            decode(carr_for_list)
            #print(">>> \t ENTER--->",carr_for_list[9],"initial pc=",hex(int(carr_for_list[8],2)))
            v1,v2,v3 = execute(carr_for_list,registers)
            v1,v2,v3 = mem_access(carr_for_list,v1,v2,v3)
            write(carr_for_list,registers,v1,v2,v3)
            # registers[0] = '00000000000000000000000000000000'
            # printregisters()
            elapsed=time.time()-start
        else:
            print("Code successfully Executed")
            break
    if(elapsed>4):
        print("Something is wrong, program took too long too execute, might be an infinite loop")
    print("run")
    print("Number of cycles taken",count*5)
    return count
    # print(registers)

def step(carr_for_list):
    # print(carr_for_list)

    string=fetch(carr_for_list)
    if string=="continue":
        decode(carr_for_list)
        print(">>> \t ENTER--->",carr_for_list[9],"initial pc=",hex(int(carr_for_list[8],2)))
        execute(carr_for_list,registers)
        registers[0] = '00000000000000000000000000000000'
        #execute one step of code
    else:
        print("code successfully Executed")
    #print(carr_for_list)
    x=int(carr_for_list[8],2)
    print("step")
    return x-4

master_list=[['NIL','NIL','NIL','NIL','NIL','NIL','NIL',-2,'NIL','NIL'] for i in range(5)]       #list of lists(carr_for_list)
master_list[0][8]='00000000000000000000000000000000'

def insert_carr():
    master_list.insert(0,['NIL','NIL','NIL','NIL','NIL','NIL','NIL',-2,'NIL','NIL'])
    master_list[0][8] = master_list[1][8]


# should be called decode of instruction to be check is completed.
def detect_data_hazard():
    # assuming new inserted master_list[0] is ['NIL','NIL','NIL','NIL','NIL','NIL','NIL','NIL',PC,'NIL'] (size 9)
    #										    rs1  rs2  imm    rd    f3    f7  opcode  IR   PC  current_func
    this_opcode = master_list[1][6]
    prev1_opcode = master_list[2][6]
    prev2_opcode = master_list[3][6]
    rss1, rss2 = master_list[1][0], master_list[1][1]
    prev1_rd, prev2_rd = master_list[2][3], master_list[3][3]
    returnlist=[]
    if(this_opcode=='NIL'):
        return [-1]
    if (prev1_opcode != 'NIL'):
        if(this_opcode == '0010111' or this_opcode == '0110111' or this_opcode == '1101111'):# i.e. new instruction is auipc or lui or jal, no problem
            return [-1]

        if(prev1_opcode == '0000011' and (prev1_rd == rss1 or prev1_rd == rss2)):  # lw x2,0(x3)
            if(this_opcode == '0100011'):  # store format 
                if(prev1_rd == rss1): #eg. sw x5,0(x2)
                    returnlist.append(['M', 'E', 1, [2, 1]])
                    # return 'M', 'E', 1, [2, 1]
                if(prev1_rd == rss2): #eg. sw x2,0(x5)
                    returnlist.append(['M', 'M', 2, [2, 1]])
                    # return 'M', 'M', 2, [2, 1]
            else:  # this will require 1 cycle stall
                if(prev1_rd == rss1 and prev1_rd == rss2):  # eg. add x4,x2,x2
                    returnlist.append(['M', 'E', 12, [2, 1]])
                    # return 'M', 'E', 12, [2, 1]
                elif(prev1_rd == rss1):  # eg. addi x3,x2,4
                    returnlist.append(['M', 'E', 1, [2, 1]])
                    # return 'M', 'E', 1, [2, 1]
                elif(prev1_rd == rss2):  # eg. beq x2,x0,loop
                    returnlist.append(['M', 'E', 2, [2, 1]])
                    # return 'M', 'E', 2, [2, 1]
        # R,I,U, [UJ] format
        elif(prev1_opcode == '0110011' or (prev1_opcode == '0010011' or prev1_opcode == '1100111') or (prev1_opcode == '0010111' or prev1_opcode == '0110111') or prev1_opcode == '1101111'):
            # NOTE WHAT TO DO IF PREV1 is of UJ format i.e. jal rd,func
            # here, I consider only forward from E stage whereas it would be possible from D to some stage for jal instruction
            # this instruction is of R,I or SB or [S] format
            if(this_opcode == '0110011' or (this_opcode == '0010011' or this_opcode == '1100111') or this_opcode == '1100011' or this_opcode == '0100011'):
                if(prev1_rd == rss1 and prev1_rd == rss2):
                    returnlist.append(['E', 'E', 12, [2, 1]])
                    # return 'E', 'E', 12, [2, 1]
                elif(prev1_rd == rss1):
                    returnlist.append(['E', 'E', 1, [2, 1]])
                    # print("BOLA rss1",returnlist)
                    # return 'E', 'E', 1, [2, 1]
                elif(prev1_rd == rss2):
                    returnlist.append(['E', 'E', 2, [2, 1]])
                    # return 'E', 'E', 2, [2, 1]
            if(this_opcode == '0000011'): #this instruction is load whereas previous is determining value after execution stage
                if(prev1_rd==rss1):
                    returnlist.append(['E', 'M', 1, [2, 1]])
                    # return 'E','M',1,[2,1]
        # else:
        #     return -1, -1, -1, [-1, -1]
    if(prev2_opcode!='NIL'):
    # check hazard for prev2 and current instruction
        if((prev2_rd == rss1 or prev2_rd == rss2)):
            # any format for prev2 instruction would result in ez forwarding,
            # prev2 has completed M,
            # prev1 has completed E,
            # current has completed D, therefore, Ry will have the desired value in case of depencey eg. lw x5,0(x2), add x3,x0,x1, sub x4,x5,x6
            # this instruction is of R,I or SB or [S] format
            if(this_opcode == '0110011' or (this_opcode == '0010011' or this_opcode == '1100111') or this_opcode == '1100011' or this_opcode == '0100011'):
                if(prev2_rd == rss1 and prev2_rd == rss2):
                    returnlist.append(['M', 'E', 12, [3, 1]])
                    # return 'M', 'E', 12, [3, 1]
                    return returnlist
                elif (prev2_rd == rss1):
                    returnlist.append(['M', 'E', 1, [3, 1]])
                    # print('HOLA rss1',returnlist)
                    return returnlist
                    # return 'M', 'E', 1, [3, 1]
                elif (prev2_rd == rss2):
                    returnlist.append(['M', 'E', 2, [3, 1]])
                    # print('HOLA rss2',returnlist)
                    return returnlist
                    # return 'M', 'E', 2, [3, 1]
        else:
            if(len(returnlist)!=0):
                return returnlist
            else:
                return [-1]

    else:
        if(len(returnlist)!=0):
            return returnlist
        else:
            return [-1]


# def run_pipelined():
#     flag=0
#     start = time.time()
#     elapsed=0
#     count=0
#     v=[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#     while elapsed < 4:
#         count=count+1
#         print(master_list[0])
#         string=fetch(master_list[0])
#         if string=="over" and master_list[4][7]==-1:    #full code completed
#             print("Code successfully executed")
#             break
#         else:
#             v[4]=v[1]
#             v[5]=v[2]
#             v[6]=v[3]
#             v[10]=v[7]                                    # exchanging values for parameters passing
#             v[11]=v[8]
#             v[12]=v[9]
#             #st=fetch(master_list[0])
#             if master_list[1][7]!=-1 and master_list[1][7]!=-2:
#                 decode(master_list[1])
#                 #print(">>> \t ENTER--->",carr_for_list[9],"initial pc=",hex(int(carr_for_list[8],2)))
#             if master_list[2][7]!=-1 and master_list[2][7]!=-2:
#                 v[1],v[2],v[3] = execute(master_list[2],registers)                       #v[1],v[2],v[3]  output of execute and  parameters for mem_access for the next iterarion  
#             if master_list[3][7]!=-1 and master_list[3][7]!=-2:
#                 v[7],v[8],v[9] = mem_access(master_list[3],v[4],v[5],v[6])               #v[7],v[8],v[9] output of mem_access and parameters for write for the next iteration
#             if master_list[4][7]!=-1 and master_list[4][7]!=-2:
#                 write(master_list[4],registers,v[10],v[11],v[12])
#             # registers[0] = '00000000000000000000000000000000'
#             #printregisters()
#             insert_carr()
#             # master_list.insert(0,['00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',-2,'00000000000000000000000000000000','00000000000000000000000000000000'])
#             # master_list[0][8]=master_list[1][8]
            
#             #if flag==1:               #flag=1 in case of stalling
#             #    stalling()
#             elapsed=time.time()-start
#     if(elapsed>4):
#         print("Something is wrong, program took too long too execute, might be an infinite loop")
#     print("run_pipelined")
#     print("NUmber of cycles taken",count-1)

i=0

def flush(number_of_steps, pc):
    for i in range(number_of_steps):    # emptying the unnecessary instruction
        master_list[i][7] = -1
    master_list[0][8] = pc  # filling the next carr_for_list with suitable pc

def stalling(i):                # i is index above it should continue as usual
    # master_list.pop(0)
    master_list.insert(i, ['NIL','NIL','NIL','NIL','NIL','NIL','NIL',-2,'NIL','NIL'])
    # master_list[i][7] = -2

def run_pipelined_data_for():
    flag = 0
    start = time.time()
    elapsed = 0
    count = 0
    pr_mem = ['nil','nil','nil'] #pipeline register for decode stage
    pr_exe = ['nil','nil','nil']
    nextflagMM=0
    stallflag=0
    no_of_data_hazards=0
    no_of_stalls=0
    print("master_list")
    for i in range(5):
        print(i,"-->",master_list[i])
    while elapsed < 4:
        count=count+1
        string = fetch(master_list[0])
        
        if string == "over" and master_list[4][7] == -1:  # full code completed
            print("Code successfully executed")
            break
        else:
            # st=fetch(master_list[0])
            if master_list[1][7] != -1 and master_list[1][7] != -2:
                decode(master_list[1])
                print(">>> \t ENTER--->",master_list[1][9], "initial pc=", hex(int(master_list[1][8], 2)))
            if master_list[4][7] != -1 and master_list[4][7] != -2:
                write(master_list[4], registers, pr_mem[0],pr_mem[1],pr_mem[2])
            if master_list[3][7] != -1 and master_list[3][7] != -2:
                pr_mem = mem_access(master_list[3], pr_exe[0],pr_exe[1],pr_exe[2])
                # print("pr_mem =",pr_mem)
            if master_list[2][7] != -1 and master_list[2][7] != -2:
                pr_exe = execute(master_list[2], registers)
                # print("pr_exe =",pr_exe)
            
            #now that decode of master_list[1] is complete we check for data hazard
            
            if(nextflagMM==1):
                # print("inside nextFLAGMM\tpr_mem=",pr_mem)
                registers[pr_mem[1]] = pr_mem[0]
                nextflagMM=0
                if(stallflag==1):
                    no_of_data_hazards-=1
                stallflag=0
            
            print("master_list")
            for i in range(5):
                print(i,"-->",master_list[i])
            
            returnlist = detect_data_hazard()
            # print(master_list[1])
            # print("returnlist----------------",returnlist)
            if(returnlist[0]!=-1):
                # print("DATA HAZARD DETECTED, forwarding case ,",fr,to,target,layer)
                print("DATA HAZARD DETECTED, forwarding case XXXXXX,",returnlist)
                no_of_data_hazards+=1
                if (returnlist[0][0]=='E'and returnlist[0][1]=='E'):  # case- E to E
                    # print("data forwarding done for",master_list[1][9],"\nreg[x",pr_exe[1],"] = ",pr_exe[0])
                    registers[pr_exe[1]] = pr_exe[0] #writing the value into the register early
                elif (returnlist[0][0]=='M' and returnlist[0][1]=='E'):
                    if(returnlist[0][3]==[3,1]):
                        nextflagMM=1
                        # register[pr_mem[1]] = pr_mem[0]
                    elif(returnlist[0][3]==[2,1]):
                        stalling(2)
                        stallflag=1
                        nextflagMM=1
                        no_of_stalls+=1
                        continue
                elif (returnlist[0][0]=='M' and returnlist[0][1]=='M'):
                    #write the value in the next cycle because then 
                    # (curr)master_list[1] would be ready for M stage and (curr)master_list[2] would have completed M stage
                    nextflagMM=1
                elif(returnlist[0][0]=='E' and returnlist[0][1]=='M'):
                    registers[pr_exe[1]] = pr_exe[0]
            # printregisters()
            insert_carr()
            elapsed = time.time()-start
    if(elapsed > 4):
        print("Something is wrong, program took too long too execute, might be an infinite loop")
    print("Pipelined Execution with DF enabled")
    print("NUmber of cycles taken:",count-1)
    print("Number of Data Hazards:",no_of_data_hazards)
    print("Number of Stalls      :",no_of_stalls)


def nstalling(i):                # i is index above it should continue as usual
    master_list.pop(0)
    master_list[0][8]=master_list[1][8]
    master_list.insert(i, ['NIL','NIL','NIL','NIL','NIL','NIL','NIL',-2,'NIL','NIL'])
    # master_list[i][7] = -2

def run_pipelined_without_data_for():
    flag = 0
    start = time.time()
    elapsed = 0
    count = 0
    # v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pr_mem = ['nil','nil','nil'] #pipeline register for decode stage
    pr_exe = ['nil','nil','nil']
    nextflagMM=0
    no_of_data_hazards=0
    print("master_list")
    for i in range(5):
        print(i,"-->",master_list[i])
    while elapsed < 4:
        count=count+1
        print(master_list[0][8])
        string = fetch(master_list[0])
        
        if string == "over" and master_list[4][7] == -1:  # full code completed
            print("Code successfully executed")
            break
        else:
            # st=fetch(master_list[0])
            
            if master_list[4][7] != -1 and master_list[4][7] != -2:
                write(master_list[4], registers, pr_mem[0],pr_mem[1],pr_mem[2])
            if master_list[3][7] != -1 and master_list[3][7] != -2:
                pr_mem = mem_access(master_list[3], pr_exe[0],pr_exe[1],pr_exe[2])
                # print("pr_mem =",pr_mem)
            if master_list[2][7] != -1 and master_list[2][7] != -2:
                pr_exe = execute(master_list[2], registers)
                # print("pr_exe =",pr_exe)
            if master_list[1][7] != -1 and master_list[1][7] != -2:
                decode(master_list[1])
                print(">>> \t ENTER--->",master_list[1][9], "initial pc=", hex(int(master_list[1][8], 2)))
            #now that decode of master_list[1] is complete we check for data hazard
            
            returnlist = detect_data_hazard()
            # print(master_list[1])
            insert_carr()
            
            print("master_list")
            for i in range(5):
                print(i,"-->",master_list[i])

            if(returnlist[0]!=-1):
                print("DATA HAZARD DETECTED, forwarding case ,",returnlist)
                no_of_data_hazards+=1
            #else:
            #    insert_carr()
                if (returnlist[0][0]=='E'and returnlist[0][1]=='E'):  # case- E to E
                    # print("data forwarding done for",master_list[1][9],"\nreg[x",pr_exe[1],"] = ",pr_exe[0])
                    nstalling(2)
                    #registers[pr_exe[1]] = pr_exe[0] #writing the value into the register early
                elif (returnlist[0][0]=='M' and returnlist[0][1]=='E'):
                    if(returnlist[0][3]==[3,1]):
                        nstalling(2)
                        #nextflagMM=1
                        # register[pr_mem[1]] = pr_mem[0]
                    elif(returnlist[0][3]==[2,1]):
                        nstalling(2)
                        #nextflagMM=1
                elif (returnlist[0][0]=='M' and returnlist[0][1]=='M'):
                    print ("enter")
                    nstalling(2)
                #write the value in the next cycle because then 
                # (curr)master_list[1] would be ready for M stage and (curr)master_list[2] would have completed M stage
                #nextflagMM=2
            
            # printregisters()
            #insert_carr()
            elapsed = time.time()-start
    if(elapsed > 4):
        print("Something is wrong, program took too long too execute, might be an infinite loop")
    print("Pipelined Execution with DF disabled")
    print("Number of cycles taken:",count-1)
    print("Number of data hazards:",no_of_data_hazards)

#while(i<976):
#    step()
#    i=i+1
print("Enter your choice for mode of running the program,\nenter 1 to enable and 0 to disable the following knobs")
knob1 = int(input(">>>\tPipelined Execution(0/1) : "))
if(knob1==1):
    knob2 = int(input(">>>\tdata forwarding    (0/1) : "))
if(knob1==0):
    run(['NIL','NIL','NIL','NIL','NIL','NIL','NIL',-2,'00000000000000000000000000000000','NIL'])
elif(knob2==0):
    run_pipelined_without_data_for()
elif(knob2==1):
    run_pipelined_data_for()
# step()
print(registers)
mem.show_Memory()
# print(stack)
