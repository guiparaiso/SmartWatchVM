# Teste de condicionais WHEN/ELSE

x = 10
y = 5

SHOW "=== Teste 1: x > y ==="
WHEN x > y THEN
    SHOW "x é maior que y"
    NOTIFY "Correto!"
ELSE
    SHOW "x NÃO é maior que y"
ENDWHEN

SHOW "=== Teste 2: y == 5 ==="
WHEN y == 5 THEN
    SHOW "y é igual a 5"
ENDWHEN

SHOW "=== Teste 3: x < y ==="
WHEN x < y THEN
    SHOW "x é menor que y"
ELSE
    SHOW "x NÃO é menor que y"
ENDWHEN

SHOW "=== Teste 4: Condicionais aninhados ==="
WHEN x > 0 THEN
    SHOW "x é positivo"
    WHEN x > 5 THEN
        SHOW "x é maior que 5"
    ELSE
        SHOW "x é 5 ou menos"
    ENDWHEN
ENDWHEN

HALT