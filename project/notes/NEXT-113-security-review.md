# NEXT-113 Security Review Notes

Status: Open hardening follow-up
Datum: 2026-09-04

## Finding: ZIP member decompression limits

Der Backup-Import begrenzt derzeit die hochgeladene ZIP-Datei, liest einzelne ZIP-Member jedoch mit `archive.read(...)`. Die Größenprüfung für Evidence erfolgt teilweise erst nach der Dekompression. Ein stark komprimiertes, bösartig erzeugtes Backup könnte deshalb vor der Prüfung deutlich mehr Arbeitsspeicher beanspruchen als die komprimierte Uploadgröße erwarten lässt.

## Empfohlene Härtung

Vor jedem `archive.read(...)` die jeweilige `ZipInfo.file_size` prüfen. Für `assessment.json` und `manifest.json` kleine, explizite Obergrenzen verwenden; für Evidence-Member höchstens `SOVRADAR_MAX_UPLOAD_BYTES`. Zusätzlich eine Obergrenze für die Summe der unkomprimierten Membergrößen und für die Zahl der ZIP-Einträge definieren.

## Einordnung

Das MVP ist lokal und nicht als ungeschützter Internetdienst vorgesehen. Das Finding verändert keine Methodik- oder Gate-Ergebnisse und blockiert den fachlichen NEXT-113-Nachweis nicht. Vor breiterer Nutzung oder dem Import nicht vertrauenswürdiger Backup-Dateien muss es geschlossen werden.
