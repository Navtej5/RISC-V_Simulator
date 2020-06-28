+-----------------------------------------------------------------------------------------------------------------------+
|															|
|					Computer Architecture (CS204)							|
|															|
|				    COURSE PROJECT : PHASE 1 and PHASE 2						|
|															|
+-----------------------------------------------------------------------------------------------------------------------+

Project made under the guidance of:
Dr. T.V.Kalyan
kalyantv@iitrpr.ac.in
IIT ROPAR

Group Members:
Navtejpreet Singh	(2018csb1107) - Worked on making .mc files, handling directives and modification of all files for overall compatibily of simulator.
Samreet Singh Dhami	(2018csb1120) - Worked on GUI using PyQt5, integrating all files for smooth functioning in the gui.
Daksh Sharma		(2018csb1082) - Worked on bulding dictionaries for necessacy convertion to machine code and error handling of reader file.
Mohit Shinde		(2018csb1103) - Worked on decode and execute of instruction for phase 2.
Mohit Rajoria		(2018csb1104) - Worked on memory and phase 2 decode and execution.

--------------------------------------------------------------------------------------------------------------------------

A Risc-V simulator was created using Python Programming Language. The simulator expects user to enter the assembly code in a certain format in the GUI:

	(1.)	All directives keywords are case sensitive and MUST contain all small alphabets (a-z)
		eg. .data, .text, .byte, .word, .halfword, .doubleword, .asciiz
	(2.)	All label directives for branch and jump instructions are also CASE SENSITIVE.
	(3.)	Any labels for branching must be followed with some instruction.(exception last one)
	(4.)	DO NOT Leave blank lines between instructions.	
	(5.)	Comments are NOT supported in this program.
	(6.)	jalr,store and load instructions can be in any of the following two formats:
		jalr  x19,0(x1) or  jalr x19,x9,0
		sw x1,0(x2) or sw x1,x2,0
		lb x1,0(x2) or lb x1,x2,0
	(7.)	Instructions can have comma(,) or space separated arguments.
	(8.)	Most of the errors and messages during run-time are displayed in the console/terminal keep checking them.
	(9.)	Program assumes that if user enters a hexadecimal value it should be in correct format
		Only a zero(0) followed by a small aplhabet 'x'(without '') is valid. (0xhhhh , where h is any valid hexadecimal character)
		Should not contain unrecognized charachter i.e. any VALID HEXADECIMAL CHARACTER may contain any digit(0 to 9) or small alphabet a to f(inclusive) only.
	

Other Instructions for decode, execution and gui app will follow this. 
GUI(using PyQt5)- Run the app.py file(on the terminal or directly), then a window will appear.(Make sure you have PyQt5     installed on your system)

	GUI(using PyQt5)- Run the app.py file(on the terminal or directly), then a window will appear. (Make sure you have PyQt5 installed on your system)

	(1.)	The App contains two tabs - Editor and Simulator
	(2.)	Editor Tab: It contains a text editor with save, open and clear option. The code should be written in the format described above. After the code is written, press the check 		button to see if the code is correct or not. If it is correct, then “No Error” will flash, then you can move to simulator tab
	(3.)	Simulator Tab: If the code is correct, then click the ‘assemble’ button and a Table will be generated with columns(‘PC’,’Machine code’,’Basic Code’,’Original Code’).
	(4.)	There are options of 
			‘Run’: Running full code at once
			‘Step’: Run only the next instruction at once
			‘Reset’: Reset the code
			‘Stop’

	(5.)	Second Half of the simulator Tab contains tables of registers(with the option in viewing in hex, decimal, ascii) and memory (data, text, heap, stack)
