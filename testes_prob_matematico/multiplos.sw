SHOW "Encontra múltiplos de 3 até 20"
number = 3
limit = 20
current = number

SHOW "Múltiplos de:"
SHOW number

LOOP current <= limit DO
    SHOW current
    current = current + number
ENDLOOP