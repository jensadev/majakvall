# Steg 2: Fruktkontrollen
# Brädan låtsas vara ett tangentbord. När du rör en frukt
# trycker brädan på en piltangent, precis som om du tryckte själv.

import board, time, touchio, usb_hid

# ##########################################################
#                   DET HÄR SKA DU ÄNDRA
# ##########################################################

# 1. Vilken platta sitter frukterna på? (1 till 6)
VANSTER_PLATTA = 1
HOGER_PLATTA = 2

# 2. Kalibrera frukterna
#    a) Kör koden och rör INTE frukterna.
#       Titta på siffrorna i utdatafönstret. De ska vara nära 0.
#    b) Håll i en frukt. Hur högt går siffran?
#    c) Välj ett tal mitt emellan och skriv in det nedan.
#    d) Kör igen och testa. Står det RÖRD bara när du rör frukten?
#       Då är du klar!
VANSTER_GRANS = 300
HOGER_GRANS = 300

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

# Tangentkoder som datorn förstår
VANSTERPIL = 0x50
HOGERPIL = 0x4F

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
        raise
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
vanster, vanster_start = starta_platta(VANSTER_PLATTA)
hoger, hoger_start = starta_platta(HOGER_PLATTA)
print("Klart! Rör en frukt.")

nedtryckta = []
senast_utskrift = 0

while True:
    vanster_varde = vanster.raw_value - vanster_start
    hoger_varde = hoger.raw_value - hoger_start

    vanster_rord = vanster_varde > VANSTER_GRANS
    hoger_rord = hoger_varde > HOGER_GRANS

    tryck_nu = []
    if vanster_rord:
        tryck_nu.append(VANSTERPIL)
    if hoger_rord:
        tryck_nu.append(HOGERPIL)

    # Skicka bara när något har ändrats
    if tryck_nu != nedtryckta:
        skicka_tangenter(tryck_nu)
        nedtryckta = tryck_nu

    if time.monotonic() - senast_utskrift > 0.3:
        print(
            "vänster: {:5d} {:4s}   |   höger: {:5d} {:4s}".format(
                vanster_varde, "RÖRD" if vanster_rord else "",
                hoger_varde, "RÖRD" if hoger_rord else "",
            )
        )
        senast_utskrift = time.monotonic()

    time.sleep(0.01)
