# Piano: 500 € in 30 giorni

> **Aggiornamento (decisioni prese):** strada scelta = **prodotto digitale**, nessuna email dal tuo Gmail.
> Il Label Kit è **già costruito e pronto da caricare**: `label-kit/label-kit.zip` (37 file, 4,5 MB).
> Immagini listing in `label-kit/listing/`, mockup in `label-kit/mockup/`, scheda in `prodotto-digitale.md`, post in `social-post.md`.
>
> **Le uniche 3 cose che devi fare tu (circa 40 minuti totali):**
> 1. Apri un account Gumroad (gumroad.com, gratuito) e collega conto/PayPal. Carica `label-kit.zip`, incolla titolo e descrizione da `prodotto-digitale.md`, prezzo 29 €, carica le 3 immagini di `listing/` + 5 mockup.
> 2. Incollami il link Gumroad: lo metto nella landing (sostituisce `GUMROAD_URL`) e la pubblico.
> 3. Pubblica i post di `social-post.md` (1 ogni 3 giorni) e, se vuoi il canale con più traffico organico, apri anche Etsy (0,20 $ per listing).
>
> **Beneficenza:** i primi 250 € vanno a [NOME ASSOCIAZIONE] (da decidere: metti il nome nei 3 file dove compare il segnaposto, oppure dimmelo e lo faccio io). Pubblica la ricevuta sulla pagina Gumroad quando arrivi a 250: è la prova sociale più forte che avremo.
>
> Target realistico con solo organico: 5–10 vendite nel mese = 145–290 €. Per arrivare a 500 € servono Etsy + i post costanti, oppure il servizio etichette in parallelo (materiale pronto in `offerta.md` e `outreach/`).


**Decisione:** vendere un servizio produttizzato di **etichette per piccoli brand cosmetici / integratori / candele / food artigianale**, con prezzo fisso e consegna in 72h. In parallelo, un prodotto digitale (template Illustrator) su Gumroad/Etsy come entrata passiva.

**Perché questo e non altro**
- Hai già il metodo (MOU Design), gli strumenti (Illustrator) e la competenza: zero tempo di apprendimento.
- Un'etichetta a 120 € × 5 clienti = 600 €. Target raggiunto con una sola vendita a settimana.
- I piccoli brand su Etsy/Instagram hanno etichette fatte con Canva: dolore evidente, budget 100–200 €, decisione rapida.
- Il freelance "generico" (Fiverr/Upwork) a 500 € in 30 giorni è aleatorio; l'outreach diretto a una nicchia è controllabile: è un gioco di numeri.

## I numeri (ipotesi conservative)
| Metrica | Valore |
|---|---|
| Contatti inviati | 150 (5 al giorno per 30 giorni) |
| Tasso risposta | 10 % → 15 risposte |
| Chiusura | 33 % → 5 clienti |
| Prezzo medio | 120 € |
| **Ricavo** | **600 €** |
| Tempo per etichetta | 2–3 h |

## Struttura cartella
- `offerta.md` — pacchetti, prezzi, cosa è incluso, FAQ.
- `outreach/` — script DM Instagram, email, follow-up, risposta alle obiezioni.
- `landing/index.html` — pagina vendita pronta (GitHub Pages o Netlify, 5 minuti).
- `tracker.csv` — pipeline contatti: compila ogni giorno.
- `prodotto-digitale.md` — scheda Gumroad/Etsy per il kit template.
- `calendario-30-giorni.md` — cosa fare ogni giorno.

## Prima cosa da fare domani (30 minuti)
1. Pubblica `landing/index.html` (vedi istruzioni in fondo al file).
2. Apri `tracker.csv` e trova 20 brand su Etsy (categoria "skin care", "candele", "integratori") con etichette brutte.
3. Manda i primi 5 DM con `outreach/dm-instagram.md`.

## Pubblicare la landing (5 minuti)
1. Nel repo su GitHub: Settings → Pages → Source "Deploy from a branch" → branch `main`, cartella `/ (root)`.
2. Sposta `piano-500-euro/landing/index.html` nella root del repo (o punta Pages a una cartella `docs/`).
3. Prima sostituisci: link Instagram, email, nome, P.IVA. Le due recensioni sono segnaposto: lasciale vuote o togli la sezione finché non hai quelle vere.
4. Alternativa: trascina la cartella `landing/` su app.netlify.com/drop. Online in 30 secondi.
