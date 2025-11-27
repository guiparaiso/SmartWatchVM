"""
vm.py - SmartWatch Virtual Machine
Executa bytecode gerado pelo compiler
"""

from vm.bytecode import *

class VM:
    def __init__(self, bytecode, strings=None, num_vars=100):
        self.bytecode = bytecode
        self.strings = strings or []
        self.pc = 0                    # program counter
        self.stack = []                # pilha de valores
        self.vars = [0.0] * num_vars   # variáveis (inicializadas com 0)
        self.call_stack = []           # pilha de chamadas (para CALL/RET)
        self.halted = False
        self.sensors = {
            'HEARTRATE': 72,      # Batimentos por minuto
            'STEPS': 0,           # Passos do dia
            'BATTERY': 85,        # Bateria %
            'TIME_HOUR': 14,      # Hora atual
            'TIME_MINUTE': 30,    # Minuto atual
            'TIME_SECOND': 0      # Segundo atual
        }

    # No lugar de apenas empilhar 0/1, empilhe valores especiais:
# Comparações empilham: 2000 (False) ou 2001 (True)

    def _format_value(self, value):
        """Formata valores para display inteligente"""
        
        # Strings: 1000-1999
        if isinstance(value, int) and 1000 <= value < 2000:
            str_idx = value - 1000
            if 0 <= str_idx < len(self.strings):
                return self.strings[str_idx]
            else:
                return f"<string[{str_idx}] not found>"
        
        # Booleanos: 2000-2001
        elif value == 2000:
            return "False"
        elif value == 2001:
            return "True"
        
        # Número normal
        else:
            return str(value)    
    def run(self, debug=False):
        """Executa o bytecode"""
        print("=== SmartWatch VM - Iniciando execução ===\n")
        
        while self.pc < len(self.bytecode) and not self.halted:
            if debug:
                self.print_state()
            
            opcode = self.bytecode[self.pc]
            self.pc += 1
            
            self.execute_instruction(opcode)
        
        print("\n=== Execução finalizada ===")
    
    def execute_instruction(self, opcode):
        """Executa uma instrução"""

        opcode_name = OPCODE_NAMES.get(opcode, f"UNK_{opcode:02x}")
        # print(f"BEFORE PC={self.pc-1:04d} {opcode_name:15s} Stack={self.stack}")
        
        # === PILHA ===
        if opcode == OP_PUSH:
            value = self.bytecode[self.pc]
            self.pc += 1
            self.stack.append(value)
        
        elif opcode == OP_POP:
            if self.stack:
                self.stack.pop()
        
        elif opcode == OP_LOAD:
            var_idx = self.bytecode[self.pc]
            self.pc += 1
            self.stack.append(self.vars[var_idx])
        elif opcode == OP_LOAD_SENSOR:
            sensor_idx = self.bytecode[self.pc]
            self.pc += 1
            
            sensor_map = ['HEARTRATE', 'STEPS', 'BATTERY', 'TIME_HOUR', 'TIME_MINUTE']
            if sensor_idx < len(sensor_map):
                sensor_name = sensor_map[sensor_idx]
                value = self.sensors[sensor_name]
                self.stack.append(value)
                print(f"  📊 Sensor {sensor_name} = {value}")
            else:
                print(f"  ❌ Sensor inválido: {sensor_idx}")
                self.stack.append(0)
            
        elif opcode == OP_STORE:
            var_idx = self.bytecode[self.pc]
            self.pc += 1
            if self.stack:
                self.vars[var_idx] = self.stack.pop()
        
        # === ARITMÉTICA ===
        elif opcode == OP_ADD:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
        
        elif opcode == OP_SUB:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
        
        elif opcode == OP_MUL:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
        
        elif opcode == OP_DIV:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                if b != 0:
                    self.stack.append(a / b)
                else:
                    print("[ERRO] Divisão por zero!")
                    self.stack.append(0)
        # ADICIONE ESTAS LINHAS AQUI ↓↓↓
        elif opcode == OP_NEG:
            if self.stack:
                value = self.stack.pop()
                self.stack.append(-value)

        elif opcode == OP_NOT:
            if self.stack:
                value = self.stack.pop()
                self.stack.append(1 if value == 0 else 0)

        elif opcode == OP_POS:
            # Não faz nada, apenas mantém o valor positivo
            pass
        
        # === COMPARAÇÕES ===
        elif opcode == OP_EQ:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(2001 if a == b else 2000)
        
        elif opcode == OP_NEQ:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(2001 if a != b else 2000)
        
        elif opcode == OP_LT:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(2001 if a < b else 2000)
        
        elif opcode == OP_LE:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(2001 if a <= b else 2000)
        
        elif opcode == OP_GT:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(2001 if a > b else 2000)
        
        elif opcode == OP_GE:
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(2001 if a >= b else 2000)
        
        # === CONTROLE DE FLUXO ===
        elif opcode == OP_JMP:
            addr = self.bytecode[self.pc]
            self.pc = addr
        
        elif opcode == OP_JZ:
            addr = self.bytecode[self.pc]
            self.pc += 1
            if self.stack:
                condition = self.stack.pop()
                if condition == 2000:  # se falso, pula
                    self.pc = addr
        
        elif opcode == OP_CALL:
            addr = self.bytecode[self.pc]
            self.pc += 1
            self.call_stack.append(self.pc)  # salva endereço de retorno
            self.pc = addr
        
        elif opcode == OP_RET:
            if self.call_stack:
                self.pc = self.call_stack.pop()
        
        # === INSTRUÇÕES SMARTWATCH ===
        elif opcode == OP_POWERON:
            print("[SMARTWATCH] ⚡ Power ON")
        
        elif opcode == OP_POWEROFF:
            print("[SMARTWATCH] 🔌 Power OFF")
        
        elif opcode == OP_SHOWTIME:
            print("[SMARTWATCH] 🕐 Mostrando horário atual")
        
        elif opcode == OP_SETTIME:
            str_idx = self.bytecode[self.pc]
            self.pc += 1
            time_str = self.strings[str_idx] if str_idx < len(self.strings) else "00:00:00"
            print(f"[SMARTWATCH] 🕐 Ajustando horário para {time_str}")
        
        elif opcode == OP_SETALARM:
            str_idx = self.bytecode[self.pc]
            self.pc += 1
            time_str = self.strings[str_idx] if str_idx < len(self.strings) else "00:00:00"
            print(f"[SMARTWATCH] ⏰ Alarme configurado para {time_str}")
        
        elif opcode == OP_SETTIMER:
            if self.stack:
                seconds = self.stack.pop()
                print(f"[SMARTWATCH] ⏲️  Timer configurado para {int(seconds)} segundos")
        
        elif opcode == OP_NOTIFY:
            str_idx = self.bytecode[self.pc]
            self.pc += 1
            msg = self.strings[str_idx] if str_idx < len(self.strings) else ""
            print(f"[SMARTWATCH] 🔔 Notificação: {msg}")
        
        elif opcode == OP_SHOW:
            if self.stack:
                value = self.stack.pop()
                # print(f"🔍 [SHOW DEBUG] Value from stack: {value} (type: {type(value)})")
                # print(f"🔍 [SHOW DEBUG] Strings pool: {self.strings}")
                
                # Debug detalhado da formatação
                # if isinstance(value, int) and 0 <= value < len(self.strings):
                #     print(f"🔍 [SHOW DEBUG] Is string index: YES, string='{self.strings[value]}'")
                # else:
                #     print(f"🔍 [SHOW DEBUG] Is string index: NO")
                    
                display_value = self._format_value(value)
                print(f" {display_value}")
                # print(f"       [DEBUG] Stack após SHOW: {self.stack}")
            else:
                print("(pilha vazia)")
        
        elif opcode == OP_HEARTBEAT:
            print("[SMARTWATCH] ❤️  Medindo batimentos cardíacos")
        
        elif opcode == OP_STEP:
            print("[SMARTWATCH] 👟 Contando passos")
        
        elif opcode == OP_MUSICPLAY:
            str_idx = self.bytecode[self.pc]
            self.pc += 1
            music = self.strings[str_idx] if str_idx < len(self.strings) else "música"
            print(f"[SMARTWATCH] 🎵 Tocando: {music}")
        
        elif opcode == OP_MUSICSTOP:
            print("[SMARTWATCH] ⏹️  Música parada")
        
        elif opcode == OP_BLUETOOTH_ON:
            print("[SMARTWATCH] 📡 Bluetooth ligado")
        
        elif opcode == OP_BLUETOOTH_OFF:
            print("[SMARTWATCH] 📡 Bluetooth desligado")
        
        elif opcode == OP_HALT:
            print("[SMARTWATCH] 🛑 Programa finalizado")
            self.halted = True
        
        else:
            print(f"[ERRO] Opcode desconhecido: 0x{opcode:02x}")

        # print(f"AFTER  PC={self.pc-1:04d} {opcode_name:15s} Stack={self.stack}")
    
    def print_state(self):
        """Imprime estado da VM (debug)"""
        print(f"PC={self.pc:04d} Stack={self.stack} Vars={self.vars[:5]}...")


if __name__ == "__main__":
    # Teste simples
    print("=== Teste da VM ===\n")
    
    # x = 10; y = 20; resultado = x + y; SHOW resultado; HALT
    test_bytecode = [
        OP_PUSH, 10,        # push 10
        OP_STORE, 0,        # x = 10
        OP_PUSH, 20,        # push 20
        OP_STORE, 1,        # y = 20
        OP_LOAD, 0,         # load x
        OP_LOAD, 1,         # load y
        OP_ADD,             # x + y
        OP_STORE, 2,        # resultado = ...
        OP_LOAD, 2,         # load resultado
        OP_SHOW,            # mostra
        OP_HALT             # fim
    ]
    
    vm = VM(test_bytecode)
    vm.run()