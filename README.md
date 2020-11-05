# Hennings QGIS Plugin

## Erste Implementation

Dies ist die erste Implementation für Hennings QGIS Plugin. Es beihaltet eine funktionale GUI mit Backend und kann als Grundlage zur Einbindung des Prozessierungsskripts dienen.

## Installationsanleitung des Plugins

Drei unterschiedliche Wege das Plugin zu installieren:

### 1. Plugin in das vorhandene default-Profil kopieren:
1. Zip-Paket herunterladen
2. Das Verzeichnis ./python/plugins/henningsqgisplugin in das Verzeichnis ./python/plugins/ im Default-Profilverzeichnis kopieren

### 2. Offizielles Plugin-Repository:
Noch nicht vorhanden 

### 3. Git clone:
1. QGIS Profilverzeichnis öffnen ("Settings" -> "User Profiles" -> "Open Active Profile Folder")
2. git clone https://github.com/PAndBee/henningsqgisplugin.git
3. QGIS öffnen
4. Auf das neue User-Profil "henningsqgisplugin" wechseln
5. "Plugins" -> "Manage and Install Plugins" -> Plugin aktivieren

## Entwicklung To-Do-Liste:

- [x] Repository erstellen
- [ ] Arbeiter-Klasse (QThread) implementieren
- [ ] Icon erstellen
- [ ] Metadata schreiben
- [ ] Test auf QGIS 3.16 unter Ubuntu20
- [ ] Plugin Test unter Windows
- [ ] Anleitung / Readme schreiben
- [ ] Testeinbindung des Plugins in das offizielle QGIS Plugin-Repositorium
