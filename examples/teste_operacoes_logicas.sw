# ======================================
# TESTE COMPLETO - OPERAÇÕES LÓGICAS
# ======================================

# 1. TESTE BÁSICO DE COMPARADORES
SHOW "=== COMPARADORES BÁSICOS ==="
SHOW 10 == 10    # True
SHOW 10 == 5     # False
SHOW 10 != 5     # True  
SHOW 10 != 10    # False
SHOW 10 > 5      # True
SHOW 5 > 10      # False
SHOW 10 < 5      # False
SHOW 5 < 10      # True
SHOW 10 >= 10    # True
SHOW 10 >= 5     # True
SHOW 5 >= 10     # False
SHOW 10 <= 10    # True
SHOW 5 <= 10     # True
SHOW 10 <= 5     # False

# 2. TESTE COM VARIÁVEIS
SHOW "=== COM VARIÁVEIS ==="
x = 15
y = 20
z = 15

SHOW x == z      # True (15 == 15)
SHOW x == y      # False (15 == 20)
SHOW x != y      # True (15 != 20)
SHOW x < y       # True (15 < 20)
SHOW y > x       # True (20 > 15)
SHOW x >= z      # True (15 >= 15)
SHOW y <= x      # False (20 <= 15)

# 3. TESTE DE EXPRESSÕES COMPLEXAS
SHOW "=== EXPRESSÕES COMPLEXAS ==="
a = 5
b = 10
c = 15

SHOW (a + b) == c          # True (5+10=15)
SHOW (b * 2) > (a + c)     # True (20 > 20? False)
SHOW (c - a) != b          # False (10 != 10? False)
SHOW (a * b) >= 50         # True (50 >= 50)
SHOW (b / 2) < a           # False (5 < 5? False)

# 4. TESTE DE LÓGICA BOOLEANA COMBINADA
SHOW "=== LÓGICA COMBINADA ==="
SHOW (5 < 10) == (10 > 5)          # True (True == True)
SHOW (5 == 5) != (10 == 5)         # True (True != False)
SHOW (10 >= 10) == (5 <= 5)        # True (True == True)

# 5. TESTE DE BORDAS
SHOW "=== CASOS DE BORDA ==="
SHOW 0 == 0                # True
SHOW 0 == 1                # False  
SHOW 1 == 1                # True
SHOW -5 < 0                # True
SHOW 1000 > 999            # True
SHOW 1 != 0                # True

# 6. TESTE COM STRINGS (para garantir que ainda funcionam)
SHOW "=== STRINGS ==="
SHOW "Hello"
SHOW "True"
SHOW "False"

SHOW "=== FIM DOS TESTES ==="
POWERON
NOTIFY "Testes de operações lógicas concluídos!"
POWEROFF
HALT