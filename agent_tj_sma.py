import json

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

MODEL_NAME = "llama3.1"


# 1. Modele
def get_llm(model: str = MODEL_NAME, temperature: float = 0.0) -> ChatOllama:
    """Retourne le modele Ollama (temperature 0 = reponses reproductibles)."""
    return ChatOllama(model=model, temperature=temperature)


# 2. Outil @tool d'exemple : Stackelberg
#    Demande : types annotes, docstring claire, sortie JSON, parametres plafonnes
@tool
def stackelberg(a: float, b: float, c: float) -> str:
    """Equilibre de Stackelberg (demande P = a - b*Q, cout unitaire c).

    Le meneur choisit q1 en premier, le suiveur repond avec q2.
    Retourne un JSON avec les quantites et les profits.
    """
    # Parametres plafonnes / valides
    if not (0 < b <= 1000 and 0 <= c < a <= 1_000_000):
        return json.dumps({"erreur": "parametres invalides : il faut 0 < b <= 1000 et 0 <= c < a"})

    q1 = (a - c) / (2 * b)
    q2 = (a - c) / (4 * b)
    profit_meneur = (a - c) ** 2 / (8 * b)
    profit_suiveur = (a - c) ** 2 / (16 * b)
    return json.dumps(
        {
            "q1": q1,
            "q2": q2,
            "profit_meneur": profit_meneur,
            "profit_suiveur": profit_suiveur,
        }
    )


TOOLS = [stackelberg]


# 3. Chaine prompt | modele | parser (a etendre a l'ultimatum)
def build_ultimatum_proposer_chain(llm: ChatOllama):
    """Proposant LLM : doit repondre par 'CHOIX: <entier entre 0 et total>'."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Tu es un joueur rationnel dans un jeu de l'ultimatum."),
            (
                "human",
                "Tu dois partager {total} unites. Tu proposes x au repondant. "
                "S'il accepte, tu gagnes {total} - x et lui x ; sinon (0, 0). "
                "Reponds uniquement par une ligne : CHOIX: <x>",
            ),
        ]
    )
    return prompt | llm | StrOutputParser()


# 4. Tests rapides
if __name__ == "__main__":
    # Test de l'outil seul (sans LLM) : a=100, b=1, c=10 -> q1=45, q2=22.5
    print(stackelberg.invoke({"a": 100, "b": 1, "c": 10}))

    # Test du modele (necessite Ollama lance)
    llm = get_llm()
    print(llm.invoke("Dis bonjour en une phrase.").content)

    # Test de la chaine ultimatum
    chain = build_ultimatum_proposer_chain(llm)
    print(chain.invoke({"total": 10}))