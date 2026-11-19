import ast
import json
import sys

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

from src.jeux import backward_induction, backward_induction_tous, construire_ultimatum, jeu_entree
from src.jeux import stackelberg as stackelberg_calcul

MODEL_NAME = "llama3.1"
TAILLE_MAX_ARBRE = 20_000   # plafond (caracteres) pour l'arbre recu du LLM
MAX_PLANS = 100             # plafond contre l'explosion combinatoire


# 1. Modele
def get_llm(model: str = MODEL_NAME, temperature: float = 0.0) -> ChatOllama:
    """Modele Ollama (temperature 0 = reponses plus reproductibles)."""
    return ChatOllama(model=model, temperature=temperature)


# 2. Outils @tool (types annotes, docstring claire, sortie JSON, parametres plafonnes)
def _erreur(message: str) -> str:
    return json.dumps({"erreur": message}, ensure_ascii=False)


# Jeux deja construits : evite que le LLM ait a recopier tout l'arbre (fragile)
JEUX_NOMMES = {"jeu_entree": jeu_entree, "ultimatum": construire_ultimatum}


def _lire_arbre(arbre):
    """Accepte un dict, un texte JSON, ou un texte au format Python (apostrophes)."""
    if isinstance(arbre, dict):
        return arbre
    try:
        return json.loads(arbre)
    except ValueError:
        return ast.literal_eval(arbre)   # le LLM envoie parfois 'cle' au lieu de "cle"


@tool
def resoudre_arbre(arbre_json: str | dict = "", tous_les_plans: bool = False, nom_jeu: str = "") -> str:
    """Resout un jeu sequentiel a information parfaite par induction a rebours.

    nom_jeu : (prefere) nom d'un jeu deja construit : "jeu_entree" ou "ultimatum".
    arbre_json : sinon, l'arbre complet en JSON. Feuille : {"gains": [g1, g2]}.
        Noeud de decision : {"joueur": 0 ou 1, "actions": {"Nom": sous_arbre}}.
        Sous-jeu simultane : {"sous_jeu": {"A": [[..]], "B": [[..]]}}.
    tous_les_plans : False = un seul plan (premiere action gardee en cas d'egalite) ;
        True = tous les plans optimaux.
    Retourne un JSON : gains, plan (une action par noeud) et chemin joue.
    """
    try:
        if nom_jeu:
            if nom_jeu not in JEUX_NOMMES:
                return _erreur(f"jeu inconnu : {nom_jeu}. Jeux disponibles : {list(JEUX_NOMMES)}")
            arbre = JEUX_NOMMES[nom_jeu]()
        else:
            texte = arbre_json if isinstance(arbre_json, str) else json.dumps(arbre_json)
            if len(texte) > TAILLE_MAX_ARBRE:
                return _erreur(f"arbre trop grand (max {TAILLE_MAX_ARBRE} caracteres)")
            arbre = _lire_arbre(arbre_json)
        if tous_les_plans:
            res = {"plans": backward_induction_tous(arbre, max_plans=MAX_PLANS)}
        else:
            res = backward_induction(arbre)
    except (ValueError, SyntaxError, KeyError, TypeError, AttributeError) as e:
        return _erreur(f"arbre invalide ou non resoluble : {e}")
    return json.dumps(res, ensure_ascii=False)


@tool
def stackelberg(a: float, b: float, c: float) -> str:
    """Equilibre de Stackelberg : demande P = a - b*Q, cout marginal c, avec a > c.

    Le meneur choisit q1 en premier, le suiveur observe q1 puis choisit q2.
    Retourne un JSON : quantites, prix, profits et verification par induction
    a rebours sur une grille (si (a - c) / b <= 200).
    """
    if not (0 < b <= 100 and 0 <= c < a <= 1000):
        return _erreur("parametres invalides : il faut 0 < b <= 100 et 0 <= c < a <= 1000")
    try:
        res = stackelberg_calcul(a, b, c, verifier=(a - c) / b <= 200)
    except ValueError as e:
        return _erreur(str(e))
    return json.dumps(res, ensure_ascii=False)


TOOLS = [resoudre_arbre, stackelberg]
TOOLS_PAR_NOM = {t.name: t for t in TOOLS}



SYSTEM_PROMPT = (
    "Tu es un assistant de theorie des jeux. Pour resoudre un jeu sequentiel, "
    "tu DOIS appeler l'outil resoudre_arbre (jamais de calcul de tete). "
    "Si le jeu a un nom connu (jeu_entree, ultimatum), passe seulement nom_jeu, "
    "sans recopier l'arbre. "
    "Reponds ensuite en francais : equilibre (gains) et chemin joue."
)


def lancer_agent(question: str, llm=None, max_tours: int = 4, verbose: bool = False) -> str:
    """Boucle simple : le modele appelle les outils jusqu'a donner sa reponse finale."""
    llm_outils = (llm or get_llm()).bind_tools(TOOLS)
    messages = [SystemMessage(SYSTEM_PROMPT), HumanMessage(question)]
    reponse = None
    for _ in range(max_tours):
        reponse = llm_outils.invoke(messages)
        messages.append(reponse)
        if not reponse.tool_calls:
            break
        for appel in reponse.tool_calls:
            if verbose:
                print("[outil]", appel["name"], appel["args"])
            outil = TOOLS_PAR_NOM.get(appel["name"])
            try:
                sortie = outil.invoke(appel["args"]) if outil else _erreur("outil inconnu")
            except Exception as e:   # erreur renvoyee au modele plutot que plantage
                sortie = _erreur(f"appel d'outil invalide : {e}")
            if verbose:
                print("[resultat]", sortie)
            messages.append(ToolMessage(content=sortie, tool_call_id=appel["id"]))
    return reponse.content


def question_jeu_entree() -> str:
    return ("Resous le jeu d'entree (nom_jeu = jeu_entree) : E choisit Entrer ou Rester_dehors ; "
            "si E entre, M choisit Accepter ou Combattre. Quel est l'equilibre ?")


# 4. Tests rapides
if __name__ == "__main__":
    # Outils seuls avec .invoke() (sans LLM)
    print(resoudre_arbre.invoke({"arbre_json": json.dumps(jeu_entree())}))
    print(stackelberg.invoke({"a": 100, "b": 1, "c": 10}))

    if "--llm" in sys.argv:   # necessite Ollama lance
        print(lancer_agent(question_jeu_entree(), verbose=True))