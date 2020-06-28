.data
STRING: .asciiz "Hansin Ahuja"
.text
lui x13,0x10000
jal x10, capitalize
beq x0, x0, exit
capitalize:
addi x1, x13, 0
addi x3,x0,97
addi x4,x0, 123


loop:
lb x2, 0(x1)
beq x2, x0, return
blt x2, x3, continue
bge x2, x4, continue
addi x2, x2, -32
sb x2,0(x1)
continue: addi x1, x1, 1
beq x0, x0, loop
return: jalr x0, 0(x10)
exit: