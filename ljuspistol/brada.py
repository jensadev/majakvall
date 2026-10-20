# Ljuspistolen: skjut ankor med ett pappersrör
# Avtryckaren är en krokodilklämma på röret. Röret är siktet.
#
# Hur kan spelet veta om du träffade? Se mysteriet i README:n.
# Svaret står i koden längre ner, om du vågar läsa den!

import board, time, touchio, analogio, usb_hid

# ##########################################################
#                   DET HÄR SKA DU ÄNDRA
# ##########################################################

# 1. Vilken platta sitter avtryckaren på? (1 till 6)
AVTRYCKARE_PLATTA = 1

# 2. Kalibrera avtryckaren
#    a) Kör koden och rör INTE avtryckaren. Siffran ska vara nära 0.
#    b) Håll i avtryckaren. Hur högt går siffran?
#    c) Välj ett tal mitt emellan och skriv in det här.
AVTRYCKARE_GRANS = 300

# 3. Kalibrera siktet
#    a) Öppna spelet, rikta röret mot anden och skjut några gånger.
#       Titta på "skillnad" i utdatafönstret.
#    b) Skjut några gånger när du pekar bredvid anden.
#    c) Välj ett tal mitt emellan och skriv in det här.
TRAFF_GRANS = 80

# ##########################################################
#           HÄRIFRÅN BEHÖVER DU INTE ÄNDRA NÅGOT
# ##########################################################

PINNAR = {
    1: board.GP2,
    2: board.GP3,
    3: board.GP4,
    4: board.GP5,
    5: board.GP18,
    6: board.GP19,
}

# Tangenter som inte skriver något, så att inget hamnar i koden av misstag
SKOTT = 0x52      # pil upp
TRAFF = 0x4B      # Page Up
MISS = 0x4E       # Page Down

# Spelet visar svart i 300 ms och sedan den vita rutan i 400 ms.
# Ändrar du här måste du ändra i spelet också.
MORKT_FRAN, MORKT_TILL = 0.15, 0.30   # sekunder efter skottet
LJUST_FRAN, LJUST_TILL = 0.30, 0.80

# True = skriv ut sensorns värden under hela skottet (för felsökning)
VISA_KURVA = True

ldr = analogio.AnalogIn(board.GP28)

tangentbord = None
for enhet in usb_hid.devices:
    if enhet.usage_page == 0x01 and enhet.usage == 0x06:
        tangentbord = enhet
if tangentbord is None:
    print("Hittar inget USB-tangentbord. Siffrorna syns, men spelet får inga skott.")


def tryck(kod):
    # Tryck ner och släpp en tangent
    if tangentbord is None:
        return
    rapport = bytearray(8)
    rapport[2] = kod
    tangentbord.send_report(rapport)
    tangentbord.send_report(bytearray(8))


def skjut():
    start = time.monotonic()
    tryck(SKOTT)

    morka = []
    ljusa = []    # (tid, värde) under den vita fasen
    kurva = []    # ett värde var 50:e ms, för felsökning
    nasta_kurvpunkt = 0
    while True:
        t = time.monotonic() - start
        if t > LJUST_TILL:
            break
        varde = ldr.value
        if MORKT_FRAN <= t < MORKT_TILL:
            morka.append(varde)
        elif t >= LJUST_FRAN:
            ljusa.append((t, varde))
        if t >= nasta_kurvpunkt:
            kurva.append(str(int(t * 1000)) + ":" + str(varde))
            nasta_kurvpunkt += 0.05
        time.sleep(0.002)

    if VISA_KURVA:
        print("kurva (ms:värde):", " ".join(kurva))

    morkt = sum(morka) // len(morka)
    # På vissa brädor ger ljus högre värde, på andra lägre. Vi räknar med båda.
    skillnad = max(abs(v - morkt) for t, v in ljusa)
    traff = skillnad > TRAFF_GRANS
    tryck(TRAFF if traff else MISS)

    # Hur lång tid tog det från skottet tills sensorn såg halva ljuset?
    fordrojning = "-"
    if skillnad > 0:
        for t, v in ljusa:
            if abs(v - morkt) > skillnad / 2:
                fordrojning = str(int(t * 1000)) + " ms"
                break

    print("PANG!  skillnad:", skillnad, "  ", "TRÄFF" if traff else "miss",
          "   ljuset syntes efter:", fordrojning)


print("Rör inte avtryckaren, mäter...")
time.sleep(0.5)
try:
    avtryckare = touchio.TouchIn(PINNAR[AVTRYCKARE_PLATTA])
except ValueError:
    print("Platta", AVTRYCKARE_PLATTA, "ger för höga värden redan från start.")
    print("  Kolla att inget stort eller blött sitter fast i klämman.")
    raise
summa = 0
for i in range(20):
    summa += avtryckare.raw_value
    time.sleep(0.01)
startvarde = summa // 20
print("Klart! Rör avtryckaren för att skjuta.")

var_rord = False
senast_utskrift = 0

while True:
    varde = avtryckare.raw_value - startvarde
    rord = varde > AVTRYCKARE_GRANS

    if rord and not var_rord:
        skjut()
    var_rord = rord

    if time.monotonic() - senast_utskrift > 0.5:
        print("avtryckare: {:5d} {}".format(varde, "RÖRD" if rord else ""))
        senast_utskrift = time.monotonic()

    time.sleep(0.01)
