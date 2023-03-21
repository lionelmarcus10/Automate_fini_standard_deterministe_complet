from B7_automate import display_data, extract_data_from_file, automate_info, standardisation, determinisation_completion

# menu principal proposant les options de l'application
def menu():
    print("1- Afficher les données de l'automate en format tableau et format de graph")
    print("2- Afficher toutes les informations de l'automate : deterministe , standart , complet")
    print("3- Transformer l'automate en un automate standard (AS)")
    print("4- Transformer l'automate en un automate deterministe complet (ADC)")
    print("5- Quitter")
    print("6- ( Bonus ) Calcul de l'automate minimal (AM)")
    print("7- ( Bonus ) Test de reconnaissance des mots")
    print("8- ( Bonus ) Creation d'un automate reconnaissant le langage complementaire")
    choix = input("choisir une option :   ")
    return choix

# fonction principale qui permet de lancer l'application
def run_program():
    restart = True
    while restart:
        print("Avec quel automate voulez vous travailler ?")
        auto_number = input("entrer le numéro de l'automate :  ")
        
        #mettre sous variable le nom du fichier
        automate = extract_data_from_file(f"B7-{auto_number}.txt")
        
        choix_menu = 0
        while choix_menu != "5":
            if choix_menu in ["1", "2", "3", "4", "5"]:
                pass
            else:
                choix_menu = menu()

            if choix_menu == "1":
                display_data(automate, int(auto_number))
            elif choix_menu == "2":
                automate_info(automate)
            elif choix_menu == "3":
                standardisation(automate,auto_number)
            elif choix_menu == "4":
                determinisation_completion(automate,auto_number)
            choix_menu = menu()
        #importer les autres fonctions
        restart = True if input("voulez vous continuer avec un autre automate ? (y/n) : ") == "y" else False
