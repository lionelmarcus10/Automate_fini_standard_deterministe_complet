
# ⚙️ Projet : Automates finis 

Projet semestriel L2 Gr. B7 de traitement d'automates finis


## 🖊️ Auteurs 

- [Lionel Toglan](https://github.com/lionelmarcus10)
- Kevin Kurtz
- Romane Segui
- Bereket Tadiwos


## 💾 Installation 

#### Installer le projet via Git :

```bash
  git clone https://github.com/lionelmarcus10/Automate_fini_standard_deterministe_complet
```

#### Installer les librairies nécessaires :
```bash
  pip install -r requirements.txt
```
**OU**

```bash
  pip install graphviz
  pip install matplotlib
  pip install pandas
  pip install pydot
  ```

Puis exécuter le fichier ``B7_main.py``

### Ressource nécessaire pour visualer les graphiques :

Avec __Visual Studio Code__ : installer `Graphviz Interactive Preview`

Avec __un autre IDE__ : copier le continu des fichiers `.dot` et les coller sur [ce site](http://www.webgraphviz.com/).

    
## 📖 Fonctionnalités 

Lors du lancement du programme principal, plusieurs fonctionnalités seront proposées :

| Numéro | Description     | 
| :-------- | :------- |
| `1` | `Afficher les données d'un automate (tableau + graph)` |
| `2` | `Afficher les informations d'un automate (det/std/compl)` |
| `3` | `Transformer un A en AS` |
| `4` | `Transformer un A en un ADC` |
| `5` | `Quitter + possibilité de choisir un autre automate` |
| `6 (Bonus)` | `Calcul de l'automate minimal` |
| `7 (Bonus)` | `Reconnaissances de mots` |
| `8 (Bonus)` | `Transformer un A en AC` |

_Légende :_ `A : automate`, `AS : automate standard`, `ADC : automate déterministe complet`,

`AC : automate complémentaire` 

## 📂 Dossiers

L'environnement du projet contient différents dossiers :

### B7_dot_file
Contient l'ensemble des dossiers d'automates
####  B7_Automates
Contient les fichiers ``.txt`` des automates initiaux
####  B7_simple_automate 
Contient les fichiers ``.dot`` des automates initiaux
#### B7_completed 
Contient les fichiers ``.dot`` des automates complets
#### B7_determinised
Contient les fichiers ``.dot`` des automates déterminisés
#### B7_determinised_completed
Contient les fichiers ``.dot`` des automates déterminisés + complets
#### B7_standardised
Contient les fichiers ``.dot`` des automates standards