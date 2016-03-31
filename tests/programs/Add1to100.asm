// Adds numbers from 1 until 100: 1 + 2 + ... + 99 + 100.

@i      // variable 'i', refers to some RAM location
M=1
@sum    // variable 'sum', refers to some RAM location
M=0

(LOOP)
    @i
    D=M     // D = i
    
    @100
    D=D-A   // D = i - 100
    @END
    D;JGT   // JUMP to END if i > 100
    
    @i
    D=M     // D = i
    
    @sum
    M=D+M   // sum = sum + i
    
    @i
    M=M+1   // i = i + 1
    
    @LOOP
    0;JMP   // Goto LOOP

(END)
    @END
    0;JMP   // End of program infinite loop

