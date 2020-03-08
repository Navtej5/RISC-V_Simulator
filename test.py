address=["0x00000000","0x00000001"]

data=["00","00"]
#print(address[0],"00")
#print(address[1],"00")
for x in range(2,400):
	s = '%#010x'%x
	address.append(s)
	data.append("00")
	if(x<100 or x%50==0):
		print(s , "00")
memory = {}
for i in range(len(address)):
	memory[address[i]] =data[i]
#print(memory)