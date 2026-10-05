# Fase 2: Label Kit come micro-servizio (dopo la prima vendita del kit)

## Modello a tre livelli
| Livello | Prezzo | Cosa ottiene | Scopo |
|---|---|---|---|
| Editor online | gratis | compila, vede le 36 etichette con filigrana | magnete, passaparola tra artigiani |
| Singola etichetta | 4 € | SVG + PDF puliti di 1 etichetta | prezzo "rompi mercato", porta al kit |
| Kit completo | 29 € | tutto, illimitato, font, guide, aggiornamenti | il prodotto che fa il fatturato |

## Meccanica (senza nuovi account né server)
1. Editor pubblicato su GitHub Pages (stessa landing). Anteprima con filigrana diagonale "LABEL KIT · anteprima".
2. Su Gumroad due prodotti: "1 etichetta" a 4 € e "Kit completo" a 29 €, entrambi con **chiave di licenza** attiva.
3. Nell'editor: campo "Hai una chiave?". Verifica con l'API Gumroad (`POST https://api.gumroad.com/v2/licenses/verify`, parametri `product_id` e `license_key`, nessuna autenticazione). Se valida: chiave da 4 € sblocca 1 download, chiave da 29 € sblocca tutto.
4. Il conteggio "1 download" si fa lato client con `increment_uses_count`: Gumroad tiene il contatore degli usi della chiave. Non è a prova di hacker, ma per un prodotto da 4 € va bene.

## Cosa serve costruire
- Filigrana in anteprima (10 righe di SVG).
- Form chiave + fetch all'API + stato "sbloccato" (50 righe di JS).
- Spostare i file font su GitHub Pages (già nel repo).
- Pagina "come funziona" con i 3 prezzi.
Tempo stimato: mezza giornata.

## Numeri
- 4 € × 125 = 500 €. Da solo non basta: serve traffico.
- Obiettivo realistico: il livello 4 € converte il 20–30 % verso il kit entro 30 giorni (chi ha un prodotto ne ha presto un secondo).
- Metrica da guardare: visitatori editor → chiavi 4 € → upgrade 29 €.

## Rischi
- Cannibalizzazione: chi avrebbe pagato 29 € paga 4 €. Mitigazione: 4 € = 1 etichetta, senza font né guide né mockup.
- Pirateria dell'editor (è HTML, si copia). Accettata: il valore è negli aggiornamenti, nei font e nel supporto.
- Traffico zero: nessun prezzo risolve un canale vuoto. Etsy e post restano obbligatori.

## Condizione per partire
Prima vendita del kit a 29 € avvenuta. Poi: costruisco, pubblico, misuro 2 settimane.
