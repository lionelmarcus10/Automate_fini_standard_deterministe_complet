import pandas as pd
import numpy as np
import pydot as pyd

""" 
Extraire les données d'un automate contenu dans un fichier texte

determiner les caracteristiques d'un automate : deterministe , standart , complet

afficher les données de l'automate en format tableau et format de graph


"""

# extraire les données d'un l'automate contenu dans un fichier texte
def extract_data_from_file(file_name):
    with open(f"{file_name}", "r") as automate_file:
        automate= automate_file.readlines()
        automate = [line.strip() for line in automate]
        automate_file.close()

    return automate

# afficher les données de l'automate en format tableau et format de graph
def display_data(automate):
    # categoriser les données de l'automate
    automate_nbr_symboles = automate[0]
    automate_nbr_states = automate[1]
    automate_nbr_and_initial_states = automate[2]
    automate_nbr_and_final_states = automate[3]
    automate_nbr_transitions = automate[4]
    automate_transitions = automate[5:]

    #extriaire les symboles de l'automate
    automate_symboles = list(set([symbol[1] for symbol in automate_transitions]))
    
    #extraire les états de l'automate
    automate_states = list(set([ state[0] for state in automate_transitions] + [ state[2] for state in automate_transitions]))
    
    #extraire les differents etats d'entrée et de sortie de l'automate
    automate_input_states = list(set([ element for element in automate_nbr_and_initial_states.split(" ")[1:]]))
    automate_output_states = list(set([ element for element in automate_nbr_and_final_states.split(" ")[1:]]))
    
    #instancifier un graph
    graph = pyd.Dot('my_graph', graph_type='graph', bgcolor='white')
    
    # ajouter les noeud (états) de l'automate dans le graph
    for state in automate_states:
        graph.add_node(pyd.Node(state, shape='circle', color='black', style='filled', fillcolor='white'))
        
    # afficher l'automate en format graph à travers une image
    graph.write_raw('input.dot')

    
    # afficher les données de l'automate en format tableau


# determiner si l'automate est deterministe
def is_determinist(automate):
    # categoriser les données de l'automate
    automate_nbr_and_initial_states = automate[2]
    automate_transitions = automate[5:]
    
    #extraire les differents etats d'entrée de l'automate
    automate_input_states = list(set([ element for element in automate_nbr_and_initial_states.split(" ")[1:]]))
    
    if(len(automate_input_states)) > 1:
        return False
    else:
        # etat ayant le meme libellé de transition vers differents etats
        libele_in_transition = []
        for transition in automate_transitions:
           libele_in_transition.append(transition[:2])
        if(len(libele_in_transition) != len(set(libele_in_transition))):
            return False
        return True


# determiner si l'automate est standard
def is_standard(automate):
    # categoriser les données de l'automate
    automate_nbr_and_initial_states = automate[2]
    automate_transitions = automate[5:]
    
    #extraire les differents etats d'entrée de l'automate
    automate_input_states = list(set([ element for element in automate_nbr_and_initial_states.split(" ")[1:]]))
    
    if(len(automate_input_states)) > 1:
        return False
    else:
        # fleche retour de l'etat initial vers l'etat initial
        for transition in automate_transitions:
            if transition[0] == transition[2] == automate_input_states[0]:
                return False
        return True


# determiner si l'automate est complet
def is_complete(automate):
    automate_transitions = automate[5:]
    #extraire les symboles de l'automate
    automate_symboles = list(set([symbol[1] for symbol in automate_transitions]))
    #extraire les états de l'automate
    automate_states = list(set([ state[0] for state in automate_transitions] + [ state[2] for state in automate_transitions] ))
    # verifier si de chaque etat sortent des flèches comprenant tous les symboles de l'automate vers d'autres etats
    final_complete_states = []
    current_complete_states = []

    for state in automate_states:
        for symbol in automate_symboles:
            final_complete_states.append(state+symbol)

    for transition in automate_transitions:
        current_complete_states.append(transition[:2])

    current_complete_states = list(set(current_complete_states))
    for element in final_complete_states:
        if element not in current_complete_states:
            return False
    return True
    

# afficher toutes les informations de l'automate : deterministe , standart , complet
def automate_info(automate):
    # savoir si l'automate est deterministe
    determinist = "deterministe" if is_determinist(automate) else "non deterministe"
    # savoir si l'automate est standart
    standard = "standard" if is_standard(automate) else "non standard"
    # savoir si l'automate est complet
    complete = "complet" if is_complete(automate) else "non complet"
    # afficher les informations de l'automate : deterministe , standart , complet
    print(f"\n\nl'automate est : { determinist}, {standard}, {complete}\n\n")


if __name__ == "__main__":
    automate = extract_data_from_file("test.txt")
    automate_info(automate)
    
    