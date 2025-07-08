FROM python:3.9-slim-buster

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# KomootGPX installieren
RUN pip install komootgpx

# Eigene Skripte kopieren
COPY start.sh .
COPY refresh_gpx.sh .
COPY python_simple_webserver.py .
COPY index.html .

# Standard-Ausgabeverzeichnis für GPX-Dateien
ENV OUTPUT_DIR=/app/gpx

# Verzeichnis erstellen
RUN mkdir -p ${OUTPUT_DIR}

# Skripte ausführbar machen
RUN chmod +x start.sh refresh_gpx.sh  # refresh_gpx.sh ausführbar machen

# Port für den Webserver freigeben
EXPOSE 8000

# Startskript beim Starten des Containers ausführen
CMD ["./start.sh"]
