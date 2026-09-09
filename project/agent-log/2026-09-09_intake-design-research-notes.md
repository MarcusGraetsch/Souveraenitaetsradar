# Assessment Intake v0.5 – Research Notes

Datum: 2026-09-09

## Quellenbasierte Designableitungen

### Schutzbedarf
BSI-Standard 200-2 beschreibt die Schutzbedarfsfeststellung über die realistisch zu erwartenden Schäden bei Verlust von Vertraulichkeit, Integrität und Verfügbarkeit einer Anwendung bzw. ihrer Informationen. Daraus folgt für den Radar: Workload-Kategorien können Fragen/Routing vorschlagen, dürfen aber keine endgültige C/I/A-Einstufung allein determinieren.

### NIS2
Die NIS2-Anwendbarkeit hängt grundsätzlich von Sektor/Tätigkeit, Unternehmensgröße und der Erbringung von Diensten bzw. Tätigkeit in der EU ab; es existieren zusätzliche Sonderfälle. Für das Intake reichen Anschrift/Land allein nicht.

### DORA
DORA gilt für enumerierte Arten von Finanzunternehmen sowie im relevanten Kontext ICT-Drittdienstleister. Für automatisches Routing muss deshalb die Organisations-/Rollenklassifikation bekannt sein.

### DSGVO
Territorialer Bezug und Verarbeitung personenbezogener Daten sind zentrale Faktoren; eine Kundenadresse allein beantwortet die Anwendbarkeit nicht.

### AI Act
Neben territorialem Bezug sind Rolle und Verwendung des KI-Systems entscheidend (z. B. Provider/Deployer). Daher sollte der Intake eine grobe KI-Rolle erfassen, sobald KI im Workload erkannt wird.

## Produktableitung

Compliance soll als `candidate -> rationale -> missing facts -> human review` modelliert werden, nicht als freies Textfeld oder automatische Rechtsfeststellung.

HUMAN GATE: HITL-08/HITL-09 vor Runtime-Migration; HITL-04 für rechtliche Schlussfolgerungen.