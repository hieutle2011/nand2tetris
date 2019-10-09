// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Initialize variables

  @R0
  D=M
  @a
  M=D

  @R1
  D=M
  @b
  M=D

  @prod
  M=0

  @i
  M=1

// Check if a, b == 0, if true goto STOP0
  @a
  D=M
  @STOP0
  D;JEQ

  @b
  D=M
  @STOP0
  D;JEQ
(LOOP)
  // if i-b>0, goto STOP1
  @b
  D=M
  @i
  D=M-D
  @STOP1
  D;JGT

  // do calculation
  @a
  D=M
  @prod
  M=M+D
  
  @i
  M=M+1
  @LOOP
  0;JMP   

(STOP0)
  @R2
  M=0
  @END
  0; JMP

(STOP1)
  @prod
  D=M
  @R2
  M=D

(END)
  @END
  0; JMP
