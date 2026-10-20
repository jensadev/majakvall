# Fruktkontrollen

Bygg en spelkontroll av frukt! Open Minds-brädan känner när du rör en frukt och
låtsas då vara ett tangentbord. Här finns två spel:

- **Akta huvudet** (`akta-huvudet/`): en spelare, två frukter. Gå åt vänster och höger och undvik hagel.
- **Het potatis** (`het-potatis/`): upp till sex spelare med varsin frukt. Kasta potatisen vidare innan den smäller.

## Det här behöver du

- En Open Minds-bräda (den sexkantiga) och en USB-kabel
- Krokodilklämmor, en per frukt
- Frukter eller grönsaker (banan och potatis fungerar, prova gärna fler)
- Chrome eller Edge

## Akta huvudet

### 1. Läs värden

1. Öppna [Open Minds IDE](https://tom-vulpes.github.io/OpenMindsWebInterface/ide.html) och klicka på **Connect board**.
2. Kopiera koden i [`akta-huvudet/1_las_varden.py`](akta-huvudet/1_las_varden.py) till editorn och klicka på **Run code**.
3. Kläm fast en frukt på platta 1 och en på platta 2.
4. Titta i utdatafönstret och rör frukterna. Hur mycket ökar siffran?

### 2. Gör brädan till ett tangentbord

1. Byt ut koden mot [`akta-huvudet/2_fruktkontroll.py`](akta-huvudet/2_fruktkontroll.py) och klicka på **Run code**.
2. Rör inte frukterna medan brädan mäter (en halv sekund).
3. Kalibrera! Följ stegen överst i koden tills det står `RÖRD` i utdatafönstret
   när du rör frukten, och bara då.

### 3. Spela

1. Öppna spelet (länken får du av läraren, eller öppna `akta-huvudet/index.html`).
2. **Klicka på spelplanen**, annars får spelet inga tangenter.
3. Rör en frukt för att börja.

### Testa att ändra

- Byt frukt. Behöver ett äpple en annan gräns än en banan?
- Flytta en frukt till platta 3 och ändra `VANSTER_PLATTA`.
- Byt plats på `VANSTER_PLATTA` och `HOGER_PLATTA`. Kan du fortfarande spela?
- Fungerar det med en gurka? En sked? Din kompis hand?

## Het potatis

1. Sätt er runt brädan. Spelare 1 klämmer fast sin frukt på platta 1, spelare 2 på platta 2 och så vidare.
2. Kopiera koden i [`het-potatis/brada.py`](het-potatis/brada.py) till IDE:t, ändra `ANTAL_SPELARE` och klicka på **Run code**.
3. Kalibrera allas frukter. Följ stegen överst i koden. Varje spelare har sin egen gräns i `GRANS`.
4. Öppna spelet (`het-potatis/index.html`), välj samma antal spelare och **klicka på spelbordet**.
5. Rör en frukt för att börja.

Reglerna: medan du håller potatisen tickar poängen upp, men de sparas först när du kastar
vidare (rör din frukt). Smäller den i din hand förlorar du poängen. Ju längre du håller,
desto troligare är det att den smäller. Vågar du?

## Plattorna

| Platta | Pinne |
|---|---|
| 1 | GP2 |
| 2 | GP3 |
| 3 | GP4 |
| 4 | GP5 |
| 5 | GP18 |
| 6 | GP19 |

Platta 7 och 8 fungerar inte på våra brädor (motstånden saknas).

## För läraren

- Plattorna är kapacitiva, så ingen jordsladd behövs. Kroppen räcker.
- Brädan mäter frukternas startvärde när programmet startar. Kläm fast frukterna först,
  starta sedan om (Run code igen). Byter man frukt mitt i behöver man starta om.
- Reagerar en frukt inte alls? Tryck in klämman ordentligt i fruktköttet, inte bara i skalet,
  och starta om. Plattan kan inte mäta högre än 10000. En väldigt stor eller blöt frukt kan
  slå i taket, och då skriver koden ut en varning.
- Brädan skickar riktiga tangenttryck till datorn. Var den har fokus spelar roll: om
  eleven har editorn markerad flyttar bananen markören i koden (och i Het potatis skrivs siffror).
- Om spelet inte reagerar: titta i spelets panel ("Vad spelet tar emot" eller ringen runt
  spelarna). Lyser den fungerar brädan och problemet är fokus. Lyser den inte, titta efter
  `RÖRD` i IDE:ts utdatafönster.
- Spelen går att testa utan bräda: piltangenterna i Akta huvudet, siffertangenterna 1 till 6
  eller klick på spelarna i Het potatis.
