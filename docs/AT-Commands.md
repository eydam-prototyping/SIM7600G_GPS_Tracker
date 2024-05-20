## Dokumentation: Arten von AT-Kommandos

AT-Kommandos (Attention-Kommandos) sind Standardbefehle zur Kommunikation mit Modems und anderen Kommunikationsgeräten. Hier sind die verschiedenen Arten von AT-Kommandos und ihre möglichen Antworten, zusammen mit Beispielen und Erklärungen ihrer Funktionalität:

### 1. Einfache AT-Kommandos mit sofortiger Bestätigung

**Beschreibung:**
Ein einfacher AT-Befehl wird gesendet und das Modem antwortet sofort mit einer Bestätigung (OK).

**Beispiel:**
```
AT
OK
```

**Erklärung:**
Der `AT`-Befehl überprüft, ob die Verbindung zum Modem besteht. Eine Antwort mit `OK` bedeutet, dass das Modem bereit ist, weitere Befehle zu empfangen.

### 2. AT-Kommandos mit Daten und anschließender Bestätigung

**Beschreibung:**
Ein AT-Befehl wird gesendet, das Modem antwortet mit Daten und schließt mit einer Bestätigung (OK) ab.

**Beispiel:**
```
AT+CSQ
+CSQ: 23,99
OK
```

**Erklärung:**
Der `AT+CSQ`-Befehl fragt die Signalstärke des Modems ab. Die Antwort `+CSQ: 23,99` gibt die Signalqualität an, gefolgt von `OK`, das den Abschluss der Datenübertragung signalisiert.

### 3. AT-Kommandos mit verzögerter Antwort

**Beschreibung:**
Ein AT-Befehl wird gesendet, und die Antwort kommt verzögert nach einer bestimmten Zeit oder nach einem bestimmten Ereignis.

**Beispiel:**
```
AT+CGATT?
+CGATT: 1
OK
```

**Erklärung:**
Der `AT+CGATT?`-Befehl fragt den Anmeldestatus im Netzwerk ab. Die Antwort `+CGATT: 1` bedeutet, dass das Modem im Netzwerk registriert ist, gefolgt von `OK`.

### 4. AT-Kommandos mit einer Zwischenantwort und späterer finaler Bestätigung

**Beschreibung:**
Ein AT-Befehl wird gesendet, das Modem gibt eine Zwischenantwort und später eine finale Bestätigung.

**Beispiel:**
```
ATD123456789;
CONNECT
...
NO CARRIER
```

**Erklärung:**
Der `ATD123456789;`-Befehl startet einen Anruf an die Telefonnummer `123456789`. Die Antwort `CONNECT` bedeutet, dass die Verbindung hergestellt wurde. `NO CARRIER` zeigt an, dass die Verbindung beendet wurde.

### 5. AT-Kommandos mit mehreren Datenantworten

**Beschreibung:**
Ein AT-Befehl wird gesendet, und das Modem antwortet mit mehreren Datenblöcken, bevor die finale Bestätigung kommt.

**Beispiel:**
```
AT+CMGL="ALL"
+CMGL: 1,"REC READ","+123456789",,"20/05/19,12:34:56+00"
Hello, this is a test message.
+CMGL: 2,"REC UNREAD","+987654321",,"20/05/19,12:35:00+00"
Another test message.
OK
```

**Erklärung:**
Der `AT+CMGL="ALL"`-Befehl listet alle SMS-Nachrichten im Speicher auf. Jede Nachricht wird mit Details wie Index, Status, Absender und Zeitstempel angezeigt, gefolgt vom Nachrichtentext. `OK` signalisiert das Ende der Nachrichtenliste.

### 6. AT-Kommandos mit Benachrichtigungen

**Beschreibung:**
Ein AT-Befehl kann dazu führen, dass das Modem später Benachrichtigungen sendet, ohne dass ein weiterer Befehl gesendet wurde.

**Beispiel:**
```
AT+CNMI=2,1,0,0,0
OK
... (später)
+CMT: "+123456789",,"20/05/19,12:40:00+00"
New message received.
```

**Erklärung:**
Der `AT+CNMI=2,1,0,0,0`-Befehl konfiguriert das Modem so, dass eingehende SMS-Nachrichten sofort angezeigt werden. Später sendet das Modem `+CMT: ...` als Benachrichtigung für eine neue eingegangene Nachricht.

### 7. AT-Kommandos mit Fehlerantworten

**Beschreibung:**
Ein AT-Befehl wird gesendet, und das Modem antwortet mit einer Fehlermeldung anstelle einer Bestätigung.

**Beispiel:**
```
AT+INVALIDCOMMAND
ERROR
```

**Erklärung:**
Der `AT+INVALIDCOMMAND`-Befehl ist ein ungültiger Befehl. Das Modem antwortet mit `ERROR`, was auf einen Syntaxfehler oder einen nicht unterstützten Befehl hinweist.

### Zusammenfassung

Diese Dokumentation bietet einen Überblick über die verschiedenen Arten von AT-Kommandos und deren typische Antworten. Durch das Verständnis und die korrekte Handhabung dieser Befehle kann eine zuverlässige Kommunikation mit dem Modem sichergestellt werden.