# Busca um número específico em um intervalo

SHOW "=== Buscando número 7 entre 1 e 10 ==="

encontrado = 0
n = 1

LOOP n <= 10 DO
    
    WHEN encontrado == 0 THEN
        
        SHOW "Testando:"
        SHOW n
        
        WHEN n == 7 THEN
            SHOW "*** ENCONTRADO! ***"
            encontrado = 1
        ELSE
            SHOW "Não é 7, continuando..."
        ENDWHEN
        
    ENDWHEN
    
    n = n + 1
ENDLOOP

WHEN encontrado == 1 THEN
    NOTIFY "Número 7 foi encontrado!"
ELSE
    NOTIFY "Número 7 NÃO foi encontrado!"
ENDWHEN

HALT