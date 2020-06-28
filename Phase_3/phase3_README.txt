+-----------------------------------------------------------------------------------------------------------------------------------------------+
|																	 	|
|							COMPUTER ARCHITECTURE(CS204)								|
|																		|
|							Course Project: RISC-V SIMULATOR							|
|									(PHASE 3)								|	
+-----------------------------------------------------------------------------------------------------------------------------------------------+

Project made under the guidance of:
Dr. T.V.Kalyan
kalyantv@iitrpr.ac.in
IIT ROPAR

Group Members:

Navtejpreet Singh	(2018csb1107) - Worked on Detecting Data-Hazards & determining Data Forwarding paths, pipelined RUN func. WITH DATA Forwarding(including stats), Branch prediction, writing Output.txt, Debugging.
Samreet Singh Dhami	(2018csb1120) - Worked on RUN function for 5-stage pipeline WITHOUT Data forwarding(including stats) and GUI using pyQT5, Debugging, Branch Prediction.
Mohit Rajoria		(2018csb1104) - Worked on Control Hazards and splitting functions into 5 stages, pipeline registers, knobs related work.
Mohit Shinde		(2018csb1103) - Worked on Control hazards and splitting functions into 5 stages and BTB and BHT creation.
Daksh Sharma		(2018csb1082) - Worked on flushing logic in misprediction and run, Branch Prediction debugging.

-----------------------------------------------------------------------------------------------------------------------------------------------

For Phase-3 pipeline was introduced to the risc-v simulator. 

1. Input code has to be given in a file named "t.asm" with guidlines similar to earlier file
	QUICK REMINDERS:
	(Each Label must correspond to some instruction.)
	(Labels must be followed with some instruction.)
	(no blank lines in the input code)

2. Improvement was made in phase 2 by shifting our memory segment from being as a list to a dictionary for easier reference.

3. An optimization was introduced, Branch Decision logic was moved from E to D stage.

4. Knobs are were introduced for toggle run mode, before each run.

5. Output from phase1 is in out.mc and outfile.mc similar to previous versions.

6. output from phase3 file is contained in Output.txt file which has: 
	- the information about knob settings selected.
	- final values of registers.
	- final values of Memory segment
	{ NOTE: all values are displayed in hex format
		Only values explicity declared during run-time or non-zero values are displayed
		values not displayed have default value of zero.}

7. GUI was made phase3 specific, which has a table with cycles increasing towards right and corresponding instructions listed vertically.
	# For NON-PIPELINED RUN
		- each instruction takes 5 cycles. eg. is attached as run.jpg
		- vertically listed instructions denote the order in which there executed.
	# For Pipelined RUN WITH DATA-FORWARDING
		- highlighted instruction(Blue colour) represent the instructions detecting DATA HAZARD.
		- these highlighted instructions detect data hazard just after decode stage, thus type of Data forwarding required for resolving it is also listed in the same cell.
		- data hazard are mentioned in decode cell as a list in format ['V','W',X,[Y,1]],
			
			-- where 'V'(Stage whose pipeline registers has the required value) and 'W'(Stage in which the value is needed for proper execution) i.e. path 'V'->'W'.
			   'V','W' can be 'D'(Decode) or 'E'(Execute) or 'M'(Mem_access) stages
			
			-- where [Y,Z] denotes the index instruction from whose 'V' stage value is needed and 1 denotes the index of instruction which required the forwarding.
			1 denotes required current instruction( the one whose decode just completed)
			2 denotes instruction whose Execute is completed
			3 denotes instruction whose Mem_access is completed
			
			-- where X (1 or 2 or 12) denotes if dependency is with (rs1 or rs2 or both).

			-- these dataforwarding path Format ['V','W',X,[Y,1]] stalls and forward path according to various possible cases.		
	
		- if it has multiple dependencies, multiple lists are mentioned in the above format.
		- In case of Misprediction the wrong steps are coloured RED.
	# For Pipelined RUN WITHOUT DATA-FORWARDING
		- Table is drawn in similar fashion without DATA FORWARDING PATHS.
		- Only the correct instructions are displayed in this.

8. Stats were printed accordingly.

NOTE: 
All load and store were counted as Data-Transfer instructions.
All R-format,I-format,S-format,U-format,UJ-format were counted in ALU - instructions.
All SB-format and Jal and Jalr instructions were counted as Control Instructions.

