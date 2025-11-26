"""
compiler.py - Compilador que lê código fonte .sw e gera bytecode
"""

import struct
from bytecode import *

class Compiler:
    def __init__(self):
        self.bytecode = []
        self.strings = []          # pool de strings
        self.vars = {}             # mapa nome -> índice
        self.labels = {}           # mapa label -> endereço
        self.unresolved_jumps = [] # [(addr, label_name, type)]
        self.next_var_idx = 0
    
    def get_var_index(self, var_name):
        """Retorna índice da variável (cria se não existir)"""
        if var_name not in self.vars:
            self.vars[var_name] = self.next_var_idx
            self.next_var_idx += 1
        return self.vars[var_name]
    
    def get_string_index(self, string):
        """Retorna índice da string no pool (cria se não existir)"""
        if string not in self.strings:
            self.strings.append(string)
        return self.strings.index(string)
    
    def emit(self, opcode, operand=None):
        """Emite uma instrução"""
        self.bytecode.append(opcode)
        if operand is not None:
            self.bytecode.append(operand)
    
    def current_address(self):
        """Retorna endereço atual (próxima instrução)"""
        return len(self.bytecode)
    
    def define_label(self, label_name):
        """Define um label no endereço atual"""
        self.labels[label_name] = self.current_address()
    
    def emit_jump(self, opcode, label_name):
        """Emite jump para label (resolve depois)"""
        addr = self.current_address()
        self.emit(opcode, 0)  # placeholder
        self.unresolved_jumps.append((addr + 1, label_name, opcode))
    
    def resolve_jumps(self):
        """Resolve todos os jumps pendentes"""
        for addr, label_name, opcode in self.unresolved_jumps:
            if label_name in self.labels:
                target = self.labels[label_name]
                self.bytecode[addr] = target
            else:
                print(f"[AVISO] Label '{label_name}' não encontrado")
    
    def compile_from_file(self, filename):
        """Compila diretamente do arquivo fonte .sw"""
        with open(filename, 'r') as f:
            source_code = f.read()
        
        self._compile_source(source_code)
        self.resolve_jumps()
        
        # Garante HALT no final
        if not self.bytecode or self.bytecode[-1] != OP_HALT:
            self.emit(OP_HALT)
    
    def _compile_source(self, source_code):
        """Compila o código fonte linha a linha"""
        lines = source_code.split('\n')
        line_num = 0
        
        for line in lines:
            line_num += 1
            line = line.strip()
            
            # Linha vazia ou comentário
            if not line or line.startswith('#'):
                continue
            
            try:
                self._compile_line(line)
            except Exception as e:
                print(f"❌ Erro na linha {line_num}: {line}")
                print(f"   {e}")
                raise
    
    def _compile_line(self, line):
        """Compila uma única linha de código"""
        
        # REMOVER COMENTÁRIOS PRIMEIRO!
        if '#' in line:
            line = line.split('#')[0].strip()
        if ';' in line:
            line = line.split(';')[0].strip()
        
        print(f"📝 [COMPILER] Processando linha: '{line}'")
        
        # LABEL:
        if line.endswith(':'):
            label_name = line[:-1].strip()
            self.define_label(label_name)
            return
        
        # WHEN condition THEN
        if line.startswith('WHEN '):
            # Implementação simplificada - pula a condição por agora
            self.emit(OP_PUSH, 1)  # sempre verdadeiro por enquanto
            return
        
        # LOOP condition DO
        if line.startswith('LOOP '):
            # Implementação simplificada
            loop_start = self.current_address()
            self.emit(OP_PUSH, 1)  # sempre verdadeiro por enquanto
            return
        
        # ENDWHEN, ENDLOOP
        if line in ['ENDWHEN', 'ENDLOOP']:
            # Por enquanto não faz nada
            return
        
        # CALL label
        if line.startswith('CALL '):
            label = line[5:].strip()
            self.emit_jump(OP_CALL, label)
            return
        
        # RETURN
        if line == 'RETURN':
            self.emit(OP_RET)
            return
        
        # HALT
        if line == 'HALT':
            self.emit(OP_HALT)
            return
        
        # VARIÁVEL = expressão
        if '=' in line and not line.startswith('SHOW'):
            parts = line.split('=')
            if len(parts) == 2:
                var_name = parts[0].strip()
                expr = parts[1].strip()
                print(f"  🟡 Assignment: {var_name} = '{expr}'")
                self._compile_expression(expr)
                var_idx = self.get_var_index(var_name)
                self.emit(OP_STORE, var_idx)
                return
        if line.startswith('SHOW'):
            # Pega tudo depois de "SHOW" (com ou sem espaço)
            if len(line) > 4:
                expr = line[4:].strip()  # Remove "SHOW" e espaços
            else:
                expr = ""
            print(f"  🟢 SHOW expression: '{expr}'")
            self._compile_expression(expr)
            self.emit(OP_SHOW)
            return
        
        
        # INSTRUÇÕES DO SMARTWATCH
        print(f"  🔴 Instrução não processada: '{line}'")
        self._compile_instruction(line)
        
    def _compile_expression(self, expr):
        """Compila uma expressão matemática completa com comparadores"""
        print(f"🔍 [COMPILER] Compilando expressão: '{expr}'")
        
        expr = expr.strip()
        
        # 1. STRINGS PRIMEIRO
        if expr.startswith('"') and expr.endswith('"'):
            string_val = expr[1:-1]
            str_idx = self.get_string_index(string_val)
            string_offset = 1000 + str_idx
            print(f"  ✅ STRING: '{string_val}' -> offset {string_offset}")
            self.emit(OP_PUSH, string_offset)
            return

        # 2. PARÊNTESES
        if expr.startswith('(') and expr.endswith(')'):
            inner = expr[1:-1].strip()
            print(f"  ✅ PARÊNTESES: ({inner})")
            self._compile_expression(inner)
            return
        
        # 🆕 3. COMPARADORES (ANTES DOS UNÁRIOS!)
        comparators = ['>=', '<=', '==', '!=', '>', '<']
        
        for comp in comparators:
            pos = expr.find(comp)
            if pos != -1:
                left = expr[:pos].strip()
                right = expr[pos + len(comp):].strip()
                print(f"  ✅ Comparador '{comp}': left='{left}', right='{right}'")
                
                self._compile_expression(left)
                self._compile_expression(right)
                
                if comp == '==': self.emit(OP_EQ)
                elif comp == '!=': self.emit(OP_NEQ)
                elif comp == '<': self.emit(OP_LT)
                elif comp == '<=': self.emit(OP_LE)
                elif comp == '>': self.emit(OP_GT)
                elif comp == '>=': self.emit(OP_GE)
                return
        
        # 4. OPERADORES UNÁRIOS (DEPOIS DOS COMPARADORES)
        if expr.startswith('-') or expr.startswith('!') or expr.startswith('+'):
            op = expr[0]
            operand = expr[1:].strip()
            print(f"  ✅ OPERADOR UNÁRIO: '{op}' em '{operand}'")
            
            self._compile_expression(operand)
            
            if op == '-':
                self.emit(OP_NEG)
                print(f"  🔧 EMITIU OP_NEG")
            elif op == '+':
                self.emit(OP_POS)
                print(f"  🔧 EMITIU OP_POS")
            elif op == '!':
                self.emit(OP_NOT)
                print(f"  🔧 EMITIU OP_NOT")
            return
        
        # 5. NÚMEROS
        try:
            value = int(expr)
            print(f"  ✅ NÚMERO: '{expr}' -> PUSH {value}")
            self.emit(OP_PUSH, value)
            return
        except ValueError:
            pass
        
        # 6. VARIÁVEIS
        if expr.isidentifier():
            var_idx = self.get_var_index(expr)
            print(f"  ✅ VARIÁVEL: '{expr}' -> LOAD {var_idx}")
            self.emit(OP_LOAD, var_idx)
            return
        
    # 7. OPERAÇÕES ARITMÉTICAS
    # ... resto do código igual ...
        
        # 6. OPERAÇÕES ARITMÉTICAS
        operators = ['+', '-', '*', '/']
        print(f"   Procurando operadores: {operators}")
        
        # Procura + e - (da direita para esquerda)
        for i in range(len(expr)-1, -1, -1):
            if expr[i] in ['+', '-']:
                # Verifica se é operador binário (não unário)
                if i == 0:
                    continue
                if expr[i-1] in ['+', '-', '*', '/', '=', '!', '<', '>']:
                    continue
                    
                left = expr[:i].strip()
                right = expr[i+1:].strip()
                print(f"  ✅ Operador binário '{expr[i]}': left='{left}', right='{right}'")
                
                self._compile_expression(left)
                self._compile_expression(right)
                
                if expr[i] == '+': 
                    self.emit(OP_ADD)
                elif expr[i] == '-': 
                    self.emit(OP_SUB)
                return
        
        # Procura * e /
        for i in range(len(expr)-1, -1, -1):
            if expr[i] in ['*', '/']:
                left = expr[:i].strip()
                right = expr[i+1:].strip()
                print(f"  ✅ Operador '{expr[i]}': left='{left}', right='{right}'")
                
                self._compile_expression(left)
                self._compile_expression(right)
                
                if expr[i] == '*': 
                    self.emit(OP_MUL)
                elif expr[i] == '/': 
                    self.emit(OP_DIV)
                return
        
        
        # 8. NÃO RECONHECIDO
        print(f"  ❌ EXPRESSÃO NÃO RECONHECIDA: '{expr}'")
        self.emit(OP_PUSH, 0)

    def _compile_instruction(self, line):
        """Compila instruções do smartwatch"""
        
        # POWERON
        if line == 'POWERON':
            self.emit(OP_POWERON)
        
        # POWEROFF
        elif line == 'POWEROFF':
            self.emit(OP_POWEROFF)
        
        # SHOWTIME
        elif line == 'SHOWTIME':
            self.emit(OP_SHOWTIME)
        
        
        # SETTIME HH:MM
        elif line.startswith('SETTIME '):
            time_str = line[8:].strip()
            str_idx = self.get_string_index(time_str)
            self.emit(OP_SETTIME, str_idx)
        
        # SETALARM HH:MM
        elif line.startswith('SETALARM '):
            time_str = line[9:].strip()
            str_idx = self.get_string_index(time_str)
            self.emit(OP_SETALARM, str_idx)
        
        # SETTIMER segundos
        elif line.startswith('SETTIMER '):
            seconds = line[9:].strip()
            if seconds.isdigit():
                self.emit(OP_PUSH, int(seconds))
                self.emit(OP_SETTIMER)
        
        # NOTIFY "mensagem"
        elif line.startswith('NOTIFY '):
            msg = line[7:].strip().strip('"')
            str_idx = self.get_string_index(msg)
            self.emit(OP_NOTIFY, str_idx)
        
        # SHOW expressão
        elif line.startswith('SHOW '):
            expr = line[5:].strip()
            self._compile_expression(expr)
            self.emit(OP_SHOW)
        
        # HEARTBEAT
        elif line == 'HEARTBEAT':
            self.emit(OP_HEARTBEAT)
        
        # STEP
        elif line == 'STEP':
            self.emit(OP_STEP)
        
        # MUSICPLAY "música"
        elif line.startswith('MUSICPLAY '):
            music = line[10:].strip().strip('"')
            str_idx = self.get_string_index(music)
            self.emit(OP_MUSICPLAY, str_idx)
        
        # MUSICSTOP
        elif line == 'MUSICSTOP':
            self.emit(OP_MUSICSTOP)
        
        # BLUETOOTH ON/OFF
        elif line.startswith('BLUETOOTH '):
            state = line[10:].strip()
            if state == 'ON':
                self.emit(OP_BLUETOOTH_ON)
            elif state == 'OFF':
                self.emit(OP_BLUETOOTH_OFF)
        
        else:
            print(f"[AVISO] Instrução não reconhecida: {line}")
            # Ignora instruções não reconhecidas
    
    def save_bytecode(self, filename):
        """Salva bytecode em arquivo binário"""
        with open(filename, 'wb') as f:
            # Magic number: "SWB\0"
            f.write(b'SWB\x00')
            
            # Versão
            f.write(struct.pack('I', 1))
            
            # Número de variáveis
            f.write(struct.pack('I', self.next_var_idx))
            
            # Número de strings
            f.write(struct.pack('I', len(self.strings)))
            
            # Pool de strings
            for s in self.strings:
                encoded = s.encode('utf-8')
                f.write(struct.pack('I', len(encoded)))
                f.write(encoded)
            
            # Bytecode - 🔥 USE 'i' (signed int) EM VEZ DE 'I' (unsigned)
            f.write(struct.pack('I', len(self.bytecode)))
            for byte in self.bytecode:
                f.write(struct.pack('i', byte))  # ← CORRIGIDO: 'i' em vez de 'I'
        
        print(f"✓ Bytecode salvo em '{filename}'")
        print(f"  - {len(self.bytecode)} instruções")
        print(f"  - {self.next_var_idx} variáveis")
        print(f"  - {len(self.strings)} strings")
    
    @staticmethod
    def load_bytecode(filename):
        """Carrega bytecode de arquivo"""
        with open(filename, 'rb') as f:
            # Verifica magic number
            magic = f.read(4)
            if magic != b'SWB\x00':
                raise ValueError("Arquivo não é bytecode SmartWatch válido")
            
            # Versão
            version = struct.unpack('I', f.read(4))[0]
            
            # Número de variáveis
            num_vars = struct.unpack('I', f.read(4))[0]
            
            # Strings
            num_strings = struct.unpack('I', f.read(4))[0]
            strings = []
            for _ in range(num_strings):
                str_len = struct.unpack('I', f.read(4))[0]
                strings.append(f.read(str_len).decode('utf-8'))
            
            # Bytecode - 🔥 USE 'i' (signed int) EM VEZ DE 'I'
            code_len = struct.unpack('I', f.read(4))[0]
            bytecode = []
            for _ in range(code_len):
                bytecode.append(struct.unpack('i', f.read(4))[0])  # ← CORRIGIDO
            
            return bytecode, strings, num_vars


# Teste simples
if __name__ == "__main__":
    # Cria um programa de teste
    test_code = """
POWERON
NOTIFY "SmartWatch VM Iniciada"
SETALARM 08:00
x = 10
y = 20
SHOW x + y
HEARTBEAT
POWEROFF
HALT
"""
    
    compiler = Compiler()
    compiler._compile_source(test_code)
    compiler.resolve_jumps()
    
    print("\n=== Bytecode Gerado ===")
    print(disassemble(compiler.bytecode, compiler.strings))
    
    print("\n=== Testando execução ===")
    from vm import VM
    vm = VM(compiler.bytecode, compiler.strings, compiler.next_var_idx)
    vm.run()