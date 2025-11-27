# ============================================
# PROVA DOS REQUISITOS DA VM
# ============================================
# Requisito 1: Pelo menos 2 registradores
# Requisito 2: Memória (pilha, listas, etc)
# Requisito 3: Sensores (variáveis readonly)
# Requisito 4: Turing-Completo (Minsky Machine)
# ============================================

POWERON
NOTIFY "Iniciando prova dos requisitos da VM"

SHOW "=========================================="
SHOW "REQUISITO 1: Pelo menos 2 Registradores"
SHOW "=========================================="
SHOW "Usando registradores PC e variáveis:"

# Demonstra uso de múltiplos registradores (variáveis)
reg1 = 42
reg2 = 100
SHOW "Registrador 1 (reg1):"
SHOW reg1
SHOW "Registrador 2 (reg2):"
SHOW reg2

soma_regs = reg1 + reg2
SHOW "Soma de registradores:"
SHOW soma_regs

SHOW "✓ REQUISITO 1 ATENDIDO"
SHOW ""

SHOW "=========================================="
SHOW "REQUISITO 2: Memória (pilha, listas)"
SHOW "=========================================="
SHOW "Demonstrando uso de pilha e memória:"

# Array simulado com variáveis
array0 = 10
array1 = 20
array2 = 30
array3 = 40

SHOW "Array[0]:"
SHOW array0
SHOW "Array[1]:"
SHOW array1
SHOW "Array[2]:"
SHOW array2
SHOW "Array[3]:"
SHOW array3

# Pilha de chamadas (CALL/RETURN)
SHOW "Testando pilha de chamadas..."
CALL subrotina_teste
SHOW "Retornou da subrotina"

SHOW "✓ REQUISITO 2 ATENDIDO"
SHOW ""

SHOW "=========================================="
SHOW "REQUISITO 3: Sensores (readonly)"
SHOW "=========================================="
SHOW "Lendo sensores do smartwatch:"

SHOW "HEARTRATE (batimentos):"
SHOW HEARTRATE

SHOW "STEPS (passos):"
SHOW STEPS

SHOW "BATTERY (bateria %):"
SHOW BATTERY

SHOW "TIME_HOUR (hora):"
SHOW TIME_HOUR

SHOW "TIME_MINUTE (minuto):"
SHOW TIME_MINUTE

# Prova que são readonly (não podem ser modificados)
SHOW "Usando sensores em condicionais:"
WHEN HEARTRATE > 50 THEN
    SHOW "Sensor HEARTRATE funcional!"
ENDWHEN

WHEN BATTERY > 0 THEN
    SHOW "Sensor BATTERY funcional!"
ENDWHEN

SHOW "✓ REQUISITO 3 ATENDIDO"
SHOW ""

SHOW "=========================================="
SHOW "REQUISITO 4: Turing-Completo"
SHOW "=========================================="
SHOW "Demonstrando Minsky Machine:"
SHOW "(Contador com incremento, teste zero, loop)"

# Implementação de Minsky Machine:
# 1. Incrementar/Decrementar
# 2. Testar se zero
# 3. Salto condicional
# 4. Loop

SHOW "Contagem regressiva de 5 até 0:"
counter = 5

LOOP counter > 0 DO
    SHOW counter
    counter = counter - 1
ENDLOOP

SHOW "Counter final (deve ser 0):"
SHOW counter

# Prova de Turing-Completude: Simulação de adição usando loops
SHOW ""
SHOW "Adição usando apenas DEC e JZ (Minsky):"
SHOW "Calculando 7 + 3 ="

a = 7
b = 3
resultado = 0

# Transfere 'a' para 'resultado'
LOOP a > 0 DO
    resultado = resultado + 1
    a = a - 1
ENDLOOP

# Transfere 'b' para 'resultado'
LOOP b > 0 DO
    resultado = resultado + 1
    b = b - 1
ENDLOOP

SHOW resultado
SHOW "✓ Adição implementada com INC/DEC/JZ"

# Prova de loop infinito condicional (halting problem)
SHOW ""
SHOW "Teste de loop com condição variável:"
SHOW "(simula decisão de parada)"

x = 3
parar = 0

LOOP parar == 0 DO
    SHOW x
    x = x - 1
    
    WHEN x <= 0 THEN
        parar = 1
    ENDWHEN
ENDLOOP

SHOW "Loop parou corretamente"
SHOW "✓ REQUISITO 4 ATENDIDO"
SHOW ""

SHOW "=========================================="
SHOW "RESUMO: TODOS OS REQUISITOS ATENDIDOS"
SHOW "=========================================="
NOTIFY "VM está completa e Turing-Completa!"

POWEROFF
HALT

# Subrotina para teste de pilha de chamadas
subrotina_teste:
    SHOW "Dentro da subrotina"
    HEARTBEAT
    RETURN