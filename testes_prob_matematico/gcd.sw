SHOW "GCD de 56 e 98 = 14"
# GCD de 56 e 98 = 14 (algoritmo de Euclides com subtração)
a = 56
b = 98

SHOW "Calculando GCD"
SHOW a
SHOW b

LOOP a != b DO
    WHEN a > b THEN
        a = a - b
    ELSE
        b = b - a
    ENDWHEN
ENDLOOP

SHOW "Resultado:"
SHOW a