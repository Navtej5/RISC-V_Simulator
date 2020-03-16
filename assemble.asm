.data
check: .word 0x00000001
addrs: .word 0x10000000
.text
lui x3,0x10000 
lb x5,0(x3) 
bne x5,x0,little
addi x10,x10,1
little: addi x10,x10,0

finish: