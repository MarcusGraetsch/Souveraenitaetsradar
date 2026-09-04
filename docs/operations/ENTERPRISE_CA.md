# Enterprise / Custom CA during Docker builds

Stand: 2026-09-04

## Problem

In Unternehmensnetzen mit TLS-Inspection oder eigener Root-/Intermediate-CA kann der Host HTTPS-Ziele erfolgreich erreichen, während ein frischer Docker-Buildcontainer der zusätzlichen CA nicht vertraut. Typisches Fehlerbild:

`SSLCertVerificationError: self-signed certificate in certificate chain`

Der erste reale NEXT-118-Installationslauf hat dieses Verhalten beim Download von Python-Buildabhängigkeiten von PyPI gezeigt.

## Unterstützter Weg

`install.sh` erstellt vor dem Build `.build/ca-bundle.crt` aus dem System-Truststore des Hosts. Der Bundle wird API- und Web-Build ausschließlich als Docker-BuildKit-Secret bereitgestellt.

- API/Python: `pip` erhält für den Installationsschritt einen kombinierten verifizierenden CA-Bundle.
- Web/Node: `npm`/Node erhält denselben Bundle als zusätzlichen/verifizierenden CA-Pfad.
- TLS-Verifikation bleibt aktiv.
- Der CA-Bundle wird nicht committed und nicht als reguläre Datei in das Docker-Build-Context aufgenommen.
- `uninstall.sh` entfernt `.build/` vollständig.

Wenn eine zusätzliche CA nicht im Host-System-Truststore liegt, kann ein PEM-Pfad explizit angegeben werden:

```bash
SOVRADAR_CA_CERT=/pfad/zur/enterprise-ca.pem ./install.sh
```

Die Datei darf eine Root-/Intermediate-CA oder einen PEM-Bundle enthalten. Sie wird mit dem erkannten System-Bundle kombiniert.

## Preflight

Vor `docker compose build` prüft der Installer HTTPS-Vertrauen für:

- `https://pypi.org/simple/setuptools/`
- `https://registry.npmjs.org/`

Scheitert bereits dieser Preflight, wird vor dem eigentlichen Build mit einer erklärenden Meldung abgebrochen.

## Nicht erlaubt

Nicht als Lösung verwenden:

- `pip --trusted-host ...`
- `NODE_TLS_REJECT_UNAUTHORIZED=0`
- globale Deaktivierung der Zertifikatsprüfung
- ungeprüftes Abschalten von SSL/TLS-Checks in npm, curl oder Docker

Das Installationsproblem ist ein Trust-Store-/PKI-Problem und wird als solches behoben.

## Diagnose

Auf dem Zielhost:

```bash
curl -Iv https://pypi.org/simple/setuptools/
curl -Iv https://registry.npmjs.org/
```

Falls die Enterprise-CA bereits systemweit installiert ist, sollten beide Prüfungen ohne Zertifikatsfehler funktionieren. Falls nicht, ist die korrekte Root-/Intermediate-CA vom Betreiber der Umgebung zu beziehen und als Trust Anchor einzubinden.

## Governance

Eine CA ist normalerweise kein Secret; dennoch behandelt das Projekt lokale Trust-Materialien als hostbezogene Build-Daten. Sie gehören nicht in Git und werden durch `.gitignore`/`.dockerignore` vom Quell- und Buildkontext getrennt. BuildKit Secrets verhindern, dass das lokale CA-Material als normale `COPY`-Schicht im Image landet.
