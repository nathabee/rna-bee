[ ] 1. Bestehendes WordPress sichern
docker compose breviouly creiert with wordpress,...

[ ] 2. Create Block Theme installieren

[ ] 3. RNA-Bee Child Theme aus Twenty Twenty-Five erzeugen

[ ] 4. Child prüfen
      [ ] Farbpalette
      [ ] Global Styles
      [ ] Sticky Header
      [ ] No-Title Template
      [ ] vorhandene Patterns
      [ ] eigenes CSS

[ ] 5. Child Theme aus Docker exportieren

[ ] 6. In Repo legen:
      wordpress/themes/rna-bee/

[ ] 7. Compose um Theme-Mount ergänzen

[ ] 8. Theme aus Git im laufenden WordPress testen

[ ] 9. Minimales rna-bee Plugin erstellen

[ ] 10. Plugin unter
       wordpress/plugins/rna-bee/
       versionieren

[ ] 11. Plugin über Compose verfügbar machen

[ ] 12. Default-Seiten festlegen
       [ ] Home
       [ ] About
       [ ] Explore

[ ] 13. Minimalen Seed-Content erstellen

[ ] 14. WP-CLI Bootstrap entwickeln
       [ ] Theme aktivieren
       [ ] Plugin aktivieren
       [ ] Default-Content entfernen
       [ ] Seiten erstellen
       [ ] Homepage setzen
       [ ] Permalinks setzen

[ ] 15. Bootstrap idempotent machen

[ ] 16. docs/wordpress.md dokumentieren

[ ] 17. Clean Installation mit leeren Volumes testen

[ ] 18. Erst wenn Clean Install funktioniert:
       aktuelle VPS-Demo-Inhalte entfernen

#################################################################################################


## Zielzustand

Nach:

```bash
git clone ...
cd rna-bee
docker compose up -d
```

soll langfristig ungefähr Folgendes entstehen:

```text
https://rna.nathabee.de

RNA Bee
├── Home
│   ├── RNA-Bee Hero / Branding
│   ├── sehr kurze Einführung
│   └── Einstieg in Simulator / Experimente
│
├── Simulator / Explore
│   └── später RNA-Bee Plugin Blocks
│
├── Examples
│   └── später echte Demo-Experimente
│
└── About
    └── kurze Erklärung + GitHub-Link
```

Nicht mehr Bestandteil dieser WordPress-Installation sind die langen Portfolio-Artikel. Die liegen jetzt auf `nathabee.de`.

## Unsere TODO-Liste

Ich würde das in sechs klar getrennte Arbeitspakete aufteilen.

| Phase | Aufgabe                              | Ergebnis                                        |
| ----- | ------------------------------------ | ----------------------------------------------- |
| **1** | Bestehende WP-Anpassungen retten     | RNA-Bee Child Theme                             |
| **2** | Child Theme in Git integrieren       | Theme wird Teil des Repositories                |
| **3** | RNA-Bee Plugin-Grundgerüst           | Funktionalität getrennt vom Theme               |
| **4** | Minimalen Default-Content definieren | Home/About statt Hello World                    |
| **5** | WordPress Bootstrap automatisieren   | Clone + Compose erzeugt definierte Installation |
| **6** | Clean-install Test                   | Beweis, dass das Repo reproduzierbar ist        |

### Phase 1 — Jetzt: Child Theme aus dem bestehenden WordPress erzeugen

Das ist unser **nächster konkreter Schritt**.

Dein bestehendes WordPress enthält bereits wertvolle DB-basierte Anpassungen:

```text
Twenty Twenty-Five
+
deine Farbpalette
+
Global Styles
+
Sticky Header
+
No-Title Template
+
eventuell weitere Template-Anpassungen
```

Wir machen daraus:

```text
Twenty Twenty-Five
        │
        └── RNA-Bee Child
              ├── style.css
              ├── theme.json
              ├── templates/
              │   └── no-title / page-no-title
              ├── parts/
              │   └── header.html
              └── patterns/
```

Dafür verwenden wir wie besprochen **Create Block Theme** und prüfen anschließend explizit, was tatsächlich exportiert wurde.

**Noch nichts manuell nachbauen.**

### Phase 2 — Theme ins Repository

Danach soll dein Repo ungefähr so aussehen:

```text
rna-bee/
├── compose.yaml
├── README.md
├── .env.example
│
├── django/
│
├── docs/
│   ├── architecture.md
│   ├── wordpress.md
│   ├── api.md
│   └── development.md
│
└── wordpress/
    ├── themes/
    │   └── rna-bee/
    │       ├── style.css
    │       ├── theme.json
    │       ├── templates/
    │       ├── parts/
    │       └── patterns/
    │
    ├── plugins/
    │   └── rna-bee/
    │
    └── bootstrap/
```

Das Theme wird anschließend per Compose in WordPress eingebunden.

Damit ist:

```text
Git
 ↓
wordpress/themes/rna-bee
 ↓
Docker bind mount
 ↓
/var/www/html/wp-content/themes/rna-bee
```

und nicht mehr:

```text
Theme-Anpassung
→ nur MariaDB
→ nur auf diesem VPS vorhanden
```

### Phase 3 — RNA-Bee Plugin

Wir erstellen zunächst nur ein kleines Plugin-Grundgerüst.

Noch keine große Simulation-UI.

Das Plugin bekommt später Dinge wie:

```text
RNA-Bee Plugin
├── API integration
├── RNA input block
├── Start experiment block
├── Experiment status
├── Folding result
└── Visualization
```

Das Theme dagegen bleibt zuständig für:

```text
RNA-Bee Theme
├── Farben
├── Typography
├── Header
├── Footer
├── Sticky Navigation
├── No-Title Template
├── Layout
└── Patterns
```

Die Grenze bleibt:

```text
Aussehen → Theme
Funktion → Plugin
```

### Phase 4 — Minimalen Default-Content definieren

Erst danach entscheiden wir exakt, was eine neue Installation bekommen soll.

Ich würde mit nur diesen Seiten beginnen:

```text
Home
About RNA Bee
Explore
```

Zum Beispiel:

**Home**

```text
[RNA-Bee Hero]

Explore RNA structure and computational evolution.

[Start Exploring]
```

**About**

```text
RNA-Bee is an open-source experimental platform
for computational RNA folding and evolution.

[GitHub]
```

**Explore**

```text
[später RNA-Bee Simulator Block]
```

Das ist Anwendung, nicht Portfolio.

Also keine:

```text
Building RNA-Bee Architecture
Why I chose Django
Docker explanation
Celery tutorial
development story
```

Diese Inhalte bleiben auf `nathabee.de` bzw. technisch in `docs/`.

### Phase 5 — Bootstrap

Hier müssen wir dann eine Designentscheidung treffen.

Ich bevorzuge:

```text
docker compose up
        ↓
WordPress startet
        ↓
WordPress DB initialisiert
        ↓
Bootstrap erkennt:
"fresh installation"
        ↓
Twenty Twenty-Five vorhanden
        ↓
RNA-Bee Child Theme aktivieren
        ↓
RNA-Bee Plugin aktivieren
        ↓
Hello World löschen
        ↓
Sample Page löschen
        ↓
Home erstellen
About erstellen
Explore erstellen
        ↓
Home als statische Startseite setzen
        ↓
Permalinks setzen
        ↓
fertig
```

Dafür ist **WP-CLI + kleines idempotentes Bootstrap-Script** wahrscheinlich die sauberste Lösung.

Wichtig: idempotent.

Das bedeutet:

```bash
./bootstrap-wordpress.sh
```

darf nicht bei jedem Container-Neustart wieder:

```text
Home
Home
Home
Home
```

erzeugen.

Es muss prüfen:

```text
Ist WordPress installiert?
Ist Theme aktiviert?
Existiert Home?
Existiert About?
Existiert Explore?
Ist Plugin aktiviert?
```

und nur Fehlendes ergänzen.

### Phase 6 — Der entscheidende Clean-Install-Test

Wenn alles fertig ist, testen wir nicht auf deiner bestehenden Installation.

Wir müssen beweisen:

```text
neue Umgebung
+
leere Volumes
+
Git Repository
```

reicht aus.

Der Test ist sinngemäß:

```bash
git clone ...
cd rna-bee

cp .env.example .env
# notwendige Werte setzen

docker compose up -d
```

Danach erwarten wir:

```text
WordPress       healthy
Django          healthy
PostgreSQL      healthy
MariaDB         healthy
Redis           healthy
Celery          running

RNA-Bee Theme   active
RNA-Bee Plugin  active

Home            exists
About           exists
Explore         exists

Hello World     gone
Sample Page     gone
```

Erst wenn dieser Test funktioniert, ist der WordPress-Teil wirklich **Teil der Anwendung** und nicht nur etwas, das zufällig auf deinem aktuellen VPS funktioniert.

## Was wir ausdrücklich nicht machen

Das ist ebenso wichtig:

```text
NO MariaDB dump als Default-Installation
NO wordpress_data Volume in Git
NO uploads aus Produktion in Git
NO komplette WordPress-Core-Installation in Git
NO Portfolio-Artikel als Seed
NO Twenty Twenty-Five Kopie in Git
```

Das Repository liefert stattdessen:

```text
our code
our configuration
our theme
our plugin
our bootstrap
minimal application content
```

WordPress selbst bleibt Runtime/Dependency.

 

 