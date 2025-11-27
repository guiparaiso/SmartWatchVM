# ======================================
# TESTE COMPLETO - OPERAÇÕES ARITMÉTICAS
# ======================================

SHOW "=== OPERAÇÕES BÁSICAS ==="
SHOW 5 + 3    # 8
SHOW 10 - 4   # 6
SHOW 6 * 7    # 42
SHOW 15 / 3   # 5
SHOW 7 / 2    # 3 (divisão inteira)

SHOW "=== SEM ESPAÇOS ==="
SHOW 5+3      # 8
SHOW 10-4     # 6  
SHOW 6*7      # 42
SHOW 15/3     # 5

SHOW "=== OPERADORES UNÁRIOS ==="
SHOW +5       # 5
SHOW -5       # -5
SHOW ++5      # 5
SHOW --5      # 5
SHOW +-5      # -5
SHOW -+5      # -5
SHOW 1+----1  # 2 (1 + -(-(-(-1))) = 1 + 1 = 2)

SHOW "=== EXPRESSÕES COMPLEXAS ==="
SHOW 2 + 3 * 4      # 14 (precedência)
SHOW (2 + 3) * 4    # 20 (parênteses)
SHOW 10 - 5 - 2     # 3 (associatividade)
SHOW 20 / 4 / 2     # 2 (associatividade)

SHOW "=== COM VARIÁVEIS ==="
a = 10
b = 3
c = -2
SHOW a + b          # 13
SHOW a - b          # 7
SHOW a * b          # 30
SHOW a + c          # 8 (10 + (-2))
SHOW b * c          # -6 (3 * (-2))
SHOW -a + b         # -7 (-10 + 3)

SHOW "=== CASOS DE BORDA ==="
SHOW 0 + 0          # 0
SHOW 0 * 5          # 0
SHOW 5 * 0          # 0
SHOW 1 / 1          # 1
SHOW 0 / 5          # 0
# SHOW 5 / 0        # Erro (divisão por zero)

SHOW "=== EXPRESSÕES MISTAS ==="
SHOW 2 * -3         # -6
SHOW -4 * -5        # 20
SHOW 10 + -2        # 8
SHOW -8 / 2         # -4
SHOW 10 - -5        # 15

SHOW "=== FIM DOS TESTES ==="
POWERON
NOTIFY "Testes aritméticos concluídos!"
POWEROFF
HALT