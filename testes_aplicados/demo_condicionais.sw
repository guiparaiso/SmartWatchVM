# ============================================
# TESTE 2: Estruturas Condicionais
# Testa: WHEN/THEN/ELSE, comparadores
# ============================================

SHOW "=== Teste de Condicionais ==="

# Teste 1: Comparação maior/menor
temperatura = 25
SHOW "Temperatura: 25°C"

WHEN temperatura > 30 THEN
    SHOW "Clima: QUENTE"
ELSE
    WHEN temperatura < 15 THEN
        SHOW "Clima: FRIO"
    ELSE
        SHOW "Clima: AGRADÁVEL"
    ENDWHEN
ENDWHEN

# Teste 2: Comparação de igualdade
passos = 10000
meta = 10000
SHOW "Passos: 10000, Meta: 10000"

WHEN passos == meta THEN
    SHOW "Meta atingida!"
    NOTIFY "Parabéns!"
ELSE
    SHOW "Meta não atingida"
ENDWHEN

# Teste 3: Comparações diversas
a = 15
b = 20
SHOW "a = 15, b = 20"

WHEN a < b THEN
    SHOW "a < b: VERDADEIRO"
ENDWHEN

WHEN a <= 15 THEN
    SHOW "a <= 15: VERDADEIRO"
ENDWHEN

WHEN a != b THEN
    SHOW "a != b: VERDADEIRO"
ENDWHEN

WHEN b >= 20 THEN
    SHOW "b >= 20: VERDADEIRO"
ENDWHEN

SHOW "=== Teste de Condicionais Completo ==="
HALT