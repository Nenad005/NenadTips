# NenadTips

NenadTips je projekat nastao kao istraživanje sportskog arbitražnog klađenja i načina na koji se podaci o kvotama mogu prikupljati, normalizovati i upoređivati između različitih kladionica na Balkanu.

## Kratko objašnjenje arbitražnog klađenja

Arbitražno klađenje je situacija u kojoj se koriste kvote iz više kladionica tako da, kada se pokriju svi mogući ishodi istog događaja, matematički postoji pozitivan ili bar neutralan očekivani rezultat. Ideja je da se pronađe kombinacija kvota čiji zbir implicitnih verovatnoća pada ispod 1.

U praksi to znači da se isti meč prati na više platformi, upoređuju se najbolje dostupne kvote i proverava da li postoji kombinacija koja ostavlja prostor za profit bez obzira na ishod utakmice.

## Kompleksno poklapanje imena

Jedan od najvećih problema u ovakvim projektima nije samo pronalaženje kvota, već prepoznavanje da dve stavke iz različitih izvora zapravo predstavljaju isti meč. Kladionice često upisuju timove različito: skraćenice, dijakritika, različit red reči, dodatni sufiksi poput `FC`, `Utd`, `AS`, ili različiti lokalni nazivi za isti klub.

Zbog toga projekat koristi slojevit pristup poklapanju imena:

1. Normalizacija teksta: uklanjanje dijakritike, specijalnih znakova i viška razmaka.
2. Zamena skraćenica i čestih varijanti punim nazivima.
3. Poređenje inicijala, pojedinačnih reči i sličnosti celog stringa.
4. Dodatno filtriranje da bi se umanjila greška kod kratkih i dvosmislenih naziva.

Takav pristup je potreban zato što jednostavno poređenje stringova nije dovoljno pouzdano za sportske podatke iz više izvora.

## Struktura podataka

Podaci se čuvaju u MongoDB bazi `NenadTips`, po kolekcijama za svaku kladionicu. Svaki dokument predstavlja jedan meč i sadrži osnovne informacije i kvote u ugnježdenoj formi.

Tipična struktura izgleda ovako:

```json
{
	"teams": {
		"home": "...",
		"away": "..."
	},
	"competition": "...",
	"time": "...",
	"match_url": "...",
	"odds": {
		"...": {
			"...": {
				"...": 1.85
			}
		}
	}
}
```

Kvote su organizovane hijerarhijski, jer različite kladionice imaju različite nazive grupa i podgrupa tržišta. Zbog toga se kasnije kvote mapiraju kroz posebne JSON fajlove sa instrukcijama za čitanje duboko ugnježdenih polja.

## Različiti načini scrapovanja podataka

Projekat koristi više pristupa, u zavisnosti od toga kako je sajt tehnički napravljen:

1. Direktni HTTP zahtevi ka backend endpointu, uz proxy kada je potreban za zaobilaženje ograničenja.
2. Selenium automatizacija za dinamičke stranice koje zahtevaju izvršavanje JavaScript-a i interakciju sa DOM-om.
3. Parsiranje HTML-a i izdvajanje podataka iz renderovanog sadržaja pomoću `BeautifulSoup`.
4. Mapiranje sirovih podataka na jedinstvenu internu strukturu pre upisa u bazu.

U ovom projektu se zato mogu videti i API-style pristup i klasično browser-based scrapovanje.

## Korišćene tehnologije

- Python
- MongoDB
- Requests
- Selenium
- BeautifulSoup
- fuzzywuzzy
- pymongo
- JSON za mapiranje i čuvanje struktura
- Lokalni proxy za prosleđivanje zahteva kada je potrebno

## Status projekta

Projekat je zatvoren nakon istraživanja tržišta i praktičnog rada sa podacima iz kladionica. Tokom istraživanja je postalo jasno da kladionice veoma često blokiraju naloge sa dugoročnim uspešnim opkladama, što značajno smanjuje održivost arbitražnog pristupa u realnim uslovima.

Zbog toga je razvoj zaustavljen kao istraživački projekat, a ne kao proizvod namenjen dugotrajnoj upotrebi.
