; ========================================
; TESTE COMPLETO - Smartwatch Language
; ========================================

; 1. TESTE: Atribuições básicas
x = 10
y = 20
nome = "Smartwatch"

; 2. TESTE: Expressões aritméticas
soma = x + y
subtracao = y - x
multiplicacao = x * 2
divisao = y / 2
complexa = (x + y) * 2 - 5

; 3. TESTE: SHOW com diferentes tipos
SHOW "=== Teste de SHOW ==="
SHOW x
SHOW nome
SHOW soma
SHOW x + y + 10

; 4. TESTE: Instruções do smartwatch
POWERON
SHOWTIME
SETTIME 10:30:00
SETALARM 07:00:00
SETTIMER 60
NOTIFY "Alarme configurado!"
HEARTBEAT
STEP
MUSICPLAY workout
BLUETOOTH ON
MUSICSTOP
BLUETOOTH OFF

; 5. TESTE: Estrutura WHEN-THEN-ELSE
contador = 5
WHEN contador == 5 THEN
  SHOW "Contador está em 5"
  NOTIFY "Valor correto!"
ELSE
  SHOW "Contador diferente de 5"
ENDWHEN

; 6. TESTE: Estrutura WHEN com comparadores
WHEN x < y THEN
  SHOW "x é menor que y"
ENDWHEN

WHEN x <= 10 THEN
  SHOW "x é menor ou igual a 10"
ENDWHEN

WHEN y > x THEN
  SHOW "y é maior que x"
ENDWHEN

WHEN y >= 20 THEN
  SHOW "y é maior ou igual a 20"
ENDWHEN

WHEN x != y THEN
  SHOW "x é diferente de y"
ENDWHEN

; 7. TESTE: Estrutura LOOP
i = 0
limite = 3
SHOW "=== Iniciando loop ==="
LOOP i < limite DO
  SHOW i
  i = i + 1
  STEP
ENDLOOP
SHOW "=== Loop finalizado ==="

; 8. TESTE: Labels e CALL
SHOW "Chamando subrotina..."
CALL subrotina1
SHOW "Voltou da subrotina"

; 9. TESTE: Loop aninhado com WHEN
a = 0
LOOP a < 2 DO
  b = 0
  LOOP b < 2 DO
    WHEN a == b THEN
      SHOW "a igual a b"
    ELSE
      SHOW "a diferente de b"
    ENDWHEN
    b = b + 1
  ENDLOOP
  a = a + 1
ENDLOOP

; 10. TESTE: Subrotinas com labels
subrotina1:
  NOTIFY "Dentro da subrotina 1"
  HEARTBEAT
  CALL subrotina2
  RETURN

subrotina2:
  NOTIFY "Dentro da subrotina 2"
  SHOW "Executando sub-rotina aninhada"
  RETURN

; 11. TESTE: Expressões complexas
resultado = (x + y) * (y - x) / 2
SHOW resultado

; 12. TESTE: Finalização
SHOW "=== Teste completo finalizado ==="
POWEROFF
HALT