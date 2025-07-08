# Komoot GPX Downloader mit Webserver

Dieses Projekt erstellt einen Docker-Container, der GPX-Dateien von Komoot herunterlädt und sie über einen einfachen Webserver bereitstellt.

Vielen Dank an https://github.com/timschneeb/KomootGPX für die Komoot-Python-Library.

![Screenshot](/webpage_example.png)

## Voraussetzungen

*   [Docker](https://www.docker.com/) und [Docker Compose](https://docs.docker.com/compose/install/) müssen installiert sein.
*   Ein Komoot-Konto.

## Installation und Verwendung

1.  **Clone das Repository:**

    ```bash
    git clone https://github.com/daranto/komoot-gpx-docker.git
    cd <VERZEICHNIS_DES_REPOSITORIES>
    ```

2.  **Konfiguration:**

    *   E-Mail und Passwort in der docker-compose Datei hinterlegen

        ```
        - KOMOOT_EMAIL="<EMAIL EINTRAGEN>"  # Umgebungsvariable für E-Mail
        - KOMOOT_PASSWORD="<PASSWORT EINTRAGEN>" # Umgebungsvariable für Passwort
        ```

        **Achtung:** Das Speichern von Passwörtern in der `docker-compose.yml`-Datei ist für lokale Tests in Ordnung, aber für Produktionsumgebungen solltest du sicherere Methoden wie Docker Secrets verwenden.

3.  **Erstelle und starte den Container:**

    ```bash
    docker-compose up -d --build
    ```

    *   `-d`: Führt den Container im Hintergrund aus.
    *   `--build`: Erstellt das Docker-Image neu, falls sich das Dockerfile geändert hat.

4.  **Zugriff auf die Webseite:**

    Öffne deinen Webbrowser und gehe zu `http://localhost:4444`. Du solltest eine Liste der heruntergeladenen GPX-Dateien sehen.

5.  **GPX-Dateien aktualisieren:**

    Klicke auf den "GPX-Dateien aktualisieren"-Button auf der Webseite, um die neuesten GPX-Dateien von Komoot herunterzuladen.

6.  **GPX-Dateien erhalten via JSON:**

    Klicke auf den "GPX-Liste (JSON)"-Button auf der Webseite, um die Namen und URLs von den aktuell verfügbaren Routen zu erhalten. Nützlich für die weitere Datenverabeitung. 

## Docker Compose Befehle

*   **Container stoppen:**

    ```bash
    docker-compose down
    ```

*   **Container-Logs anzeigen:**

    ```bash
    docker-compose logs -f komootgpx-web
    ```

    `-f`: Verfolgt die Logs in Echtzeit.

*   **Container neu erstellen (z.B. nach Änderungen am Dockerfile):**

    ```bash
    docker-compose up -d --build
    ```

## Konfiguration

Die folgenden Umgebungsvariablen können konfiguriert werden:

*   `KOMOOT_EMAIL`: Deine Komoot-E-Mail-Adresse.
*   `KOMOOT_PASSWORD`: Dein Komoot-Passwort.

## Dateistruktur
```
komoot-gpx-docker/
├── docker-compose.yml # Docker Compose Konfiguration
├── Dockerfile # Docker Image Definition
├── README.md # Diese Datei
├── start.sh # Skript zum Starten des Webservers und Herunterladen von GPX-Dateien (einmalig)
├── refresh_gpx.sh # Skript zum Aktualisieren der GPX-Dateien
├── python_simple_webserver.py # Python Webserver Skript
├── index.html # (Optional) Statische Indexseite
└── requirements.txt # Python Abhängigkeiten
```
