from testfinal import Memory
import math
import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,  QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
import sys
from PyQt5.QtCore import Qt
mem = Memory()
mem.show_Memory()

myfile = open('output.txt','w')
myfile.write('============================================== KNOB SETTINGS ===============================================================\n')

def printregisters(f,cycle):
    if f==1:
        print("\n","------ The Registers after ",cycle," cycle(s) are ------","\n")
        for i in [0,1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]:
            print("\t\tx{}\t".format(i),'0x'+(hex(int(registers[i],2)).replace('0x','').zfill(8)))
        print("\n")

def printregistersRUN():
    print('\n-------The registers after 5 cycles or next Instruction are-------')
    for i in [0,1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]:
        print("\t\tx{}\t".format(i),'0x'+(hex(int(registers[i],2)).replace('0x','').zfill(8)))
    print("\n")

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

def get_inst(inst):
    rfile=open("outfile.mc","r+")
    bc=rfile.readlines()
    inst="0x"+(hex(int(inst,2)).replace("0x","")).zfill(8)
    # print(inst)
    #exit()
    for i in bc:
        i=i.split(' ',2)
        if i[1]==inst:
            return i[2].replace('\n','')

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
btb = {} # (KEY)PC -> (VALUE)TARGET-ADDRESS
b_hist = {} # (KEY)PC -> (VALUE)prediction-bit

def fetch(carr_for_list,stallflag):
    # print("inside FETCH",carr_for_list,' stallflag=',stallflag)
    if(stallflag==0):
        carr_for_list[7] = getIR(i_file,int(carr_for_list[8],2))
        if carr_for_list[8] in btb.keys():
            if b_hist[carr_for_list[8]]==1:
                # predict = btb[carr_for_list[8]];
                predict = btb[carr_for_list[8]]
            else:
                predict = bin(int(carr_for_list[8],2)+4).replace("0b","")
            carr_for_list[8] = bin(int(carr_for_list[8],2)+4).replace("0b","")
            if(carr_for_list[7]==-1):
                return "over",predict
            return "continue",predict

    # if(stallflag==0):
        carr_for_list[8]=bin(int(carr_for_list[8],2)+4).replace("0b","")
    else:
        return 'continue',carr_for_list[8]
    if(carr_for_list[7]==-1):
        return "over",-1;
    return "continue",-1;

def update_bht(pc,taken,target):
    # print("updating BHT",pc,taken)
    b_hist[pc]=taken
    # print(b_hist,btb)

'''0:rs1 1:rs2 2:imm 3:rd 4:f3 5:f7 6:opcode 7:ir 8:pc 9:current_function '''
def decode(carr_for_list,bhtflag):
    #print(carr_for_list)
    ins=carr_for_list[7]
    opcode = ins[25:32]
    carr_for_list[6]=opcode
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
        return 1,carr_for_list[8],"R";

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

        return 1,carr_for_list[8],"S";


            #'''0:rs1 1:rs2 2:imm 3:rd 4:f3 5:f7 6:opcode 7:ir 8:pc 9:current_function '''

    elif(opcode=="1100011"):#sb
        carr_for_list[1]=ins[7:12]
        carr_for_list[0]=ins[12:17]
        carr_for_list[4]=ins[17:20]
        carr_for_list[2]=(ins[0]+ins[24]+ins[1:7]+ins[20:24]) #this still needs to be multiplied by 2 for execution
        # carr_for_list[2]=carr_for_list[2][1::]+'0'
        offset=extractsignedvalue(carr_for_list[2],12)*2
        target = bin(int(carr_for_list[8],2)+ offset - 4).replace("0b","")
        # print('inside decode-- instruction is BRANCH')
        if(knob1==1):
            if bin(int(carr_for_list[8],2) - 4).replace("0b","") not in btb.keys():
                btb[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=target
                b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=0

        if carr_for_list[4]=="000":
            carr_for_list[9]="beq"
            m=int(carr_for_list[0],2)
            n=int(carr_for_list[1],2)
            o=extractsignedvalue(carr_for_list[2],12)*2
            # print(carr_for_list[8],"inside beq function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
            if(knob1==1):
                if extractsignedvalue(registers[m],32)==extractsignedvalue(registers[n],32):
                    if bin(int(carr_for_list[8],2) - 4).replace("0b","") in b_hist.keys():
                        if b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]==1:
                            return 1, target,["SB",1] # 1 implies the prediction is correct . the branch is taken
                        else:
                            # b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")] = 1
                            return 0,target ,["SB",1]#prediction is wrong,  target address is returned
                else:
                    if bin(int(carr_for_list[8],2) - 4).replace("0b","") in b_hist.keys():
                        if b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]==0:
                            return 1,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0] # 1 implies the prediction is correct . the branch is  not taken
                        else:
                            # b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")] = 0
                            return 0,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0]#prediction is wrong. target address is returned
            elif(knob1==0):
                if extractsignedvalue(registers[m],32)==extractsignedvalue(registers[n],32):
                    return 1,target ,["SB",1]#prediction is wrong,  target address is returned
                else:
                    return 1,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0] 

        elif carr_for_list[4]=="001":
            carr_for_list[9]="bne"
            m=int(carr_for_list[0],2)
            n=int(carr_for_list[1],2)
            o=extractsignedvalue(carr_for_list[2],12)*2
            # print(carr_for_list[8],"inside beq function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
            if(knob1==1):
                if extractsignedvalue(registers[m],32)!=extractsignedvalue(registers[n],32):
                    if bin(int(carr_for_list[8],2) - 4).replace("0b","") in b_hist.keys():
                        if b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]==1:
                            return 1, target,["SB",1] # 1 implies the prediction is correct . the branch is taken
                        else:
                            # b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")] = 1
                            return 0,target ,["SB",1]#prediction is wrong,  target address is returned
                else:
                    if bin(int(carr_for_list[8],2) - 4).replace("0b","") in b_hist.keys():
                        if b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]==0:
                            return 1,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0] # 1 implies the prediction is correct . the branch is  not taken
                        else:
                            # b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")] = 0
                            return 0,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0]#prediction is wrong. target address is returned
                        # b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=0
            elif(knob1==0):
                if extractsignedvalue(registers[m],32)!=extractsignedvalue(registers[n],32):
                    return 1, target,["SB",1] # 1 implies the prediction is correct . the branch is taken
                else:
                    return 1,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0] # 1 implies the prediction is correct . the branch is  not taken
                                
        elif carr_for_list[4]=="101":
            carr_for_list[9]="bge"
            m=int(carr_for_list[0],2)
            n=int(carr_for_list[1],2)
            o=extractsignedvalue(carr_for_list[2],12)*2
            # print('value of registers comparing',registers[m],registers[n])
            # print("DECODE bge function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
            if(knob1==1):
                if extractsignedvalue(registers[m],32)>=extractsignedvalue(registers[n],32):
                    if bin(int(carr_for_list[8],2) - 4).replace("0b","") in b_hist.keys():
                        if b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]==1:
                            return 1, target,["SB",1] # 1 implies the prediction is correct . the branch is taken
                        else:
                            # b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")] = 1
                            return 0,target ,["SB",1]#prediction is wrong,  target address is returned
                else:
                    if bin(int(carr_for_list[8],2) - 4).replace("0b","") in b_hist.keys():
                        if b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]==0:
                            return 1,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0] # 1 implies the prediction is correct . the branch is  not taken
                        else:
                            # b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")] = 0
                            return 0,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0]#prediction is wrong. target address is returned
                        # b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=0
            elif(knob1==0):
                if extractsignedvalue(registers[m],32)>=extractsignedvalue(registers[n],32):
                    return 1, target,["SB",1] # 1 implies the prediction is correct . the branch is taken
                else:
                    return 1,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0] # 1 implies the prediction is correct . the branch is  not taken
                
        elif carr_for_list[4]=="100":
            carr_for_list[9]="blt"
            m=int(carr_for_list[0],2)
            n=int(carr_for_list[1],2)
            o=extractsignedvalue(carr_for_list[2],12)*2
            # print(carr_for_list[8],"inside blt function",extractsignedvalue(registers[m],32),extractsignedvalue(registers[n],32))
            # print(b_hist,"\t",btb)
            if(knob1==1):
                if extractsignedvalue(registers[m],32)<extractsignedvalue(registers[n],32):
                    # print("should be TAKEN")
                    if bin(int(carr_for_list[8],2) - 4).replace("0b","") in b_hist.keys():
                        # print("found in BTB and should be TAKEN ")
                        if b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]==1:
                            return 1,target,["SB",1] # 1 implies the prediction is correct . the branch is taken
                        else:
                            # b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")] = 1
                            return 0,target,["SB",1]
                else:
                    if bin(int(carr_for_list[8],2) - 4).replace("0b","") in b_hist.keys():
                        # print('found in BTB and Should be NOT TAKEN')
                        if b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]==0:
                            # print("BLT RETURNED",1,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",1])
                            return 1,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0] # 1 implies the prediction is correct . the branch is  not taken
                        else:
                            # print("BLT RETURNED",0,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0])
                            # b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")] = 0
                            return 0,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0]    #prediction is wrong. target address is returned
            elif(knob1==0):
                if extractsignedvalue(registers[m],32)<extractsignedvalue(registers[n],32):
                    return 1,target,["SB",1] # 1 implies the prediction is correct . the branch is taken
                else:
                    return 1,bin(int(carr_for_list[8],2)).replace("0b","") ,["SB",0]

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

        return 1,carr_for_list[8],"LOAD";

    elif opcode=="0010111": #U-auipc
        carr_for_list[2]=ins[0:20]
        carr_for_list[3]=ins[20:25]
        carr_for_list[9]="auipc"
        return 1,carr_for_list[8],"U";

    elif opcode=="0110111": #U-lui
        carr_for_list[2]=ins[0:20]
        carr_for_list[3]=ins[20:25]
        carr_for_list[9]="lui"
        return 1,carr_for_list[8],"U";

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

        return 1,carr_for_list[8],"I";

    elif opcode=="1100111": #jalr
        carr_for_list[2]=ins[0:12]
        carr_for_list[0]=ins[12:17]
        carr_for_list[3]=ins[20:25]
        carr_for_list[4]=ins[17:20]
        carr_for_list[9]="jalr"
        m=extractsignedvalue(carr_for_list[2],12) #imm
        # print('Jalr decoding...........................................')
        k=int(carr_for_list[0],2) #rs1
        n=m+int(registers[k],2) #relative address to load from memory
        o=int(carr_for_list[3],2)
        # print('rs1=',k, 'registers[rs1]=',registers[k],'offset =',m, n ,'target register =',o)
        # temp=com_32(bin(int(registers[8],2)+4).replace("0b",""))
        # carr_for_list[10]=temp
        if(knob1==1):
            if bin(int(carr_for_list[8],2) - 4).replace("0b","") not in btb.keys():
                # print('NOT In BTB')
                btb[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=bin(int(converttosignedvalue(n,32),2)).replace('0b','')
                # btb[bin(int(carr_for_list[8],2) - 4).replace("0b","")] = converttosignedvalue(n,32)
                b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=0
            else:
                btb[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=bin(int(converttosignedvalue(n,32),2)).replace('0b','')
            # btb[bin(int(carr_for_list[8],2) - 4).replace("0b","")] = converttosignedvalue(n,32)
            # print('its btb TARGET=',btb[bin(int(carr_for_list[8],2) - 4).replace("0b","")],'\n and should be =',converttosignedvalue(n,32))
            if b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]==0:
                b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=1
                return 0,converttosignedvalue(n,32),["JALR",1]
            else:
                b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=1
                return 1,converttosignedvalue(n,32),["JALR",1]
        elif(knob1==0):
            return 1,converttosignedvalue(n,32),['JALR',1]
        # btb[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=converttosignedvalue(n,32)

        # carr_for_list[8]=bin(n).replace("0b","").zfill(32)
        # carr_for_list[8] = converttosignedvalue(n,32)

    elif opcode=="1101111": #jal
        # carr_for_list[2][0]=ins[0]
        # carr_for_list[2][1:9]=ins[12:20]
        # carr_for_list[2][10]=ins[11]
        carr_for_list[2]=ins[0]+ins[12:20]+ins[11]+ins[1:11]
        carr_for_list[3]=ins[20:25]
        carr_for_list[9]="jal"
        m=extractsignedvalue(carr_for_list[2],20)*2 #imm
        n=int(carr_for_list[3],2) #rd
        # print("jump from jal=",m,"pc before=",int(carr_for_list[8],2))
        # temp = com_32(bin(int(carr_for_list[8],2)).replace("0b",""))#storing return address in register
        # carr_for_list[10]=temp
        if(knob1==1):
            if bin(int(carr_for_list[8],2) - 4).replace("0b","") not in btb.keys():
                btb[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=bin(int(carr_for_list[8],2)+m - 4).replace("0b","")
                b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=0

            if b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]==0:
                b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=1
                return 0,bin(int(carr_for_list[8],2)+m - 4).replace("0b",""),["JAL",1]
            else:
                b_hist[bin(int(carr_for_list[8],2) - 4).replace("0b","")]=1
                return 1,bin(int(carr_for_list[8],2)+m - 4).replace("0b",""),["JAL",1]
        elif(knob1==0):
            return 1,bin(int(carr_for_list[8],2)+m - 4).replace("0b",""),["JAL",1]

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
    # print(x, converttosignedvalue( extractsignedvalue(bin(int('0x'+x,16))[2:],8),32 ) , 'oyoyoyoyoy')
    y=int(carr_for_list[3],2)
    return converttosignedvalue(n,32),y,"LOADBYTE";
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
    return converttosignedvalue(n,32),y,"LOADWORD";

        # print("loaded value =",x)
    # print("mama mia",int('0x'+x,16),x)

def lh(carr_for_list):
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    y=int(carr_for_list[3],2)
    return converttosignedvalue(n,32),y,"LOADHALF"
    #registers[y]=converttosignedvalue(extractsignedvalue(bin(int('0x'+x,16))[2:],16),32)

def sb(carr_for_list):
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    itit = registers[y]
    return converttosignedvalue(n,32),itit,"S";
    #returning final address, register_to_access , "S"

def sw(carr_for_list):
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    # print(k,m,registers[k])
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    itit = registers[y]
    return converttosignedvalue(n,32),itit,"S";
    #returning final address, register_to_access , "S"

def sh(carr_for_list):
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    itit = registers[y]
    return converttosignedvalue(n,32),itit,"S";
    #returning final address, register_to_access , "S"

def sd(carr_for_list): #venus didn't overwrite upper 4 bytes to '00', thus this also works similarly
    m=extractsignedvalue(carr_for_list[2],12)
    k=int(carr_for_list[0],2)
    n=m+int(registers[k],2)
    y=int(carr_for_list[1],2)
    itit = registers[y]
    return converttosignedvalue(n,32),itit,"S";
    #returning final address, register_to_access , "S"

def beq(carr_for_list):
    return 1,1,"SB";

def bge(carr_for_list):
    return 1,1,"SB";

def bne(carr_for_list):
    return 1,1,"SB";

def blt(carr_for_list):
    return 1,1,"SB";

def lui(carr_for_list):
    m=int(carr_for_list[2],2)
    n=int(carr_for_list[3],2)
    # registers[n]=bin(m).replace("0b","")+"000000000000"
    # registers[n]=com_32(registers[n])
    return com_32(bin(m).replace("0b","")+"000000000000"),n,"U";

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
    if knob1==1 and knob2==0:
        carr_for_list[8]=com_32(bin(int(carr_for_list[8],2)+m-4).replace("0b",""))
        return com_32(bin(int(carr_for_list[8],2)-m+4).replace("0b","")),n,"J1"
    elif knob1==1 and knob2==1:
        return com_32(carr_for_list[8]),n,'J1'
    # print('executionJAL',carr_for_list[8])
    #exit()
    return com_32(carr_for_list[8]),n,'J1'

def jalr(carr_for_list): #jalr x0,0(x1)
    # m=extractsignedvalue(carr_for_list[2],12) #imm
    # k=int(carr_for_list[0],2) #rs1
    # n=m+int(registers[k],2) #relative address to load from memory
    # print(register)
    o=int(carr_for_list[3],2)
    # temp=com_32(bin(int(registers[8],2)+4).replace("0b",""))
    # # carr_for_list[8]=bin(n).replace("0b","").zfill(32)
    # carr_for_list[8] = converttosignedvalue(n,32)
    # # print(carr_for_list[8])
    return com_32(carr_for_list[8]),o,"J2"

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
        if  (fun_name=="sb"):
            n = int(v1,2) # index where final address is stored
            itit = v2 # index where itit is stored
            if(n<500000000):
                mem.add_data_at(n,itit[24:32])
            else:
                stack[hex(n)]=hex(int(itit[24:32],2))[2::].zfill(2)
            return 1,1,"S";
        elif(fun_name=="sw"):
            n = int(v1,2) # index where final address is stored
            itit = v2 # index where itit is stored
            # print(n+3,n+2,n+1,n,m)
            #itit = registers[y]
            add3,add2,add1,add0=hex(n+3),hex(n+2),hex(n+1),hex(n)
            val3,val2,val1,val0=hex(int(itit[0:8],2))[2::].zfill(2), hex(int(itit[8:16],2))[2::].zfill(2),hex(int(itit[16:24],2))[2::].zfill(2),hex(int(itit[24:],2))[2::].zfill(2)
            # print('storing at',add0,add1,add2,add3)
            # print('value     ',val0,val1,val2,val3)
            if(n+3<500000000): #store in data segment and append the list
                mem.add_data_at(n+3,itit[0:8])
                mem.add_data_at(n+2,itit[8:16])
                mem.add_data_at(n+1,itit[16:24])
                mem.add_data_at(n,itit[24:32])
            elif(int( add3 ,16)>0x7ffffff3):
                print("can't write in memory after 0x7ffffff3")
            else: #store in stack
                stack[add3]=val3
                stack[add2]=val2
                stack[add1]=val1
                stack[add0]=val0
                # print(stack)
            return 1,1,"S";
        elif(fun_name=="sh"):
            n = int(v1,2) # index where final address is stored
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
        n = int(v1,2)#index of address
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
        n = int(v1,2)#index of address
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
        n = int(v1,2)#index of address
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

def write(carr_for_list,registers,v1,v2,v3,v4=1):
    ins_type = v3 # index where ins_type is stored
    index = v2 #index where index of destination register is stored
    result = v1 #value to be stored
    # print("Writing this time",index,result,ins_type)
    if(v4=='skip'):
        return
    if(ins_type == "R"):
        if index!=0:
            registers[index] = result
        # print("after write value of reg[",index,'] = ',registers[index],ins_type)
    elif(ins_type == "I"):
        # print('writing I format value',result ,'in',index)
        if index!=0:
            registers[index] = result
            # print(registers[index])
    elif(ins_type == "U"):
        if index!=0:
            registers[index] = result
    elif(ins_type == "S"):#do nothing
        nothingness = "sad"
    elif(ins_type == "SB"):#do nothing
        nothingness = "sad"
    elif(ins_type == "J1"):
        # nothingness = "sad"
        # print('wubbalubba',index,result)
        if index!=0:
            registers[index] = result
            # print('value of register updated by JAL INST. reg[',index,'] =',registers[index])
    elif(ins_type == "J2"):
        # nothingness = "sad"
        if index!=0:
            registers[index] = result
    elif(ins_type == "LOADBYTE"):
        if index!=0:
            registers[index] = result
    elif(ins_type == "LOADWORD"):
        # print('LOAD EXECUTION',index,result)
        if index!=0:
            registers[index] = result
            # print(' x',index,' = ',hex(int(registers[index],2))[2::].zfill(8) ,sep='')
    elif(ins_type == "LOADHALF"):
        if index!=0:
            registers[index] = result

def run(carr_for_list):
    rfile=open("outfile.mc","r+")
    bc=rfile.readlines()
    start=time.time()
    elapsed=0
    count=0
    no_of_alu=0
    no_of_cont=0
    no_of_dt=0
    j,k=0,0
    while elapsed < 4:
        #print(list[7])
        t=int(carr_for_list[8],2)
        string,lemme=fetch(carr_for_list,0)
        #print(string)
        if string=="continue":
            count=count+1  #for GUI
            curr_pc = carr_for_list[8]
            bs1,bs2,bs3=decode(carr_for_list,0)
            carr_for_list[8]=bs2
            # print(carr_for_list)
            if(carr_for_list[9]=='beq' or carr_for_list[9]=='bne' or carr_for_list[9]=='blt' or carr_for_list[9]=='bge' or carr_for_list[9]=='jal' or carr_for_list[9]=='jalr'):
                no_of_cont+=1
                if(carr_for_list[9]=='jal' or carr_for_list[9]=='jalr'):
                    no_of_alu+=1
            else:
                no_of_alu+=1
            if(carr_for_list[9]=='lh' or carr_for_list[9]=='lb' or carr_for_list[9]=='lw' or carr_for_list[9]=='sb' or carr_for_list[9]=='sw' or carr_for_list[9]=='sh'):
                no_of_dt+=1
            
            v1,v2,v3 = execute(carr_for_list,registers)
            v1,v2,v3 = mem_access(carr_for_list,v1,v2,v3)
            if(carr_for_list[9]=='jal'):
                v1 = com_32(curr_pc)
            write(carr_for_list,registers,v1,v2,v3)
            # registers[0] = '00000000000000000000000000000000'
            # printregisters()
            # if()
            elapsed=time.time()-start
            i=bc[int(t/4)]
            i=i.split(' ',2)
            i[2]=i[2].replace("\n","")
            item=QtWidgets.QTableWidgetItem(i[2])
            #item.setBackground(QtGui.QColor(255,0,0))
            #self.table.selectRow(j)
            window.tableWidget.setVerticalHeaderItem(j,item)
            window.tableWidget.setItem(j,k+0,QTableWidgetItem("Fetch"))
            window.tableWidget.setItem(j,k+1,QTableWidgetItem("Decode"))
            #self.table.item(j,k).setBackground(QtGui.QColor(125,125,125))
            window.tableWidget.setItem(j,k+2,QTableWidgetItem("Execute"))
            window.tableWidget.setItem(j,k+3,QTableWidgetItem("Mem_Access"))
            window.tableWidget.setItem(j,k+4,QTableWidgetItem("Reg_Update"))
            j=j+1
            k=k+5
            printregistersRUN()
        else:
            print("Code successfully Executed")
            printregistersRUN()
            break
    if(elapsed>4):
        print("Something is wrong, program took too long too execute, might be an infinite loop")
    print("----------------Non pipelined run-----------------")
    print("1.  Total Number of cycles taken\t\t: ",count*5)
    print('2.  Number of Instructions exeuted\t\t: ',count)
    print('3.  Cycles Per Instruction (CPI)\t\t: ',5)
    print('4.  Number of Data-Transfer Inst.\t\t: ',no_of_dt)
    print('5.  Number of ALU Instr. executed\t\t: ',no_of_alu)
    print('6.  Number of Branch Instr. executed\t: ',no_of_cont)
    print('7.  Number of Stalls in pipeline\t\t: ', '0')
    print('8.  Number of Data Hazards\t\t\t: ','0')
    print('9.  Number of Branch Hazards\t\t: ','0')
    print('10. Number of Branch Mispredictions\t\t: ','0')
    print('11. No. of Stalls due to Data Hazards  : ','0')
    print('12. No. of stalls due to branch hazards: ','0')
    
    myfile.write("\n----------------Non pipelined run-----------------")
    myfile.write("\n1.  Total Number of cycles taken\t\t: "+str(count*5))
    myfile.write('\n2.  Number of Instructions exeuted\t\t: '+str(count))
    myfile.write('\n3.  Cycles Per Instruction (CPI)\t\t: '+str(5))
    myfile.write('\n4.  Number of Data-Transfer Inst.\t\t: '+str(no_of_dt))
    myfile.write('\n5.  Number of ALU Instr. executed\t\t: '+str(no_of_alu))
    myfile.write('\n6.  Number of Branch Instr. executed\t: '+str(no_of_cont))
    myfile.write('\n7.  Number of Stalls in pipeline\t\t: '+ '0')
    myfile.write('\n8.  Number of Data Hazards\t\t\t\t: '+'0')
    myfile.write('\n9.  Number of Branch Hazards\t\t\t: '+'0')
    myfile.write('\n10. Number of Branch Mispredictions\t\t: '+'0')
    myfile.write('\n11. No. of Stalls due to Data Hazards\t: '+'0')
    myfile.write('\n12. No. of stalls due to branch hazards : '+'0')
    
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
    # print('this_opcode =',this_opcode,' rss1 =',rss1,'prev2_opcde =',prev2_opcode,' prev2_rd =',prev2_rd)
    if(this_opcode=='NIL'):
        return [-1]
    if (prev1_opcode != 'NIL' and prev1_rd!='00000' and prev1_rd!='NIL'):
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
            elif (this_opcode=='1100011'): #this instruction is branch instruction
                if(prev1_rd==rss1 and prev1_rd==rss2): #this requires two cycles stalls
                    returnlist.append(['M','D',12,[2,1]])
                elif(prev1_rd==rss1):
                    returnlist.append(['M','D',1,[2,1]])
                elif(prev1_rd==rss2):
                    returnlist.append(['M','D',2,[2,1]])
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
            # this instruction is of R,I or [S] format
            if(this_opcode == '0110011' or (this_opcode == '0010011' or this_opcode == '1100111') or this_opcode == '0100011'):
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
            elif (this_opcode == '1100011'): #this instruction is branch needs, values in D stage, NEEDS 1 cycle stall
                if(prev1_rd==rss1 and prev1_rd==rss2):
                    returnlist.append(['E','D',12,[2,1]])
                elif(prev1_rd==rss1):
                    returnlist.append(['E','D',1,[2,1]])
                elif(prev1_rd==rss2):
                    returnlist.append(['E','D',2,[2,1]])
            elif(this_opcode == '0000011'): #this instruction is load whereas previous is determining value after execution stage
                if(prev1_rd==rss1):
                    returnlist.append(['E', 'E', 1, [2, 1]])
                    # return 'E','M',1,[2,1]
        # else:
        #     return -1, -1, -1, [-1, -1]

    if(prev2_opcode!='NIL'):
    # check hazard for prev2 and current instruction
        if(prev2_rd!='00000' and prev2_rd!='NIL' and (prev2_rd == rss1 or prev2_rd == rss2)):
            # any format for prev2 instruction would result in ez forwarding,
            # prev2 has completed M,
            # prev1 has completed E,
            # current has completed D, therefore, Ry will have the desired value in case of depencey eg. lw x5,0(x2), add x3,x0,x1, sub x4,x5,x6
            # this instruction is of R,I or [S] format load format
            # print('HOOOOOOOOLLLLLLLLLUUUU U U U U U UU s')
            if((this_opcode == '0110011' or (this_opcode == '0010011' or this_opcode == '1100111') or this_opcode == '0100011') or this_opcode=='0000011'):
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

            elif(this_opcode == '1100011'):
                if(prev2_opcode=='0000011'): #load instruction
                    if(prev2_rd==rss1 and prev2_rd==rss2): #needs 1 cycle stall
                        returnlist.append(['M','D',12,[3,1]])
                        return returnlist
                    elif (prev2_rd==rss1):
                        returnlist.append(['M','D',1,[3,1]])
                        return returnlist
                    elif (prev2_rd==rss2):
                        returnlist.append(['M','D',2,[3,1]])
                        return returnlist
                elif(prev2_opcode=='0110011' or prev2_opcode=='0010011' or (prev2_opcode=='0010111' or prev2_opcode=='0110111') or prev2_opcode=='1101111' or prev2_opcode=='1100111'): #R,I,U,UJ
                    # print('``````````````````````````````````````detecting hazard')
                    if(prev2_rd==rss1 and prev2_rd==rss2): #no stalling required
                        returnlist.append(['E','D',12,[3,1]])
                        return returnlist
                    elif (prev2_rd==rss1):
                        returnlist.append(['E','D',1,[3,1]])
                        return returnlist
                    elif (prev2_rd==rss2):
                        returnlist.append(['E','D',2,[3,1]])
                        return returnlist
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

def flush_dada(pc):
    master_list[0][7] = -1  # it won't be executed
    # master_list[0][8] = pc  # filling the next carr_for_list with suitable pc
    master_list.insert(0,['NIL','NIL','NIL','NIL','NIL','NIL','NIL','NIL',pc,'NIL'])
    # print('flush done with new pc at 0 as',pc)

i=0

def flush(number_of_steps, pc):
    for i in range(number_of_steps):    # emptying the unnecessary instruction
        master_list[i][7] = -1
    master_list[0][8] = pc  # filling the next carr_for_list with suitable pc

def stalling(i):                # i is index above it should continue as usual
    # master_list.pop(0)
    master_list.insert(i, ['NIL','NIL','NIL','NIL','NIL','NIL','NIL',-2,'NIL','NIL'])
    # master_list[i][7] = -2


def print_pipelined(pr_fd,pr_de,pr_em,pr_mw,f,cycle):
    if(f==1):
        # ," , "+"Rb = ",str((hex(int(pr_de[1],2)).replace('0x','').zfill(8))),)))," , "+"Imm = ",str((hex(int(pr_de[2],2)).replace('0x','').zfill(8)))," ,"+"Rd = ",str((hex(int(pr_de[3],2)).replace('0x','').zfill(8)))
        '''printing pipeline registers'''
        print("------  The Pipeline Registers after ",cycle," cycles  ------")
        print("\tBetween F & D : " + "IR = ",str((hex(int(pr_fd[0],2)).replace('0x','').zfill(8))),)
        print("\tBetween D & E : " + "Ra = ",str((hex(int(pr_de[0],2)).replace('0x','').zfill(8)))," , "+"Rb = ",str((hex(int(pr_de[1],2)).replace('0x','').zfill(8)))," , "+"Rd = ",str((hex(int(pr_de[2],2)).replace('0x','').zfill(8)))," , "+"Imm = ",str((hex(int(pr_de[3],2)).replace('0x','').zfill(8))))
        print("\tBetween E & M : " + "Rz = ",str((hex(int(pr_em[0],2)).replace('0x','').zfill(8)))," , "+"Rb = ",str((hex(int(pr_em[1],2)).replace('0x','').zfill(8)))," , "+"Rd = ",str((hex(int(pr_em[2],2)).replace('0x','').zfill(8)))," , "+"Imm = ",str((hex(int(pr_em[3],2)).replace('0x','').zfill(8))))
        print("\tBetween M & W : " + "Ry = ",str((hex(int(pr_mw[0],2)).replace('0x','').zfill(8)))," , "+"Rd = ",str((hex(int(pr_mw[1],2)).replace('0x','').zfill(8))),)
        # print("\t\tRy : " + str((hex(int(pr_printing[4],2)).replace('0x','').zfill(8))))

def printknob5(pr_printing,f):
    if(f!=-1):
        # ," , "+"Rb = ",str((hex(int(pr_de[1],2)).replace('0x','').zfill(8))),)))," , "+"Imm = ",str((hex(int(pr_de[2],2)).replace('0x','').zfill(8)))," ,"+"Rd = ",str((hex(int(pr_de[3],2)).replace('0x','').zfill(8)))
        '''printing pipeline registers'''
        print("------  The Pipeline Registers for ",f,"th instruction   ------")
        print("\tBetween F & D : " + "IR = ",str((hex(int(pr_printing[0],2)).replace('0x','').zfill(8))),)
        print("\tBetween D & E : " + "Ra = ",str((hex(int(pr_printing[1],2)).replace('0x','').zfill(8)))," , "+"Rb = ",str((hex(int(pr_printing[2],2)).replace('0x','').zfill(8)))," , "+"Rd = ",str((hex(int(pr_printing[3],2)).replace('0x','').zfill(8)))," , "+"Imm = ",str((hex(int(pr_printing[4],2)).replace('0x','').zfill(8))))
        print("\tBetween E & M : " + "Rz = ",str((hex(int(pr_printing[5],2)).replace('0x','').zfill(8)))," , "+"Rb = ",str((hex(int(pr_printing[6],2)).replace('0x','').zfill(8)))," , "+"Rd = ",str((hex(int(pr_printing[7],2)).replace('0x','').zfill(8)))," , "+"Imm = ",str((hex(int(pr_printing[8],2)).replace('0x','').zfill(8))))
        print("\tBetween M & W : " + "Ry = ",str((hex(int(pr_printing[9],2)).replace('0x','').zfill(8)))," , "+"Rd = ",str((hex(int(pr_printing[10],2)).replace('0x','').zfill(8))),)
        # print("\t\tRy : " + str((hex(int(pr_printing[4],2)).replace('0x','').zfill(8))))

def run_pipelined_data_for():
    flag = 0
    j=0
    rfile=open("outfile.mc","r+")
    bc=rfile.readlines()
    j,k=0,0
    start = time.time()
    elapsed = 0
    count = 0
    pr_mem = ['nil','nil','nil'] #pipeline register for decode stage
    pr_exe = ['nil','nil','nil']
    pr_printing = ['0','0','0','0','0','0','0','0','0','0','0'] #Ir Ra Rb Rd imm Rz Rb Rd imm Ry Rd
    pr_fd = ['0']#IR
    pr_de = ['0','0','0','0'] #Ra Rb Rd imm
    pr_em = ['0','0','0','0'] #Rz Rb Rd imm
    pr_mw = ['0','0'] #Ry Rd
    nextflagMM=0
    nextflagMD=0
    nextflagED=0
    stallflag,flushflag=0,0
    no_of_data_hazards=0
    no_of_stalls=0
    no_of_mispred=0
    no_of_inst = 0
    no_of_dt = 0
    no_of_alu = 0
    no_of_control =0
    stalls_by_DF = 0
    stalls_by_BP = 0
    lemme=[-1,-1]
    bs1,bs2,bs3=-1,-1,[-1,-1]
    curr_pc='00000'
    print("master_list")
    hj,hj_prev=-1,-1
    blank=[]
    blank2=[]
    blank3=[]
    # for i in range(5):
    #     if(master_list[i][8]!='NIL'):
    #         print(i,"-->",master_list[i],' **** ',hex(int(master_list[i][8],2)))
    #     else:
    #         print(i,"-->",master_list[i],' **** ')
    app_flag=0
    while elapsed < 60:
        count=count+1
        t=0
        if(master_list[4][7]!=-1 and master_list[4][7]!=-2 and master_list[4][6]!='NIL'):
            no_of_inst+=1
            if(master_list[4][9]=='beq' or master_list[4][9]=='bge' or master_list[4][9]=='bne' or master_list[4][9]=='blt' or master_list[4][9]=='jal' or master_list[4][9]=='jalr'):
                no_of_control+=1
                if(master_list[4][9]=='jal' or master_list[4][9]=='jalr'):
                    no_of_alu+=1
            else:
                no_of_alu+=1
            if(master_list[4][9]=='sh' or master_list[4][9]=='sw' or master_list[4][9]=='sb' or master_list[4][9]=='lh' or master_list[4][9]=='lb' or master_list[4][9]=='lw'):
                no_of_dt+=1
        # if(master_list[1][8]!='NIL'):
        #     print("\n>>> (",count,") [",no_of_inst,"] \t ENTER--->",master_list[1][9], "initial pc=", hex(int(master_list[1][8], 2)))
        # else:
        #     print("\n>>> \t ENTER--->",master_list[1][9], "initial pc=", 'NIL')

        # print('before execution of below stages x1',registers[1],stallflag,nextflagED,nextflagMD,nextflagMM)
        # print('x5=',registers[5],' and x7=',registers[7])
        
        # lemme[2] = lemme[1]
        lemme[1] = lemme[0]                             

        string,lemme[0]=fetch(master_list[0],stallflag)            #lemme[0] is -1 if no branching found, else it represents next pc(target)
        # print("lemme[0] = ",lemme[0])
        if master_list[0][7]!='NIL' and master_list[0][7]!=-1:
            pr_fd[0] = master_list[0][7]
        if (int(master_list[0][8],2) == knob5*4):
            pr_printing[0] = master_list[0][7]
        if (string == "over" and master_list[4][7] == -1 and master_list[3][7]==-1 and master_list[2][7]==-1 and master_list[1][7]==-1):  # full code completed
            print("Code successfully executed")
            break
        else:
            if master_list[4][7] != -1 and master_list[4][7] != -2:
                write(master_list[4], registers, pr_mem[0],pr_mem[1],pr_mem[2],pr_mem[3])
                #z=int(master_list[4][8],2)
                #print(int(z/4))
                window.tableWidget.setItem(k+t,count-1,QTableWidgetItem("Reg_Update"))
                t=t+1
                app_flag=1
                #hj=get_inst(master_list[4][7])
                #item=QTableWidgetItem(hj)
                #window.tableWidget.setVerticalHeaderItem(j,item)
                #j=j+1
            
            if master_list[3][7] != -1 and master_list[3][7] != -2:
                pr_mem = mem_access(master_list[3], pr_exe[0],pr_exe[1],pr_exe[2])
                window.tableWidget.setItem(k+t,count-1,QTableWidgetItem("Mem_Access"))
                t=t+1
                pr_mem = list(pr_mem)
                pr_mem.append(pr_exe[3])
                if pr_mem[1]=='LOADBYTE' or  pr_mem[1]=='LOADWORD' or  pr_mem[1]=='LOADHALF':
                    pr_mw[0] = pr_mem[0]
                # pr_mw[1] = pr_mem[1]
                if master_list[3][3] != 'NIL':
                    pr_mw[1]=master_list[3][3]
                if (int(master_list[3][8],2) == knob5*4):
                    if pr_mem[1]=='LOADBYTE' or  pr_mem[1]=='LOADWORD' or  pr_mem[1]=='LOADHALF':
                        pr_printing[9] = pr_mem[0]
                    if master_list[3][3] != 'NIL':
                        pr_printing[10]=master_list[3][3]
            
            if master_list[2][7] != -1 and master_list[2][7] != -2:
                pr_exe = execute(master_list[2], registers)
                window.tableWidget.setItem(k+t,count-1,QTableWidgetItem("Execute"))
                t=t+1
                pr_exe = list(pr_exe)
                pr_exe.append(-1)
                # print('pr_exe ',pr_exe)
                if pr_exe[0]!='NIL':
                    pr_em[0] = com_32(str(pr_exe[0]))
                if master_list[2][3] != 'NIL':
                    pr_em[2]=master_list[2][3]
                if  master_list[2][1] != 'NIL':
                    pr_em[1]=registers[int(master_list[2][1],2)]
                if master_list[2][2] != 'NIL':
                    pr_de[3]=master_list[2][2]
                if (int(master_list[2][8],2) == knob5*4):
                    if pr_exe[0]!='NIL':
                        pr_printing[5] = com_32(str(pr_exe[0]))
                    if master_list[2][3] != 'NIL':
                        pr_printing[6]=master_list[2][3]
                    if  master_list[2][1] != 'NIL':
                        pr_printing[7]=registers[int(master_list[2][1],2)]
                    if master_list[2][2] != 'NIL':
                        pr_printing[8]=master_list[2][2]
                
            if master_list[1][7] != -1 and master_list[1][7] != -2:
                # print("decoding master_list[1]",master_list[1][9])
                curr_pc = master_list[1][8]
                bs1,bs2,bs3=decode(master_list[1],stallflag)        #bs1 tells if predition right or wrong, bs2 is target, bs3 tells type,bs4 tells if this time it is taken or not
                window.tableWidget.setItem(k+t,count-1,QTableWidgetItem("Decode"))
                t=t+1
                hj=get_inst(master_list[1][7])
                if hj_prev!=hj:
                    hj=get_inst(master_list[1][7])
                    item=QTableWidgetItem(hj)
                    window.tableWidget.setVerticalHeaderItem(j,item)
                    j=j+1
                    hj_prev=hj
                # print("Test : ",master_list[1][0],)
                if master_list[1][0] != 'NIL':
                    pr_de[0]=registers[int(master_list[1][0],2)]
                if master_list[1][1] != 'NIL':
                    pr_de[1]=registers[int(master_list[1][1],2)]
                if master_list[1][3]!='NIL':
                    pr_de[2]=master_list[1][3]
                if master_list[1][2] != 'NIL':
                    pr_de[3]=master_list[1][2]
                if (int(master_list[1][8],2) == knob5*4):
                    if master_list[1][0] != 'NIL':
                        pr_printing[1]=registers[int(master_list[1][0],2)]
                    if master_list[1][1] != 'NIL':
                        pr_printing[2]=registers[int(master_list[1][1],2)]
                    if master_list[1][3]!='NIL':
                        pr_printing[3]=master_list[1][3]
                    if master_list[1][2] != 'NIL':
                        pr_printing[4]=master_list[1][2]
            
            else:
                bs1,bs2,bs3 = -1,-1,[-1,-1]

            print_pipelined(pr_fd,pr_de,pr_em,pr_mw,knob4,count)
            printregisters(knob3,count)
            if master_list[4][8] != 'NIL' and int(master_list[4][8],2)==knob5*4:
                printknob5(pr_printing,knob5)
            #now that decode of master_list[1] is complete we check for data hazard

            # for i in range(5):
            #     if(master_list[i][8]!='NIL'):
            #         print(i,"-->",master_list[i],' **** ',hex(int(master_list[i][8],2)))
            #     else:
            #         print(i,"-->",master_list[i],' **** ')
            # print('x1=0x',hex(int(registers[1],2))[2::].zfill(8),' x2=0x',hex(int(registers[2],2))[2::].zfill(8),' x3=0x',registers[3],' x4=',registers[4],' x5=',registers[5],' x6=',registers[6],' x7=',registers[7],' x8=',registers[8],' x9=',registers[9],' x10=',registers[10],' x11=',registers[11],' x13=',registers[13])
            
            # print('x5 =',registers[5])
            window.tableWidget.setItem(k+t,count-1,QTableWidgetItem("Fetch"))
            if app_flag==1:
                k=k+1
                app_flag=0 
            
            if(stallflag==0):
                returnlist = detect_data_hazard()
                if(returnlist[0]!=-1):
                    window.tableWidget.selectRow(j-1)
                    listToStr = ' '.join(map(str,returnlist))
                    listToStr = 'Decode'+listToStr
                    window.tableWidget.setItem(j-1,count-1,QTableWidgetItem(listToStr))            
            else:
                returnlist = [-1]

            if(nextflagMM==1):
                # print("inside nextFLAGMM\tpr_mem=",pr_mem)
                registers[pr_mem[1]] = pr_mem[0]
                pr_mem[3]='skip'
                nextflagMM=0
                # if(stallflag==0):
                #     print('REGISTERS CHANGED HERE',pr_mem)
                #     registers[pr_mem[1]] = pr_mem[0]
                #     nextflagMM=0
                if(stallflag!=0):
                    # no_of_data_hazards-=1
                    stallflag=0

            if(nextflagED==1): # 0 or 1 cycle stalls

                # registers[pr_exe[1]] = pr_exe[0]
                nextflagED=0
                if(stallflag!=0):
                    stallflag-=1
                    # no_of_data_hazards-=1

            if(nextflagMD==1): # 1 or 2 cycle stalls
                # registers[pr_mem[1]] = pr_mem[0]
                # print('just changed in MD',pr_mem[1], 'to',pr_mem[0] )
                if(stallflag!=0):
                    if(stallflag==2):
                        registers[pr_mem[1]] = pr_mem[0]
                        pr_mem[3]='skip'
                        stalling(2)
                    stallflag-=1
                    if(stallflag==0):
                        # registers[pr_mem[1]] = pr_mem[0]
                        # no_of_data_hazards-=1
                        nextflagMD=0

                #print(">>> \t ENTER--->",carr_for_list[9],"initial pc=",hex(int(carr_for_list[8],2)))

            # returnlist = detect_data_hazard()
            
            # if(stallflag==0):
            #     returnlist = detect_data_hazard()
            # else:
            #     returnlist = [-1]
            
            fetchedInst = master_list[0][7]
            
            if(returnlist[0]!=-1):
                # print("DATA HAZARD DETECTED, forwarding case ,",fr,to,target,layer)
                # print("DATA HAZARD DETECTED, forwarding case D.A.N.G.E.R.,",returnlist)
                no_of_data_hazards+=1
                if   (returnlist[0][0]=='E' and returnlist[0][1]=='E'):  # case- E to E
                    # print("data forwarding done for",master_list[1][9],"\nreg[x",pr_exe[1],"] = ",pr_exe[0])
                    registers[pr_exe[1]] = pr_exe[0] #writing the value into the register early
                    pr_exe[3]='skip'
                
                elif (returnlist[0][0]=='M' and returnlist[0][1]=='E'):
                    if(returnlist[0][3]==[3,1]):
                        # nextflagMM=1
                        registers[pr_mem[1]] = pr_mem[0]
                        pr_mem[3]='skip'
                    elif(returnlist[0][3]==[2,1]):
                        stalling(2)
                        stallflag=1
                        nextflagMM=1
                        no_of_stalls+=1
                        stalls_by_DF+=1
                        # continue
                
                elif (returnlist[0][0]=='M' and returnlist[0][1]=='M'):
                    #write the value in the next cycle because then i.e. wait one cycle to write the value
                    # (curr)master_list[1] would be ready for M stage and (curr)master_list[2] would have completed M stage
                    nextflagMM=1
                    
                elif (returnlist[0][0]=='E' and returnlist[0][1]=='D'): #for branch resolution we need data at decode stage
                    if(returnlist[0][3]==[2,1]): # 1 cycle stalls
                        nextflagED=1
                        stalling(2)
                        registers[pr_exe[1]]=pr_exe[0] # we already have values from E stage of instruction at index 2
                        stallflag=1
                        no_of_stalls+=1
                        stalls_by_DF+=1
                        pr_exe[3]='skip'
                        # continue
                    elif(returnlist[0][3]==[3,1]): #no stall required
                        registers[pr_mem[1]] = pr_mem[0] #as it was dependent on E stage of instruction at index 3 but it has now completed its memory stage so we can take registers value from it
                        pr_mem[3]='skip'
                        # nextflagED=1
                
                elif (returnlist[0][0]=='M' and returnlist[0][1]=='D'):
                    if(returnlist[0][3]==[3,1]): # 1 cycle stalls
                        stalling(2)
                        stallflag=1
                        nextflagMD=1
                        registers[pr_mem[1]] = pr_mem[0] #because mem of 3rd is already done but we need a stall to decode the instruction again
                        pr_mem[3]='skip'
                        no_of_stalls+=1
                        stalls_by_DF+=1
                        # continue
                    elif(returnlist[0][3]==[2,1]): #2 cycle stalls
                        stalling(2)
                        nextflagMD=1
                        stallflag=2
                        no_of_stalls+=2
                        stalls_by_DF+=2
                        # continue
            
            # if(bs3[0]=='SB' or bs3[0]=='JAL' or bs3[0]=='JALR'):
            #     print('\n++++++++++++++++++++++++++++++++++++\ninstruction fetched =',com_32(bin(int(master_list[0][8],2)-4)[2::]),' vs. bs2=',com_32(bs2),'\nthis means = prediction is [[[[ bs1=',bs1 ,'type =',bs3[0],'stallflag=',stallflag,"]]]] , lemme[1]=",lemme[1])
            # else:
            #     print('instruction fetched =',(bin(int(master_list[0][8],2)-4)[2::]),' vs. bs2=',(bs2),'this means = prediction is',bs1,"\n, lemme[1]=",lemme[1],'stallflag=',stallflag)    
            # print(hex(int(curr_pc,2)),'value returned after decode are','\t|#|#|#|#|\t bs1 =',bs1,'bs2 =',bs2,'bs3',bs3)
            
            if lemme[1] == -1:                        #not foudd in btb
                # print('lemme [1] == -1')
                if ((bs3[0] == "SB" or bs3[0] == "JAL" or bs3[0] == "JALR") and stallflag==0 and com_32(bin(int(master_list[0][8],2)-4)[2::])!=com_32(bs2) ):    #new entry in btb
                    # if master_list[1][8] != bs2:       #everything is messed up->masterlist0 is bullshit,flush it, call new target
                    # print('-------------------needs flushing now')
                    flush_dada(bs2)
                    flushflag=1
                    no_of_stalls+=flushflag
                    stalls_by_BP+=flushflag
                    no_of_mispred+=1
                elif((bs3[0] == "SB" or bs3[0] == "JAL" or bs3[0] == "JALR") and stallflag==0 and com_32(bin(int(master_list[0][8],2)-4)[2::])==com_32(bs2)):
                    insert_carr()
                    continue
            else:                                     #was found in fetch in btb
                # bin(int(master_list[0][8],2)-4)[2::] is the pc of instruction fetched during this cycle and bs2 is the  pc of target
                if ((bs3[0] == "SB" or bs3[0] == "JAL" or bs3[0] == "JALR") and com_32(bin(int(master_list[0][8],2)-4)[2::])!=com_32(bs2) and stallflag==0):# and bin(int(master_list[0][8],2)-4)[2::]!=bs2):                          #predictin mesed up
                    flush_dada(bs2)
                    flushflag=1                   #everything is messed up->masterlist0 is bullshit,flush it, call new target
                    no_of_stalls+=flushflag
                    stalls_by_BP+=flushflag
                    no_of_mispred+=1
                elif((bs3[0] == "SB" or bs3[0] == "JAL" or bs3[0] == "JALR") and stallflag==0 and com_32(bin(int(master_list[0][8],2)-4)[2::])==com_32(bs2)):# bin(int(master_list[0][8],2)-4)[2::]==bs2):
                    insert_carr()
                    continue

            # print('\t\t\t\t\t\t\tstallflag =',stallflag,'flushflag =',flushflag)
            # print('afterwards\t\t\t\t',stallflag,bs3[0],b_hist)

            # if(master_list[4][9]=='jalr'):
            #     sys.exit()
            
            if(stallflag==0):
                if(flushflag==0):
                    insert_carr()
                if lemme[0] != -1:                                  #wow we predicted something
                    master_list[0][8] = lemme[0]                    #pc set as new pc
                    # print("master_list[0][8], pc = ",master_list[0][8])
                if(bs3[0] == "SB" or bs3[0] == "JAL" or bs3[0] == "JALR"):
                    update_bht(bin(int(curr_pc,2)-4)[2::],bs3[1],bs2)
                    master_list[0][8] = bs2
                    # print('\t\t\t\t\tnow',master_list[0])
            # print('afterwards\t\t\t\t',stallflag,bs3[0],b_hist)
            if flushflag==1:
                blank.append(j)
                # print(fetchedInst)
                if(fetchedInst!=-1 and fetchedInst!=-2):
                    blank2.append(get_inst(fetchedInst))
                else:
                    blank2.append('NONONO')
                blank3.append(count)
            flushflag=0
            elapsed = time.time()-start
            # print('register x1 =',registers[1])
                    
    if(elapsed > 60):
        print("Something is wrong, program took too long too execute, might be an infinite loop")
    
    print("---------Pipelined Execution with DF enabled--------")
    print("1.  Total Number of cycles taken\t:",count-1)
    print('2.  Number of instructions executed\t:',no_of_inst)
    print('3.  Cycles Per Instruction (CPI)\t:',(count-1)/no_of_inst)
    print('4.  Number of Data-Transfer inst.\t:',no_of_dt)
    print('5.  Number of ALU instr. executed\t:',no_of_alu)
    print('6.  Number of Control inst. executed\t:',no_of_control)
    print("7.  Number of Stalls in the pipeline\t:",no_of_stalls)
    print("8.  Number of Data Hazards\t\t:",no_of_data_hazards)
    print('9.  Number of Branch Hazards\t\t:',stalls_by_BP)
    print('10. Number of Branch Mispredictions\t:',no_of_mispred)
    print('11. No. of Stalls due to Data Hazards\t:',stalls_by_DF)
    print('12. No. of Stalls due to Branch Hazard\t:',stalls_by_BP)
    fd=0
    for sam in blank:
        window.tableWidget.insertRow(sam+fd)
        #fd+=1
        item=QtWidgets.QTableWidgetItem("WRONG FETCH "+blank2[fd])
        #item.setBackground(QtGui.QColor(255,0,0))
        #self.table.selectRow(j)
        vaal1 = window.tableWidget.item(sam+fd+1,blank3[fd]-1)
        vaal2 = window.tableWidget.item(sam+fd+1,blank3[fd]-2)
        # print(vaal1,vaal1.text(),vaal2)
        if(vaal1!=None):
            window.tableWidget.setItem(sam+fd,blank3[fd]-1,QTableWidgetItem(vaal1.text()))
            window.tableWidget.item(sam+fd,blank3[fd]-1).setBackground(QtGui.QColor(255,0,0))
            window.tableWidget.setItem(sam+fd+1,blank3[fd]-1,QTableWidgetItem(''))
        if(vaal2!=None):
            window.tableWidget.setItem(sam+fd,blank3[fd]-2,QTableWidgetItem(vaal2.text()))
            window.tableWidget.item(sam+fd,blank3[fd]-2).setBackground(QtGui.QColor(255,0,0))
            window.tableWidget.setItem(sam+fd+1,blank3[fd]-2,QTableWidgetItem(''))  
        window.tableWidget.setVerticalHeaderItem(sam+fd,item)
        # window.tableWidget.setItem(sam+fd+1,blank3[fd]-1,QTableWidgetItem(''))
        # window.tableWidget.setItem(sam+fd+1,blank3[fd]-2,QTableWidgetItem(''))
        # window.tableWidget.setItem(sam+fd,blank3[fd]-1,QTableWidgetItem('Fetch'))
        # window.tableWidget.item(sam+fd,blank3[fd]-1).setBackground(QtGui.QColor(255,0,0))
        fd+=1
    print(blank)
    print(blank2)
    #exit()
    
    myfile.write("\n---------Pipelined Execution with DF enabled--------")
    myfile.write("\n1.  Total Number of cycles taken\t\t: "+str(count-1))
    myfile.write('\n2.  Number of instructions executed\t\t: '+str(no_of_inst))
    myfile.write('\n3.  Cycles Per Instruction (CPI)\t\t: '+ str((count-1)/no_of_inst))
    myfile.write('\n4.  Number of Data-Transfer inst.\t\t: '+str(no_of_dt))
    myfile.write('\n5.  Number of ALU instr. executed\t\t: '+str(no_of_alu))
    myfile.write('\n6.  Number of Control inst. executed\t: '+str(no_of_control))
    myfile.write("\n7.  Number of Stalls in the pipeline\t: "+str(no_of_stalls))
    myfile.write("\n8.  Number of Data Hazards\t\t\t\t: "+str(no_of_data_hazards))
    myfile.write('\n9.  Number of Branch Hazards\t\t\t: '+str(stalls_by_BP))
    myfile.write('\n10. Number of Branch Mispredictions\t\t: '+str(no_of_mispred))
    myfile.write('\n11. No. of Stalls due to Data Hazards\t: '+str(stalls_by_DF))
    myfile.write('\n12. No. of Stalls due to Branch Hazard\t: '+str(stalls_by_BP))


def nstalling(i):                # i is index above it should continue as usual
    master_list.pop(0)
    master_list[0][8]=master_list[1][8]
    master_list.insert(i, ['NIL','NIL','NIL','NIL','NIL','NIL','NIL',-2,'NIL','NIL'])
    # master_list[i][7] = -2

def run_pipelined_without_data_for():
    print("enter")
    rfile=open("outfile.mc","r+")
    bc=rfile.readlines()
    app_flag = 0
    j,k=0,0
    flag = 0
    start = time.time()
    elapsed = 0
    count = 0
    lemme=[-1,-1]
    # v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pr_mem = ['nil','nil','nil'] #pipeline register for decode stage
    pr_exe = ['nil','nil','nil']
    pr_printing = ['0','0','0','0','0','0','0','0','0','0','0'] #Ir Ra Rb Rd imm Rz Rb Rd imm Ry Rd
    pr_fd = ['0']
    pr_de = ['0','0','0','0'] #Ra Rb Rd imm
    pr_em = ['0','0','0','0'] #Rz Rb Rd imm
    pr_mw = ['0','0'] #Ry Rd
    nextflagMM=0
    no_of_data_hazards=0
    #predict=0
    changer=[-1,-1]
    stat1=0   #Total number of cycles
    stat2=0   #total instructions executed
    stat3=0   #CPI
    stat4=0   #Number of Data-transfer(load and store) instructions executed
    stat5=0   #number of ALU instructions executed
    stat6=0   # Number of control instructions executed
    stat7=0   #Number of stalls in the pipeline
    stat8=0   #Number of data hazards
    stat9=0   #Number of control hazards
    stat10=0   #Number of branch mispredictions
    stat11=0    #number of stalls due to data hazards
    stat12=0   #Number of stalls due to control hazards
    t=0
    kkpk=0
    previous='nil'
    print("master_list")
    for i in range(5):
        print(i,"-->",master_list[i])
    while elapsed < 30:
        t=0
        stat1=stat1+1
        changer[0]=master_list[0][8]
        # print(master_list[0][8])
        z_prev=int(master_list[0][8],2)
        string,lemme[0]=fetch(master_list[0],0)           #POOP#lemme[0] is -1 if no branching found, else it represents next pc(target)
        
        # print(string,lemme[0])
        if master_list[0][7]!='NIL' and master_list[0][7]!=-1:
            pr_fd[0] = master_list[0][7]
        if (int(master_list[0][8],2) == knob5*4):
            pr_printing[0] = master_list[0][7]
        #lemme[1]=lemme[0]
        if string == "over" and master_list[4][7] == -1:  # full code completed
            print("Code successfully executed")
            break
        else:
            # st=fetch(master_list[0])
            #if lemme[0] != -1:                                  #wow we predicted something
            #    master_list[0][8] = lemme[0]                    #pc set as new pc
            if master_list[4][7] != -1 and master_list[4][7] != -2:
                write(master_list[4], registers, pr_mem[0],pr_mem[1],pr_mem[2])
                window.tableWidget.setItem(k+t,stat1-1,QTableWidgetItem("Reg_Update"))
                t=t+1
                app_flag=1
                hj=get_inst(master_list[4][7])
                item=QTableWidgetItem(hj)
                window.tableWidget.setVerticalHeaderItem(j,item)
                j=j+1
                stat2=stat2+1
                abc=master_list[4][6]
                if abc=="0100011" or abc=="0000011":
                    stat4=stat4+1
                if abc=="1100011" or abc=="1101111" or abc=="1100111":
                    stat6=stat6+1
                if abc=='1101111' or abc=='1100111':
                    stat5+=1
            if master_list[3][7] != -1 and master_list[3][7] != -2:
                pr_mem = mem_access(master_list[3], pr_exe[0],pr_exe[1],pr_exe[2])
                #print(t,k)
                window.tableWidget.setItem(k+t,stat1-1,QTableWidgetItem("Mem_Access"))
                t=t+1
                #print(">>> \t ENTER--->",master_list[4][9],"initial pc=",master_list[4][8])
                # print("pr_mem =",pr_mem)
            if master_list[2][7] != -1 and master_list[2][7] != -2:
                pr_exe = execute(master_list[2], registers)
                window.tableWidget.setItem(k+t,stat1-1,QTableWidgetItem("Execute"))
                t=t+1
                if pr_exe[0]!='NIL':
                    pr_em[0] = com_32(str(pr_exe[0]))
                if master_list[2][3] != 'NIL':
                    pr_em[2]=master_list[2][3]
                if  master_list[2][1] != 'NIL':
                    pr_em[1]=registers[int(master_list[2][1],2)]
                if master_list[2][2] != 'NIL':
                    pr_de[3]=master_list[2][2]
                if (int(master_list[2][8],2) == knob5*4):
                    if pr_exe[0]!='NIL':
                        pr_printing[5] = com_32(str(pr_exe[0]))
                    if master_list[2][3] != 'NIL':
                        pr_printing[6]=master_list[2][3]
                    if  master_list[2][1] != 'NIL':
                        pr_printing[7]=registers[int(master_list[2][1],2)]
                    if master_list[2][2] != 'NIL':
                        pr_printing[8]=master_list[2][2]
                # print("pr_exe =",pr_exe)
            if master_list[1][7] != -1 and master_list[1][7] != -2:
                bs1,bs2,bs3=decode(master_list[1],0)        #bs1 tells if predition right or wrong, bs2 is target, bs3 tells type
                bs2=bin(int(bs2,2)).replace("0b","")
                window.tableWidget.setItem(k+t,stat1-1,QTableWidgetItem("Decode"))
                t=t+1
                #z=int(bs2,2)
                #previous='nil'
                #if z!=z_prev:
                #    kkpk=1
                #if len(bc)>int(z/4) and (z_prev==z or kkpk==1):
                #    i=bc[int(z/4)]
                #    i=i.split(' ',2)
                #    item=QTableWidgetItem(i[2])
                #    if i[2]!=previous:
                #        window.tableWidget.setVerticalHeaderItem(j,item)
                #        j=j+1
                #        previous=i[2]
                    #item.setTextAlignment(Qt.AlignHCenter)
                    #print(j,i[2])
                #    if kkpk==1:
                #        kkpk=0
                if master_list[1][0] != 'NIL':
                    pr_de[0]=registers[int(master_list[1][0],2)]
                if master_list[1][1] != 'NIL':
                    pr_de[1]=registers[int(master_list[1][1],2)]
                if master_list[1][3]!='NIL':
                    pr_de[2]=master_list[1][3]
                if master_list[1][2] != 'NIL':
                    pr_de[3]=master_list[1][2]
                if (int(master_list[1][8],2) == knob5*4):
                    if master_list[1][0] != 'NIL':
                        pr_printing[1]=registers[int(master_list[1][0],2)]
                    if master_list[1][1] != 'NIL':
                        pr_printing[2]=registers[int(master_list[1][1],2)]
                    if master_list[1][3]!='NIL':
                        pr_printing[3]=master_list[1][3]
                    if master_list[1][2] != 'NIL':
                        pr_printing[4]=master_list[1][2]
                # print(bs1,bs2,bs3,lemme[1])
                #if(bs3[0]=="JALR"):
                #    exit()
                if bs3[0] == "SB" or bs3[0] == "JAL" or bs3[0] == "JALR":
                    
                    if lemme[1]!=bs2:
                        flag=bs2
                        if bs3[0]=="JAL" or bs3[0]=="JALR":
                            count+=1
                        if bs3[0]=="SB" and lemme[1]!=-1:
                            if (changer[1] in b_hist.keys()) and b_hist[changer[1]]==1:
                                # print("enter1")
                                count+=1
                                update_bht(changer[1],0,-1)
                            elif (changer[1] in b_hist.keys()) and b_hist[changer[1]]==0 :
                                # print("enter2")
                                count+=1
                                update_bht(changer[1],1,-1)
                        #print("prediction is not correct")
                        # print(b_hist,changer[1],btb)
                    else:
                        print()
                        #count+=1
                        #nextflagMM+=1

            window.tableWidget.setItem(k+t,stat1-1,QTableWidgetItem("Fetch"))
            if app_flag==1:
                k=k+1
                app_flag=0    
            changer[1]=changer[0]
            returnlist = detect_data_hazard()
            # print(master_list[1])
            insert_carr()
            #if lemme[0]!=-1:
            #    master_list[0][8]=lemme[0]
            #lemme[1]=lemme[0]
            if flag!=0:
                stat12+=1
                master_list.pop(1)
                master_list.insert(1,['NIL','NIL','NIL','NIL','NIL','NIL','NIL',-2,'NIL','NIL'])
                master_list[0][8]=flag
                flag=0
            
            
            #print(returnlist)
            if(returnlist[0]!=-1):
                # print("DATA HAZARD DETECTED, forwarding case ,",returnlist)
                stat11+=1
            #else:
            #    insert_carr()
                if (returnlist[0][0]=='E'and returnlist[0][1]=='E'):  # case- E to E
                    # print("data forwarding done for",master_list[1][9],"\nreg[x",pr_exe[1],"] = ",pr_exe[0])
                    nstalling(2)
                    #registers[pr_exe[1]] = pr_exe[0] #writing the value into the register early
                elif (returnlist[0][0]=='M' and returnlist[0][1]=='E'):
                    if(returnlist[0][3]==[3,1]):
                        nstalling(2)
                        nextflagMM+=1
                        # register[pr_mem[1]] = pr_mem[0]
                    elif(returnlist[0][3]==[2,1]):
                        nstalling(2)
                        #nextflagMM=1
                elif (returnlist[0][0]=='M' and returnlist[0][1]=='M'):
                    # print ("enter")
                    nstalling(2)
                elif(returnlist[0][0]=='E' and returnlist[0][1]=='M'):
                    registers[pr_exe[1]] = pr_exe[0]
                    #exit()
                elif (returnlist[0][0]=='E' and returnlist[0][1]=='D'):
                    if(returnlist[0][3]==[2,1]): # 1 cycle stalls
                        #nextflagED=1
                        nstalling(2)
                        #stallflag=1
                        #continue
                    elif(returnlist[0][3]==[3,1]): #no stall required
                        nextflagMM+=1
                        nstalling(2)
                elif (returnlist[0][0]=='M' and returnlist[0][1]=='D' ):
                    if(returnlist[0][3]==[3,1]): # 1 cycle stalls
                        nstalling(2)
                        nextflagMM+=1
                        #stallflag=1
                        #nextflagMD=1
                        #continue
                    elif(returnlist[0][3]==[2,1]): #2 cycle stalls
                        nstalling(2)
                        #nextflagMD=1
                        #stallflag=2
                        #continue
                #write the value in the next cycle because then 
                # (curr)master_list[1] would be ready for M stage and (curr)master_list[2] would have completed M stage
                #nextflagMM=2
            
            # printregisters()
            #insert_carr()
            elapsed = time.time()-start
            if lemme[0]!=-1:
                master_list[0][8]=lemme[0]
            lemme[1]=lemme[0]
        print_pipelined(pr_fd,pr_de,pr_em,pr_mw,knob4,stat1)
        printregisters(knob3,stat1)
        if master_list[4][8] != 'NIL' and int(master_list[4][8],2)==knob5*4:
            printknob5(pr_printing,knob5)
    if(elapsed > 30):
        print("Something is wrong, program took too long too execute, might be an infinite loop")
    stat12=count
    stat10=stat12
    stat3=(stat1-1)/stat2
    stat7=stat11+stat12
    #stat8=int(stat11/2)
    stat8=nextflagMM
    stat9=stat6
    stat5+=stat2-stat6
    print("-------Pipelined Execution with DF disabled-----")
    print("1.  Total Number of cycles taken\t:",stat1-1)
    print("2.  total instructions executed\t\t:",stat2)
    print("3.  Cycle Per Instruction (CPI)\t\t:",stat3)
    print("4.  Number of Data-transfer inst\t:",stat4)
    print("5.  number of ALU inst. executed\t:",stat5)
    print("6.  Number of control inst. executed\t:",stat6)
    print("7.  Number of stalls in the pipeline\t:",stat7)
    print("8.  Number of data hazards\t\t:",stat8)
    print("9.  Number of Branch hazards\t\t:",stat12)
    print("10. Number of branch mispredictions\t:",stat10)
    print("11. No. of stalls due to data hazards\t:",stat11)
    print("12. No. of stalls due to control hazards:",stat12)
    myfile.write("---------Pipelined Execution with DF disabled-------\n"+"STATS OF THE PROGRAM\n1.  Total Number of cycles taken\t\t: "+str(stat1-1)+"\n2.  total instructions executed\t\t\t: "+str(stat2)+"\n3.  Cycle Per Instruction (CPI)\t\t\t: "+str(stat3)+"\n4.  Number of Data-transfer inst\t\t: "+str(stat4)+"\n5.  number of ALU inst. executed\t\t: "+str(stat5)+"\n6.  Number of control inst. executed\t: "+str(stat6)+"\n7.  Number of stalls in the pipeline\t: "+str(stat7)+"\n8.  Number of data hazards\t\t\t\t: "+str(stat8)+"\n9.  Number of Branch hazards\t\t\t: "+str(stat12)+"\n10. Number of branch mispredictions\t\t: "+str(stat10)+"\n11. No. of stalls due to data hazards\t: "+str(stat11)+"\n12. No. of stalls due to control hazards: "+str(stat12))
    # print(nextflagMM)
    # print(count)

#while(i<976):
#    step()
#    i=i+1
class Window(QWidget):
    def __init__(self):
        super().__init__()
 
        self.title = "Phase3 Block Diagram"
        self.top = 100
        self.left = 100
        self.width = 1500
        self.height = 800
        self.tableWidget=QTableWidget()
 
        self.InitWindow()
 
 
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
 
        self.creatingTables()
 
 
        self.show()
 
    def creatingTables(self):
        #self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(1000)
        self.tableWidget.setColumnCount(1500)
        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.vBoxLayout)
        #self.table.selectRow(j)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)




print("Enter your choice for mode of running the program,\nenter 1 to enable and 0 to disable the following knobs")
knob1 = int(input(">>>\tKNOB 1:: Pipelined Execution (0/1): "))
myfile.write(">>>\tKNOB 1:: Pipelined Execution (0/1): "+ str(knob1))
if(knob1==1):
    knob2 = int(input(">>>\tKNOB 2:: data forwarding    (0/1) : "))
    myfile.write("\n>>>\tKNOB 2:: data forwarding     (0/1): "+str(knob2))
else:
    print(">>>\tKNOB 2:: data forwarding    (0/1):  N.A ")
    myfile.write("\n>>>\tKNOB 2:: data forwarding     (0/1): N.A.")
knob3 = int(input(">>>\tKNOB 3:: Print Registers at the end of each cycle(0/1) : "))
myfile.write("\n>>>\tKNOB 3:: Print Registers at the end of each cycle(0/1) : "+str(knob3))
if(knob1==1):
    knob4 = int(input(">>>\tKNOB 4:: Print Pipelined Registers at the end of each cycle(0/1) : "))
    myfile.write("\n>>>\tKNOB 4:: Print Pipelined Registers at the end of each cycle(0/1) : "+str(knob4))
else:
    print(">>>\tKNOB 4:: Print Pipelined Registers at the end of each cycle(0/1) : N.A.")
    myfile.write("\n>>>\tKNOB 4:: Print Pipelined Registers at the end of each cycle(0/1) : N.A.")
knob5 = int(input(">>>\tKNOB 5:: Print Pipelined Registers for a specific instruction (Enter Instruction Number or enter -1 for not printing) : "))
myfile.write("\n>>>\tKNOB 5:: Print Pipelined Registers for a specific instruction (Enter Instruction Number or enter -1 for not printing) : ")
if(knob1==1):
    myfile.write(str(knob5))
else:
    myfile.write('N.A.')
myfile.write('\n============================================================================================================\nNOTE: ONLY FINAL STATES ARE PRESENT IN THIS FILE. CHECK TERMINAL FOR OUTPUTS AFTER EACH CYCLE IF KNOB ENABLED.\n\n\nSTATS WITH ABOVE KNOB SETTINGS ARE AS FOLLOWS:-\n')    

#knob4 = int(input(">>>\tPrint Pipelined Registers at the end of each cycle(0/1) : "))
#knob5 = int(input(">>>\tPrint Pipelined Registers for a specific instruction (Enter Instruction Number or enter -1 for not printing) : "))
if(knob1==0):
    App = QApplication(sys.argv)
    window = Window()
    run(['NIL','NIL','NIL','NIL','NIL','NIL','NIL',-2,'00000000000000000000000000000000','NIL'])
    sys.exit(App.exec())
    
elif(knob2==0):
    App = QApplication(sys.argv)
    window = Window()
    run_pipelined_without_data_for()
    window.tableWidget.resizeColumnsToContents()
    sys.exit(App.exec())
    print(btb)
    print(b_hist)
elif(knob2==1):
    App = QApplication(sys.argv)
    window = Window()
    run_pipelined_data_for()
    window.tableWidget.resizeColumnsToContents()
    sys.exit(App.exec())
# step()
# print(registers)
myfile.write('\n\n\n\nSCROLL FOR FINAL STATES OF MEMORY AND REGISTERS\n\n\n================================================== REGISTERS ==================================================')
for i in range(32):
    print(registers[i],'\tx',i, ' = ','0x'+(hex(int(registers[i],2))[2::].zfill(8)),sep='')
    if(i<=9):
        myfile.write('\n x'+str(i)+'  = '+'0x'+(hex(int(registers[i],2))[2::].zfill(8)))
    else:
        myfile.write('\n x'+str(i)+' = '+'0x'+(hex(int(registers[i],2))[2::].zfill(8)))

def printDict(dicto,order='asc'):
    j=0
    print('------------------+-------------------+-------------------+-------------------+')
    print('     add    : val |     add     : val |     add     : val |     add     : val |')
    print('------------------+-------------------+-------------------+-------------------+')
    myfile.write('\n----------------+-----------------+-----------------+-----------------+\n    add   : val |    add    : val |    add    : val |    add    : val |\n----------------+-----------------+-----------------+-----------------+\n')
    if(order=='asc'):
        for i in sorted(dicto.keys()):
            j+=1
            print(i,' : ',dicto[i],end=' | ')
            if(j==4):
                j=0
                print('')
        print('---------------------------------------------------------------------------')
        myfile.write('----------------+-----------------+-----------------+-----------------+\n\n')
    else:
        ll=[]
        for i in sorted(dicto.keys(),reverse=True):
            j+=1
            ll.append(i)
            # print(i,': ',dicto[i],end=' | ')
            if(j==4):
                j=0
                for kkk in [3,2,1,0]:
                    print(ll[kkk],' : ',dicto[ll[kkk]],end=' | ')
                    myfile.write(str(ll[kkk]) + ': '+str(dicto[ll[kkk]])+ '  | ')
                ll=[]
                print('')
                myfile.write('\n')
        print('------------------------------------------------------------------------------\n\n')
        myfile.write('----------------+-----------------+-----------------+-----------------+\n\n')
oppo1,oppo2=mem.show_Memory()

# print(stack)
myfile.write('\n\n================================================== MEMORY SEGMENT ==================================================\n NOTE:\n1. All values in following tables are in hex format\n2. Values and address not displayed have a default "00" value\n')
myfile.write('\n                              DATA SEGMENT')

printDict(oppo2,'desc')
myfile.write('\n                             STACK SEGMENT')
printDict(stack,'desc')
myfile.close()