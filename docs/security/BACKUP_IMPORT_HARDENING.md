# Backup-Import Hardening

Der lokale MVP akzeptiert strukturierte Radar-Backup-ZIPs. Die Importlogik verwendet keine Dateisystem-Extraktion aus fremden Pfaden; ZIP-Member werden gezielt gelesen und Evidence wird unter neu erzeugten internen Dateinamen gespeichert.

Vor einem Einsatz mit nicht vertrauenswürdigen Backup-Dateien ist zusätzlich eine Decompression-Bomb-Abwehr erforderlich. Vor jedem `archive.read(...)` müssen `ZipInfo.file_size`, die Anzahl der Member und die Summe der unkomprimierten Größen gegen explizite Grenzwerte geprüft werden. `assessment.json` und `manifest.json` sollen deutlich kleinere Limits als Raw Evidence erhalten.

Dieses Dokument beschreibt ein offenes Security-Hardening-Finding und keine bereits implementierte Schutzmaßnahme.
