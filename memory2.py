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
        arr=val.split(' ')
        myreturnvalue = len(self.data)
        if(type=='.byte'):
            for x in arr:
                if(len(x)>1): ###NO need to convert if passed value is already in hex
                    if(x[0]=='0' and x[1]=='x'):
                        y = com(x[2::],2)
                        self.data.append(y)
                    else:
                        self.data.append(hex(int(x))[2::])
                else: #not a hex
                    self.data.append(hex(int(x))[2::])
        elif(type=='.word'):
            for x in arr:
                if(len(x)>1): ###NO need to convert if passed value is already in hex
                    if(x[0]=='0' and x[1]=='x'):
                        y = com(x[2::],8)
                    else: #not hex
                        y=hex(int(x))[2::]
                        y=com(y,8)
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
                    if(x[0]=='0' and x[1]=='x'):
                        y = com(x[2::],4) 
                    else: # not a hex
                        y=hex(int(x))[2::]
                        y=com(y,4)
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
                    if(x[0]=='0' and x[1]=='x'):
                        y = com(x[2::],16)
                    else:    # not a hex
                        y=str(hex(int(x)))[2:]
                        y=com(y,16)
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
        print("data segment---------------------------------------------------------------------------------------------------------\n", self.data,"\n\n")
        print("text segment"+"("+str(len(self.text))+")","---------------------------------------------------------------------------------------------------------\n", self.text,"\n\n")




#0x10000000
