# Used to change the name of cities that do not exist anymore or that the geolocator tool had difficulty finding

def modification_ville(d):
    if 'Port-Royal' in d:
        d = 'Annapolis Royal, Nouvelle-Écosse'
    elif 'Sherbrooke (St-Michel)' in d:
        d = 'Sherbrooke, Estrie'
    elif 'Erbach' in d:
        d = 'Wurtzbourg, Allemagne'
    elif 'Québec (Metropolitan Church)' in d:
        d = 'Québec, Québec'
    elif "L'Ancienne-Lorette, Capital-Nationale" in d:
        d = "L'Ancienne-Lorette"
    elif "Beaubassin" in d:
        d = "Beaubassin"
    elif "Saint-Antoine-de-l'Isle-aux-Grues" in d:
        d = "Saint-Antoine-de-l'Isle-aux-Grues"
    elif "Saint-Hyacinte" in d:
        d = "Saint-Hyacinthe, Montérégie"
    elif 'Saint-Jean-sur-Richelieu (Saint-Valentin)' in d:
        d = "Saint-Jean-sur-Richelieu, Montérégie"
    elif 'Saint-Jean-sur-Richelieu (Saint-Athanase-de-Bleury)' in d:
        d = "Saint-Jean-sur-Richelieu, Montérégie"
    elif 'Québec (Notre-Dame-de-Québec)' in d:
        d = "Basilique-cathédrale Notre-Dame de Québec, Québec, Québec, Canada"
    elif 'Québec, Capitale-Nationale' in d:
        d = "Québec, Québec, Canada"
    elif 'Saint-Charles-les-Mines' in d:
        d = 'Grand-Pré, Nouvelle-Écosse'
    elif 'Laval, Laval' in d:
        d = 'Laval, Québec, Canada'
    elif d == 'Acadie':
        d = 'Annapolis Royal, Nouvelle-Écosse'
    elif d == 'Grand-Pré (Acadie), Nouvelle-Écosse':
        d = 'Grand-Pré, Nouvelle-Écosse'
    elif d == 'Acadie, Nouvelle-Écosse':
        d = 'Annapolis Royal, Nouvelle-Écosse'
    elif d == 'Saint-Pierre, Cap-Breton, Nouvelle-Écosse':
        d = 'St. Peter''s, Nova Scotia'
    return d