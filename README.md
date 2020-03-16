# Assembler.hack

Assembler.hack is a 16-bit machine language assembler for the 16-bit Hack Assembly Language. This was done as part of building a complete 16-bit computer from the grounds up through the book, and [MOOC](https://www.coursera.org/learn/build-a-computer/), *Elementes of Computing Systems*, which is informally known as [nand2tetris](http://www.nand2tetris.org). Hack is also the name of the computer.

## Contents

- [Description](#description)
- [Example Usage](#example-usage)
- [Intro to Hack Assembly](#intro-to-hack-assembly)
  - [Predefined Symbols](#predefined-symbols)
  - [Types of Instructions](#types-of-instructions)
    - [A-INSTRUCTIONS](#a-instructions)
    - [L-INSTRUCTIONS](#l-instructions)
    - [C-INSTRUCTIONS](#c-instructions)
- [References](#references)
  - [Computer Architecture](#computer-architecture)
  - [C-Instructions Reference](#c-instructions-reference)

## Description

Assembler.hack takes a program source code file written in the Hack Assembly Language (see: intro section below), which is a *.asm* text file, and then assembles it into binary machine code (Hack Machine Language). The assembled machine code program is then written to a new *.hack* text file with the same name.

The Assembling process is implemented in two passes. The first pass scans the whole program, registering the labels only in the Symbol Table. The second pass scans the whole program again, registering all variables in the Symbol Table, substituting the symbols with their respective memory and/or instruction addresses from the Symbol Table, generating binary machine code and then writing the assembled machine code to the new *.hack* text file.

Source code is organized into several components, the decisions for their names, interfaces and APIs were already specified in the book as sort of a specification-implementation contract. All components of the Assembler reside in the **/Assembler** directory, as follows:

1. **Assembler.py**: Main module. Implements the two passes and glues the other components together.
2. **Parser.py**: Simple Parser. Parses the instructions by looking ahead 1 or 2 characters to determine their types and structures.
3. **Lex.py**: A simple Lexer which is used by the Parser to break an instruction to smaller parts and sturcture it in a way that makes it easy to convert it to machine code.
4. **Code.py**: Generates binary machine code for instructions. For C-Instructions, it generates machine code for its constituting parts and then merges them back altogether.
5. **SymbolTable.py**: Implements a lookup table which is used to register symbols (labels and variables) and look up their memory addresses.

## Example Usage

*Note: You might need to read the [Intro to Hack Assembly](#intro-to-hack-assembly) section below to understand the instructions in Max.asm source code.*

```bash
$ python Assembler.py Max.asm
```

### Max.asm

```asm
// Given two numbers stored in the registers R0 and R1,
// compute the maximum between them and store it in the R2 register.

  @R0
  D=M              // D = first number
  @R1
  D=D-M            // D = first number - second number
  @OUTPUT_FIRST
  D;JGT            // if D>0 (first is greater) goto output_first
  @R1
  D=M              // D = second number
  @OUTPUT_D
  0;JMP            // goto output_d

(OUTPUT_FIRST)
  @R0
  D=M              // D = first number

(OUTPUT_D)
  @R2
  M=D              // M[2] = D (greatest number)

(INFINITE_LOOP)
  @INFINITE_LOOP
  0;JMP            // infinite loop
```

### Max.hack

```binary
0000000000000000
1111110000010000
0000000000000001
1111010011010000
0000000000001010
1110001100000001
0000000000000001
1111110000010000
0000000000001100
1110101010000111
0000000000000000
1111110000010000
0000000000000010
1110001100001000
0000000000001110
1110101010000111
```

## Intro to Hack Assembly

The Hack Assembly Language is minimal, it mainly consists of 3 types of instructions. It ignores whitespace and allows programs to declare symbols with a single symbol declaration instruction. Symbols can either be labels or variables. It also allows the programmer to write comments in the source code, for example: `// this is a single line comment`.

If you cannot contain your excitement then head over to the [tests](tests/) directory and check out the testing programs, **.asm** files contain programs written in the Hack Assembly Language, and **.hack** files contain their equivalent binary machine code programs (Hack Machine Language).

### Predefined Symbols

- **A**: Address Register.
- **D**: Data Register.
- **M**: Refers to the register in Main Memory whose address is currently stored in **A**.
- **SP**: RAM address 0.
- **LCL**: RAM address 1.
- **ARG**: RAM address 2.
- **THIS**: RAM address 3.
- **THAT**: RAM address 4.
- **R0**-**R15**: Addresses of 16 RAM Registers, mapped from 0 to 15.
- **SCREEN**: Base address of the Screen Map in Main Memory, which is equal to 16384.
- **KBD**: Keyboard Register address in Main Memory, which is equal to 24576.

### Types of Instructions

1. A-Instruction: Addressing instructions.
2. C-Instruction: Computation instructions.
3. L-Instruction: Labels (Symbols) declaration instructions.

#### A-INSTRUCTIONS

##### Symbolic Syntax of an A-Instruction

`@value`, where value is either a decimal non-negative number or a Symbol.

Examples:

- `@21`
- `@R0`
- `@SCREEN`

##### Binary Syntax of an A-Instruction

`0xxxxxxxxxxxxxxx`, where `x` is a bit, either 0 or 1. A-Instructions always have their MSB set to 0.

Examples:

- `000000000001010`
- `011111111111111`

##### Effects of an A-Instruction

Sets the contents of the **A** register to the specified value. The value is either a non-negative number (i.e. 21) or a Symbol. If the value is a Symbol, then the contents of the **A** register is set to the value that the Symbol refers to but not the actual data in that Register or Memory Location.

#### L-INSTRUCTIONS

Symbols can be either variables or lables. Variables are symbolic names for memory addresses to make remembering these addresses easier. Labels are instructions addresses that allow multiple jumps in the program easier to handle. Symbols declaration is not a machine instruction because machine code doesn't operate on the level of abstraction of that of labels and variables, and hence it is considered a pseudo-instruction.

##### Declaring Variables

Declaring variables is a straight forward A-Instruction, example:

```asm
@i
M=0
```

The instruction `@i` declares a variable "i", and the instruction `M=0` sets the memory location of "i" in Main Memory to 0, the address "i" was automatically generated and stored in **A** Register by the instruction.

##### Declaring Labels

To declare a label we need to use the command `(LABEL_NAME)`, where "LABEL_NAME" can be any name we desire to have for the label, as long as it's wraped between parentheses. For example:

```asm
(LOOP)
  // ...
  // instruction 1
  // instruction 2
  // instruction 3
  // ...
  @LOOP
  0;JMP
```

The instruction `(LOOP)` declares a new label called "LOOP", the assembler will resolve this label to the address of the next instruction (A or C instruction) on the following line.

The instruction `@LOOP` is a straight-forward A-Instruction that sets the contents of **A** Register to the instruction address the label refers to, whereas the `0;JMP` instruction causes an unconditional jump to the address in **A** Register causing the program to execute the set of instructions between `(LOOP)` and `0;JMP` infinitely.

#### C-INSTRUCTIONS

##### Symbolic Syntax of a C-Instruction

*dest* = *comp* ; *jmp*, where:

1. *dest*: Destination register in which the result of computation will be stored.
2. *comp*: Computation code.
3. *jmp*: The jump directive.

Examples:

- `D=0`
- `M=1`
- `D=D+1;JMP`
- `M=M-D;JEQ`

##### Binary Syntax of a C-Instruction

`1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3`, where:

- `111` bits: C-Instructions always begin with bits `111`.
- `a` bit: Chooses to load the contents of either **A** register or **M** (Main Memory register addressed by **A**) into the ALU for computation.
- Bits `c1` through `c6`: Control bits expected by the ALU to perform arithmetic or bit-wise logic operations.
- Bits `d1` through `d3`: Specify which memory location to store the result of ALU computation into: **A**, **D** or **M**.
- Bits `j1` through `j3`: Specify which JUMP directive to execute (either conditional or uncoditional).

##### Effects of a C-Instruction

Performs a computation on the CPU (arithmetic or bit-wise logic) and stores it into a destination register or memory location, and then (optionally) JUMPS to an instruction memory location that is usually addressed by a value or a Symbol (label).

## References

*The following reference images are taken from the [nand2tetris Coursera MOOC](https://www.coursera.org/learn/build-a-computer).*

### Computer Architecture

![Computer Architecture](assets/computer_arch.png "Computer Architecture")

![Computer Architecture Implementation](assets/computer_arch_impl.png "Computer Architecture")

### C-Instructions Reference

![C-Instructions Reference](assets/c_instructions_reference.png "C-Instructions Reference")

## License

This project is licensed under the [MIT License](LICENSE).
