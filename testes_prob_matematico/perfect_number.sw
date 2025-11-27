SHOW "Verifica se 6 é perfeito (1+2+3=6)"
num = 6
sum = 0
divisor = 1

LOOP divisor < num DO
    temp = num / divisor
    # Se divisor divide num (temp * divisor == num)
    WHEN temp * divisor == num THEN
        sum = sum + divisor
    ENDWHEN
    divisor = divisor + 1
ENDLOOP

SHOW "Número:"
SHOW num
WHEN sum == num THEN
    SHOW "Perfeito"
ELSE
    SHOW "Não perfeito"
ENDWHEN