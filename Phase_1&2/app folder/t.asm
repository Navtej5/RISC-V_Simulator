.data
var1: .word 1,5,-4,3,7,8,6,12
.text
addi x11,x0,8
addi x4,x0,1
addi x30,x11,0
sub x4,x11,x4
auipc x10,65536
addi x10,x10,-16
jal x1,sort
beq x0,x0,exit
sort:addi x2,x2,-8
sw x1,4(x2)
sw x11,0(x2)
addi x5,x11,-1
addi x7, x0, 0
bge x5,x7,L1
addi x11,x0,1
addi x2,x2,8
jalr x0,x1,0
L1:addi x11,x11,-1
jal x1,sort
lw x11,0(x2)
lw x1,4(x2)
addi x2,x2,8
loop: sub x31,x30,x11
beq x22,x31,L2
add x23,x23,x0
addi x4,x0,2
sll x5,x22,x4
add x5,x5,x10
addi x29,x5,0
lw x9,0(x5)
sub x5,x5,x10
addi x6,x5,4
add x6,x6,x10
lw x13,0(x6)
addi x22,x22,1
blt x9,x13,loop 
sw x9,0(x6)
sw x13,0(x29)
beq x22,x31,L2
bne x22,x31,loop
L2: addi x22,x0,0
jalr x0,x1,0
exit: