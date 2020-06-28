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
        add = hex(add).zfill(8)
        self.data[add] = hex(int(val, 2)).replace('0x', '').zfill(2)
        # x=int(0x10000000)
        # y=int(add)
        # z=y-x
        # if(len(self.data)<z and z<536000000):
        #     for i in range(len(self.data),z+1):
        #         self.data.append('00')
        # # print(int(val,2))
        # if(z<536000000):
        #     self.data[z]=hex(int(val,2))[2:].zfill(2)
        # else:
        #     ss = 2147483632-y
        #     if(len(stack)<ss):
        #         self.stack.append('00')
        # print("finished storing",self.data[z])

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


mo = Memory()
# mo.add_data_at(268435456, '00001111')
# mo.add_data('.dword', '12 -2 0xffa')
mo.add_data('.asciiz','Hello World')
# mo.get_data_at(268435460)
mo.show_Memory()
