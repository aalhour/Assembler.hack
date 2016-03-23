# ASSEMBLER.HACK

Assembler.hack is a 16-bit machine language assembler for the, minimal 16-bit, Hack Assembly Language. This was done as part of building a complete 16-bit computer from the grounds up through the book, and [MOOC](https://www.coursera.org/learn/build-a-computer/), *Elementes of Computing Systems*, which is informally known as [nand2tetris](http://www.nand2tetris.org). Hack is also the name of the computer.

## DESCRIPTION

Assembler.hack takes a program source file written in the Hack Assembly Language (see: introduction below), with the file extension *.asm*, and then compiles it into binary machine code (Hack Machine Language), the machine code is then written to a new file with the same name but with the extension *.hack*.

How to use:

```bash
python Assembler HelloWorld.asm
```

## REQUIREMENTS

  * Python 3.5.1

## INTRO TO THE HACK ASSEMBLY (AND MACHINE) LANGUAGE

The Hack assembly language is minimal, it mainly consists of 2 types of instructions. It ignores whitespace and allows the program to declare symbols with a single symbol declaration instruction. Symbols can either be labels or variables.

If you cannot contain the excitement then head over to the [tests](tests/) directory and check out the testing programs (\*.asm and \*.hack).
 
### Predefined Symbols:

  * **A**: Address Register.
  * **D**: Data Register.
  * **M**: Refers to the register in Main Memory whose address is currently stored in **A** (Address Register).
  * **SCREEN**: Refers to the base address of the Screen Map in Main Memory.
  * **KEYBOARD**: Refers to address of the Keyboard Register in Main Memory.
  * **R0**-**R15**: Addresses of 16 registers that are mapped with addresses 0 to 15. 

### Comments and Whitespaces:

All whitespaces are ignored and `// this is a single line comment`.

### Types of Instructions:

  1. A-Instructions: Addressing instructions.
  2. C-Instructions: Computation instructions.

#### A-Instructions:

###### Symbolic Syntax:

`@value`, where value is either a decimal non-negative number or a SYMBOL. 

Examples:
  * `@21`
  * `@SCREEN` 

###### Binary Syntax:

`0xxxxxxxxxxxxxxx`, where `x` is either a 0 or 1. A-Instructions always have their MSB set to 0.

Example:
  * `000000000001010`
  * `011111111111111`

###### Effects:

Sets the contents of the **A** register to the specified value. The value is either a non-negative number (i.e. 21) or a Symbol. If the value is a symbol then the contents of the **A** register becomes the value that SYMBOL refers to but not the actual data in that SYMBOL register/location.

#### C-Instructions:

###### Symbolic Syntax

*dest* = *comp* ; *jmp*, where:

  1. *dest*: Destination register in which the result of computation will be stored.
  2. *comp*: Computation code.
  3. *jmp*: The jump directive.

Examples:
  * `D=0`
  * `D=D+1`
  * `M=M-D`

###### Binary Syntax: 

`1 1 1 a c1 c2 c3 c4 c5 c6 d1 d2 d3 j1 j2 j3`, where:

  * `111`: C-Instructions always begin with bits `111`.
  * `a` bit: Chooses to load the contents of either **A** register or **M** (Main Memory register addressed by **A**) into the ALU for computation.
  * Bits `c1` through `c6`: Control bits expected by the ALU to perform the arithmetic or bit-wise logical operation.
  * Bits `d1` through `d3`: Specify which memory location to store result into: **A**, **D** or **M**.
  * Bits `j1` through `j3`: Specify which JUMP directive for execute.

###### Effects:

Performs a computation on the CPU (arithmetic or bit-wise logical) and stores it into a destination register, and then, optionally, JUMPS into an instruction memory location that is usually addressed by a label (SYMBOL).

###### Reference:

![C-Instructions Reference](assets/c_instructions_reference.png "C-Instructions Reference")

## LICENSE

This project is licensed under the [MIT License](LICENSE).

