# Ljuspistol, test: kan ljussensorn se skillnad på svart och vit skärm?
# Öppna testsidan, rikta röret mot skärmen och titta i utdatafönstret.
# Varje sekund skrivs det lägsta och högsta värdet under den sekunden ut.
# Stor skillnad = sensorn ser blinkningarna tydligt.

import board, time, analogio

ldr = analogio.AnalogIn(board.GP28)

while True:
    lagst = 65535
    hogst = 0
    slut = time.monotonic() + 1.0
    while time.monotonic() < slut:
        varde = ldr.value
        lagst = min(lagst, varde)
        hogst = max(hogst, varde)
        time.sleep(0.002)
    print("lägst:", lagst, "  högst:", hogst, "  skillnad:", hogst - lagst)
