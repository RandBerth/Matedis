#REGLAS DE INFERENCIA
"""
Esta lista de funciones implementa las reglas de inferencia lógica más comunes. Cada función recibe una lista de premisas y verifica si se cumple la regla de inferencia correspondiente. Si se cumple, retorna la conclusión inferida. En caso contrario, retorna None.
"""

def modus_ponens(premises):
    """
    Descripción: Verifica si se cumple la regla de inferencia Modus Ponens.
    Args:
        premises(str): Premisas a evaluar.

    Returns:
        str: Conclusión inferida o None.
    """
    for premise in premises:
        if "entonces" in premise:
            antecedent, consequent = premise.split("entonces")
            antecedent = antecedent.replace("si", "").strip()
            consequent = consequent.strip()
            p_label = f"P: {antecedent.capitalize()}"
            q_label = f"Q: {consequent.capitalize()}"
            cls_label = f"Conclusión: {consequent.capitalize()}"
            if antecedent in premises:
                return f"\u00BB {p_label}\n\u00BB {q_label}\n\u2234 {cls_label}\n"
    return None

def modus_tollens(premises):
    """
    Descripción: Verifica si se cumple la regla de inferencia Modus Tollens.
    Args:
        premises (str): Premisas a evaluar.
        
    Returns:
        str: Conclusión inferida o None
    """
    for premise in premises:
        if "entonces" in premise:
            antecedent, consequent = premise.split("entonces")
            antecedent = antecedent.replace("si", "").strip()
            consequent = consequent.strip()
            negated_consequent = "no " + consequent
            p_label = f"P: {antecedent.capitalize()}"
            q_label = f"Q: {consequent.capitalize()}"
            cls_label = f"Conclusión: No {antecedent}"
            for p in premises:
                if negated_consequent in p:
                    return f"\u00BB {p_label}\n\u00BB {q_label}\n\u2234 {cls_label}\n"
    return None

def hypothetical_syllogism(premises):
    """
    Descripción: Verifica si se cumple la regla de inferencia Silogismo Hipotético.
    Args:
        premises (str): Premisas a evaluar.
        
    Returns:
        str: Conclusión inferida o None
    """
    for premise1 in premises:
        if "entonces" in premise1:
            antecedent1, consequent1 = premise1.split("entonces")
            antecedent1 = antecedent1.replace("si", "").strip()
            consequent1 = consequent1.strip()
            for premise2 in premises:
                if premise1 != premise2 and "entonces" in premise2:
                    antecedent2, consequent2 = premise2.split("entonces")
                    antecedent2 = antecedent2.replace("si", "").strip()
                    consequent2 = consequent2.strip()
                    p_label = f"P: {antecedent1.capitalize()}"
                    q_label = f"Q: {consequent1.capitalize()}"
                    r_label = f"R: {consequent2.capitalize()}"
                    cls_label = f"Conclusión: {antecedent1.capitalize()} entonces {consequent2}"
                    if consequent1 == antecedent2:
                        return f"\u00BB {p_label}\n\u00BB {q_label}\n\u00BB {r_label}\n\u2234 {cls_label}\n"
    return None

def disjunctive_syllogism(premises):
    for premise in premises:
        if " o " in premise:
            antecedent, consequent = premise.split(" o ")
            antecedent = antecedent.strip()
            consequent = consequent.strip()
            negated_antecedent = "no " + antecedent
            p_label = f"P: {antecedent.capitalize()}"
            q_label = f"Q: {consequent.capitalize()}"
            cls_label = f"Conclusión: {consequent.capitalize()}"
            for p in premises:
                if negated_antecedent in p:
                    return f"\u00BB {p_label}\n\u00BB {q_label}\n\u2234 {cls_label}\n"
    return None

def constructive_syllogism(premises):
    """
    Descripción: Verifica si se cumple la regla de inferencia Silogismo Constructivo.
    Args:
        premises (str): Premisas a evaluar.
        
    Returns:
        str: Conclusión inferida o None
    """
    for premise1 in premises:
        if "entonces" in premise1:
            antecedent1, consequent1 = premise1.split("entonces")
            antecedent1 = antecedent1.replace("si", "").strip()
            consequent1 = consequent1.strip()
            p_label = f"P: {antecedent1.capitalize()}"
            q_label = f"Q: {consequent1.capitalize()}"

        for premise2 in premises:
            if premise1 != premise2 and "entonces" in premise2:
                antecedent2, consequent2 = premise2.split("entonces")
                antecedent2 = antecedent2.replace("si", "").strip()
                consequent2 = consequent2.strip()
                r_label = f"R: {antecedent2.capitalize()}"
                s_label = f"S: {consequent2.capitalize()}"
                cls_label = f"Conclusión: {consequent1.capitalize()} o {consequent2}"
            for premise3 in premises:
                if " o " in premise3:
                    antecedent3, consequent3 = premise3.split(" o ")
                    antecedent3 = antecedent3.strip()
                    consequent3 = consequent3.strip()
            if antecedent1 == antecedent3 and  antecedent2 == consequent3:
                return f"\u00BB {p_label}\n\u00BB {q_label}\n\u00BB {r_label}\n\u00BB {s_label}\n\u2234 {cls_label}\n"

    return None

def destructive_syllogism(premises):
    """
    Descripción: Verifica si se cumple la regla de inferencia Modus Tollens.
    Args:
        premises (str): Premisas a evaluar.
        
    Returns:
        str: Conclusión inferida o None
    """
    for premise1 in premises:
        if "entonces" in premise1:
            antecedent1, consequent1 = premise1.split("entonces")
            antecedent1 = antecedent1.replace("si", "").strip()
            consequent1 = consequent1.strip()
            p_label = f"P: {antecedent1.capitalize()}"
            q_label = f"Q: {consequent1.capitalize()}"
        for premise2 in premises:
            if premise1 != premise2 and "entonces" in premise2:
                antecedent2, consequent2 = premise2.split("entonces")
                antecedent2 = antecedent2.replace("si", "").strip()
                consequent2 = consequent2.strip()
                r_label = f"R: {antecedent2.capitalize()}"
                s_label = f"S: {consequent2.capitalize()}"
                cls_label = f"Conclusión: No {antecedent1} o no {antecedent2}"
            for premise3 in premises:
                if " o " in premise3:
                    antecedent3, consequent3 = premise3.split(" o ")
                    antecedent3 = antecedent3.replace("no","").strip()
                    consequent3 = consequent3.replace("no","").strip()
            if consequent1 == antecedent3 and  consequent2 == consequent3:
                return f"\u00BB {p_label}\n\u00BB {q_label}\n\u00BB {r_label}\n\u00BB {s_label}\n\u2234 {cls_label}\n"
    return None

#FALTA EDITAR SALIDA
# CONJUNCIÓN
def conjunction(premises):
    """
    Descripción: Verifica si se cumple la regla de inferencia Conjugación.
    Args:
        premises (str): Premisas a evaluar.
        
    Returns:
        str: Conclusión inferida o None
    """
    words = [" o ", "entonces", " y ", " si "]
    for premise in premises:
        if any(any(word in premise.lower() for word in words) for premise in premises):
            antecedent = premises[0].strip()
            consequent = premises[1].strip()
            p_label = f"P: {antecedent.capitalize()}"
            q_label = f"Q: {consequent.capitalize()}"
            cls_label = f"Conclusión: {antecedent.capitalize()} y {consequent}"
            return f"\u00BB {p_label}\n\u00BB {q_label}\n\u2234 {cls_label}\n"
    return None

def exportation(premises):
    """
    Descripción: Verifica si se cumple la regla de inferencia Exportación.
    Args:
        premises (str): Premisas a evaluar.
        
    Returns:
        str: Conclusión inferida o None
    """
    for premise in premises:
        if " y " in premise and "entonces" in premise and not "no" in premise:
            antecedents, consequent = premise.split("entonces")
            antecedent1, antecedent2 = antecedents.split(" y ")
            antecedent1 = antecedent1.replace(',', '').strip()
            antecedent2 = antecedent2.replace(',', '').strip()
            consequent = consequent.replace(',', '').strip()
            p_label = f"P: {antecedent1.capitalize()}"
            r_label = f"R: {antecedent2.capitalize()}"
            q_label = f"Q: {consequent.capitalize()}"
            cls_label = f"Conclusión: {antecedent1.capitalize()} entonces, {antecedent2} entonces {consequent}"
            return f"\u00BB {p_label}\n\u00BB {r_label}\n\u00BB {q_label}\n\u2234 {cls_label}\n"
    return None

def imports(premises):
    """
    Descripción: Verifica si se cumple la regla de inferencia Importación.
    Args:
        premises (str): Premisas a evaluar.
        
    Returns:
        str: Conclusión inferida o None
    """
    for premise in premises:
        if "entonces" in premise and not " y " in premise:
            parts = premise.split("entonces")
        if len(parts) == 3:
            antecedent = parts[0].replace("si", "").replace(",","").strip()
            consequent1 = parts[1].replace("si", "").strip()
            consequent2 = parts[2].strip()
            p_label = f"P: {antecedent.capitalize()}"
            r_label = f"R: {consequent1.capitalize()}"
            q_label = f"Q: {consequent2.capitalize()}"
            cls_label = f"Conclusión: Si {antecedent} y {consequent1}, entonces {consequent2}"
        return f'\u00BB {p_label}\n\u00BB {r_label}\n\u00BB {q_label}\n\u2234 {cls_label}\n'
    return None

def simplification(premises):
    """
    Descripción: Verifica si se cumple la regla de inferencia Simplificación.
    Args:
        premises (str): Premisas a evaluar.
        
    Returns:
        str: Conclusión inferida o None
    """
    for premise in premises:
        if " y " in premise:
            antecedent, consequent = premise.split(" y ")
            antecedent = antecedent.strip()
            consequent = consequent.strip()
            p_label = f"P: {antecedent.capitalize()}"
            q_label = f"Q: {consequent.capitalize()}"
            cls_label = f"Conclusión: {antecedent.capitalize()}"
            return f"\u00BB {p_label}\n\u00BB {q_label}\n\u2234 {cls_label}\n"
    return None

def absurd(premises):
    """
    Descripción: Verifica si se cumple la regla de inferencia Reducción al Absurdo.
    Args:
        premises (str): Premisas a evaluar. 
    Returns:
        str: Conclusión inferida o None
    """
    for premise in premises:
        if "entonces" in premise:
            antecedent, consequents = premise.split("entonces")
            antecedent = antecedent.replace("si","").replace(",","").strip()
            consequent1, consequent2= consequents.split(" y ")
            consequent1 = consequent1.strip()
            consequent2 = consequent2.replace("no", "").strip()
            p_label = f"P: {antecedent.capitalize()}"
            q_label = f"R: {consequent1.capitalize()}"
            cls_label = f"Conclusión: No {antecedent}"
            if consequent1 == consequent2:
                return f'\u00BB {p_label}\n\u00BB {q_label}\n\u2234 {cls_label}\n'
    return None

