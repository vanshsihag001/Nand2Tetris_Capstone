(LOOP)
    @KBD
    D=M
    @PRESSED
    D;JNE
    @color          // no key: white
    M=0
    @DRAW
    0;JMP
(PRESSED)
    @color          // key: black
    M=-1
(DRAW)
    @19168
    D=A
    @addr
    M=D             // addr = first word of row 87
    @20
    D=A
    @rows
    M=D             // rows = 20
(ROWLOOP)
    @rows
    D=M
    @LOOP
    D;JLE           // all rows done -> check key again
    @color
    D=M
    @addr
    A=M
    M=D             // word 0
    A=A+1
    M=D             // word 1
    A=A+1
    M=D             // word 2
    A=A+1
    M=D             // word 3 (4 words = 64 px)
    @32
    D=A
    @addr
    M=D+M           // next screen row
    @rows
    M=M-1
    @ROWLOOP
    0;JMP
