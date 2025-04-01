from unidecode import unidecode
from fuzzywuzzy import fuzz
import random
from Reglas_inferencia import *
from datetime import datetime
import string
import pandas as pd

def normalizar(texto):
    """
    Descripción: Normaliza el texto para facilitar la comparación.
    Args:
        texto (str): Texto a normalizar.
    Returns:
        str: Texto normalizado.
    """
    
    texto = unidecode(texto).lower().strip()
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    return texto

# APPLY INFERENCE RULES
def infer_conclusion(premises):
    """
    Descripción: Inferir una conclusión a partir de las premisas dadas
    Args:
        premises (str): Premisas separadas por punto y coma.
    Returns:
        str: Conclusión inferida.
    """
    
    premises = [premise.strip().lower() for premise in premises.split(";")] # Normalizar las premisas

    if len(premises) == 2:
      conclusion = modus_ponens(premises) # 2 premisas
      if conclusion:
          return f"\n\u00BB Regla: Modus Ponens\n{conclusion}"

      conclusion = modus_tollens(premises) # 2 premisas
      if conclusion:
          return f"\n\u00BB Regla: Modus Tollens\n{conclusion}"

      conclusion = disjunctive_syllogism(premises) # 2 premisas
      if conclusion:
          return f"\n\u00BB Regla: Silogismo Disyuntivo\n{conclusion}"

      conclusion = hypothetical_syllogism(premises) # 2 premisas
      if conclusion:
          return f"\n\u00BB Regla: Silogismo Hipotético\n{conclusion}"

      conclusion = conjunction(premises) # 2 premisas
      if conclusion:
          return f"\n\u00BB Regla: Conjunción\n{conclusion}"
    
    if len(premises) == 1:
        conclusion = exportation(premises) # 1 premisa
        if conclusion:
          return f"\n\u00BB Regla: Exportación\n{conclusion}"

        conclusion = imports(premises) # 1 premisa
        if conclusion:
          return f"\n\u00BB Regla: Importación\n{conclusion}"

        conclusion = absurd(premises) # 1 premisa
        if conclusion:
          return f"\n\u00BB Regla: Reducción al absurdo\n{conclusion}"

        conclusion = simplification(premises) # 1 premisa
        if conclusion:
          return f"\n\u00BB Regla: Simplificación\n{conclusion}"

    if len(premises) == 3:
      conclusion = constructive_syllogism(premises) # 3 premisas
      if conclusion:
          return f"\n\u00BB Regla: Silogismo Constructivo\n{conclusion}"
      conclusion = destructive_syllogism(premises) # 3 premisas
      if conclusion:
          return f'\n\u00BB Regla: Silogismo Destructivo\n{conclusion}'
    return "\u26A0 No se pudo inferir una conclusión con las premisas dadas."

def obtener_saludo():
    """
    Descripción: Obtener un saludo dependiendo de la hora actual.
    Returns:
        str: Saludo correspondiente.
    """
    
    hora_actual = int(datetime.now().hour)
    if 5 <= hora_actual < 12:
        return "Buenos días!"
    elif 12 <= hora_actual < 18:
        return "Buenas tardes!"
    else:
        return "Buenas noches!"

def entrar_inferencia(entrada):
    """
    Descripción: Verificar si el usuario quiere entrar al modo de inferencia.
    Args:
        entrada (str): Mensaje del usuario.
        
    Returns:
        bool: True si el usuario quiere entrar al modo de inferencia, False en caso contrario.
    """
    entrada_norm = normalizar(entrada)
    return any(word in entrada_norm for word in ["premisa", "conclusion", "premisas", "inferir"])

class FisiBot:
    """
    Clase para el chatbot de Fisibotin.
    """
    
    def __init__(self): #Constructor de Fisibot
        """
        Inicializa el chatbot con las respuestas cargadas desde un archivo .xlsx. En caso de no existir, se cargan las respuestas predefinidas.
        """
        try:
            self.dataframe = pd.read_excel('Conversación.xlsx')
            self.fisibot = {}
            
            for index, row in self.dataframe.iterrows():
                input_key = normalizar(row['Usuario'])
                if input_key not in self.fisibot:
                    self.fisibot[input_key] = []
                self.fisibot[input_key].append(row['Chatbot'])
        except:
            # En caso no exista el .xlsx
            self.fisibot = {
                "hola": ["¡Hola! ¿Cómo estás? ¿En qué te puedo ayudar hoy?", "Hola, soy Fisibotin. ¿En qué puedo ayudarte?"],
                "como estas": ["¡Estoy bien, gracias por preguntar! ¿En qué te puedo ayudar hoy?", "¡Todo bien! ¿Y tú? ¿Necesitas ayuda con algo hoy?"],
                "como me puedes ayudar": ["Puedo ayudarte con inferencias lógicas utilizando diferentes reglas como el Modus Ponens, Modus Tollens, Silogismo Hipotético, etc. ¡Solo dime las premisas separadas por punto y coma!"],
                "gracias": ["¡De nada! Si necesitas algo más, no dudes en decírmelo. ¡Que tengas un gran día!", "¡Es un placer ayudarte! Estoy aquí para lo que necesites."]
            }

    def obtener_respuesta(self, entrada_usuario):
        """
        Descripción: Obtiene la respuesta del chatbot a partir de la entrada del usuario.
        Args:
            entrada_usuario (str): Entrada del usuario.
            
        Returns:
            str: Respuesta del chatbot.
        """
        entrada_usuario = normalizar(entrada_usuario)
        if entrada_usuario == "que hora es":
            hora_actual = datetime.now().strftime("%H:%M")
            return f"La hora actual es {hora_actual}."

        # Find the best match
        umbral = 40
        mejor_coincidencia = None
        mejor_similitud = 0

        for clave in self.fisibot:
            similitud = fuzz.ratio(entrada_usuario, clave)
            if similitud > mejor_similitud and similitud >= umbral:
                mejor_coincidencia = clave
                mejor_similitud = similitud

        if mejor_coincidencia:
            return random.choice(self.fisibot[mejor_coincidencia])
        else:
            return "\u26A0 Lo siento, no entiendo lo que me estás diciendo."
