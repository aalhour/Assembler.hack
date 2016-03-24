# ASSEMBLER.HACK

Assembler.hack is a 16-bit machine language assembler for the 16-bit Hack Assembly Language. This was done as part of building a complete 16-bit computer from the grounds up through the book, and [MOOC](https://www.coursera.org/learn/build-a-computer/), *Elementes of Computing Systems*, which is informally known as [nand2tetris](http://www.nand2tetris.org). Hack is also the name of the computer.

## DESCRIPTION

Assembler.hack takes a program source file written in the Hack Assembly Language (see: introduction below), with the file extension *.asm*, and then assembles it into binary machine code (Hack Machine Language), the assembled machine code program is then written to a new file with the same name but with the extension *.hack*.

The Assembler is implemented as a Two-Passes or Two-Stages assembler. The first pass scans the whole program and registers symbols in the symbol table. The second pass scans the whole program again substituting the symbols with their respective addresses in the symbol table, in addition to generating binary machine code and writing the resulting assembled machine code to a new file.

Source code is organized into several components, the decisions for their names, interfaces and APIs were already specified in the book as sort of an specification-implementation contract, however, all components reside in the *Assembler* directory as follows:

  1. **Assebmler.py**: Main module. Implements the two passes and glues the other components together.
  2. **Parser.py**: Simple Parser. Parses the instructions by looking ahead 1 or 2 characters to determine their types and structure.
  3. **Lex.py**: Simple Lexer. Used in Parser. Breaks an instruction to smaller parts and extract its different even smaller parts if it's a C-Instruction.
  4. **Code.py**: Generates binary machine code for instructions. For C-Instructions, it generates machine code for its parts and then combines them altogether together.
  5. **SymbolTable.py**: Implements the symbol table interface which is necessary for registering symbols (address values, labels and variables) and looking up their memory addresses.

How to use:

```bash
$ ./Assembler.py HelloWorld.asm
```

#### Requirements

  * Python 3.5.1

## INTRO TO THE HACK ASSEMBLY LANGUAGE

The Hack Assembly Language is minimal, it mainly consists of 2 types of instructions. It ignores whitespace and allows the program to declare symbols with a single symbol declaration instruction. Symbols can either be labels or variables. It also allows the programmer to write comments in the source code, for example: `// this is a single line comment`. 

If you cannot contain your excitement then head over to the [tests](tests/) directory and check out the testing programs, *\*.asm* for the assembly language programs, and *\*.hack* for their equivalent binary machine code programs.
 
### Predefined Symbols

  * **A**: Address Register.
  * **D**: Data Register.
  * **M**: Refers to the register in Main Memory whose address is currently stored in **A**.
  * **SP**: RAM address 0.
  * **LCL**: RAM address 1.
  * **ARG**: RAM address 2.
  * **THIS**: RAM address 3.
  * **THAT**: RAM address 4.
  * **R0**-**R15**: Addresses of 16 registers that are mapped with addresses 0 to 15.
  * **SCREEN**: Base address of the Screen Map in Main Memory, which is equal to 16384.
  * **KBD**: Keyboard Register Address in Main Memory, which is equal to 24576. 

### Types of Instructions:

  1. A-Instructions: Addressing instructions.
  2. C-Instructions: Computation instructions.

#### A-INSTRUCTIONS:

##### Symbolic Syntax:

`@value`, where value is either a decimal non-negative number or a SYMBOL. 

Examples:
  * `@21`
  * `@SCREEN` 

##### Binary Syntax:

`0xxxxxxxxxxxxxxx`, where `x` is a bit, either 0 or 1. A-Instructions always have their MSB set to 0.

Example:
  * `000000000001010`
  * `011111111111111`

##### Effects:

Sets the contents of the **A** register to the specified value. The value is either a non-negative number (i.e. 21) or a Symbol. If the value is a symbol then the contents of the **A** register becomes the value that SYMBOL refers to but not the actual data in that SYMBOL register/location.

#### C-INSTRUCTIONS:

##### Symbolic Syntax:

*dest* = *comp* ; *jmp*, where:

  1. *dest*: Destination register in which the result of computation will be stored.
  2. *comp*: Computation code.
  3. *jmp*: The jump directive.

Examples:
  * `D=0`
  * `D=D+1`
  * `M=M-D`

##### Binary Syntax: 

`1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3`, where:

  * `111`: C-Instructions always begin with bits `111`.
  * `a` bit: Chooses to load the contents of either **A** register or **M** (Main Memory register addressed by **A**) into the ALU for computation.
  * Bits `c1` through `c6`: Control bits expected by the ALU to perform the arithmetic or bit-wise logical operation.
  * Bits `d1` through `d3`: Specify which memory location to store result into: **A**, **D** or **M**.
  * Bits `j1` through `j3`: Specify which JUMP directive for execute.

##### Effects:

Performs a computation on the CPU (arithmetic or bit-wise logical) and stores it into a destination register, and then, optionally, JUMPS into an instruction memory location that is usually addressed by a label (SYMBOL).

##### Reference:

![C-Instructions Reference](assets/c_instructions_reference.png "C-Instructions Reference")

## LICENSE

This project is licensed under the [MIT License](LICENSE).

