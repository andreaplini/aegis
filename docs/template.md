**Indice template **** - ****DOCUMENTO DI ANALISI DEI **** ****REQUISITI ****–**** RAD**

1. **Introduzione**

2. In questa prima fase introduttiva del documento, chiariremo gli scopi del sistema, l’area di

3. copertura, gli obiettivi e i criteri di successo, eventuali deﬁnizioni, acronimi e abbreviazioni

4. da tenere a mente e forniremo una breve panoramica del sistema

In questa prima fase introduttiva del documento, chiariremo gli scopi del sistema, l’area di copertura (dominio), gli obiettivi e i criteri di successo, eventuali definizioni, acronimi e abbreviazioni da tenere a mente e forniremo una breve panoramica del sistema.

2. **Sistema corrente**

Nella seconda fase di stesura del RAD, analizziamo il sistema attuale (qualora esista).! Nel caso non abbiamo a disposizione alcun sistema attuale, in quanto stiamo affrontando un problema di ingegnerizzazione greenfield, quindi stiamo progettando un sistema ex-novo e i requisiti ci vengono comunicati dal committente (v.  intervista col committente), non ci soffermeremo su questa fase della elicitazione dei requisiti, ma passeremo a descrivere direttamente il sistema preposto.

3. **Sistema proposto**

In questa fase dell’elicitazione dei requisiti e di stesura del RAD, ci soffermiamo su quella che è la parte principale: la de**fi**nizione del sistema pr**o**posto. In base alle informazioni che abbiamo acquisito mediante l’intervista con il committente, possiamo redigere un primo prototipo di sistema da proporgli.

**3.1 Panoramica**** (obiettivi del sistema)**

Descrivere il sistema proposto e i principali obiettivi.

**3.2 Requisiti funzionali**

È possibile descrivere i Requisiti funzionali sia attraverso delle tabelle (vedi esempio sotto) che attraverso delle descrizioni verbali dove andremo a numerare i requisiti come segue nell’esempio**:**

FR1: Creazione di un account personale*** ***=> Chiunque può creare un account con nome utente, codice fiscale e password e differenziarsi tra cittadino, medico e autorità sanitaria.

FR2:…..

**![Immagine che contiene testo, schermata, Carattere, numero

Descrizione generata automaticamente](template_assets/package/word/media/image1.png)**

**3.3 Requisiti non funzionali**

Di seguito alcuni esempi di requisiti non funzionali. Esempi: Interfaccia utente e fattori umani; Documentazione; Considerazioni hardware; Caratteristiche delle prestazioni; Gestione errori e condizioni limite; Interfacciamento del sistema; Problemi di qualità; Modifiche del sistema; Ambiente fisico; Problemi di sicurezza; Problemi di risorse e gestione.

Anche per questi requisiti possiamo usare una forma di rappresentazione tabellare (vedi esempio sotto), oppure un elenco come quello che segue:

*NFR1: Sicurezza: le password dei singoli utenti non dovranno mai essere visualizzate e accessibili dall’esterno.*

*NFR2: …*

**![Immagine che contiene testo, schermata, Carattere, numero

Descrizione generata automaticamente](template_assets/package/word/media/image2.png)**

  4.4. **Vincoli (“Pseudo requisiti”) **

Dettati dal committente o da limiti hardware o software.

  5.5. **Modelli del sistema**

    i. **Utenti del sistema** (descrizione degli utenti, dei ruoli e del contesto di utilizzo)

    ii. **Scenari** (con descrizione degli utenti, dei ruoli e del contesto di utilizzo)

![Immagine che contiene testo, schermata, Carattere, linea

Descrizione generata automaticamente](template_assets/package/word/media/image3.png)

    iii. **Modello casi d’uso**

**Diagramma dei casi d’uso globale (UML)**

**![Immagine che contiene schermata, cerchio, Policromia, arte

Descrizione generata automaticamente](template_assets/package/word/media/image4.png)**

**Specifiche**** dei casi d’uso**

(descrizione dei casi di uso del sistema sotto forma di tabella dei casi d’uso)

![Immagine che contiene testo, schermata, Carattere, numero

Descrizione generata automaticamente](template_assets/package/word/media/image5.png)

    iv. **Modello ****degli**** oggetti**

4. Una  volta  deﬁniti  i  casi  d’uso  e  gli  scenari,  possiamo  iniziare  a  redigere  un  modello

5. dell’analisi.

In questa sezione si definiscono le caratteristiche strutturali e le astrazioni del dominio di applicazione.

In particolare, si vuole definire l’insieme di oggetti di tipo Entity, boundary e Control, in quanto rappresentano le informazioni persistenti mantenute dal sistema (oggetti del

dominio applicativo).

**Oggetti ****entity**** dei casi d’uso**.**![Immagine che contiene testo, schermata, Carattere, ricevuta

Descrizione generata automaticamente](template_assets/package/word/media/image6.png)**

**Oggetti ****bounday**** dei casi d’uso****![Immagine che contiene testo, schermata, Carattere, ricevuta

Descrizione generata automaticamente](template_assets/package/word/media/image7.png)**

**Oggetti control dei casi d’uso**![Immagine che contiene testo, schermata, Carattere, documento

Descrizione generata automaticamente](template_assets/package/word/media/image8.png)

**Diagrammi delle class****i**

![Immagine che contiene testo, diagramma, Piano, Parallelo

Descrizione generata automaticamente](template_assets/package/word/media/image9.png)

    i. **Modelli dinamici**

Vengono descritti qui di seguito i diagrammi delle sequenze per i casi d’uso ritenuti più importanti all’interno del sistema.

I mode3lli Dinamici possono comprendere anche i diagramma degli stati e/o delle attività

![Immagine che contiene testo, diagramma, Parallelo, linea

Descrizione generata automaticamente](template_assets/package/word/media/image10.png)

4. **Interfaccia utente**** (vedi ****file “indice_template_interfaccia_utente.docx”)**** **

4.1 **Descrizione del Prototipo Realizzato:**

    1.%2.1. Scopo (Ruolo, Interfaccia, Implementazione),

    2.%2.2. Modo d’Uso (Statico, Dinamico, Interattivo),

    3.%2.3. Fedeltà (Bassa o Alta Fedeltà),

    4.%2.4. Completezza Funzionale (prototipo orizzontale o verticale),

    5.%2.5. Durata (usa e getta, evolutivo, incrementale, interattivo)

  1.1. **Test di Usabilità****:**

    1.%2.1. **Obiettivi del test** (descrivere brevemente gli obiettivi del test)

    2.%2.2. **Metodologia usata** (Specificare quanti utenti hanno partecipato al test, il loro livello di esperienza e le loro caratteristiche in relazione al prodotto in esame. Specificare i compiti, gli scenari assegnati, il contesto in cui si è svolto il test, e la strumentazione utilizzata. Descrivere come p stato condotto il test e da chi, quanto tempo è durato. (per ciascun utente e complessivamente), quali misure sono state raccolte, il ruolo degli osservatori e come sono stati analizzati i risultati.

    3.%2.3. **Sintesi delle Misure** (Fornire una tabella di sintesi delle misure raccolte. Per Esempio, i tempi di esecuzione e la percentuale dei compiti che sono stati portati a termine con successo, complessivamente e per ciascun utente). Aggiungere commenti ove opportuno

    4.%2.4. **Analisi dei risultati** (Descrivere analiticamente i problemi incontrati da ciascun utente durante il test, compito per compito, allegando ove opportuno degli screenshot significativi e assegnando ad ogni problema un livello di gravità. Ogni problema sarà numerato, per un più facile riferimento. Descrivere in dettaglio, se significativi, reazioni e commenti degli utenti, registrati durante le prove. Questa sezione è utile a formulare tutti i possibili interventi per rimuovere i problemi descritti, senza che sia necessario tornare ad esaminare il prodotto

    5.%2.5. **Sintesi delle interviste** (Sintetizzare i risultati delle interviste effettuate a ciascun utente dopo l’esecuzione del test)

    6.%2.6. **Raccomandazioni finali** (inserire la descrizione analitica degli interventi migliorativi proposti, raggruppati per livelli di priorità (per esempio: 1: interventi indispensabili; 2: interventi necessari, 3: interventi auspicabili). Per ogni intervento proposto si farà riferimento al problema relativo. Descritto nella sezione precedente. Gli interventi saranno numerati per facilitarne la tracciabilità)

4.3 **Valutazione dell’Usabilità: **

- Con riferimento ai principi dell’ISO 9241-110 valutare l’usabilità del sistema realizzato e, se possibile, confrontarla con l’usabilità di un sistema simile. A questo scopo, occorrerà esaminare ciascun sistema e attribuire un “voto” al grado di applicazione di ogni principio. Sarà poi possibile visualizzare i voti (voto medio dei voti dati dagli “n” valutatori considerati) ottenuti in un diagramma a stella (in cui si è usata una scala da 0 - voto minimo - a 4 – voto massimo) ottenendo il profilo di qualità del sistema.

**![Immagine che contiene diagramma, linea, schermata, cerchio

Descrizione generata automaticamente](template_assets/package/word/media/image11.png)**

4. **Allegati **(qualsiasi dato utile raccolto durante il test.)

5. **Glossario:** Definiamo in questa ultima fase del RAD, i termini più usati all’interno dell’intero documento con  le  rispettive  definizioni,  in  modo  tale  da  aiutare la consultazione  dello  stesso a nuovi sviluppatori.

**Indice documento di progettazione**** System Design ****Document**

1. Introduzione

1.1 Scopo del sistema

1.2 Obiettivi di progettazione

1.3 Definizioni, acronimi e abbreviazioni

1.4 Riferimenti

1.5 Panoramica

2. Sistema corrente

1. Sistema proposto

1.1 Panoramica

1.2 Decomposizione del sistema

1.3 Hardware/Software mapping

1.4 Gestione dei dati persistenti

1.5 Controllo accessi e sicurezza

1.6 Decisioni sul flusso di controllo globale

1.7 Condizioni limite

4. Servizi del sottosistema

**5. Glossario**
