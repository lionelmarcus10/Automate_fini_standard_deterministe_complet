import pandas as pd
import pydot as pyd
import re
import plotly.figure_factory as ff
import pandas as pd

""" 
Extraire les données d'un automate contenu dans un fichier texte

determiner les caracteristiques d'un automate : deterministe , standart , complet

afficher les données de l'automate en format tableau et format de graph


"""




# extraire les données d'un l'automate contenu dans un fichier texte
def extract_data_from_file(file_name):
    # extraire les données de l'automate contenu dans un fichier texte et le parser
    with open(f"Automates_B7/{file_name}", "r") as automate_file:
        # extraction des données de l'automate
        automate= automate_file.readlines()
        automate = [line.strip() for line in automate]
        automate_file.close()
        # filtrer les données de l'automate ( symbole epsilon ) car il n'est pas reconnu durant certaines opérations
        for i in range(5,len(automate)):
            if "Îµ" in automate[i]:
                automate[i] = automate[i].replace("Îµ","µ")
        # diviser en une liste de 3 elements les transitions de l'automate
        symbols = ["a","b","c","d","µ"]
        for i in range(5,len(automate)):
            transition = automate[i]
            for symbol in symbols:
                if symbol in transition:
                    automate[i] = re.split(f'({symbol})',transition)
                    break 

    return automate

#visual_displayer
#prendre en parametre la colonne des etats de l'automate
def visual_displayer(df):

    fig =  ff.create_table(df)
    fig.update_layout(
        autosize=False,
        width=700,
        height=500,
    
    )
    #fig.show()
    print("\n\n")
    print(df.to_markdown())
    print("\n\n")
# colonne des entree et sortie de l'automate
# afficher les données de l'automate en format tableau et format de graph
def display_data(automate,*number):
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
    graph = pyd.Dot('my_graph', graph_type='digraph', bgcolor='white')

    # ajouter les noeud (états) de l'automate dans le graph
     # cas d'un automate avec un seul état lisant le mot vide
    if(automate_nbr_transitions == "0" and automate_nbr_states == "1"):
        graph.add_node(pyd.Node(automate_input_states[0], shape='doublecircle', color='black', style='filled', fillcolor='burlywood'))
    else:

        # ajouter les noeud (états) de l'automate dans le graph
        for state in automate_states:

            # ajout des noeuds (états) en fonction de leur type ( entrée , sortie , entrée et sortie )
             # entrée et sortie
            if state in automate_input_states and state in automate_output_states:
                graph.add_node(pyd.Node(state, shape='doublecircle', color='black', style='filled', fillcolor='burlywood'))
            # sortie
            elif state in automate_output_states:
                graph.add_node(pyd.Node(state, shape='doublecircle', color='black', style='filled', fillcolor='white'))
            # entrée
            elif state in automate_input_states:
                graph.add_node(pyd.Node(state, shape='circle', color='black', style='filled', fillcolor='burlywood'))

        # relier les noeuds (états) de l'automate dans le graph
        for transition in automate_transitions:
            if transition[1] == "µ":
                graph.add_edge(pyd.Edge(transition[0], transition[2], label="eps",))
            else:
                graph.add_edge(pyd.Edge(transition[0], transition[2], label=transition[1],))
        

    # afficher l'automate en format graph ( .dot ) à travers une image ( extension vscode : graphviz preview )
    if(number):
        graph.write_raw(f'dot_file/output-{number[0]}.dot')
    else:
        graph.write_raw('dot_file/output.dot')
    
    # afficher les données de l'automate en format tableau
    df = pd.DataFrame(data="--",index=automate_states,columns=automate_symboles)
    for symbol in automate_symboles:
        
        for state in automate_states:
            trans_state = [state]
            for transition in automate_transitions:
                if transition[0] == state and transition[1] == symbol:
                     trans_state.append(transition[2])
            list(set(trans_state))
            if(len(trans_state) == 1 ):
                df.loc[state,symbol] = "---"
            else:
                df.loc[state,symbol] = ",".join(trans_state[1:])
        
        
    col = []
    for element in automate_states:
        if element in automate_input_states and element in automate_output_states:
            col.append("E/S")
        elif element in automate_output_states:
            col.append("S")
        elif element in automate_input_states:
            col.append("E")
        elif element not in automate_input_states and element not in automate_output_states:
            col.append("")
    df.insert(0, "",col, True)
     
    visual_displayer(df)

  

# determiner si l'automate est deterministe
def is_determinist(automate):
    # categoriser les données de l'automate
    automate_nbr_and_initial_states = automate[2]
    automate_transitions = automate[5:]
    
    #extraire les differents etats d'entrée de l'automate
    automate_input_states = list(set([ element for element in automate_nbr_and_initial_states.split(" ")[1:]]))
    
    # si l'autome a plus d'un etat d'entrée
    if(len(automate_input_states)) > 1:
        print( "l'automate n'est pas deterministe car il a plus d'un etat d'entrée")
        return False
    else:
        # etat ayant le meme libellé de transition vers differents etats
        libele_in_transition = []
        for transition in automate_transitions:
           libele_in_transition.append("".join(transition[:2]))
        if(len(libele_in_transition) != len(set(libele_in_transition))):
            print( "l'automate n'est pas deterministe car il a des etats ayant le meme libellé de transition vers differents etats")
            return False
        return True


# determiner si l'automate est standard
def is_standard(automate):
    # categoriser les données de l'automate
    automate_nbr_and_initial_states = automate[2]
    automate_transitions = automate[5:]
    
    #extraire les differents etats d'entrée de l'automate
    automate_input_states = list(set([ element for element in automate_nbr_and_initial_states.split(" ")[1:]]))
    
    # si l'autome a plus d'un etat d'entrée
    if(len(automate_input_states)) > 1:
        print( "l'automate n'est pas standard car il a plus d'un etat d'entrée")
        return False
    else:
        # fleche retour de l'etat initial vers l'etat initial
        for transition in automate_transitions:
            if transition[0] == transition[2] == automate_input_states[0]:
                print( "l'automate n'est pas standard car il a une fleche retour ( transition ) de l'etat initial vers l'etat initial")
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
        current_complete_states.append("".join(transition[:2]))

    current_complete_states = list(set(current_complete_states))
    for element in final_complete_states:
        if element not in current_complete_states:
            return False
    return True
    

# determiner si l'automate est deterministe complet ( ADC)
def is_determinist_complete(automate):
    if(is_determinist(automate) and is_complete(automate)):
        return True
    return False

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


#  Rendre deterministe complet l'automate
def determinisation_completion(automate):
    DC = is_determinist_complete(automate)
    if(DC):
        print("\n\nl'automate est déja deterministe complet\n\n")
    else:
        # verifier si c'est un automate deterministe
        determinist = is_determinist(automate)
        # verifier si c'est un automate complet
        complete = is_complete(automate)
        # determiniser l'automate
        # completer l'automate
        pass

# standardiser l'automate    
def standardisation(automate,*number):
    # savoir si l'automate est standart
    standard = is_standard(automate)
    if(standard):
        print("\n\nl'automate est déja standard\n\n")
    else:
        # categoriser les données de l'automate
        automate_nbr_and_initial_states = automate[2]
        automate_nbr_and_final_states = automate[3]
        automate_transitions = automate[5:]

        #extriaire les symboles de l'automate
        automate_symboles = list(set([symbol[1] for symbol in automate_transitions]))
        
        #extraire les états de l'automate
        automate_states = list(set([ state[0] for state in automate_transitions] + [ state[2] for state in automate_transitions]))
        
        #extraire les differents etats d'entrée et de sortie de l'automate
        automate_input_states = list(set([ element for element in automate_nbr_and_initial_states.split(" ")[1:]]))
        automate_output_states = list(set([ element for element in automate_nbr_and_final_states.split(" ")[1:]]))
        
        #instancifier un graph
        graph = pyd.Dot('my_graph', graph_type='digraph', bgcolor='white')
        
        # ajouter les noeud (états) de l'automate dans le graph
        for state in automate_states:
            graph.add_node(pyd.Node(state, shape='circle', color='black', style='filled', fillcolor='white'))
        # relier les noeuds (états) de l'automate dans le graph
        for transition in automate_transitions:
            graph.add_edge(pyd.Edge(transition[0], transition[2], label=transition[1],))
        # mettre un double cercle sur les etats de sortie
        for state in automate_output_states:
            graph.get_node(state)[0].set_shape("doublecircle")

        # creer un nouveau noeud i pour l'etat initial d'entrée
        graph.add_node(pyd.Node('i', shape='circle', color='black', style='filled', fillcolor='burlywood'))
        # relier le noeud i avec l'etat initial d'entrée
        init_trans = []
        for state in automate_input_states:
            for transition in automate_transitions:
                if(transition[0] == state):
                    init_trans.append(transition[1:])
        for element in init_trans:
            graph.add_edge(pyd.Edge('i', element[1], label=element[0],color='red', style="filled"))
        
        if( any(element in automate_input_states for element in automate_output_states)):
            graph.get_node('i')[0].set_shape("doublecircle")

        # afficher l'automate en format graph ( .dot ) à travers une image ( extension vscode : graphviz preview)
        if(number):
            graph.write_raw(f'dot_file/standard-output-{int(number[0])}.dot')
        else:
            graph.write_raw('dot_file/standard-output.dot')
        
        # afficher les données de l'automate en format tableau
        df = pd.DataFrame(data="--",index=automate_states,columns=automate_symboles)
        for symbol in automate_symboles:
            
            for state in automate_states:
                trans_state = [state]
                for transition in automate_transitions:
                    if transition[0] == state and transition[1] == symbol:
                        trans_state.append(transition[2])
                list(set(trans_state))
                if(len(trans_state) == 1 ):
                    df.loc[state,symbol] = "---"
                else:
                    df.loc[state,symbol] = ",".join(trans_state[1:])
        
        col = []
        row_standart = []
        for element in automate_states:
            if element in automate_input_states and element in automate_output_states:
                col.append("S")
                row_standart.append(element)
            elif element in automate_output_states:
                col.append("S")
            elif element in automate_input_states:
                col.append("")
                row_standart.append(element)
            elif element not in automate_input_states and element not in automate_output_states:
                col.append("")
        df.insert(0, "",col, True)
        


        row_standart = list(set(row_standart))
        final_row = ['i',"E/S"] if(any( i in automate_output_states for i in row_standart)) else ["i","E"]
        #determiner row_standart element in each symbol
        s_row = []
        for symbol in automate_symboles:
            temp = []
            temp2 = df.query('index in @row_standart')[symbol]
            for i in range(len(temp2)):
                temp.append(temp2[i])
            temp = list(set(temp))
            temp = [i for i in temp if i != "---"]
            temp = ",".join(temp)
            s_row.append(temp)
        final_row.extend(s_row)
        # ajouter la nouvelle ligne dans le tableau
        df.loc[f"{final_row[0]}"] = final_row[1:]
        

        # add new row of standardisation
        
        visual_displayer(df)
        
#verifier si l'automate contient un ε
def have_epsilon(automate):
    automate_transitions = automate[5:]
    for transition in automate_transitions:
        if("µ" in transition):
            return True
    return False
    #return True if("µ" in any(transition)for transition in automate_transitions) else False

# fontion pour trouver les epsilon cloture pour chaque etat
def find_eps_cloture(automate_transitions, automate_states):
        #if(have_epsilon(x) == True):

            # liste des transitions qui portent le symbole ε
            eps_cloture = []
            state_transitions = [transition for transition in automate_transitions if'µ' in transition]

            # trouver les premières epsilon cloture de chaque etat
            for state in automate_states:
                # trouver toutes les transitions qui partent de l'etat et portent le symbole ε
                # prendre la deuxieme valeur et la conserver
                state_transitions2 = [state,list(set([state] + [transition[-1] for transition in state_transitions if transition[0] == state]))]
                eps_cloture.append(state_transitions2)

            # pour chaque state , ajouter toutes les clotures epsilon possible ( de ses autres clotures epsilon)
            eps_cloture2 = eps_cloture
            k = True
            while k:

                temp_closure = eps_cloture2

                for state in automate_states:
                    
                    y = eps_cloture[automate_states.index(state)][-1]
                    for element in y:
                        x = eps_cloture2[automate_states.index(state)][-1] + eps_cloture2[automate_states.index(element)][-1]
                        x = list(set(x))
                        eps_cloture2[automate_states.index(state)][-1] = x
                if temp_closure == eps_cloture2:
                    k = False
            return eps_cloture2
                    
def determinisation(automate):

    # categoriser les données de l'automate
    automate_nbr_and_initial_states = automate[2]
    automate_nbr_and_final_states = automate[3]
    automate_transitions = automate[5:]

    automate_symboles = list(set([ transition[1] for transition in automate_transitions]))
    automate_states = list(set([ state[0] for state in automate_transitions] + [ state[2] for state in automate_transitions]))

    #extraire les differents etats d'entrée et de sortie de l'automate
    automate_input_states = list(set([ element for element in automate_nbr_and_initial_states.split(" ")[1:]]))
    automate_output_states = list(set([ element for element in automate_nbr_and_final_states.split(" ")[1:]]))
     
    terminal = "E/S" if any( i in automate_output_states for i in automate_input_states) else "E"

    # modelisation pandas 
    df = pd.DataFrame(data="--",index=automate_states,columns=automate_symboles)

    # verifier si l'automate contient un ε car la determinisation est differente dans ce cas
    if(have_epsilon(automate)):
        # supprimer le symbole ε de la liste des symboles car il n'est pa considéré durant la determinisation
        automate_symboles = [symbol for symbol in automate_symboles if symbol != "µ"]
        # trouver les epsilon cloture pour chaque etat
        eps_cloture = find_eps_cloture(automate_transitions, automate_states)

        # selectionner les transitions qui ne portent pas le symbole ε
        wanted_transitions = [transition for transition in automate_transitions if transition[1] != "µ"]

        # modelisation pandas 
        df = pd.DataFrame(data="--",index=automate_input_states,columns=automate_symboles)



        # faire une boucle pour remplir le tableau avec new results of states        
        for symbol in automate_symboles:
            for state in automate_input_states:
                if type(state) != list:    
                    temp_trans_state = []
                    for additional_state in eps_cloture[automate_states.index(state)][-1]:
                        for transition in wanted_transitions:
                            if transition[0] == additional_state and transition[1] == symbol:
                                temp_trans_state.append(transition[2])
                    temp_trans_state = list(set(temp_trans_state))
                    if(len(temp_trans_state) == 0 ):
                        df.loc[state,symbol] = "---"
                    else:
                        df.loc[state,symbol] = "-".join(temp_trans_state[:])
        # fonction qui fait la table de transition des nouveaux etats



        # debut de la boucle
        modif = True

        while modif:
            # prendre les nouveaux etats de chaque ligne
            new_state = []
            for index, row in df.iterrows():
                for element in row:
                        new_state.append(element)
            new_state = list(set(new_state))
            # les mettre dans une liste
            new_state = [element for element in new_state if element != "---"]
            # verifier si les nouveaux etats sont deja dans les etats présent dans la colonne du tableau
            new_state2 = []
            for i in range(len(new_state)):
                
                if new_state[i] not in df.index:
                    new_state2 = new_state2 + [new_state[i]]
            new_state = new_state2

            # condition d'arret pour la boucle
            if len(new_state) == 0:
                modif = False
            # refaire la ligne de transition pour chaque nouvel etat
            for state in new_state: 
                temp_main_state = []
                for symbol in automate_symboles:
                    # trouver chaque transition de l'etat pour chaque symbole
                    x = state.split("-")
                    temp_states1 = [] 
                    for single_state in x:

                        for additional_state in eps_cloture[automate_states.index(single_state)][-1]:
                            for transition in wanted_transitions:
                                if transition[0] == additional_state and transition[1] == symbol:
                                    temp_states1.append(transition[2])
                                

                    temp_states1 = list(set(temp_states1))
                    temp_main_state.append(temp_states1)

                for i in range(len(temp_main_state)):
                    if len(temp_main_state[i]) == 0:
                        temp_main_state[i] = "---"
                    else:
                        temp_main_state[i] = "-".join(temp_main_state[i])
                
                # ajouter la ligne de transition dans le tableau pour l'etat 
                df.loc[f"{state}"] = temp_main_state

        # fin de la boucle    
            
        # remodeler pour la lecture de liste dans des listes TODO
        """col = []
        for element in automate_input_states:
            if element in automate_input_states and element in automate_output_states:
                col.append("E/S")
            elif element in automate_output_states:
                col.append("S")
            elif element in automate_input_states:
                col.append("E")  
            elif element not in automate_input_states and element not in automate_output_states:
                col.append("")
        

        df.insert(0, "",col, True)"""
        
        visual_displayer(df)

    else:
        pass
    pass               

 
                


# dire pourquoi l'automate n'est pas complet

# determiniser l'automate -
# completer l'automate 
# lire un langage complémentaire
# prettytable
# minimiser l'automate
# tester les mots


if __name__ == '__main__':

    x = extract_data_from_file("B7-35.txt")
    display_data(x,35)
    automate_info(x)
    determinisation(x)


    