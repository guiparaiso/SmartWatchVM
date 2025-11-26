"""
bytecode.py - Definições das instruções da SmartWatch VM
"""

# === OPERAÇÕES DE PILHA ===
OP_PUSH = 0x01      # PUSH <value>     - empilha valor
OP_POP = 0x02       # POP              - desempilha
OP_LOAD = 0x03      # LOAD <var_idx>   - carrega variável
OP_STORE = 0x04     # STORE <var_idx>  - armazena em variável

# === OPERAÇÕES ARITMÉTICAS ===
OP_ADD = 0x10       # ADD              - soma (pop 2, push resultado)
OP_SUB = 0x11       # SUB              - subtração
OP_MUL = 0x12       # MUL              - multiplicação
OP_DIV = 0x13       # DIV              - divisão

# Operações unárias
OP_NEG = 50   # Negação aritmética (-)
OP_NOT = 51   # Negação lógica (!)
OP_POS = 52   # Valor positivo (+)

# === OPERAÇÕES DE COMPARAÇÃO ===
OP_EQ = 0x20        # EQ               - ==
OP_NEQ = 0x21       # NEQ              - !=
OP_LT = 0x22        # LT               - <
OP_LE = 0x23        # LE               - <=
OP_GT = 0x24        # GT               - >
OP_GE = 0x25        # GE               - >=

# === CONTROLE DE FLUXO ===
OP_JMP = 0x30       # JMP <addr>       - pula para endereço
OP_JZ = 0x31        # JZ <addr>        - pula se zero (false)
OP_CALL = 0x32      # CALL <addr>      - chama label
OP_RET = 0x33       # RET              - retorna de chamada

# === INSTRUÇÕES SMARTWATCH ===
OP_POWERON = 0x40
OP_POWEROFF = 0x41
OP_SHOWTIME = 0x42
OP_SETTIME = 0x43   # SETTIME <string_idx>
OP_SETALARM = 0x44  # SETALARM <string_idx>
OP_SETTIMER = 0x45  # SETTIMER
OP_NOTIFY = 0x46    # NOTIFY <string_idx>
OP_SHOW = 0x47      # SHOW
OP_HEARTBEAT = 0x48
OP_STEP = 0x49
OP_MUSICPLAY = 0x4A # MUSICPLAY <string_idx>
OP_MUSICSTOP = 0x4B
OP_BLUETOOTH_ON = 0x4C
OP_BLUETOOTH_OFF = 0x4D
OP_HALT = 0xFF      # HALT             - para execução

# Dicionário para debug (nome da instrução)
OPCODE_NAMES = {
    OP_PUSH: "PUSH",
    OP_POP: "POP",
    OP_LOAD: "LOAD",
    OP_STORE: "STORE",
    OP_ADD: "ADD",
    OP_SUB: "SUB",
    OP_MUL: "MUL",
    OP_DIV: "DIV",
    OP_EQ: "EQ",
    OP_NEQ: "NEQ",
    OP_LT: "LT",
    OP_LE: "LE",
    OP_GT: "GT",
    OP_GE: "GE",
    OP_JMP: "JMP",
    OP_JZ: "JZ",
    OP_CALL: "CALL",
    OP_RET: "RET",
    OP_POWERON: "POWERON",
    OP_POWEROFF: "POWEROFF",
    OP_SHOWTIME: "SHOWTIME",
    OP_SETTIME: "SETTIME",
    OP_SETALARM: "SETALARM",
    OP_SETTIMER: "SETTIMER",
    OP_NOTIFY: "NOTIFY",
    OP_SHOW: "SHOW",
    OP_HEARTBEAT: "HEARTBEAT",
    OP_STEP: "STEP",
    OP_MUSICPLAY: "MUSICPLAY",
    OP_MUSICSTOP: "MUSICSTOP",
    OP_BLUETOOTH_ON: "BLUETOOTH_ON",
    OP_BLUETOOTH_OFF: "BLUETOOTH_OFF",
    OP_HALT: "HALT",
}

def disassemble(bytecode, strings=None):
    """
    Descompila bytecode para formato legível (debug)
    """
    pc = 0
    lines = []
    
    while pc < len(bytecode):
        addr = pc
        opcode = bytecode[pc]
        pc += 1
        
        name = OPCODE_NAMES.get(opcode, f"UNKNOWN({opcode:02x})")
        
        # Instruções com operandos
        if opcode in [OP_PUSH, OP_LOAD, OP_STORE, OP_JMP, OP_JZ, OP_CALL,
                      OP_SETTIME, OP_SETALARM, OP_NOTIFY, OP_MUSICPLAY]:
            if pc < len(bytecode):
                operand = bytecode[pc]
                pc += 1
                
                # Se for índice de string, mostra a string
                if opcode in [OP_SETTIME, OP_SETALARM, OP_NOTIFY, OP_MUSICPLAY] and strings:
                    if 0 <= operand < len(strings):
                        lines.append(f"{addr:04d}: {name:15s} {operand:5d}  ; \"{strings[operand]}\"")
                    else:
                        lines.append(f"{addr:04d}: {name:15s} {operand:5d}")
                else:
                    lines.append(f"{addr:04d}: {name:15s} {operand:5d}")
            else:
                lines.append(f"{addr:04d}: {name:15s} <missing operand>")
        else:
            lines.append(f"{addr:04d}: {name}")
    
    return "\n".join(lines)