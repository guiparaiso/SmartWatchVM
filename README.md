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
Program      = { Line } ;

Line         = [ Label ] Instruction [ Comment ] ;

Label        = Identifier ":" ;

Instruction  = PowerOn 
             | PowerOff 
             | ShowTime 
             | SetTime
             | SetAlarm 
             | SetTimer
             | Notify 
             | HeartBeat 
             | Step 
             | MusicPlay 
             | MusicStop 
             | Bluetooth
             | Halt ;

PowerOn      = "POWERON" ;
PowerOff     = "POWEROFF" ;
ShowTime     = "SHOWTIME" ;
SetTime      = "SETTIME" Time ;
SetAlarm     = "SETALARM" Time ;
SetTimer     = "SETTIMER" Number ;
Notify       = "NOTIFY" QuotedText ;
HeartBeat    = "HEARTBEAT" ;
Step         = "STEP" ;
MusicPlay    = "MUSICPLAY" Track ;
MusicStop    = "MUSICSTOP" ;
Bluetooth    = "BLUETOOTH" BluetoothState ;
Halt         = "HALT" ;

Time         = Digit Digit ":" Digit Digit ":" Digit Digit ;
Number       = Digit { Digit } ;
Track        = Identifier ;
QuotedText   = '"' { ANY - '"' } '"' ;

BluetoothState = "ON" | "OFF" ;

Identifier   = Letter { Letter | Digit | "_" } ;
Digit        = "0".."9" ;
Letter       = "A".."Z" | "a".."z" ;

Comment      = ";" { ANY } ;
