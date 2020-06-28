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
carr_for_list=['00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000',
 '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000',
 '00000000000000000000000000000000'] #list of strings

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
    carr_for_list[7] = getIR(i_file,int(carr_for_list[8],2))
    if(carr_for_list[7]==-1):
        return "over"
    carr_for_list[8]=bin(int(carr_for_list[8],2)+4).replace("0b","")
    return "continue"

'''0:rs1 1:rs2 2:imm 3:rd 4:f3 5:f7 6:opcode 7:ir 8:pc 9:current_function '''
def decode(carr_for_list):
    #print(carr_for_list)
    ins=carr_for_list[7]
    opcode = ins[25:32]
    if(opcode=="0110011"):#r-format
        carr_for_list[5]=ins[0:7]
        carr_for_list[1]=ins[7:12]
        carr_for_list[0]=ins[12:17]
        carr_for_list[4]=ins[17:20]
        carr_for_list[3]=ins[20:25]

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
        carr_for_list[1]=ins[7:12]
        carr_for_list[0]=ins[12:17]
        carr_for_list[4]=ins[17:20]
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

        elif carr_for_list[4]=="001":
            carr_for_list[9]="bne"

        elif carr_for_list[4]=="101":
            carr_for_list[9]="bge"

        elif carr_for_list[4]=="100":
            carr_for_list[9]="blt"

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

    elif opcode=="0010011": #andi ori addi
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
        add()
    elif(fun_name=="and"):
        and1()
    elif(fun_name=="or"):
        or1()
    elif(fun_name=="sll"):
        sll()
    elif(fun_name=="slt"):
        slt()
    elif(fun_name=="sra"):
        sra()
    elif(fun_name=="srl"):
        srl()
    elif(fun_name=="sub"):
        sub()
    elif(fun_name=="xor"):
        xor()
    elif(fun_name=="mul"):
        mul()
    elif(fun_name=="div"):
        div()
    elif(fun_name=="rem"):
        rem()
    elif(fun_name=="addi"):
        addi()
    elif(fun_name=="andi"):
        andi()
    elif(fun_name=="ori"):
        ori()
    elif(fun_name=="lb"):
        lb()
    elif(fun_name=="ld"):
        ld()
    elif(fun_name=="lh"):
        lh()
    elif(fun_name=="lw"):
        lw()
    elif(fun_name=="jalr"):
        jalr()
    elif(fun_name=="sb"):
        sb()
    elif(fun_name=="sw"):
        sw()
    elif(fun_name=="sd"):
        sd()
    elif(fun_name=="sh"):
        sh()
    elif(fun_name=="beq"):
        beq()
    elif(fun_name=="bne"):
        bne()
    elif(fun_name=="bge"):
        bge()
    elif(fun_name=="blt"):
        blt()
    elif(fun_name=="auipc"):
        auipc()
    elif(fun_name=="lui"):
        lui()
    elif(fun_name=="jal"):
        jal()

#list_fun=[add, and1, or1, sll, slt, sra, srl, sub, xor, mul, div, rem,addi, andi, ori, lb, ld, lh, lw, jalr,sb, sw, sd, sh,beq, bne, bge, blt, auipc, lui,jal]


def add():
    #print(carr_for_list)
    m=int(carr_for_list[0],2)#values in registers and carr_for_list are in binary format
    n=int(carr_for_list[1],2)
    x=extractsignedvalue(registers[m],32) + extractsignedvalue(registers[n],32)
    o=int(carr_for_list[3],2)
    # print(x,"herffffffffffffffffre")
    registers[o]=converttosignedvalue(x,32)
    # print("yo")
    #print(m)
    #print(n)
    #print(x)


def and1():
    # print("yooooooo2")
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    # print(int(registers[m],2),int(registers[n],2))
    x = extractsignedvalue(registers[m],32) & extractsignedvalue(registers[n],32)
    # print(x,"ans")
    o=int(carr_for_list[3],2)
    # print(o)
    registers[o]=converttosignedvalue(x,32)
    # print(registers[o])

def or1():
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    x = extractsignedvalue(registers[m],32) | extractsignedvalue(registers[n],32)
    o = int(carr_for_list[3],2)
    registers[o]=converttosignedvalue(x,32)

def slt():
    # print("9999999999999999999999999999999999999999999999999")
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    o=int(carr_for_list[3],2)
    if extractsignedvalue(registers[m],32) < extractsignedvalue(registers[n],32):
        # print('yessssssssssssssss')
        registers[o]=converttosignedvalue(1,32)
    else:
        registers[o]=converttosignedvalue(0,32)

def sll():
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
    registers[o]=converttosignedvalue(x,32)
    # print(registers[o],"hererere")
    
def sra():
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
    registers[o]=converttosignedvalue(x,32)
    # print(registers[o],"hererere",len(registers[o]))
    
def srl():
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
            registers[o]=com_32(v)
    else:
        x=0
        registers[o]=converttosignedvalue(v,32)
    
def sub():
    m=int(carr_for_list[0],2)
    n=int(carr_for_list[1],2)
    x=extractsignedvalue(registers[m],32) - extractsignedvalue(registers[n],32)
    o=int(carr_for_list[3],2)
    registers[o]=converttosignedvalue(x,32)
    # print("yo1")

def xor():
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    x = extractsignedvalue(registers[m],32) ^ extractsignedvalue(registers[n],32)
    # print("iiiiiiiiiiiiiiiii",converttosignedvalue(extractsignedvalue(registers[m],32)^extractsignedvalue(registers[n],32),32))
    o=int(carr_for_list[3],2)
    registers[o]=converttosignedvalue(x,32)

def mul():
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    x = extractsignedvalue(registers[m],32) * extractsignedvalue(registers[n],32)
    o=int(carr_for_list[3],2)
    registers[o]=converttosignedvalue(x,32)

def div():
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    if(extractsignedvalue(registers[n],32)==0):
        print("division by zero not allowed")
        return "error : division by zero not allowed"
    x = int(extractsignedvalue(registers[m],32) / extractsignedvalue(registers[n],32))
    o=int(carr_for_list[3],2)
    registers[o]=converttosignedvalue(x,32)

def rem():
    m = int(carr_for_list[0],2)
    n = int(carr_for_list[1],2)
    x = extractsignedvalue(registers[m],32) % extractsignedvalue(registers[n],32)
    o=int(carr_for_list[3],2)
    registers[o]=converttosignedvalue(x,32)

def addi():
    m = int(carr_for_list[0],2)
    n = str(carr_for_list[2])
    # print("immediate value =",n,extractsignedvalue(n,12))
    # print(registers[m],extractsignedvalue(registers[m],32))
    x = extractsignedvalue(registers[m],32) + extractsignedvalue(n,12)
    # print((x))
    # print(converttosignedvalue(x,32))
    o = int(carr_for_list[3],2)
    registers[o]=converttosignedvalue(x,32)

def andi():
    # print(carr_for_list)
    m = int(carr_for_list[0],2)
    n = str(carr_for_list[2])
    # print("debug",m,n)
    x = extractsignedvalue(registers[m],32) & extractsignedvalue(n,12)
    o = int(carr_for_list[3],2)
    registers[o]=converttosignedvalue(x,32)

def ori():
    m = int(carr_for_list[0],2)
    n = str(carr_for_list[2])
    x = extractsignedvalue(registers[m],32) | extractsignedvalue(n,12)
    o = int(carr_for_list[3],2)
    registers[o]=converttosignedvalue(x,32)

def lb():
    m=extractsignedvalue(carr_for_list[2],12) #immediate value
    k=int(carr_for_list[0],2) #rs1
    n=m+extractsignedvalue(registers[k],32) #calculate r[rs1] + imm
    # print(hex(n),m,k)
    if(n<500000000):
        # print("address",hex(n))
        x=mem.get_data_at(n)  #to be reviewed
    else:
        try:
            x=stack[hex(n)]
        except:
            x='00'
    # print(x, converttosignedvalue( extractsignedvalue(bin(int('0x'+x,16))[2:],8),32 ) , 'oyoyoyoyoy')
    y=int(carr_for_list[3],2)
    registers[y]=converttosignedvalue(extractsignedvalue(bin(int('0x'+x,16))[2:],8),32)

def lw():
    # print("m=====",carr_for_list[2])
    m=extractsignedvalue(carr_for_list[2],12)
    # print(m)
    k=int(carr_for_list[0],2)
    # print("address in register ",hex(int(registers[k],2)))
    n=m+int(registers[k],2)
    # print("n=====",(n-268435456))
    # print(hex(n),n)
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
        # print("loaded value =",x)
    # print("mama mia",int('0x'+x,16),x)
    y=int(carr_for_list[3],2)
    registers[y]=converttosignedvalue(extractsignedvalue(bin(int('0x'+x,16))[2:],32),32)

def ld():
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    if(n+3<500000000):
        x1=mem.get_data_at(n)
        x2=mem.get_data_at(n+1)
        x3=mem.get_data_at(n+2)
        x4=mem.get_data_at(n+3)
        x=x4+x3+x2+x1
    else:#they are in stack
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
    y=int(carr_for_list[3],2)
    registers[y]=converttosignedvalue(extractsignedvalue(bin(int('0x'+x,32))[2:],16),32)

def lh():
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
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
    y=int(carr_for_list[3],2)
    registers[y]=converttosignedvalue(extractsignedvalue(bin(int('0x'+x,16))[2:],16),32)

def sb():
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    #n = should be a address
    # n=500000010
    if(n<500000000):
        # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        mem.add_data_at(n,registers[y][24:32])
        # mem.add_data_at(n,)
    else:
        # print("sssssssssssssssssssssssssssssssssssssssssssssssss")
        stack[hex(n)]=hex(int(registers[y][24:32],2))[2::].zfill(2)

def sw():
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    # print(k,m,registers[k])
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    # print(n+3,n+2,n+1,n,m)
    itit = registers[y]
    add3,add2,add1,add0=hex(n+3),hex(n+2),hex(n+1),hex(n)
    val3,val2,val1,val0=hex(int(itit[0:8],2))[2::].zfill(2), hex(int(itit[8:16],2))[2::].zfill(2),hex(int(itit[16:24],2))[2::].zfill(2),hex(int(itit[24:],2))[2::].zfill(2)
    # print(add3,add2,add1,add0)
    if(n+3<500000000): #store in data segment and append the list
        mem.add_data_at(n+3,registers[y][0:8])
        mem.add_data_at(n+2,registers[y][8:16])
        mem.add_data_at(n+1,registers[y][16:24])
        mem.add_data_at(n,registers[y][24:32])
    if(int( add3 ,16)>0x7ffffff3):
        print("can's write in memory after 0x7ffffff3")
    else: #store in stack
        stack[add3]=val3
        stack[add2]=val2
        stack[add1]=val1
        stack[add0]=val0
        # print(stack)
    
def sh():
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    add1,add0=hex(n+1),hex(n)
    val1,val0=hex(int(registers[y][16:24],2))[2::].zfill(2),hex(int(registers[y][24:],2))[2::].zfill(2)
    if(n+1<500000000):
        mem.add_data_at(n+1,registers[y][16:24])
        mem.add_data_at(n,registers[y][24:32])
    
    else:
        stack[add1]=val1
        stack[add0]=val0

def sd(): #venus didn't overwrite upper 4 bytes to '00', thus this also works similarly
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    # mem.add_data_at(n+7,'00000000')
    # mem.add_data_at(n+6,'00000000')
    # mem.add_data_at(n+5,'00000000')
    # mem.add_data_at(n+4,'00000000')
    itit = registers[y]
    add3,add2,add1,add0=hex(n+3),hex(n+2),hex(n+1),hex(n)
    val3,val2,val1,val0=hex(int(itit[0:8],2))[2::].zfill(2),hex(int(itit[8:16],2))[2::].zfill(2),hex(int(itit[16:24],2))[2::].zfill(2),hex(int(itit[24:],2))[2::].zfill(2)
    if(n+3<500000000):
        mem.add_data_at(n+3,registers[y][0:8])
        mem.add_data_at(n+2,registers[y][8:16])
        mem.add_data_at(n+1,registers[y][16:24])
        mem.add_data_at(n,registers[y][24:32])
    else:
        stack[add3]=val3
        stack[add2]=val2
        stack[add1]=val1
        stack[add0]=val0


def beq():
    m=int(carr_for_list[0],2)
    n=int(carr_for_list[1],2)
    o=extractsignedvalue(carr_for_list[2],12)*2
    # print(carr_for_list[8],"inside beq function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
    if (extractsignedvalue(registers[m],32)==extractsignedvalue(registers[n],32)):
        # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
        if(o>0):
            carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
        else:
            carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")
        # print('pc changed to',carr_for_list[8])

def bge():
    m=int(carr_for_list[0],2)
    n=int(carr_for_list[1],2)
    o=extractsignedvalue(carr_for_list[2],12)*2
    if extractsignedvalue(registers[m],32)>=extractsignedvalue(registers[n],32):
        # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
        if(o>0):
            carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
        else:
            carr_for_list[8]=bin(int(carr_for_list[8],2)+ o- 4).replace("0b","")

def bne():
    m=int(carr_for_list[0],2)
    n=int(carr_for_list[1],2)
    o=extractsignedvalue(carr_for_list[2],12)*2
    # print(carr_for_list[8],"inside BNE function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
    if extractsignedvalue(registers[m],32)!=extractsignedvalue(registers[n],32):
        # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
        if(o>0):
            carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
        else:
            carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")

def blt():
    m=int(carr_for_list[0],2)
    n=int(carr_for_list[1],2)
    o=extractsignedvalue(carr_for_list[2],12)*2
    if extractsignedvalue(registers[m],32)<extractsignedvalue(registers[n],32):
        # print("jump by",o,"in from current pc",int(carr_for_list[8],2))
        if(o>0):
            carr_for_list[8]=bin(int(carr_for_list[8],2)+ o -4).replace("0b","")
        else:
            carr_for_list[8]=bin(int(carr_for_list[8],2)+ o - 4).replace("0b","")

def lui():
    m=int(carr_for_list[2],2)
    n=int(carr_for_list[3],2)
    # print("ayeayeaye",bin(m).replace("0b",""))
    registers[n]=bin(m).replace("0b","")+"000000000000"
    registers[n]=com_32(registers[n])
    # print(n,(registers[n]))
    # print(registers)

def auipc(): #should add to register values given value + current pc
    m=int(carr_for_list[2],2) #current imm/given value
    n=int(carr_for_list[3],2)
    a = int(carr_for_list[8],2) #current pc
    registers[n]=bin(m).replace("0b","")+"000000000000"
    registers[n]=bin(int(registers[n],2)+int(carr_for_list[8],2) - 4 ).replace("0b","")
    registers[n] = com_32(registers[n])
    
def jal():
    m=extractsignedvalue(carr_for_list[2],20)*2 #imm
    n=int(carr_for_list[3],2) #rd
    # print("jump from jal=",m,"pc before=",int(carr_for_list[8],2))
    registers[n]=com_32(bin(int(carr_for_list[8],2)).replace("0b",""))#storing return address in register
    
    carr_for_list[8]=bin(int(carr_for_list[8],2)+m - 4).replace("0b","") #updating program counter
    # print("hoooooooooooooooooooooooooo   pc after=",int(carr_for_list[8],2))
    # print("after jal = register file is\n",printregisters())

def jalr(): #jalr x0,0(x1)
    m=extractsignedvalue(carr_for_list[2],12) #imm
    k=int(carr_for_list[0],2) #rs1
    n=m+int(registers[k],2) #relative address to load from memory
    o=int(carr_for_list[3],2)
    registers[o]=com_32(bin(int(registers[8],2)+4).replace("0b",""))
    # carr_for_list[8]=bin(n).replace("0b","").zfill(32)
    carr_for_list[8] = converttosignedvalue(n,32)
    # print(carr_for_list[8])

def run():
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
            print(">>> \t ENTER--->",carr_for_list[9],"initial pc=",hex(int(carr_for_list[8],2)))
            execute(carr_for_list,registers)
            registers[0] = '00000000000000000000000000000000'
            # printregisters()
            elapsed=time.time()-start
        else:
            print("Code successfully Executed")
            break
    if(elapsed>2):
        print("Something is wrong, program took too long too execute, might be an infinite loop")
    print("run")
    return count
    # print(registers)
    
def step():
    # print(carr_for_list)
    
    string=fetch(carr_for_list)
    if string=="continue":
        decode(carr_for_list)
        execute(carr_for_list,registers)
        #execute one step of code
    else:
        print("code successfully Executed")
    #print(carr_for_list)
    x=int(carr_for_list[8],2)
    print("step")
    return x-4

def reset():
    global carr_for_list
    carr_for_list=['00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000',
 '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000',
 '00000000000000000000000000000000'] 
    global registers
    registers=['00000000000000000000000000000000','00000000000000000000000000000000','01111111111111111111111111110000','00010000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000','00000000000000000000000000000000',
'00000000000000000000000000000000','00000000000000000000000000000000']

    #print(carr_for_list)
    print("reset")
def stop():
    print("execution stopped")

def previous():
    print("previous")
#while true:         # iska ek baar dekh lena dhaami
#    fetch(carr_for_list)
#    decode(carr_for_list)
#    execute(carr_for_list,registers)
run()
print(registers)
mem.show_Memory()
print(stack)
#x=step()
#reset()
#x=step()
#reset()
#x=step()
#x=step()
#x=step()
#print(int('000001000000',2))
#print(bin(4).replace("0b",""))