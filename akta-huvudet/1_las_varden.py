# Steg 1: Läs värden från touchplattorna
# Kör koden och titta i utdatafönstret.
# Rör en frukt och se hur siffran växer!

import board, time, touchio

# Platta 1 och 2. Byt gärna till en annan platta (se listan i README).
vanster = touchio.TouchIn(board.GP2)
hoger = touchio.TouchIn(board.GP3)

while True:
    print("Platta 1:", vanster.raw_value, "   Platta 2:", hoger.raw_value)
    time.sleep(0.2)
