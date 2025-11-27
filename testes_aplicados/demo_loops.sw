# ============================================
# TESTE 3: Estruturas de Repetição
# Testa: LOOP/DO/ENDLOOP, aninhamento
# ============================================

SHOW "=== Teste de Loops ==="

# Loop simples: contagem
SHOW "Contagem de 1 a 5:"
contador = 1
LOOP contador <= 5 DO
    SHOW contador
    contador = contador + 1
ENDLOOP

# Loop com condicional: pares e ímpares
SHOW "Números pares de 0 a 10:"
n = 0
LOOP n <= 10 DO
    # Simula módulo: se n/2*2 == n, então é par
    metade = n / 2
    dobro = metade * 2
    
    WHEN dobro == n THEN
        SHOW n
    ENDWHEN
    
    n = n + 1
ENDLOOP

# Loop aninhado: tabuada
SHOW "Tabuada (3 x 3):"
i = 1
LOOP i <= 3 DO
    j = 1
    LOOP j <= 3 DO
        resultado = i * j
        SHOW resultado
        j = j + 1
    ENDLOOP
    i = i + 1
ENDLOOP

# Loop com break simulado (flag)
SHOW "Busca pelo número 7:"
encontrado = 0
busca = 1
LOOP busca <= 10 DO
    WHEN encontrado == 0 THEN
        WHEN busca == 7 THEN
            SHOW "Encontrado: 7"
            encontrado = 1
        ENDWHEN
        busca = busca + 1
    ENDWHEN
ENDLOOP

SHOW "=== Teste de Loops Completo ==="
HALT