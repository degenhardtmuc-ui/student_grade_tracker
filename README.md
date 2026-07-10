# Student Grade Tracker / Notenverwaltung

Dieses Repository enthält unser gemeinsames Python-Projekt **Student Grade Tracker**.

Das Ziel des Projekts ist eine kleine Notenverwaltung.

Mit dem Programm sollen später zum Beispiel Studierende, Kurse und Noten verwaltet werden können.

Wir arbeiten gemeinsam mit:

- Python
- Git
- GitHub
- Visual Studio Code
- Terminal auf dem Mac

---

# Teil 2: GitHub-Repository erstellen und verbinden

Dieser Abschnitt erklärt, wie ein neues GitHub-Repository erstellt und auf dem eigenen Mac verbunden wird.

Wichtig:

```text
Nur eine Person erstellt das Repository auf GitHub.
Alle anderen Teilnehmer werden danach eingeladen.
```

---

## 1. Neues Repository auf GitHub erstellen

Zuerst auf GitHub einloggen:

```text
https://github.com
```

Danach oben rechts auf das Plus-Zeichen klicken.

Dann auswählen:

```text
New repository
```

Als Repository-Name verwenden:

```text
student-grade-tracker
```

oder:

```text
notenverwaltung
```

Empfohlene Einstellungen:

```text
Visibility: Private
Add README: On
Add .gitignore: Python
License: No license
```

Danach auf den grünen Button klicken:

```text
Create repository
```

Merksatz:

```text
Ein Repository ist der Projektordner auf GitHub.
```

---

## 2. Warum ein neues Repository?

Für ein gemeinsames Projekt sollte ein eigenes Repository verwendet werden.

Das ist übersichtlicher als ein altes Kurs-Repository.

Vorteile:

- Das Projekt ist sauber getrennt.
- Alte Übungsdateien werden nicht vermischt.
- Alle arbeiten am gleichen Projektstand.
- Der Verlauf bleibt nachvollziehbar.
- Das Repository kann später leichter präsentiert werden.

Merksatz:

```text
Ein Gruppenprojekt bekommt ein eigenes Repository.
```

---

## 3. Kursteilnehmer einladen

Die Person, die das Repository erstellt hat, lädt die anderen Teilnehmer ein.

Auf GitHub im Repository öffnen:

```text
Settings
```

Dann:

```text
Access
```

Dann:

```text
Collaborators
```

Dann:

```text
Add people
```

Dort werden die GitHub-Namen oder E-Mail-Adressen der anderen Teilnehmer eingetragen.

Die eingeladenen Personen müssen die Einladung annehmen.

Merksatz:

```text
Collaborators sind Personen, die am Repository mitarbeiten dürfen.
```

---

## 4. Repository-Adresse kopieren

Im GitHub-Repository auf den grünen Button klicken:

```text
Code
```

Dann den Reiter auswählen:

```text
HTTPS
```

Die Adresse sieht ungefähr so aus:

```text
https://github.com/USERNAME/student-grade-tracker.git
```

oder:

```text
https://github.com/USERNAME/notenverwaltung.git
```

Diese Adresse kopieren.

Wichtig:

```text
USERNAME wird durch den echten GitHub-Benutzernamen ersetzt.
```

---

## 5. Repository auf den Mac herunterladen

Jetzt wird das Repository auf den eigenen Mac geladen.

Dazu das Terminal öffnen.

Zum Beispiel auf den Desktop wechseln:

```bash
cd ~/Desktop
```

Dann das Repository klonen:

```bash
git clone https://github.com/USERNAME/student-grade-tracker.git
```

oder:

```bash
git clone https://github.com/USERNAME/notenverwaltung.git
```

Danach in den Projektordner wechseln:

```bash
cd student-grade-tracker
```

oder:

```bash
cd notenverwaltung
```

Prüfen, ob man im richtigen Ordner ist:

```bash
pwd
```

Den Inhalt anzeigen:

```bash
ls
```

Merksatz:

```text
git clone lädt das GitHub-Projekt auf den eigenen Computer.
```

---

## 6. Verbindung zu GitHub prüfen

Im Projektordner eingeben:

```bash
git remote -v
```

Wenn alles richtig verbunden ist, sieht man ungefähr:

```text
origin  https://github.com/USERNAME/student-grade-tracker.git (fetch)
origin  https://github.com/USERNAME/student-grade-tracker.git (push)
```

Merksatz:

```text
origin ist die Verbindung zwischen lokalem Ordner und GitHub.
```

---

## 7. Projekt in Visual Studio Code öffnen

Wenn man im Projektordner ist, kann man das Projekt mit VS Code öffnen:

```bash
code .
```

Falls dieser Befehl nicht funktioniert, öffnet man VS Code manuell:

```text
File → Open Folder → student-grade-tracker
```

oder:

```text
File → Open Folder → notenverwaltung
```

---

# Teil 3: Gruppenarbeit mit Pull, Commit und Push

Dieser Abschnitt erklärt den normalen Arbeitsablauf im Gruppenprojekt.

---

## 1. Immer zuerst den neuesten Stand holen

Bevor man an dem Projekt arbeitet, sollte man immer zuerst den aktuellen Stand von GitHub holen:

```bash
git pull
```

Warum?

Vielleicht hat eine andere Person bereits etwas geändert.

Merksatz:

```text
Vor dem Arbeiten immer git pull.
```

---

## 2. Dateien bearbeiten

Danach kann man im Projekt arbeiten.

Zum Beispiel:

- Python-Dateien ändern
- neue Klassen erstellen
- Tests schreiben
- README erweitern
- Fehler verbessern

---

## 3. Änderungen anzeigen

Nach dem Bearbeiten kann man prüfen, was geändert wurde:

```bash
git status
```

Git zeigt dann zum Beispiel:

- neue Dateien
- geänderte Dateien
- gelöschte Dateien

Merksatz:

```text
git status zeigt, was sich im Projekt verändert hat.
```

---

## 4. Änderungen vormerken

Alle Änderungen vormerken:

```bash
git add -A
```

Merksatz:

```text
git add merkt Änderungen für den nächsten Commit vor.
```

---

## 5. Änderungen lokal speichern

Die vorgemerkten Änderungen werden mit einem Commit gespeichert:

```bash
git commit -m "Kurze Beschreibung der Änderung"
```

Beispiel:

```bash
git commit -m "Add student class"
```

oder:

```bash
git commit -m "Add grade calculation"
```

Merksatz:

```text
git commit speichert Änderungen lokal auf dem eigenen Computer.
```

---

## 6. Änderungen zu GitHub hochladen

Nach dem Commit werden die Änderungen zu GitHub hochgeladen:

```bash
git push
```

Merksatz:

```text
git push lädt meine gespeicherten Änderungen zu GitHub hoch.
```

---

## 7. Typischer Arbeitsablauf

Jedes Mal, wenn man am Projekt arbeitet:

```bash
git pull
```

Dann Dateien bearbeiten.

Danach:

```bash
git status
git add -A
git commit -m "Kurze Beschreibung der Änderung"
git push
```

Merksatz:

```text
pull vor der Arbeit.
push nach der Arbeit.
```

---

## 8. Beispiel für einen kompletten Ablauf

```bash
cd ~/Desktop/student-grade-tracker

git pull

git status

git add -A

git commit -m "Add gradebook class"

git push
```

oder bei anderem Ordnernamen:

```bash
cd ~/Desktop/notenverwaltung

git pull

git status

git add -A

git commit -m "Add gradebook class"

git push
```

---

## 9. Wichtige Regeln für Gruppenarbeit

Bitte immer beachten:

- Vor dem Arbeiten immer `git pull` ausführen.
- Nicht gleichzeitig wild dieselbe Datei bearbeiten.
- Kleine Änderungen machen.
- Verständliche Commit-Nachrichten schreiben.
- Regelmäßig pushen.
- Keine fremden Änderungen einfach überschreiben.
- Bei Fehlermeldungen erst nachfragen.
- Keine Passwörter oder privaten Dateien hochladen.

Merksatz:

```text
Git hilft nur dann gut, wenn alle sauber arbeiten.
```

---

## 10. Gute Commit-Nachrichten

Eine Commit-Nachricht soll kurz erklären, was geändert wurde.

Gute Beispiele:

```bash
git commit -m "Add student class"
```

```bash
git commit -m "Add course class"
```

```bash
git commit -m "Add tests for gradebook"
```

```bash
git commit -m "Update README"
```

Nicht so gut:

```bash
git commit -m "stuff"
```

```bash
git commit -m "änderung"
```

```bash
git commit -m "test"
```

Merksatz:

```text
Eine gute Commit-Nachricht sagt kurz, was gemacht wurde.
```

---

## 11. Sinnvolle Projektstruktur

Eine einfache Struktur für das Projekt kann so aussehen:

```text
student-grade-tracker/
│
├── README.md
├── .gitignore
├── main.py
├── student.py
├── course.py
├── gradebook.py
└── tests/
    ├── __init__.py
    └── test_gradebook.py
```

oder bei deutschem Namen:

```text
notenverwaltung/
│
├── README.md
├── .gitignore
├── main.py
├── student.py
├── course.py
├── gradebook.py
└── tests/
    ├── __init__.py
    └── test_gradebook.py
```

---

## 12. Bedeutung der Dateien

### README.md

Die Datei `README.md` erklärt das Projekt.

Sie ist die Startseite des Repositories auf GitHub.

---

### .gitignore

Die Datei `.gitignore` sagt Git, welche Dateien nicht hochgeladen werden sollen.

Zum Beispiel:

```text
.venv
__pycache__
*.pyc
.env
```

Merksatz:

```text
.gitignore hält unnötige und private Dateien aus GitHub heraus.
```

---

### main.py

Die Datei `main.py` kann als Startdatei des Programms benutzt werden.

---

### student.py

Die Datei `student.py` enthält die Klasse für Studierende.

---

### course.py

Die Datei `course.py` enthält die Klasse für Kurse.

---

### gradebook.py

Die Datei `gradebook.py` enthält die Hauptlogik der Notenverwaltung.

---

### tests/

Der Ordner `tests` enthält die Testdateien.

Tests prüfen automatisch, ob unser Code funktioniert.

---

## 13. Wenn man zwischen Repositories wechseln möchte

Ein Git-Repository ist einfach ein Ordner auf dem eigenen Mac.

Repository wechseln bedeutet deshalb:

```text
Ordner wechseln
```

Beispiel:

```bash
cd ~/Desktop/Software_Engineering
```

oder:

```bash
cd ~/Desktop/student-grade-tracker
```

Danach prüfen:

```bash
pwd
git status
```

Merksatz:

```text
Git-Repo wechseln bedeutet im Terminal den Ordner wechseln.
```

---

## 14. Mini-Spickzettel

Die wichtigsten Befehle:

```bash
git clone https://github.com/USERNAME/student-grade-tracker.git

cd student-grade-tracker

git remote -v

code .

git pull

git status

git add -A

git commit -m "Beschreibung"

git push
```

---

## 15. Wichtigster Merksatz

```text
Git speichert Änderungen.
GitHub teilt Änderungen mit der Gruppe.
git pull holt Änderungen.
git push sendet Änderungen.
```
## Hilfreiche Ressourcen für den Student Grade Tracker

Die folgenden Internetseiten unterstützen die Entwicklung des Student Grade Trackers. Sie behandeln unter anderem Datenvalidierung, objektorientierte Programmierung, Datenpersistenz, Datenbanken, Debugging und UML-Diagramme.

---

### Datenvalidierung

#### Regex101

[Regex101: Reguläre Ausdrücke erstellen und testen](https://regex101.com/)

Ein Online-Werkzeug zum Schreiben, Testen und Erklären regulärer Ausdrücke. Es kann im Student Grade Tracker beispielsweise zur Entwicklung einer Prüfung für E-Mail-Adressen oder andere Texteingaben verwendet werden.

> **Hinweis:** Ein regulärer Ausdruck sollte für die E-Mail-Prüfung nicht unnötig kompliziert werden. Für das Projekt genügt normalerweise eine verständliche und gut getestete Basisprüfung.

---

### CSV-Dateien und Datenpersistenz

#### Python CSV-Modul

[W3Schools: Python CSV Module](https://www.w3schools.com/python/ref_module_csv.asp)

Eine Einführung in das eingebaute Python-Modul `csv`. Das Modul kann verwendet werden, um Studierende, Kurse oder Noten in CSV-Dateien zu speichern und später wieder einzulesen.

Typische Anwendungsfälle im Projekt:

* Studierendendaten exportieren
* Noten in einer Tabelle speichern
* gespeicherte Datensätze wieder laden
* Daten mit Tabellenkalkulationsprogrammen austauschen

---

### JSON-Verarbeitung

#### `object_pairs_hook` bei `json.loads()`

[Stack Overflow: Understanding object_pairs_hook in json.loads()](https://stackoverflow.com/questions/54519626/understanding-object-pairs-hook-in-json-loads)

Der Beitrag erklärt die besondere Option `object_pairs_hook` des JSON-Moduls. Damit können Schlüssel-Wert-Paare verarbeitet werden, bevor daraus ein normales Dictionary entsteht.

Diese Funktion kann beispielsweise hilfreich sein, wenn:

* die Reihenfolge von Einträgen gezielt verarbeitet werden soll,
* doppelte JSON-Schlüssel erkannt werden sollen,
* eine eigene Datenstruktur erzeugt werden soll.

> **Hinweis:** Für das normale Speichern und Laden der Notenverwaltung reichen zunächst meistens `json.dump()` und `json.load()`. `object_pairs_hook` ist ein weiterführendes Spezialthema.

---

### Datenbanken

#### SQLite mit Python

[Python-Dokumentation: sqlite3](https://docs.python.org/3/library/sqlite3.html)

Die offizielle Python-Dokumentation zum eingebauten Modul `sqlite3`. Mit SQLite können Daten dauerhaft in einer lokalen Datenbank gespeichert und strukturiert abgefragt werden.

Mögliche Tabellen im Student Grade Tracker:

* `students`
* `courses`
* `grades`
* `enrollments`

Mit SQLite können Datensätze erstellt, gelesen, geändert und gelöscht werden.

> **Hinweis:** SQLite eignet sich gut als spätere Erweiterung. Für eine erste Projektphase sind CSV- oder JSON-Dateien meist leichter umzusetzen.

---

### Objektorientierte Programmierung

#### Python-Datenmodell

[Python-Dokumentation: Data Model](https://docs.python.org/3/reference/datamodel.html)

Die offizielle Referenz zum Python-Datenmodell. Sie erklärt, wie Python-Objekte, Klassen, Attribute, Methoden und Spezialmethoden funktionieren.

Für den Student Grade Tracker sind insbesondere folgende Spezialmethoden interessant:

* `__init__()` zum Initialisieren eines Objekts
* `__str__()` für eine benutzerfreundliche Textdarstellung
* `__repr__()` für eine entwicklerfreundliche Darstellung
* `__eq__()` zum Vergleichen von Objekten

Diese Methoden können beispielsweise in den Klassen `Student`, `Course` und `GradeBook` verwendet werden.

---

### Objekte und Referenzen visualisieren

#### Memory Graph

[Memory Graph: Python-Objekte visualisieren](https://memory-graph.com/#breakpoints=8&continues=1&play)

Memory Graph stellt Python-Objekte, Variablen, Referenzen und Beziehungen grafisch dar. Dadurch wird sichtbar, welche Variable auf welches Objekt verweist und wie Objekte miteinander verbunden sind.

Im Student Grade Tracker kann das Werkzeug dabei helfen, Beziehungen zwischen folgenden Objekten nachzuvollziehen:

* `GradeBook`
* `Student`
* `Course`
* Listen mit Studierenden oder Kursen
* Dictionaries mit Noten und Zuordnungen

---

### UML und Projektdokumentation

#### diagrams.net

[diagrams.net: UML- und Ablaufdiagramme erstellen](https://app.diagrams.net/)

Ein kostenloses Browser-Werkzeug zum Erstellen von UML-Klassendiagrammen, Ablaufdiagrammen und Architekturübersichten.

Für den Student Grade Tracker kann damit beispielsweise ein Klassendiagramm für folgende Klassen erstellt werden:

* `Student`
* `Course`
* `GradeBook`
* mögliche Speicher- oder Repository-Klassen

Das Diagramm kann Attribute, Methoden und Beziehungen zwischen den Klassen darstellen.

---

## Empfohlene Reihenfolge für das Projekt

1. Klassen und Beziehungen zunächst mit diagrams.net planen.
2. `Student`, `Course` und `GradeBook` als Python-Klassen umsetzen.
3. Die Objektbeziehungen mit Memory Graph untersuchen.
4. Eingaben und E-Mail-Adressen prüfen.
5. Daten zunächst in CSV- oder JSON-Dateien speichern.
6. SQLite später als mögliche Erweiterung ergänzen.
7. Alle wichtigen Funktionen mit automatisierten Tests absichern.
