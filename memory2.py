def com(ii8,n):
    x = len(ii8)
    if x==n:
        return ii8
    else:
        m = ii8[::-1]
        # i=0
        for y in range(0,n-x):
            m = m + '0'
        m = m[::-1]
        return m


class Memory:
    data=[]
    text=[]
    def add_data_at(self, add, val ):    
        #'''value format yet to be decided---->binary format'''#storing in maybe hex
        x=int(0x10000000)
        y=int(add)
        z=y-x
        if(len(data)<z):
            for i in range(len(data),z):
                self.data.append('00')
        self.data[z]=hex(int(val))[2:]
    
    
    def add_data(self,type,val):
        if(type !='.asciiz'):
            val = val.replace(",",' ')
        arr=val.split(' ')
        myreturnvalue = len(self.data)
        if(type=='.byte'):
            for x in arr:
                if(len(x)>1): ###NO need to convert if passed value is already in hex
                    if(x[0]=='0' and x[1]=='x' and len(x)<=4):
                        y = com(x[2::],2)
                        self.data.append(y)
                    else:
                        if(len(hex(int(x)))<=4):
                            self.data.append(com(hex(int(x))[2::],2))
                        else:
                            print("can't store",x,"in a byte, because value is too large. truncating the value and storing 1 least significant nibble")
                            self.data.append(hex(int(x))[-2:])
                else: #not a hex
                    self.data.append(com(hex(int(x))[2::],2))
        elif(type=='.word'):
            for x in arr:
                if(len(x)>1): ###NO need to convert if passed value is already in hex
                    if(x[0]=='0' and x[1]=='x' and len(x)<=10):
                        y = com(x[2::],8)
                    else: #not hex
                        y=hex(int(x))[2::]
                        if(len(y)<=8):
                            y=com(y,8)
                        else:
                            print("can't store",x ,"in a word, because value is too large. truncating the value and storing 4 least significant bytes")
                            y=y[-8:]
                else: #length <=1
                    y=hex(int(x))[2::]
                    y=com(y,8)
                y1=y[0:2]
                y2=y[2:4]
                y3=y[4:6]
                y4=y[6:8]
                self.data.append(y4)
                self.data.append(y3)
                self.data.append(y2)
                self.data.append(y1)

        elif(type=='.halfword'):
            for x in arr:
                if(len(x)>1): ###NO need to convert if passed value is already in hex
                    if(x[0]=='0' and x[1]=='x' and len(x)<=6):
                        y = com(x[2::],4) 
                    else: # not a hex
                        y=hex(int(x))[2::]
                        if(len(y)<=4):
                            y=com(y,4)
                        else:
                            print("can't store",x,"in a halfword, because value is too large, truncating and storing 2 least significant bytes")
                            y=y[-4:]
                else: #length <=1
                    y=hex(int(x))[2::]
                    y=com(y,4)
                y1=y[0:2]
                y2=y[2:4]
                self.data.append(y2)
                self.data.append(y1)
        elif(type=='.doubleword'): 
            for x in arr:
                if(len(x)>1): ###NO need to convert if passed value is already in hex
                    if(x[0]=='0' and x[1]=='x' and len(x)<=18):
                        y = com(x[2::],16)
                    else:    # not a hex
                        y=str(hex(int(x)))[2:]
                        if(len(y)<=16):
                            y=com(y,16)
                        else:
                            print("couldn't store",x,'in a doubleword, as value is too large, truncating and storing 8 least significant bytes')
                            y=y[-16:]
                else: #length <=1
                    y=str(hex(int(x)))[2:]
                    y=com(y,16)
                y1=y[0:2]
                y2=y[2:4]
                y3=y[4:6]
                y4=y[6:8]
                y5=y[8:10]
                y6=y[10:12]
                y7=y[12:14]
                y8=y[14:16]
                self.data.append(y8)
                self.data.append(y7)
                self.data.append(y6)
                self.data.append(y5)
                self.data.append(y4)
                self.data.append(y3)
                self.data.append(y2)
                self.data.append(y1)
        elif(type=='.asciiz'):
            for x in range(len(val)):
                self.data.append(hex(ord(val[x]))[2::])
                
        #print(val,"stored at =" ,hex(myreturnvalue+268435456))
        #print(self.data)
        return hex(int(myreturnvalue+268435456))
    def get_data_at(self, add ):
        x=int(0x10000000)
        y=int(add)
        z=y-x
        return self.data[z]
    def add_text(self, val):
        self.text.append(val)
    
    def show_Memory(self):
        # print("data segment---------------------------------------------------------------------------------------------------------\n",self.data)
        data_out=[]
        for x in range(len(self.data)):
            # print(hex(268435456 + x)," ",self.data[x])
            data_out.append( str(hex(268435456 + x))+ " : " + str(self.data[x]) )
        # print("text segment"+"("+str(len(self.text))+")","---------------------------------------------------------------------------------------------------------\n", self.text,"\n\n")
        return data_out




#0x10000000
