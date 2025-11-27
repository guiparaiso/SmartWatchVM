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
            condition = line[5:].strip()
            if condition.endswith(' THEN'):
                condition = condition[:-5].strip()
            
            print(f"  🔵 WHEN: compilando condição '{condition}'")
            
            # Compila a condição
            self._compile_expression(condition)
            
            # Se falso, pula para ELSE ou ENDWHEN
            # Cria label único
            import time
            else_label = f"__else_{int(time.time() * 1000000)}"
            
            # Guarda o label no contexto (usa uma pilha de contextos)
            if not hasattr(self, 'context_stack'):
                self.context_stack = []
            self.context_stack.append({'else_label': else_label, 'end_label': None})
            
            # JZ = Jump if Zero (se condição for falsa/0)
            self.emit_jump(OP_JZ, else_label)
            return
        
        # ELSE
        if line == 'ELSE':
            if not hasattr(self, 'context_stack') or not self.context_stack:
                print("❌ ELSE sem WHEN")
                return
            
            context = self.context_stack[-1]
            
            # Cria label para fim do WHEN
            import time
            end_label = f"__end_{int(time.time() * 1000000)}"
            context['end_label'] = end_label
            
            # Pula o ELSE (quando THEN é verdadeiro)
            self.emit_jump(OP_JMP, end_label)
            
            # Define o label do ELSE
            self.define_label(context['else_label'])
            return
        
        # ENDWHEN
        if line == 'ENDWHEN':
            if not hasattr(self, 'context_stack') or not self.context_stack:
                print("❌ ENDWHEN sem WHEN")
                return
            
            context = self.context_stack.pop()
            
            # Se não teve ELSE, define o else_label aqui
            if context['end_label'] is None:
                self.define_label(context['else_label'])
            else:
                # Se teve ELSE, define o end_label
                self.define_label(context['end_label'])
            return
        
        # LOOP condition DO
        if line.startswith('LOOP '):
            condition = line[5:].strip()
            if condition.endswith(' DO'):
                condition = condition[:-3].strip()
            
            print(f"  🔵 LOOP: compilando condição '{condition}'")
            
            # Marca o início do loop
            import time
            loop_start = f"__loop_start_{int(time.time() * 1000000)}"
            loop_end = f"__loop_end_{int(time.time() * 1000000)}"
            
            self.define_label(loop_start)
            
            # Compila a condição
            self._compile_expression(condition)
            
            # Se falso, sai do loop
            self.emit_jump(OP_JZ, loop_end)
            
            # Guarda contexto do loop
            if not hasattr(self, 'context_stack'):
                self.context_stack = []
            self.context_stack.append({'loop_start': loop_start, 'loop_end': loop_end})
            return
        
        # ENDLOOP
        if line == 'ENDLOOP':
            if not hasattr(self, 'context_stack') or not self.context_stack:
                print("❌ ENDLOOP sem LOOP")
                return
            
            context = self.context_stack.pop()
            
            # Volta para o início do loop
            self.emit_jump(OP_JMP, context['loop_start'])
            
            # Define label de saída
            self.define_label(context['loop_end'])
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
        """Compila uma expressão matemática completa"""
        print(f"🔍 [COMPILER] Compilando expressão: '{expr}'")
        
        expr = expr.strip()
        
        # 1. STRING
        if expr.startswith('"') and expr.endswith('"'):
            string_val = expr[1:-1]
            str_idx = self.get_string_index(string_val)
            string_offset = 1000 + str_idx
            print(f"  ✅ STRING: '{string_val}' -> offset {string_offset}")
            self.emit(OP_PUSH, string_offset)
            return
        
        # 2. PARÊNTESES
        if expr.startswith('('):
            depth = 1
            for i in range(1, len(expr)):
                if expr[i] == '(': depth += 1
                elif expr[i] == ')': depth -= 1
                if depth == 0:
                    inner = expr[1:i]
                    remaining = expr[i+1:].strip()
                    print(f"  ✅ PARÊNTESES: ({inner}), resto: '{remaining}'")
                    self._compile_expression(inner)
                    if remaining:
                        # Processa resto como nova expressão binária
                        for j, op in enumerate(remaining):
                            if op in ['+', '-', '*', '/']:
                                right = remaining[j+1:].strip()
                                self._compile_expression(right)
                                if op == '+': self.emit(OP_ADD)
                                elif op == '-': self.emit(OP_SUB)
                                elif op == '*': self.emit(OP_MUL)
                                elif op == '/': self.emit(OP_DIV)
                                return
                    return
        
        # 3. COMPARADORES
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
        
        # 4. NÚMERO
        try:
            value = int(expr)
            print(f"  ✅ NÚMERO: '{expr}' -> PUSH {value}")
            self.emit(OP_PUSH, value)
            return
        except ValueError:
            pass
        
        # 5. VARIÁVEL
        if expr.isidentifier():
            var_idx = self.get_var_index(expr)
            print(f"  ✅ VARIÁVEL: '{expr}' -> LOAD {var_idx}")
            self.emit(OP_LOAD, var_idx)
            return
        
        # 6. OPERADOR UNÁRIO no início
        if expr[0] in ['-', '+']:
            # Encontra onde termina o operando do unário
            i = 0
            while i < len(expr) and expr[i] in ['-', '+']:
                i += 1
            
            # Agora procura o fim do operando (até próximo operador binário)
            depth = 0
            operand_end = len(expr)
            
            for j in range(i, len(expr)):
                if expr[j] == '(': 
                    depth += 1
                elif expr[j] == ')': 
                    depth -= 1
                elif depth == 0 and expr[j] in ['+', '-', '*', '/']:
                    # Encontrou operador binário
                    operand_end = j
                    break
            
            unary_part = expr[:i]
            operand = expr[i:operand_end].strip()
            remaining = expr[operand_end:].strip()
            
            print(f"  ✅ UNÁRIO: '{unary_part}' em '{operand}', resto: '{remaining}'")
            
            # Compila o operando
            self._compile_expression(operand)
            
            # Aplica negação se necessário
            if unary_part.count('-') % 2 == 1:
                self.emit(OP_PUSH, -1)
                self.emit(OP_MUL)
            
            # Se tem resto, processa como binário
            if remaining:
                op = remaining[0]
                right = remaining[1:].strip()
                self._compile_expression(right)
                if op == '+': self.emit(OP_ADD)
                elif op == '-': self.emit(OP_SUB)
                elif op == '*': self.emit(OP_MUL)
                elif op == '/': self.emit(OP_DIV)
            
            return
        
        # 7. OPERADORES BINÁRIOS
        # Procura + e - (menor precedência) - ÚLTIMO da esquerda para direita
        depth = 0
        last_add_sub = -1

        for i in range(len(expr)):
            if expr[i] == '(': depth += 1
            elif expr[i] == ')': depth -= 1
            
            if depth == 0 and expr[i] in ['+', '-']:
                # Verifica se não é unário
                if i > 0:
                    before = expr[:i].rstrip()
                    if before and before[-1] not in ['+', '-', '*', '/', '(']:
                        last_add_sub = i  # Atualiza sempre = pega o ÚLTIMO

        if last_add_sub != -1:
            op = expr[last_add_sub]
            left = expr[:last_add_sub].strip()
            right = expr[last_add_sub+1:].strip()
            print(f"  ✅ Binário '{op}': left='{left}', right='{right}'")
            self._compile_expression(left)
            self._compile_expression(right)
            if op == '+': self.emit(OP_ADD)
            else: self.emit(OP_SUB)
            return

        # Procura * e / (maior precedência) - ÚLTIMO
        depth = 0
        last_mul_div = -1

        for i in range(len(expr)):
            if expr[i] == '(': depth += 1
            elif expr[i] == ')': depth -= 1
            
            if depth == 0 and expr[i] in ['*', '/']:
                if i > 0:
                    before = expr[:i].rstrip()
                    if before and before[-1] not in ['+', '-', '*', '/', '(']:
                        last_mul_div = i  # Pega o ÚLTIMO

        if last_mul_div != -1:
            op = expr[last_mul_div]
            left = expr[:last_mul_div].strip()
            right = expr[last_mul_div+1:].strip()
            print(f"  ✅ Binário '{op}': left='{left}', right='{right}'")
            self._compile_expression(left)
            self._compile_expression(right)
            if op == '*': self.emit(OP_MUL)
            else: self.emit(OP_DIV)
            return
                
        # NÃO RECONHECIDO
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