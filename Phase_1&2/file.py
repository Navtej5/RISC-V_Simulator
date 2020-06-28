# from reader import Memory
s = "Hello ya'all : #how are you ? "
print("FILE.PY RUNNING NOW-------------------------------------------")
# print(int('0xFF',16))
# x,n=3,1
# print(x,bin(x))
# print('000000000*000050000*000050000*0*00500005')
# p = bin(x).replace('0b','').zfill(4)
# if(x<0):

# print(p)
# n = 9

# rep =bin(-6 & 0xffffffff).replace('0b','').zfill(32)
# print(bin(-6 & 0xffffffff).replace('0b','').zfill(32))
# for _ in range(n):
#     rep = ('0' + rep)[:32]
#     print(rep)


# def extractsignedvalue(binstring, n):
#     if(len(binstring) == n):
#         if(binstring[0] == '0'):
#             return int(binstring, 2)
#         else:
#             return int(binstring, 2)-2**(n)
#     else:
#         return int(binstring, 2)
# def converttosignedvalue(number,n): #decimal number in number and decimal unit in n
#     pop = -1
#     if(n==12):
#         pop = 0xfff
#     elif(n==4):
#         pop=0xf
#     elif(n==20):
#         pop = 0xfffff
#     elif( n ==32):
#         pop = 0xffffffff
#     # print(pop)
#     # print(number)
#     ans = bin( number & pop).replace("0b",'').zfill(n)
#     print(number,ans,"answer",hex(pop))
#     if(number<(-1)*(2**(3)) or number>2**3 - 1):
#         print("error: value overflow!!!!!!!!!!!!!!!!!!!")
#     # elif(number >0 and ans[0]!='0'):
#     #     print("error: value overflow")
#     # else:
#     return ans
# print(extractsignedvalue(bin(int('0xff',16))[2::],8))
# print(converttosignedvalue(int('0xff',16),4))
# print(converttosignedvalue(7,4))
# print(,extractsignedvalue('1100', 32))
# print(bin(8),)
print(hex(12).zfill(5))
print('0x'+(hex(268435456)[2::].zfill(8)))