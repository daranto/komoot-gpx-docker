#!/bin/bash

# Standardwerte aus Umgebungsvariablen lesen
EMAIL="${KOMOOT_EMAIL}"
PASSWORD="${KOMOOT_PASSWORD}"
OUTPUT_DIR="/app/gpx"

# Überprüfen, ob E-Mail und Passwort vorhanden sind
if [ -z "$EMAIL" ] || [ -z "$PASSWORD" ]; then
  echo "Fehler: KOMOOT_EMAIL und KOMOOT_PASSWORD Umgebungsvariablen müssen gesetzt sein."
  exit 1
fi

# Ausgabeverzeichnis leeren
echo "Leere Ausgabeverzeichnis: ${OUTPUT_DIR}"
rm -rf "${OUTPUT_DIR}"/*

# Ausgabeverzeichnis neu erstellen
mkdir -p "${OUTPUT_DIR}"

# KomootGPX-Befehl zusammenstellen
KOMOOTGPX_CMD="komootgpx -o ${OUTPUT_DIR} -m \"${EMAIL}\" -p \"${PASSWORD}\" -a"

echo "Führe aus: komootgpx -o ${OUTPUT_DIR} -m <zensiert> -p <zensiert> -a"
eval $KOMOOTGPX_CMD
