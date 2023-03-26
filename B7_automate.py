import pandas as pd
import pydot as pyd
import re
import plotly.figure_factory as ff
import pandas as pd

""" 
Extraire les données d'un automate contenu dans un fichier texte

determiner les caracteristiques d'un automate : deterministe , standart , complet

afficher les données de l'automate en format tableau markdown et format de graph ( dot file et tableau dans le navigateur)


"""




# extraire les données d'un l'automate contenu dans un fichier texte
def extract_data_from_file(file_name):
    # extraire les données de l'automate contenu dans un fichier texte et le parser
    with open(f"B7_Automates/{file_name}", "r") as automate_file:
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

    df2 = df.copy()
    state = []
    for row, col in df.iterrows():
        state.append(row)
    df2.insert(0, "",state, True)

    fig =  ff.create_table(df2)
    fig.update_layout(
        autosize=False,
        width=700,
        height=500,
    
    )
    fig.show()
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
        graph.write_raw(f'B7_dot_file/B7_simple_automate/B7-output-{number[0]}.dot')
    else:
        graph.write_raw('B7_dot_file/B7_simple_automate/B7-output.dot')

    
    df = create_automate_simple_table(automate_states,automate_symboles,automate_transitions)
        
        
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

    print("\naffichage de l'automate en format tableau : ") 
    visual_displayer(df)

    
def create_automate_simple_table(automate_states,automate_symboles,automate_transitions):
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
    return df


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
            print( "l'automate n'est pas complet car il a des etats qui ne sortent pas de flèches comprenant tous les symboles de l'automate vers d'autres etats")
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
def determinisation_completion(automate,*number):
    DC = is_determinist_complete(automate)
    if(DC):
        automate_transitions = automate[5:]
        #extriaire les symboles de l'automate
        automate_symboles = list(set([symbol[1] for symbol in automate_transitions]))
        #extraire les états de l'automate
        automate_states = list(set([ state[0] for state in automate_transitions] + [ state[2] for state in automate_transitions]))
        
        df = create_automate_simple_table(automate_states,automate_symboles,automate_transitions)
        print("\n\nl'automate est déja deterministe complet\n\n")
        automate_nbr_and_initial_states = automate[2]
        automate_nbr_and_final_states = automate[3]
        #extraire les differents etats d'entrée et de sortie de l'automate
        automate_input_states = list(set([ element for element in automate_nbr_and_initial_states.split(" ")[1:]]))
        automate_output_states = list(set([ element for element in automate_nbr_and_final_states.split(" ")[1:]]))

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
        
        return df

    else:
        # verifier si c'est un automate deterministe
        determinist = is_determinist(automate)
        # verifier si c'est un automate complet
        complete = is_complete(automate)
        # determiniser l'automate
        if(complete and not determinist):
            df = determinisation(automate,number)
        elif(not complete and not determinist):
            df = determinisation(automate,number)
            df = completion(df,number)
        elif(not complete and determinist):
            df = completion(automate,number)
        
        

        # creer une modelisation graphique de l'automate
        graph = pyd.Dot('my_graph', graph_type='digraph', bgcolor='white')
        # ajouter les etats de l'automate
        for element in df.index:
            if df.loc[element][0] == "E/S":
                graph.add_node(pyd.Node(element, shape="doublecircle", style="filled", fillcolor="blurlywood"))
            elif df.loc[element][0] == "E":
                graph.add_node(pyd.Node(element, shape="circle", style="filled", fillcolor="burlywood"))
            elif df.loc[element][0] == "S":
                graph.add_node(pyd.Node(element, shape="doublecircle", style="filled", fillcolor="white"))
            elif df.loc[element][0] == "S/E":
                graph.add_node(pyd.Node(element, shape="circle", style="filled", fillcolor="white"))

        # ajouter les transitions de l'automate
        for element in df.index:
            for i in range(1,len(df.loc[element])):
                graph.add_edge(pyd.Edge(element, df.loc[element][i], label=df.columns[i]))

        # afficher le graphique de l'automate
        if number:
            graph.write_raw(f'B7_dot_file/B7_determinised_completed/B7-determinised-completed-output-{number[0]}.dot')
        else:
            graph.write_raw('B7_dot_file/B7_determinised_completed/B7-determinised-completed-output.dot')
            
        # afficher l'automate
        print("\n\n l'automate deterministe complet est : \n\n")
        visual_displayer(df)
        
    return df

# standardiser l'automate    
def standardisation(automate,*number):
    # savoir si l'automate est standart
    standard = is_standard(automate)
    if(standard):
        print("\n\nl'automate est déja standard\n\n")
        return "l'automate est déja standard"
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
            graph.write_raw(f'B7_dot_file/B7_standardised/B7-standard-output-{int(number[0])}.dot')
        else:
            graph.write_raw('B7_dot_file/B7_standardised/B7-standard-output.dot')
        
        # afficher les données de l'automate en format tableau
        
        df = create_automate_simple_table(automate_states,automate_symboles,automate_transitions)
        
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
        

        #affichage
        print("\n\nAutomate standardisé : ")
        visual_displayer(df)
        return df
        
        
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

# fonction pour determiniser l'automate                    
def determinisation(automate,*number):

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
    df = pd.DataFrame(data="--",index=automate_input_states,columns=automate_symboles)

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

    else:
        for symbol in automate_symboles:
            for state in automate_input_states:
                if type(state) != list:
                    temp_trans_state = []
                    for transition in automate_transitions:
                        if transition[0] == state and transition[1] == symbol:
                            temp_trans_state.append(transition[2])
                    temp_trans_state = list(set(temp_trans_state))
                    if(len(temp_trans_state) == 0 ):
                        df.loc[state,symbol] = "---"
                    else:
                        df.loc[state,symbol] = "-".join(temp_trans_state[:])
        
        # debut de la boucle
        modif = True

        while modif:
            # recupérer les nouveaux etats
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
                                for transition in automate_transitions:
                                    if transition[0] == single_state and transition[1] == symbol:
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
    
    # ajouter les indications des etats d'entree et de sortie
    col = []
    for element in df.index:
        x  = element.split("-")
        content= ""
        for single_state in x:
            if single_state in automate_input_states and single_state in automate_output_states:
                content = "E/S"
                break
            elif single_state in automate_output_states:
                content = "S"
                break
            elif single_state in automate_input_states:
                content = "E"
                break
        col.append(content)
    df.insert(0, "",col, True)

    print("automate determinisé: ")
    visual_displayer(df)
        
            

    # creer une modelisation graphique de l'automate
    graph = pyd.Dot('my_graph', graph_type='digraph', bgcolor='white')
    
    # ajouter les etats ( noeuds ) de l'automate
    for index, row in df.iterrows():
        if df.loc[index][0] == "E/S":
            graph.add_node(pyd.Node(index, shape='doublecircle', color='black', style='filled', fillcolor='burlywood'))
        elif df.loc[index][0] == "E":
            graph.add_node(pyd.Node(index, shape='circle', color='black', style='filled', fillcolor='burlywood'))
        elif df.loc[index][0] == "S":
            graph.add_node(pyd.Node(index, shape='doublecircle', color='black', style='filled', fillcolor='white'))
        elif df.loc[index][0] == "":
            graph.add_node(pyd.Node(index, shape='circle', color='black', style='filled', fillcolor='white'))
    # ajouter les transitions ( relier les noeuds / etats)
    for row, columns in df.iterrows():
        for i in range(1,len(columns)):
            if columns[i] != "---":
                graph.add_edge(pyd.Edge(row, columns[i], label=columns.index[i]))
          

    
    if(number):
        graph.write_raw(f'B7_dot_file/B7_determinised/B7-determinised_output-{number[0]}.dot')
    else:
        graph.write_raw('B7_dot_file/B7_determinised/B7-determinised_output.dot')

    return df              

#fonction pour rendre complet un automate:
def completion(automate,*number):
    # si c'est un automate extrait d'un fichier
    if(type(automate) == list):
        #extraire les informations de l'automate
        automate_nbr_and_initial_states = automate[2]
        automate_nbr_and_final_states = automate[3]
        #extraire les transitions de l'automate
        automate_transitions = automate[5:]
        #extriaire les symboles de l'automate
        automate_symboles = list(set([symbol[1] for symbol in automate_transitions]))
        #extraire les états de l'automate
        automate_states = list(set([ state[0] for state in automate_transitions] + [ state[2] for state in automate_transitions]))
        # creer un dataframe
        df =  create_automate_simple_table(automate_states,automate_symboles,automate_transitions)
         #extraire les differents etats d'entrée et de sortie de l'automate
        automate_input_states = list(set([ element for element in automate_nbr_and_initial_states.split(" ")[1:]]))
        automate_output_states = list(set([ element for element in automate_nbr_and_final_states.split(" ")[1:]]))

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


    else:
    # c'est un automate determinisé
        df = automate

    # Processus de completion pour les automates simple et deterministe ( mettre les etats poubelles)
    for row, columns in df.iterrows():
            for i in range(len(columns)):
                if columns[i] == "---":
                    df[f'{columns.index[i]}'][row] = "P"
    # ajouter l'etat poubelle dans le tableau
    df.loc["P"] = "P"
    df.loc["P"][0] = ""
    
    # creer une modelisation graphique de l'automate
    graph = pyd.Dot('my_graph', graph_type='digraph', bgcolor='white')
   
    # creer les noeuds de l'automate
    for row in df.index:
        if df[f"{columns.index[0]}"][row] == "E":
            graph.add_node(pyd.Node(row, shape='circle', color='black', style='filled', fillcolor='burlywood'))
        elif df[f"{columns.index[0]}"][row] == "S":
            graph.add_node(pyd.Node(row, shape='doublecircle', color='black', style='filled', fillcolor='white'))
        elif df[f"{columns.index[0]}"][row] == "E/S":
            graph.add_node(pyd.Node(row, shape='doublecircle', color='black', style='filled', fillcolor='burlywood'))
        elif df[f"{columns.index[0]}"][row] == "":
            graph.add_node(pyd.Node(row, shape='circle', color='black', style='filled', fillcolor='white'))
    
    # creer les transitions entre les differents noeuds de l'automate
    for row, columns in df.iterrows():
        for i in range(1,len(columns)):
            graph.add_edge(pyd.Edge(row, columns[i], label=columns.index[i]))
    
    # afficher le graph de l'automate
    if number:
        graph.write_raw(f'B7_dot_file/B7_completed/B7-completed-output-{number[0]}.dot')
    else:
        graph.write_raw('B7_dot_file/B7_completed/B7-completed-output.dot')

    print("\n\nautomate completé: ")
    visual_displayer(df) 
    return df

#lecture de language complementaire
def complementarisation(automate,*number):
    # verifier si Automate est deterministe et complet sinon le determiniser et le completer
    if(is_determinist_complete(automate) == False):
        if(number):
            df = determinisation_completion(automate,number[0])
        else:
            df = determinisation_completion(automate)
    else:
        if(type(automate) == list):
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

            df = create_automate_simple_table(automate_states,automate_symboles,automate_transitions)

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
        else:
            df = automate
            
    # faire la complementarisation
     # supprimer les sorties de l'automate
     # mettre les sorties au niveau des etats qui n'en avaient pas avant
    for row, columns in df.iterrows():
        if(columns[0] == "E/S"):
            df[f"{columns.index[0]}"][row] = "E"
        elif(columns[0] == "S"):
            df[f"{columns.index[0]}"][row] = ""
        elif(columns[0] == "E"):
            df[f"{columns.index[0]}"][row] = "E/S"
        elif(columns[0] == ""):
            df[f"{columns.index[0]}"][row] = "S"
    
    # creer le graph puis le mettre dans un fichier .dot
    graph = pyd.Dot('my_graph', graph_type='digraph', bgcolor='white')
    # creer les noeuds de l'automate
    for row in df.index:
        if df[f"{columns.index[0]}"][row] == "E":
            graph.add_node(pyd.Node(row, shape='circle', color='black', style='filled', fillcolor='burlywood'))
        elif df[f"{columns.index[0]}"][row] == "S":
            graph.add_node(pyd.Node(row, shape='doublecircle', color='black', style='filled', fillcolor='white'))
        elif df[f"{columns.index[0]}"][row] == "E/S":
            graph.add_node(pyd.Node(row, shape='doublecircle', color='black', style='filled', fillcolor='burlywood'))
        elif df[f"{columns.index[0]}"][row] == "":
            graph.add_node(pyd.Node(row, shape='circle', color='black', style='filled', fillcolor='white'))
    # creer les transitions entre les differents noeuds de l'automate
    for row, columns in df.iterrows():
        for i in range(1,len(columns)):
            graph.add_edge(pyd.Edge(row, columns[i], label=columns.index[i]))
    # afficher le graph de l'automate
    if number:
        graph.write_raw(f'B7_dot_file/B7_complementarised/B7-complementarised-output-{number[0]}.dot')
    else:
        graph.write_raw('B7_dot_file/B7_complementarised/B7-complementarised-output.dot')
    

    print("\n\n automate complementaire: ")
    visual_displayer(df)
    return df                   


# reconnaitre un mot dans un automate
def word_recognition(automate):
    # demander à l'utilisateur de saisir le mot à reconnaitre, le mot correspondant à la fin du mot sera "fin"
    word = input("Entrer le mot à reconnaitre: ")
    det_comp = determinisation_completion(automate)
    # verifier si le mot est reconnu par l'automate
    visual_displayer(det_comp)
    while(word != "fin"):
        print(f"le mot à reconnaitre est: {word}")
        # essayer de reconnaitre le mot dans l'automate
        start = []
        # trouver les entrées de l'automate
        for row, columns in det_comp.iterrows():
            if(columns[0] == "E/S" or columns[0] == "E"):
                start.append(row)
        # Pour chaque entrée : 
        possible_first_stransitions = []
        for element in start:
            ele_line = det_comp.loc[element]
            # lister toutes les transitions possibles à partir de l'entrée ( copier la ligne de l'etat )
            try:
                    x = ele_line[word[0]]
                    possible_first_stransitions.append(x)  
            except:
                break
        if(len(possible_first_stransitions) == 0):
            print("\n\nNon\n\n")
        else:
            word = word[1:]
            # pour chaque element de transition possible
            for element in possible_first_stransitions:
                # faire une boucle pour parcourir le mot à reconnaitre
                reconnue = 0
                k = element
                while reconnue == 0:
                    # trouver une condition d'arrêt de la boucle
                    try:
                        if(len(word) == 0):
                            if(det_comp[f"{columns.index[0]}"][k] == "S" or det_comp[f"{columns.index[0]}"][k] == "E/S"  ):
                                print("\n\nOui\n\n")
                                return 0
                            else:
                                reconnue = 1
                                break
                        k2 = det_comp[word[0]][k]
                        # si la longueur du mot est supérieur à 1 on incrémente
                        if(len(word) > 1):
                            word = word[1:]
                            k = k2
                        # sinon on cherche à savoir si c'est une sortie 
                        else:
                            # si c'est une sortie on affiche oui
                            if det_comp[f"{columns.index[0]}"][k2] == "S" or det_comp[f"{columns.index[0]}"][k2] == "E/S":
                                print("\n\nOui\n\n")
                                return 0
                            else:
                            # sinon on affiche non
                                reconnue = 1
                    except:
                        reconnue = 1
            if reconnue == 1:
                print("\n\nNon\n\n")
                
                    
             

        # demander à saisir le nouveau mot à reconnaitre
        print("\nvous pouvez saisir un autre mot à reconnaitre ou taper 'fin' pour quitter\n")
        word = input("Entrer le nouveau mot à reconnaitre: ")
    pass

if __name__ == '__main__':

    x = extract_data_from_file("B7-2.txt")
    df = word_recognition(x)
