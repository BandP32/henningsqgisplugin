# Hennings QGIS Plugin

## Erste Implementation

Dies ist die erste Implementation für Hennings QGIS Plugin. Es beinhaltet eine funktionale GUI mit Backend, welches als Grundlage zur Einbindung des Prozessierungsskripts dienen kann.

## Installationsanleitung des Plugins

Es gibt drei unterschiedliche Wege das Plugin zu installieren:

### 1. Plugin in das vorhandene QGIS-default-Profil kopieren:
1. Zip-Paket herunterladen
2. Das Verzeichnis ./python/plugins/henningsqgisplugin in das Verzeichnis ./python/plugins/ im Default-Profilverzeichnis kopieren

### 2. Git clone:
1. QGIS Profilverzeichnis öffnen ("Settings" -> "User Profiles" -> "Open Active Profile Folder")
2. git clone https://github.com/PAndBee/henningsqgisplugin.git
3. QGIS öffnen
4. Auf das neue User-Profil "henningsqgisplugin" wechseln
5. "Plugins" -> "Manage and Install Plugins" -> Plugin aktivieren
https://plugins.qgis.org/publish/

### 3. Herunterladen über offizielles Plugin-Repository:

Noch nicht implementiert. Hier ist eine Anleitung dazu:
https://plugins.qgis.org/publish/

## Entwicklung To-Do-Liste:

- [x] Repository erstellen
- [x] Arbeiter-Klasse (QThread) implementieren
- [ ] Icon erstellen
- [ ] Metadata schreiben
- [x] Test auf QGIS 3.16 unter Ubuntu 20
- [ ] Plugin Test unter Windows
- [ ] Anleitung / Readme schreiben
- [ ] Testeinbindung des Plugins in das offizielle QGIS Plugin-Repositorium
