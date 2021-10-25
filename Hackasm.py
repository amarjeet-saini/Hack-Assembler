import sys

def cleanUp(fhandle):
    '''
    input : assumes valid input file handle give
    removes whitespace and comment from input HACK assembly program 
    modification written in temp file
    return : None
    '''
    fhandle1 = open('temp.asm','w')
    
    for line in fhandle:
        line = line.rstrip() 
        condn = False # assu
        instruction = [] #
        k = 0
        # iterate over each instruction
        for i in range(len(line)):
            # comment in instruction skip and nxt instr
            if i < len(line) -1 and line[i:i+2] == '//':
                break
                
            # white space present in instruction we skip, not adding to list
            if line[i] == ' ':
                continue
            
            instruction.append(line[i])
            condn = True

        if condn:
            s = ''.join(instruction)+"\n"
            fhandle1.write(s)
    fhandle1.close() 

symbolTable = {
    # initialization with pre-defined symbols
    'SP'    :   0, 
    'LCL'   :   1,
    'ARG'   :   2,
    'THIS'  :   3,
    'THAT'  :   4,
    'R0'    :   0,
    'R1'    :   1,
    'R2'    :   2,
    'R3'    :   3,
    'R4'    :   4,
    'R5'    :   5,
    'R6'    :   6,
    'R7'    :   7,
    'R8'    :   8,
    'R9'    :   9,
    'R1O'   :   10,
    'R11'   :   11,
    'R12'   :   12,
    'R13'   :   13,
    'R14'   :   14,
    'R15'   :   15,
    'SCREEN':   16384,
    'KBD'   :   24576
}

def passOne():
    '''
    handle symbollic inst present by parsing entire asm code
    modify symbol table 
    input: file handle assumes fhandle correctly supplied
    return: None
    '''
    try:
        fhandle1 = open('temp.asm')
    except IOError:
        print('cant open the file')
    
    count = 0   # track of instruction
    
    for line in fhandle1:
        # a-inst symbol table
        found = False
        # a-instruction and contain symbol in inst
        if line[0] == '@' and not(line[1:-1].isdigit()):
            # add all symbol to dict with key as -1
            for key in symbolTable:
                if line[1:-1] == key:
                    found = True
            if found == False:
                symbolTable[line[1:-1]] = -1
        # resolve is (xxx)
        if line[0] == '(':
            # check label already present
            present = False
            for key in symbolTable:
                if line[1:-2] == key:
                    symbolTable[key] = count
                    present = True
            if not present:
                symbolTable[line[1:-2]] = count 
            continue
        count = count + 1
    
    fhandle1.close()

def addAddrOfVar():
    '''
    modify symbol table by adding addr of variable 
    R0-R15 predefined , start from 16
    input : return : None
    '''
    start = 16
    for k in symbolTable:
        if symbolTable[k] == -1:
            symbolTable[k] = start
            start = start + 1

def passTwo():
    '''
    modify inst @ xxx with a number using symbol table 
    file2 writing modified with instruction
    '''
    # file 1 read
    try:
        fhandle1 = open('temp.asm')
    except IOError:
        print('cant open the file temp')
    
    # file 2 write
    try:
        fhandle2 = open('temp1.asm','w')
    except IOError:
        print('cant open the file temp1')

    for line in fhandle1:
        # replace @ xx with @ value
        line = line.rstrip()
        inst = ['@',0]
        modify = False
        if line[0] == '@' and not(line[1:2].isdigit()):
            for key in symbolTable:
                if line[1:] == key:
                    inst[1] = str(symbolTable[key])
                    modify = True
                    break
        if line[0] != '(':
            if modify == False:
                s = line + "\n"
            else:
                s = ''.join(inst) + "\n"
            fhandle2.write(s)

    fhandle1.close()
    fhandle2.close()

def convt2bin(n):
    '''
    input: int 
    return: 15 bit value of n
    '''
    res = format(n, "015b")
    return res

def getCompCode(inpComp):
    '''
    input: computation symbol i.e c-instructioon : destn = comp; jump
    return: 7 bit value format ac1c2c3c4c5c6
    '''
    if (inpComp == "0"): return "0101010"
    if (inpComp == "1"): return "0111111"
    if (inpComp == "-1"): return "0111010"
    if (inpComp == "D"): return "0001100"
    if (inpComp == "A"): return "0110000"
    if (inpComp == "M"): return "1110000"
    if (inpComp == "!D"): return "0001101"
    if (inpComp == "!A"): return "0110001"
    if (inpComp == "!M"): return "1110001"
    if (inpComp == "-D"): return "0001111"
    if (inpComp == "-A"): return "0110011"
    if (inpComp == "-M"): return "1110011"
    if (inpComp == "D+1"): return "0011111"
    if (inpComp == "A+1"): return "0110111"
    if (inpComp == "M+1"): return "1110111"
    if (inpComp == "D-1"): return "0001110"
    if (inpComp == "A-1"): return "0110010"
    if (inpComp == "M-1"): return "1110010"
    if (inpComp == "D+A"): return "0000010"
    if (inpComp == "D+M"): return "1000010"
    if (inpComp == "D-A"): return "0010011"
    if (inpComp == "D-M"): return "1010011"
    if (inpComp == "A-D"): return "0000111"
    if (inpComp == "M-D"): return "1000111"
    if (inpComp == "D&A"): return "0000000"
    if (inpComp == "D&M"): return "1000000"
    if (inpComp == "D|A"): return "0010101"
    if (inpComp == "D|M"): return "1010101"

def getDestnCode(inpDestn):
    '''
    input: destn symbol i.e destn = comp; jump
    return: 3 bit value format d1d2d3
    '''
    if (inpDestn == ""): return "000"
    if (inpDestn == "M"): return "001"
    if (inpDestn == "D"): return "010"
    if (inpDestn == "MD"): return "011"
    if (inpDestn == "A"): return "100"
    if (inpDestn == "AM"): return "101"
    if (inpDestn == "AD"): return "110"
    if (inpDestn == "AMD"): return "111"

def getJumpCode(inpJump):
    '''
    input: jump symbol i.e destn = comp; jump
    return: 3 bit value format j1j2j3
    '''
    if (inpJump == ""): return "000"
    if (inpJump == "JGT"): return "001"
    if (inpJump == "JEQ"): return "010"
    if (inpJump == "JGE"): return "011"
    if (inpJump == "JLT"): return "100"
    if (inpJump == "JNE"): return "101"
    if (inpJump == "JLE"): return "110"
    if (inpJump == "JMP"): return "111"

def passThree(fname):
    '''
    read file with no symbols (.asm file) and write machine code into  .hack file
    input : fname org file for name of output file
    return : None
    '''
    OutFile = fname[:fname.find('.')] + '.hack'
    
    try:
        fhandle1 = open('temp1.asm')
    except IOError:
        print('cant open the file temp1')

    try:
        fhandle2 = open(OutFile,'a')
    except IOError:
        print('cant open the file out')
    
    for line in fhandle1:
        line = line.rstrip()
        inst = [0] * 15
        # handle a-type inst
        if line[0] == '@':
            inst[:] = convt2bin(int(line[1:]))
            s = "0" + ''.join(inst) + "\n"
        
        # handle c-type inst
        else:
            dest_b = ''
            comp_b = ''
            jump_b = ''
            cp = len(line)
            eq = 0
            for i in range(len(line)):
                if line[i] == '=':
                    eq = i
                if line[i] == ';':
                    cp = i

            dest_b = getDestnCode(line[:eq])
            
            # handle cases with destn and no destn
            if eq == 0:
                # format : 0;JMP (no destn)
                comp_b = getCompCode(line[eq: cp])
            else :
                # format : dest = comp; jmp
                comp_b = getCompCode(line[eq+1 : cp])
            
            # handle cases with jump and no jump
            if cp == len(line):
                # format : MD=M-1
                jump_b = getJumpCode(line[cp:])
            else:
                # format : 0;JMP
                jump_b = getJumpCode(line[cp+1:])

            s = "111" + comp_b + dest_b + jump_b + "\n"

        fhandle2.write(s)
    
    fhandle1.close()
    fhandle2.close()


def main(argv):
    
    try:
        fhandle = open(argv[1],'r+')
    except IOError:
        print('cant open the file')
    
    cleanUp(fhandle)
    passOne()
    addAddrOfVar()
    passTwo()
    passThree(argv[1])

if __name__ == "__main__":
    main(sys.argv)
