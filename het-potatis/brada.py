# Het potatis: fruktkontroll för upp till 6 spelare
# Varje spelare har en frukt på sin platta. När du rör din frukt
# trycker brädan på din siffertangent (spelare 1 = tangent 1 och så vidare).

import board, time, touchio, usb_hid

# ##########################################################
#                   DET HÄR SKA DU ÄNDRA
# ##########################################################

# 1. Hur många spelare är ni? (2 till 6)
#    Spelare 1 har platta 1, spelare 2 har platta 2 och så vidare.
ANTAL_SPELARE = 6

# 2. Kalibrera frukterna, en i taget
#    a) Kör koden och rör INTE frukterna.
#       Titta på siffrorna i utdatafönstret. De ska vara nära 0.
#    b) Håll i en frukt. Hur högt går dess siffra?
#    c) Välj ett tal mitt emellan och skriv in det vid rätt spelare.
#    d) Kör igen och testa. Står det RÖRD bara när du rör frukten?
#       Då är den frukten klar!
GRANS = {
    1: 300,
    2: 300,
    3: 300,
    4: 300,
    5: 300,
    6: 300,
}

# ##########################################################
#           HÄRIFRÅN BEHÖVER DU INTE ÄNDRA NÅGOT
# ##########################################################

# Plattornas nummer och vilken pinne de sitter på.
# Platta 7 (GP20) och 8 (GP21) fungerar inte på våra brädor.
PINNAR = {
    1: board.GP2,
    2: board.GP3,
    3: board.GP4,
    4: board.GP5,
    5: board.GP18,
    6: board.GP19,
}

# Tangentkoder för siffrorna 1 till 6
TANGENTKODER = {1: 0x1E, 2: 0x1F, 3: 0x20, 4: 0x21, 5: 0x22, 6: 0x23}

# Högre än så här kan touchplattan inte mäta
TAK = 10000

# Leta upp brädans tangentbord
tangentbord = None
for enhet in usb_hid.devices:
    if enhet.usage_page == 0x01 and enhet.usage == 0x06:
        tangentbord = enhet
if tangentbord is None:
    print("Hittar inget USB-tangentbord. Siffrorna syns, men inga tangenter skickas.")


def skicka_tangenter(koder):
    # Ett tangentbord skickar 8 byte: 2 för shift med mera, sedan upp till 6 tangenter
    if tangentbord is None:
        return
    rapport = bytearray(8)
    for i, kod in enumerate(koder):
        rapport[2 + i] = kod
    tangentbord.send_report(rapport)


def starta_platta(nr):
    try:
        platta = touchio.TouchIn(PINNAR[nr])
    except ValueError:
        print("Platta", nr, "ger för höga värden redan från start.")
        print("  Frukten är kanske för stor eller blöt. Prova en mindre frukt.")
        return None, 0
    # Mät värdet när ingen rör frukten, så vet vi var noll är
    summa = 0
    for i in range(20):
        summa += platta.raw_value
        time.sleep(0.01)
    start = summa // 20
    if start > TAK - 1000:
        print("Varning: platta", nr, "är nära taket (" + str(start) + " av " + str(TAK) + ").")
        print("  Den kan ha svårt att känna när du rör frukten. Prova en mindre frukt.")
    return platta, start


print("Rör inte frukterna, mäter...")
time.sleep(0.5)
plattor = {}
startvarde = {}
for nr in range(1, ANTAL_SPELARE + 1):
    platta, start = starta_platta(nr)
    if platta is not None:
        plattor[nr] = platta
        startvarde[nr] = start
print("Klart! Rör en frukt.")

nedtryckta = []
senast_utskrift = 0

while True:
    tryck_nu = []
    rader = []

    for nr, platta in plattor.items():
        varde = platta.raw_value - startvarde[nr]
        rord = varde > GRANS[nr]
        if rord:
            tryck_nu.append(TANGENTKODER[nr])
        rader.append("{}: {:4d} {:4s}".format(nr, varde, "RÖRD" if rord else ""))

    # Skicka bara när något har ändrats
    if tryck_nu != nedtryckta:
        skicka_tangenter(tryck_nu)
        nedtryckta = tryck_nu

    if time.monotonic() - senast_utskrift > 0.3:
        print(" | ".join(rader))
        senast_utskrift = time.monotonic()

    time.sleep(0.01)
