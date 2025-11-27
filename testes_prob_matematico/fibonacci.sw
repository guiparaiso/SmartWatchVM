SHOW "# Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13..."
n = 10
a = 0
b = 1
count = 0

SHOW "Fibonacci:"

LOOP count < n DO
    SHOW a
    temp = a + b
    a = b
    b = temp
    count = count + 1
ENDLOOP