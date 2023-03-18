import pandas as pd
import pydot as pyd
import re
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
     
    print("\n\n",df,"\n\n")

# determiner si l'automate est deterministe
def is_determinist(automate):
    # categoriser les données de l'automate
    automate_nbr_and_initial_states = automate[2]
    automate_transitions = automate[5:]
    
    #extraire les differents etats d'entrée de l'automate
    automate_input_states = list(set([ element for element in automate_nbr_and_initial_states.split(" ")[1:]]))
    
    # si l'autome a plus d'un etat d'entrée
    if(len(automate_input_states)) > 1:
        return False
    else:
        # etat ayant le meme libellé de transition vers differents etats
        libele_in_transition = []
        for transition in automate_transitions:
           libele_in_transition.append("".join(transition[:2]))
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
    
    # si l'autome a plus d'un etat d'entrée
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
        print(row_standart)
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
        #final2 = [ [[].append(i) for i in automate_input_states if i in j] for j in s_row]       
        #print(s_row, final2)

        # add new row of standardisation
        
        print("\n\n",df,"\n\n")
        
#verifier si l'automate contient un ε
def have_epsilon(automate):
    automate_transitions = automate[5:]
    return True if("ε" in any(transition)for transition in automate_transitions) else False

# fontion pour trouver les epsilon cloture pour chaque etat
def eps_cloture(automate_transitions, automate_states):
        if(have_epsilon(x) == True):

            # liste des transitions qui portent le symbole ε
            eps_cloture = []
            state_transitions = [transition for transition in automate_transitions if'µ' in transition]

            # trouver les premières epsilon cloture de chaque etat
            for state in automate_states:
                # trouver toutes les transitions qui partent de l'etat et portent le symbole ε
                # prendre la deuxieme valeur et la conserver
                state_transitions2 = [state,list(set([state] + [transition.split("µ")[-1] for transition in state_transitions if transition.split("µ")[0] == state]))]
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
                    
                

    # fonction pour determiniser en haut
                

#determiner les états ( simple ou double caractère) de l'automate


if __name__ == '__main__':

    x = extract_data_from_file("B7-32.txt")
    display_data(x,32)
    print(eps_cloture(x))

    