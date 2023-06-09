#!/bin/bash

# Pfad zur SD-Karte festlegen (bin diesem Beispiel /dev/mmcblk0)
SD_KARTE="/dev/mmcblk0"

# Pfad zum Speichern des Image-Dateisystems festlegen (bin diesem Beispiel /home/pi/images)
IMAGE_SPEICHERORT="/home/pi/images"

# Name des Image-Dateisystems festlegen (bin diesem Beispiel raspbian.img)
IMAGE_NAME="raspbian.img"

# Dateisystem der SD-Karte aushängen, falls es bereits gemountet ist
sudo umount ${SD_KARTE}*

# Image des Dateisystems der SD-Karte erstellen und speichern
sudo dd bs=4M if=${SD_KARTE} of=${IMAGE_SPEICHERORT}/${IMAGE_NAME}

# Prüfen, ob das Image-Dateisystem erfolgreich erstellt wurde
if [ $? -eq 0 ]; then
    echo "Das Image-Dateisystem wurde erfolgreich erstellt und gespeichert."
else
    echo "Es ist ein Fehler beim Erstellen des Image-Dateisystems aufgetreten."
fi