# First Install & Consultant Evaluation

Stand: 2026-09-04

Dieses Runbook ist für den ersten manuellen Test des Souveränitäts-Radars gedacht. Ziel ist nicht, sofort einen echten Kundenfall vollständig zu bewerten, sondern Installation, Bedienlogik und fachliche Plausibilität aus Beratersicht zu prüfen.

## 1. Voraussetzungen

- Linux-Host oder VM mit Docker Engine und Docker Compose v2
- Git
- Browserzugriff auf den Host
- für den ersten Test keine echten Kundendaten, Secrets oder Cloud-Credentials verwenden

Die Anwendung besitzt im MVP noch keine Authentisierung. Für den ersten Test deshalb die Standardbindung `127.0.0.1` verwenden.

## 2. Installation

```bash
git clone https://github.com/MarcusGraetsch/Souveraenitaetsradar.git
cd Souveraenitaetsradar
git checkout main
./install.sh
```

Bei der Installationsfrage die lokale Bindung `127.0.0.1` wählen.

Danach prüfen:

```bash
./test.sh
```

Erwartet:

- API healthy
- mindestens 100 Methodenfragen geladen
- Web erreichbar
- Docker-Services laufen

Weboberfläche: `http://localhost:8080`

## 3. Empfohlener erster manueller Testfall

Für die erste Evaluation einen bewusst synthetischen, aber realistischen Fall verwenden:

> Ein KI-Agent verarbeitet sensible Fachdaten und greift auf interne Fachsysteme zu. Der Service soll in einer Cloud-/Managed-Service-Architektur betrieben werden. Datenresidenz, Schlüsselhoheit, Exit, IAM/Trust Anchors, Unterauftragnehmer und Security Controls sind relevant. Es liegen zunächst nur teilweise Nachweise vor.

Der Fall ist absichtlich nicht vollständig. Fehlende Nachweise sollen sichtbar zu `UNVERIFIED` bzw. Evidence Gaps führen und nicht automatisch als `FAIL` oder `PASS` interpretiert werden.

## 4. Evaluation in der Weboberfläche

### A. Assessment und Scope

Prüfen:

- Ist verständlich, welche Angaben zu Workload, Kritikalität, CIA und Kontrollraum erwartet werden?
- Ist klar, dass regulatorischer Kontext und Scope Beraterangaben sind und keine automatische Rechtsfeststellung?
- Fehlen wichtige Scope-Felder?

### B. Relevanzprofil und Guided Questions

Prüfen:

- Sind Screening, Klärung und Deep Dive als Arbeitslogik verständlich?
- Sind `needs_review`-Fragen sichtbar statt still ausgeblendet?
- Ist `Alle Fragen / Audit` auffindbar?
- Wirkt die unmittelbare Fragenmenge noch zu groß oder fachlich unpassend?

Bekanntes offenes UX-Thema: NEXT-116 / Issue #22 adressiert die noch große Screening-/Clarification-Queue.

### C. Evidence

Mindestens drei synthetische Nachweise anlegen, beispielsweise:

1. Vertrag/DPA-Zusammenfassung für Jurisdiktion und Effective Control.
2. Architektur-/Konfigurationsnachweis für Datenstandort oder KMS.
3. Exit-/Restore-Testprotokoll.

Prüfen:

- Sind Evidence Type, Quelle, Datum, Applied State und Trust-Dimensionen verständlich?
- Ist der Unterschied zwischen `available`, `documented`, `configured`, `tested` und `attested` nachvollziehbar?
- Ist verständlich, dass `Effective Trust = min(base_trust, scope_fit, freshness_fit)` konservativ berechnet wird?
- Ist klar, dass öffentliche Provider-Dokumentation Service Capability belegt, aber nicht automatisch die Kundenkonfiguration?

### D. Human-reviewed Claims und Hard Gates

Mindestens einen Claim bewusst als `reviewed` anlegen und einen anderen zunächst nur als Draft belassen.

Prüfen:

- Ändert nur ein human-reviewed/approved Claim die Gate-Bewertung?
- Bleibt ein Gate ohne ausreichenden Claim/Evidence `UNVERIFIED`?
- Ist der Unterschied zwischen Requirement, Applied Capability und Evidence Trust verständlich?
- Wird ein technisches Unterschreiten des Requirements als `FAIL` sichtbar?
- Werden Requirement-Overrides als Consultant-Entscheidung und nicht als Normvorgabe dargestellt?

## 5. Export, Report, Backup und Restore

Im Ergebnisbereich nacheinander prüfen:

- Structured JSON
- Consultant Report
- strukturiertes Backup
- Vollbackup inkl. Evidence nur nach expliziter Bestätigung
- Restore als neues Assessment

Erwartete Schutzlogik:

- Standardexport enthält keine Raw-Evidence-Dateien.
- Consultant Report enthält keine Raw Evidence und keine freigegebenen Evidence-Textauszüge.
- Vollbackup ist explizites Opt-in.
- Restore überschreibt kein bestehendes Assessment.
- Gates werden nach Restore neu berechnet und semantisch verglichen.

Offene Security-Hardening-Punkte für nicht vertrauenswürdige Importdateien sind separat als Issues #25 und #26 dokumentiert.

## 6. Optional: reproduzierbarer NEXT-101-Techniktest

Für einen reproduzierbaren Test des synthetischen Customer Evidence Packs auf dem Host kann eine lokale Python-Umgebung verwendet werden:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e . -r requirements-dev.txt -r apps/api/requirements.txt
python tools/validation/customer_evidence_pack_pilot.py
python tools/validation/customer_evidence_pack_webapp.py \
  --base-url http://127.0.0.1:8080 \
  --output .runtime/exports/manual-next-101-webapp.json
```

Der Pilot benötigt keine Cloud-Credentials. Die erwartete Evidence-Coverage-Baseline ist:

- 3 `VERIFIED`
- 4 `REVIEW_REQUIRED`
- 1 `INSUFFICIENT`
- 3 `MISSING`
- 5 Evidence-Klassen

Im Webapp-Pilot darf nur der explizit vorgegebene synthetische Human-Reviewed Claim Gate-Wirkung entfalten. Erwarteter Gate-Zustand ist `HG-01 PASS`, die übrigen sieben Gates bleiben `UNVERIFIED`.

## 7. Evaluation protokollieren

Für jedes Problem möglichst notieren:

- **Stelle:** Seite/Funktion/Feld
- **Beobachtung:** Was war unklar, falsch oder umständlich?
- **Erwartung:** Was hätte ein Berater stattdessen erwartet?
- **Schwere:** blocker / fachlich kritisch / UX / nice-to-have
- **Methodik oder Produkt?** Handelt es sich um eine fachliche Regel oder nur um Darstellung/Bedienung?

Besonders wertvoll sind Stellen, an denen die Software zu einem Ergebnis führt, das fachlich überraschend wirkt. Diese Fälle sollten nicht vorschnell als UI-Fehler behandelt werden, sondern gegen Evidence, Claim, Requirement und Gate-Logik zurückverfolgt werden.

## 8. Stoppen oder vollständig entfernen

Daten behalten:

```bash
./stop.sh
```

Später wieder starten:

```bash
./start.sh
```

Vollständig entfernen:

```bash
./uninstall.sh
```

Die vollständige Deinstallation löscht PostgreSQL-Daten, `.runtime/`, lokale Evidence-Dateien, `.env`, Container, Netzwerk, Volume und lokal gebaute Images. Das Git-Repository bleibt standardmäßig bestehen.
