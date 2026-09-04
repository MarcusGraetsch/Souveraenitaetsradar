# NEXT-119 — Enterprise/custom CA support for Docker builds

Datum: 2026-09-04
Issue: #29
Parent validation: NEXT-118 / Issue #28
Branch: `fix/next-119-enterprise-ca-build`

## Auslöser

Erster echter manueller Installationslauf auf einer frischen VM. `./install.sh` lief bis zum Docker-Build. Der API-Build scheiterte bei:

```text
RUN pip install --no-cache-dir -e . -r apps/api/requirements.txt
```

Fehler:

```text
SSLCertVerificationError: self-signed certificate in certificate chain
https://pypi.org/simple/setuptools/
```

Der Web-Build wurde dadurch abgebrochen; deshalb musste npm im selben Trust-Modell berücksichtigt werden.

## Einordnung

- Produkt-/Installationsblocker für Enterprise-Netze mit TLS-Inspection, Proxy oder eigener CA.
- Kein Methoden-, Evidence- oder Gate-Fehler.
- NEXT-118 bleibt offen und wird nach erfolgreicher Installation fortgesetzt.

## Sicherheitsentscheidung

TLS-Prüfung wird nicht deaktiviert. Nicht zulässig als Produktlösung:

- pip `--trusted-host`
- `NODE_TLS_REJECT_UNAUTHORIZED=0`
- globale SSL-Verify-Deaktivierung

Stattdessen wird ein expliziter verifizierender CA-Bundle verwendet.

## Implementierung

1. `scripts/prepare-build-ca.sh`
   - erkennt übliche Linux-System-CA-Bundles,
   - kombiniert optional `SOVRADAR_CA_CERT`,
   - schreibt `.build/ca-bundle.crt`,
   - Buildmaterial ist git-ignored.
2. `install.sh`
   - bereitet CA-Bundle vor,
   - preflightet PyPI und npm Registry,
   - bricht mit konkreter Anleitung ab, falls Trust nicht hergestellt ist.
3. Docker Compose
   - gibt den CA-Bundle als BuildKit-Secret an API und Web weiter.
4. API-Dockerfile
   - kombiniert Container-System-CA + Build-Secret nur für den pip-Installationsschritt.
5. Web-Dockerfile
   - verwendet Build-Secret für Node/npm TLS-Verifikation.
6. `.dockerignore`
   - schließt `.runtime`, `.build`, `.env`, lokale Evidence-/Credential-Pfade und Schlüsselmaterial aus dem Buildcontext aus.
7. `uninstall.sh`
   - entfernt `.build/` zusammen mit allen übrigen generierten Daten.
8. CI
   - bereitet den Build-CA-Bundle auch im direkten Compose-Smoke-Test vor,
   - prüft beim Lifecycle, dass `.build/` nach Uninstall entfernt ist.

## Unterstützter manueller Pfad

Falls Enterprise-CA bereits im Host-Truststore liegt:

```bash
./install.sh
```

Falls zusätzliche PEM-CA explizit erforderlich ist:

```bash
SOVRADAR_CA_CERT=/pfad/zur/enterprise-ca.pem ./install.sh
```

## Review-Hinweise für nächste Agents

- Nicht auf `--trusted-host` oder TLS-Off zurückfallen.
- BuildKit-Secret beibehalten; CA nicht per `COPY` in das Image übernehmen.
- Standard-CI muss ohne Custom CA grün bleiben.
- Reale NEXT-118-VM ist der entscheidende Akzeptanztest nach Merge.
