import os
import json

def lade_woerter_aus_liste(dateipfad):
    with open(dateipfad, 'r', encoding='ISO-8859-1') as file:
        return [line.strip() for line in file if line.strip()]
    
def sammle_reime_und_fuege_neue_woerter_hinzu(verzeichnis, daten):
    naechste_id = max([item['id'] for item in daten['words']]) + 1

    for dateiname in os.listdir(verzeichnis):
        grundwort = dateiname[:-4]  # Entfernt die .txt-Endung
        if not any(wort['word'] == grundwort for wort in daten['words']):
            # Fügt das Grundwort hinzu, falls es noch nicht existiert
            daten['words'].append({"id": naechste_id, "word": grundwort})
            naechste_id += 1

        pfad = os.path.join(verzeichnis, dateiname)
        with open(pfad, 'r', encoding='ISO-8859-1') as datei:
            reime = datei.read().splitlines()

        grundwort_id = [wort['id'] for wort in daten['words'] if wort['word'] == grundwort][0]
        reime_ids = []

        for reim in reime:
            if not any(wort['word'] == reim for wort in daten['words']):
                # Fügt den neuen Reim hinzu, falls er noch nicht existiert
                daten['words'].append({"id": naechste_id, "word": reim})
                reime_ids.append(naechste_id)
                naechste_id += 1
            else:
                reim_id = [wort['id'] for wort in daten['words'] if wort['word'] == reim][0]
                reime_ids.append(reim_id)

        # Verknüpft die IDs des Grundworts mit seinen Reimen
        daten['rhymes'][str(grundwort_id)] = reime_ids

    return daten

def erstelle_endgueltige_json_struktur(wortliste_pfad, reime_verzeichnis, ziel_json_dateipfad):
    worte = lade_woerter_aus_liste(wortliste_pfad)
    daten = {"words": [], "rhymes": {}}

    # Initialisiere Wörter mit IDs
    for id, wort in enumerate(worte, start=1):
        daten["words"].append({"id": id, "word": wort})

    # Reime sammeln, neue Wörter hinzufügen und verknüpfen
    daten = sammle_reime_und_fuege_neue_woerter_hinzu(reime_verzeichnis, daten)

    # JSON-Struktur speichern
    speichere_als_json(daten, ziel_json_dateipfad)


def speichere_als_json(daten, dateipfad):
    with open(dateipfad, 'w', encoding='ISO-8859-1') as datei:
        json.dump(daten, datei, ensure_ascii=False, indent=4)



# Pfadangaben
wortliste_pfad = 'FreestyleApp/words/CollectedWords.txt'
reime_verzeichnis = 'FreestyleApp/rhymes'
ziel_json_dateipfad = 'worte_und_reime.json'

# Endgültige JSON-Struktur erstellen und speichern
erstelle_endgueltige_json_struktur(wortliste_pfad, reime_verzeichnis, ziel_json_dateipfad)

print("Die Umwandlung wurde erfolgreich abgeschlossen.")
