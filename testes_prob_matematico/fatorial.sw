SHOW "FATORIAL"
# 6! = 720
n = 6
result = 1
i = 1

LOOP i <= n DO
    result = result * i
    i = i + 1
ENDLOOP

SHOW "Fatorial:"
SHOW n
SHOW result