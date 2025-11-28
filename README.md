# SmartWatch- VM and Lang ⌚

A virtual machine that simulates the behavior of a **smartwatch**.  

---

## Overview

SmartWatchVM is a virtual machine designed to demonstrate language design and virtual machine architecture in a playful context with the goal to put in practice the concepts learned during class.

With seven registers (`TIME`, `ALARM`, `HEART`, `STEP`, `TRACK`, `BT`, `TIMER`) and thirteen instructions, it simulates the behavior of a smartwatch while keeping the computational model minimal.

SmartWatchVM is perfect for:

 **Computer Science Education**: Learning how languages and VMs are structured.  

 **Grammar & Parsing Practice**: Defining languages with EBNF and building interpreters.  

 **Simulation**: Modeling daily smartwatch scenarios (alarms, workouts, notifications).  

 **Compiler Construction**: Writing parsers and simple backends for a constrained VM.  

 **Theoretical Exploration**: Understanding abstraction between syntax (EBNF) and semantics (execution).  

---

## Language Instructions

The instructions supported by the VM are:

| Instruction  | Operand(s)   | Description |
|--------------|--------------|-------------|
| `POWERON`    | –            | Turns the smartwatch on |
| `POWEROFF`   | –            | Turns the smartwatch off |
| `SHOWTIME`   | –            | Displays the current time |
| `SETTIME`    | `<HH:MM:SS>` | Sets the current time |
| `SETALARM`   | `<HH:MM:SS>` | Sets an alarm |
| `SETTIMER`   | `<seconds>`  | Sets a countdown timer in seconds |
| `NOTIFY`     | `"<text>"`   | Shows a notification |
| `HEARTBEAT`  | –            | Measures heart rate |
| `STEP`       | –            | Records a step |
| `MUSICPLAY`  | `<track>`    | Plays a music track |
| `MUSICSTOP`  | –            | Stops the music |
| `BLUETOOTH`  | `ON \| OFF`  | Enables or disables bluetooth connection |
| `HALT`       | –            | Halts the program execution |

---

## EBNF Grammar

The grammar of the SmartWatchVM language is defined in [`smartwatchvm.ebnf`](smartwatchvm.ebnf).

```ebnf
Program   = { Line } ;

Line      = [ Label ] Statement [ Comment ] ;
Label     = Identifier ":" ;

Statement = Instr
          | Assignment
          | IfBlock
          | WhileBlock
          | Call
          | Return
          | Halt ;

Instr     = "POWERON" 
          | "POWEROFF"
          | "SHOWTIME"
          | "SETTIME" Time
          | "SETALARM" Time
          | "SETTIMER" Number
          | "NOTIFY" QuotedText
          | "SHOW" Expr
          | "HEARTBEAT"
          | "STEP"
          | "MUSICPLAY" Identifier
          | "MUSICSTOP"
          | "BLUETOOTH" ("ON" | "OFF")
          ;

Assignment = Identifier "=" Expr ;

IfBlock   = "WHEN" CondExpr "THEN" { Line } [ "ELSE" { Line } ] "ENDWHEN" ;
WhileBlock= "LOOP" CondExpr "DO" { Line } "ENDLOOP" ;

Call      = "CALL" Identifier ;
Return    = "RETURN" ;
Halt      = "HALT" ;

CondExpr  = Expr ( "==" | "!=" | "<" | "<=" | ">" | ">=" ) Expr ;

Expr      = Term { ("+"|"-") Term } ;
Term      = Factor { ("*"|"/") Factor } ;
Factor    = Number | QuotedText | Identifier | "(" Expr ")" ;

Time      = Digit Digit ":" Digit Digit ":" Digit Digit ;
Number    = Digit { Digit } ;
QuotedText= '"' { ANY - '"' } '"' ;
Identifier= Letter { Letter | Digit | "_" } ;

Comment   = ";" { ANY } ;
Digit     = "0".."9" ;
Letter    = "A".."Z" | "a".."z" ;

```

## Quick Start

### Installation

```bash
git clone https://github.com/yourusername/SmartWatch-VM.git
cd SmartWatch-VM
```

### Building The Compiler

```bash

# Easy way - use the build script:
./build.sh

# Manual build:
cd lang/
bison -d parser.y    # Generates parser.c and parser.h
flex lexer.l         # Generates lexer.c  
cd ..
gcc -o smartwatch_vm lang/parser.c lang/lexer.c -lfl

```

### Running Programs
```bash
# Run a program file
python3 main.py examples/fibonacci.sw

# Run syntax verification only
python3 main.py --check program.sw

# Run with debug output
python3 main.py --debug program.sw
```

### Your First SmartWatch Program
Create `hello_watch.sw`:
```
POWERON
SHOW "Hello, SmartWatch!"

# Track heart rate and steps
WHEN HEARTRATE > 70 THEN
    NOTIFY "High heart rate detected"
    SHOW STEPS
ENDWHEN

# Simple counter loop
counter = 1
LOOP counter <= 5 DO
    SHOW counter
    counter = counter + 1
ENDLOOP

POWEROFF
```

Run it:
```bash
python3 main.py hello_watch.sw
```

---

## Language Overview

SmartWatchVM is a virtual machine designed to demonstrate language design and virtual machine architecture in the context of wearable devices. It combines realistic smartwatch sensors with Turing-complete computational capabilities.

### Key Features
- **7 Specialized Registers** simulating smartwatch hardware
- **Real-time Sensor Simulation** (heart rate, steps, battery, time)
- **Structured Programming** with loops and conditionals
- **Syntax Verification** with detailed error reporting
- **Mathematical Computation** capabilities

---

## SmartWatch Architecture

### Register Set
| Register | Type | Description |
|----------|------|-------------|
| `TIME` | Read-Write | Current time manipulation |
| `ALARM` | Read-Write | Alarm settings |
| `HEART` | Read-Only | Heart rate sensor (60-120 bpm) |
| `STEP` | Read-Only | Step counter |
| `TRACK` | Read-Write | Music track control |
| `BT` | Read-Write | Bluetooth status |
| `TIMER` | Read-Write | Countdown timer |

### Sensor Simulation
The VM includes realistic sensor simulation that updates dynamically:

```python
self.sensors = {
    'HEARTRATE': 72,      # Batimentos por minuto
    'STEPS': 0,           # Passos do dia  
    'BATTERY': 85,        # Bateria %
    'TIME_HOUR': 14,      # Hora atual
    'TIME_MINUTE': 30,    # Minuto atual
    'TIME_SECOND':00,
}
```

---

## Language Syntax

### Core Instructions
```
# Power Management
POWERON, POWEROFF

# Time Operations  
SHOWTIME, SETTIME "14:30:00", SETALARM "07:00:00", SETTIMER 60

# Health Monitoring
HEARTBEAT, STEP, SHOW HEARTRATE, SHOW STEPS

# Media Control
MUSICPLAY "playlist", MUSICSTOP

# Connectivity
BLUETOOTH ON, BLUETOOTH OFF

# Notifications
NOTIFY "Message", SHOW expression

# Program Control
HALT, CALL function, RETURN
```

### Structured Programming
```
# Conditional execution
WHEN HEARTRATE > 100 THEN
    NOTIFY "High intensity workout"
    SHOW "Take a break"
ELSE
    SHOW "Normal activity"
ENDWHEN

# Loops
counter = 0
LOOP counter < 10 DO
    STEP
    counter = counter + 1
    SHOW counter
ENDLOOP

# Functions
main:
    CALL calculate_steps
    RETURN

calculate_steps:
    SHOW "Calculating..."
    RETURN
```

---

## Example Programs

The `testes_prob_matematico/` directory contains implementations of classical algorithms adapted for smartwatch context:

- **`fibonacci.sw`** - Fibonacci sequence generation
- **`gcd.sw`** - Greatest Common Divisor using Euclidean algorithm  
- **`factorial.sw`** - Iterative factorial computation
- **`prime_check.sw`** - Prime number verification
- **`collatz.sw`** - Collatz conjecture sequence
- **`workout_tracker.sw`** - Exercise monitoring with heart rate
- **`battery_saver.sw`** - Power management simulation
- **`smart_alarm.sw`** - Context-aware alarm system

## Test Suite

The `testes_aplicados/` directory contains comprehensive tests organized by language features:

- **`demo_basico.sw`** - Tests variables, expressions, and output instructions
- **`demo_condicionais.sw`** - Tests conditional logic with WHEN/THEN/ELSE
- **`demo_loops.sw`** - Tests loop structures and nested iterations
- **`demo_smartwatch.sw`** - Complete smartwatch application testing all instructions
- **`requisitos.sw`** - VM requirement validation (registers, memory, sensors, Turing-completeness)


## VM Implementation

### Computational Model
SmartWatchVM is **Turing-complete** through:
- **2 General-purpose registers** for computation
- **Unbounded memory** via stack operations  
- **Conditional branching** with `WHEN/THEN/ELSE`
- **Loop constructs** with `LOOP/DO/ENDLOOP`
- **Function calls** with `CALL/RETURN`

### Parser Architecture
```c
/* Two-phase analysis */
1. Syntax parsing with Bison/Flex
2. Semantic checking (variables, labels)
3. Code generation for VM execution
```

### Error Detection
The parser provides detailed error reporting:
```
🚨 ERRO SINTÁTICO DETALHADO:
   Mensagem: syntax error
   Linha: 15
   Token atual: 'unknown'
   Próximos tokens: 258 259 260
```

---

## Compiler Design

### Target Architecture Constraints
When building compilers for SmartWatchVM, consider:

1. **Register Allocation**
   - 2 computational registers available
   - 5 sensor registers (read-only)
   - Stack available for temporary storage

2. **Control Flow**
   - Structured programming constructs
   - Label-based function calls
   - Conditional execution

3. **Sensor Integration**
   - Real-time sensor data access
   - Read-only sensor variables
   - Automatic sensor simulation

### Compilation Patterns
```
# Variable assignment
x = 10            → SET TIME 10

# Arithmetic operations
result = a + b    → ADD operations via loops

# Conditionals  
IF x > 5 THEN     → WHEN TIME > 5 THEN
```

---

## Theoretical Foundation

### Turing Completeness
SmartWatchVM is Turing complete because it can simulate a Minsky machine:
- **Unbounded storage** through registers and stack
- **Conditional branching** via WHEN/LOOP constructs  
- **Arbitrary computation** through mathematical operations

### Language Design
- **Context-Free Grammar** defined in EBNF
- **Lexical Analysis** with Flex
- **Syntax Analysis** with Bison
- **Semantic Analysis** with symbol tables

---

## Testing & Verification

### Syntax Checking
```
# Detailed syntax analysis
=== ANÁLISE SINTÁTICA ===

--- VARIÁVEIS ENCONTRADAS (3) ---
  [1] counter        : ✓ definida, usada
  [2] steps          : ✓ definida, não usada
  [3] temp           : ✗ indefinida, usada

--- LABELS ENCONTRADOS (2) ---
  [1] main           : ✓ definido, chamado
  [2] calculate      : ✓ definido, não chamado
```

### Sensor Integration Testing
```
# Verify sensor access
SHOW HEARTRATE      # 72
SHOW STEPS          # 0
SHOW BATTERY        # 85
```

---


**SmartWatch VM** - Where wearable computing meets language design! ⌚💻