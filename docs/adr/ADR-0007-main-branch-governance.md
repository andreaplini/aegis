# ADR-0007: governance del branch main

## Metadati

| Campo | Valore |
|---|---|
| ID | ADR-0007 |
| Titolo | Governance del branch main |
| Stato | Proposto |
| Data | 16 novembre 2026 |
| Responsabile | Proprietario del repository, da designare |
| Revisori | Maintainer e responsabile tecnico, da designare |
| Requisiti correlati | NFR-15, OPEN-09, ENG-02, ENG-07 ed ENG-09 |

## Contesto e problema

La verifica GitHub del 16 novembre 2026 ha rilevato `main` senza protezione e nessun ruleset. Il workflow `Genera documenti DOCX` è filtrato per percorsi e può non produrre un check su modifiche che non toccano tali percorsi. Un controllo richiesto come stato obbligatorio deve invece essere pubblicato per ogni pull request destinata a `main`.

Il repository non ha ancora una build applicativa. Un gate sempre attivo può verificare i documenti, i requisiti e le regole di tracciabilità già disponibili. Non equivale a compilazione o test applicativi. Il quality gate dovrà essere esteso quando ENG-03 introduce la build.

## Driver decisionali

| Driver | Criterio |
|---|---|
| Integrità di `main` | Le modifiche arrivano tramite un flusso di revisione configurato dal proprietario. |
| Check affidabile | Il check obbligatorio viene pubblicato anche quando una modifica non interessa i percorsi dell’export DOCX. |
| Verifica riproducibile | Il check usa lo stesso comando locale `make check-docs`. |
| Accesso amministrativo | La proposta non presume un numero di maintainer o una possibilità di auto approvazione. |
| Evoluzione del quality gate | Build, test e analisi applicative si aggiungono quando sono implementati e approvati in ENG-03 ed ENG-07. |
| Recupero | Il proprietario mantiene un percorso amministrativo documentato per correggere un ruleset che impedisca un rilascio necessario. |

## Opzioni considerate

| Opzione | Vantaggi | Costi e rischi | Requisiti soddisfatti o non soddisfatti |
|---|---|---|---|
| Nessuna protezione | Consente push diretti e non introduce nuovi blocchi. | Errori o modifiche non verificate possono raggiungere `main`. | Non fornisce il gate richiesto da OPEN-09. È lo stato osservato. |
| Protezione di `main` senza check obbligatorio | Richiede il flusso di pull request scelto dal proprietario. | La revisione da sola non prova che i controlli automatizzati siano passati. | Soddisfa parte di OPEN-09 ma non rende obbligatoria la verifica documentale. |
| Ruleset con pull request e check sempre attivo | Associa la protezione a un controllo stabile che copre ogni pull request. | Richiede configurazione e approvazione del proprietario. Numero di approvazioni e gestione delle eccezioni dipendono dai maintainer effettivi. | Può soddisfare OPEN-09 con il check `Verifica documentazione`. Non sostituisce i controlli applicativi futuri di ENG-07. |

## Proposta per approvazione

Configurare un ruleset applicato al branch predefinito `main` con pull request obbligatorie, divieto di force push e cancellazione del branch e check `Verifica documentazione` obbligatorio. Risolvere le conversazioni di revisione prima del merge. Il numero di approvazioni, le eccezioni amministrative e la policy di aggiornamento del branch devono essere scelti dal proprietario in base al numero e ai ruoli dei maintainer.

Il workflow [.github/workflows/quality-checks.yml](../../.github/workflows/quality-checks.yml) esegue `make check-docs` per ogni push e pull request verso `main`, senza filtri sui percorsi. Il suo job pubblica il check `Verifica documentazione`. Il workflow di esportazione DOCX resta un controllo aggiuntivo sui percorsi documentali. Quando esisterà una build applicativa, ENG-07 dovrà aggiungere i relativi check e aggiornare l’elenco dei controlli richiesti.

La proposta non modifica le impostazioni remote di GitHub e non sceglie quante approvazioni richiedere. Il ruleset va configurato solo dopo l’approvazione del proprietario, poi verificato con pull request di prova che dimostrino sia il blocco quando il check fallisce sia il merge quando check e policy risultano soddisfatti.

## Decisione

Non approvata. Il proprietario del repository deve approvare il flusso di pull request, il numero di review, gli eventuali bypass amministrativi e la policy di merge. Dopo l’approvazione, un maintainer configura il ruleset e registra l’esito delle prove.

## Conseguenze attese se approvata

- Le pull request verso `main` eseguono un controllo documentale indipendente dai percorsi modificati.
- Il check richiesto è distinto dall’export DOCX, che resta limitato ai file interessati.
- Le regole remote diventano tracciabili rispetto alla proposta e al risultato di una prova pratica.
- Il gate applicativo resta incompleto fino all’introduzione di build, test e analisi previsti da ENG-03 ed ENG-07.
- Le decisioni sul numero di review e sulle eccezioni restano responsabilità del proprietario.

## Verifica e revisione

| Evidenza richiesta | Criterio di accettazione | Responsabile | Esito e riferimento |
|---|---|---|---|
| Gate del workflow | Il workflow senza filtri sui percorsi produce il check `Verifica documentazione` su push e pull request verso `main`. Il push è verificato. La prova con pull request resta da eseguire | Responsabile repository, da designare | In corso. [Check riuscito su main](https://github.com/kairosci/aegis/actions/runs/43967406617). Pull request non provata |
| Approvazione OPEN-09 | Flusso di pull request, numero di approvazioni, bypass e policy di merge sono documentati | Proprietario del repository | In attesa |
| Configurazione remota | Ruleset applicato al branch `main` con protezioni e check approvati | Maintainer, da designare | Non superato. [Verifica di sola lettura in CONTRIBUTING](../CONTRIBUTING.md#stato-della-governance-github): la protezione del branch restituisce `Branch not protected` e la lista ruleset è vuota, verificato il 16 novembre 2026 |
| Pull request con check fallito | Il merge è rifiutato dalle regole configurate | Maintainer, da designare | Non eseguito |
| Pull request con policy soddisfatta | Il merge è consentito e l’esito resta consultabile | Maintainer, da designare | Non eseguito |
| Evoluzione ENG-07 | I check di build, test e analisi applicativa sono aggiunti e richiesti dopo ENG-03 | Responsabile tecnico, da designare | In attesa |

Riesaminare la decisione quando cambiano i maintainer, il workflow CI, i check di ENG-07 o le impostazioni di merge del repository.
