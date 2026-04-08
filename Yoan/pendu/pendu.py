import random
import time
from unidecode import unidecode

class Pendu :

  # Variables temporaires
  lettres_devinees = []
  mot_a_deviner = ""
  mot_a_afficher = ""
  vies = 0

  # Fonction permettant d'initialiser le pendu
  # Renvoie la data (=état du jeu) correspondante
  def initialiser(mot_a_deviner, vies, start_time=None):
    mot_a_deviner = unidecode(mot_a_deviner).upper()
    print("le mot à deviner est "+mot_a_deviner)
    if start_time is None:
      start_time = time.time()
    data = {
     "mot_a_deviner" : mot_a_deviner, # Le mot à deviner (en MAJUSCULES)
     "mot_a_afficher" : "-" * len(mot_a_deviner),   # Le mot à afficher
     "lettres_testees" : [],        # Liste des lettres déjà devinées
     "vies" : vies,                  # Nombre de vies restantes
     "victoire" : False,             # True si le mot a été trouvé
     "defaite" : False,              # True si plus de vies
     "input" : "",                   # Lettre ou mot entré par l'utilisateur
     "erreurs": 0,
     "score": 0,
     "start_time": start_time,
     "temps_total": 0,
     "sl": 0
    }
    return data

  # Fonction principale à appeler en lui fournissant la data
  # La data est un dictionnaire avec les clés suivantes :
  #    mot_a_deviner, mot_a_afficher, lettres_devinees,
  #    vies, victoire, defaite, dernier_input
  # L'input est simplement la chaîne de caractère donnée au pendu
  def deviner(data, input):
    # On récupère toutes les données dans des variables temporaires
    global mot_a_afficher
    global mot_a_deviner
    global vies
    global lettres_devinees
    lettres_devinees = data["lettres_testees"]
    mot_a_deviner = data["mot_a_deviner"]
    mot_a_afficher = data["mot_a_afficher"]
    vies = data["vies"]
    erreurs = data.get("erreurs", 0)
    sl = data.get("sl", 0)
    start_time = data.get("start_time", time.time())
    entree = unidecode(input).upper()
    
    # On prépare la data (=état du jeu) qui sera envoyé en retour
    data_retour = {
      "dernier_input" : entree,
      "victoire" : False,
      "defaite" : False
    }
    
    # On appelle les fonctions deviner_lettre ou deviner_mot qui font tout le boulot
    if len(entree) == 1:
      message, erreurs, sl = Pendu.deviner_lettre(entree, erreurs, sl)
    else:
      message, erreurs, sl = Pendu.deviner_mot(entree, erreurs, sl)

    # On met à jour la data qui sera envoyée en retour
    data_retour["vies"] = vies
    data_retour["mot_a_deviner"] = mot_a_deviner
    data_retour["mot_a_afficher"] = mot_a_afficher
    data_retour["lettres_testees"] = lettres_devinees
    data_retour["erreurs"] = erreurs
    data_retour["start_time"] = start_time
    data_retour["temps_total"] = int(time.time() - start_time)
    data_retour["victoire"] = not "-" in mot_a_afficher
    data_retour["sl"] = sl

    if data_retour["victoire"]:
      data_retour["score"] = max(0, 1000 - data_retour["erreurs"] * 50 - data_retour["temps_total"])
    else:
      data_retour["score"] = max(0, 1000 + data_retour["sl"] * 30 - data_retour["temps_total"] * data_retour["erreurs"] * 5)

    if vies <= 0 :
      data_retour["defaite"] = True

    # Et enfin on retourne notre data !
    return data_retour

  # Fonction gérant le fait de deviner la présence de la lettre voulue dans le mot
  def deviner_lettre(lettre, erreurs, sl):
    global lettres_devinees
    global mot_a_deviner
    global vies
    if lettre in lettres_devinees:
      return "Cette lettre a déjà été devinée !", erreurs, sl
    else:
      lettres_devinees.append(lettre)
      print(lettre+" / "+mot_a_deviner)
      if lettre in mot_a_deviner:
        sl += 1
        Pendu.remplacer_lettre(lettre)
        return "Bonne lettre !", erreurs, sl
      else:
        Pendu.enlever_vie()
        erreurs += 1
        return "La lettre n'est pas dans le mot ! Il vous reste " + str(vies) + " vies.", erreurs, sl

  # Fonction gérant le fait de deviner le mot
  def deviner_mot(mot, erreurs, sl):
    global mot_a_afficher
    global mot_a_deviner
    global vies
    if mot == mot_a_deviner:
      mot_a_afficher = mot
      return "", erreurs, sl
    else:
      Pendu.enlever_vie()
      erreurs += 1
      return "Désolé, ce n'est pas ce mot ! Il vous reste " + str(vies) + " vies.", erreurs, sl

  # Enlève une vie
  def enlever_vie():
    global vies
    vies = vies - 1

  # Actualise le mot à afficher en remplaçant les "-" concernés par la lettre donnée
  def remplacer_lettre(lettre):
    global mot_a_afficher
    global mot_a_deviner
    for i in range(len(mot_a_deviner)):
      if mot_a_deviner[i] == lettre:
        mot = list(mot_a_afficher)
        mot[i] = lettre
        mot_a_afficher = ''.join(mot)