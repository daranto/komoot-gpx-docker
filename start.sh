#!/bin/bash

# Webserver im Hintergrund starten
echo "Starte Webserver auf Port 8000..."
python python_simple_webserver.py &

#Beim ersten Start einmalig die Daten laden
./refresh_gpx.sh

# Container am Laufen halten
tail -f /dev/null
