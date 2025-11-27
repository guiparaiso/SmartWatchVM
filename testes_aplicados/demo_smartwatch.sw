# ============================================
# TESTE 4: Aplicação Smartwatch Completa
# Testa: todas as instruções do smartwatch,
# estruturas aninhadas, fluxo complexo
# ============================================

POWERON
NOTIFY "SmartWatch iniciado!"
SHOWTIME

SHOW "=== Rotina Diária do SmartWatch ==="

# Configuração inicial
SETTIME 07:00:00
SETALARM 07:30:00
BLUETOOTH ON

# Monitoramento de batimentos
batimentos = 72
SHOW "Batimentos cardíacos: 72 bpm"

WHEN batimentos > 100 THEN
    NOTIFY "ALERTA: Batimentos elevados!"
    HEARTBEAT
ELSE
    WHEN batimentos < 60 THEN
        NOTIFY "ALERTA: Batimentos baixos!"
        HEARTBEAT
    ELSE
        NOTIFY "Batimentos normais"
        HEARTBEAT
    ENDWHEN
ENDWHEN

# Rotina de exercícios com séries
SHOW "Iniciando exercícios..."
MUSICPLAY workout

serie = 1
LOOP serie <= 3 DO
    SHOW "--- Série:"
    SHOW serie
    
    # Contador de passos por série
    passos = 0
    meta_passos = 10
    
    LOOP passos < meta_passos DO
        STEP
        passos = passos + 1
        
        # Feedback no meio da série
        WHEN passos == 5 THEN
            NOTIFY "Metade da série!"
        ENDWHEN
    ENDLOOP
    
    SHOW "Série completa!"
    serie = serie + 1
ENDLOOP

# Timer de descanso
SHOW "Tempo de descanso..."
SETTIMER 30
MUSICSTOP

# Verificação final
passos_totais = 30
meta_diaria = 30

WHEN passos_totais >= meta_diaria THEN
    NOTIFY "META DIÁRIA ATINGIDA!"
    SHOW "Parabéns! Meta completa."
ELSE
    faltam = meta_diaria - passos_totais
    SHOW "Faltam passos:"
    SHOW faltam
ENDWHEN

# Finalização
SHOW "Rotina finalizada!"
BLUETOOTH OFF
POWEROFF
HALT