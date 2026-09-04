# Agent Session – NEXT-118 Post-Pilot Security/UX Hardening

Datum: 2026-09-04
Branch: `fix/next-118-security-ux-hardening`
Rollen: `developer`, anschließend `reviewer/security` Self-Review
Reviewklasse: C – sensibler Datenpfad / Evidence-to-LLM

## Anlass

Der erste reale Fresh-VM-Consultant-Durchlauf von NEXT-118 hat mehrere konkrete Produktbefunde geliefert. Dieser Change adressiert bewusst nur kleine, klar abgegrenzte Hardening-/UX-Punkte und verändert keine Gate-, Risiko- oder Souveränitätsmethodik.

## Scope

### 1. LLM Bridge – Datenminimierung (#43)

Beobachtung aus dem realen Pilot:

- `Evidence.description` wurde im Prompt ausgegeben, obwohl `content_excerpt` leer war und der Prompt zugleich `[kein Textauszug im Radar]` anzeigte.
- Damit konnte eine interne freie Beschreibung unbeabsichtigt in einen extern kopierten LLM-Prompt gelangen.

Änderung:

- freie interne `Evidence.description` wird nicht mehr in den LLM-Prompt übertragen;
- nur `content_excerpt` gilt als ausdrücklich freigegebener Evidence-Inhalt;
- bei leerem Auszug erscheint `[kein Textauszug für LLM freigegeben]`;
- Promptvertrag erklärt die Trennung ausdrücklich;
- Regressionstest mit Sensitive-Sentinel verhindert erneute Beschreibung-Leakage.

Nicht gelöst: vollständiges Processing-Profile-/Endpoint-Routing aus #43. Assessment-Header und Metadaten bleiben im bestehenden MVP-Bridge-Modell enthalten.

### 2. Restore-Übersicht (#54)

Beobachtung:

- Restore erzeugte korrekt ein neues Assessment;
- API enthielt Original + Restore;
- React-Assessment-Liste blieb bis manuellem Browser-Reload veraltet.

Änderung:

- nach erfolgreichem Restore ohne Gate-Drift zeigt die UI kurz die Erfolgsmeldung und lädt die Anwendung nach 1,2 s neu;
- dadurch erscheint automatisch die Assessment-Übersicht mit aktualisierter Liste;
- API-Regressionstest prüft zusätzlich, dass Original- und Restore-ID gleichzeitig vorhanden bleiben.

Spätere UX-Option: clientseitiger Refresh ohne Full Reload plus Aktion `Restore öffnen`.

### 3. Vollbackup-/Restore-Sprache (#52 Teilmenge)

- verständlichere Warnung vor vollständigem Backup;
- Hinweis auf mögliche vertrauliche Nachweisdateien und geschützte Ablage;
- Restore-Hilfe nennt explizit Radar-JSON/Radar-ZIP und schließt Consultant Report als Importdatei aus.

Die umfassende Ergebnis-/Terminologie-Überarbeitung aus #52 bleibt offen.

### 4. Uninstall Repository-Löschung (#55)

Beobachtung:

- nach bereits erfolgreicher Deinstallation genügte ein versehentliches `j`, um zusätzlich den lokalen Git-Clone zu löschen.

Änderung:

- Repository-Löschung ist explizit als optionale Zusatzaktion getrennt;
- Standard: Repository behalten;
- Löschung nur noch bei exakter Eingabe `DELETE REPO`;
- bei uncommitted/untracked Git-Änderungen wird `git status --porcelain` angezeigt und zusätzlich `DELETE REPO WITH CHANGES` verlangt.

## Nicht-Scope

- Question Answer Types / #38
- LLM Answer Proposal Review / #49
- Consultant-Terminologie Hard Gates / #50
- Gate Requirement UX / #51
- Consultant Report / Management Summary / #53
- vollständige AI Processing Profiles / #43
- ZIP-Bomb-/Schema-Hardening #25/#26

## Tests / Akzeptanz

Erwartete CI-Prüfungen:

- `python tools/validate_repo.py`
- kompletter pytest-Lauf inkl. neuer LLM-Bridge-Sentinel-Tests
- API-Tests inkl. Original+Restore-Listenassertion
- Frontend TypeScript/Vite Build
- Compose Smoke
- vollständiger Consultant-Walkthrough
- Stop/Restart/Test
- Uninstall: bestehender CI-Pfad `DELETE` + `n` muss weiterhin sauber alle Runtime-Ressourcen löschen und den Repo-Ordner behalten

## Security Review – Self-Review

- keine Credentials oder Cloud-Account-Zugriffe eingeführt;
- keine neue Netzwerkverbindung zur LLM Bridge;
- Datenfluss wurde restriktiver, nicht weiter geöffnet;
- Gate-/Risk-Engine unverändert;
- Raw Evidence bleibt lokal;
- `content_excerpt` bleibt der explizite Copy/Paste-Freigabepfad;
- #43 bleibt offen, weil feld-/artefaktbezogene Processing Profiles noch fehlen.

## Handoff

Nach grüner CI:

1. PR mergen.
2. #54 und #55 nach Merge schließen, sofern Merge-Verifikation passt.
3. #43 offen lassen; nur konkretes Description-Leak-Finding ist behoben.
4. NEXT-118 auf frischer Installation kurz re-testen: Evidence ohne freigegebenen Auszug -> Prompt darf Beschreibung nicht enthalten; Restore -> Übersicht aktualisiert sich automatisch; Uninstall -> `j` darf Repository nicht löschen.
