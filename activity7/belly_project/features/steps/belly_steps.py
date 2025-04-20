from behave import given, when, then
import re

# Función para convertir palabras numéricas a números
def convertir_palabra_a_numero(palabra):
    try:
        return int(palabra)
    except ValueError:
        numeros = {
            "cero": 0, "uno": 1, "una":1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
            "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11,
            "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciséis": 16,
            "diecisiete":17, "dieciocho":18, "diecinueve":19, "veinte":20,
            "treinta": 30, "cuarenta":40, "cincuenta":50, "sesenta":60, "setenta":70,
            "ochenta":80, "noventa":90, "media": 0.5
        }
        return numeros.get(palabra.lower(), 0)

# Función para convertir palabras numéricas en inglés a números
def convertir_palabra_a_numero_ingles(palabra):
    try:
        return int(palabra)
    except ValueError:
        # Manejar números compuestos como "forty five" 
        if " " in palabra:
            partes = palabra.lower().split()
            resultado = 0
            for parte in partes:
                resultado += convertir_palabra_a_numero_ingles(parte)
            return resultado
            
        numeros_en_ingles = {
            "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
            "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
            "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
            "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
            "eighty": 80, "ninety": 90, "half": 0.5
        }
        return numeros_en_ingles.get(palabra.lower(), 0)

@given('que he comido {cukes:g} pepinos')
def step_given_eaten_cukes(context, cukes):
    context.belly.comer(float(cukes))

@when('espero {time_description}')
def step_when_wait_time_description(context, time_description):
    time_description = time_description.strip('"').lower()
    print(f"Descripción original: '{time_description}'")
    
    # Detectar si es inglés o español
    es_ingles = False
    if "hour" in time_description or "minute" in time_description or "second" in time_description:
        es_ingles = True
        print("Detectado como inglés")
  
    if es_ingles:
        time_description = time_description.replace('and', ' ')
    else:
        time_description = time_description.replace('y', ' ')
    
    time_description = time_description.strip()
    print(f"Descripción normalizada: '{time_description}'")

    # Manejar casos especiales como 'media hora' o 'half hour'
    if time_description == 'media hora' or time_description == 'half hour':
        total_time_in_hours = 0.5
    else:
        # Definir patrones para ambos idiomas
        if es_ingles:
            pattern = re.compile(
                r'(?:(\w+(?:\s+\w+)?|\d+)\s*hours?)?\s*'    # horas en inglés 
                r'(?:(\w+(?:\s+\w+)?|\d+)\s*minutes?)?\s*'  # minutos en inglés (permitiendo palabras compuestas)
                r'(?:(\w+(?:\s+\w+)?|\d+)\s*seconds?)?'     # segundos en inglés (permitiendo palabras compuestas)
            )
        else:
            pattern = re.compile(
                r'(?:(\w+|\d+)\s*horas?)?\s*'    # horas en español
                r'(?:(\w+|\d+)\s*minutos?)?\s*'  # minutos en español
                r'(?:(\w+|\d+)\s*segundos?)?'    # segundos en español
            )
        
        match = pattern.match(time_description)
        if match:
            hours_word = match.group(1) or "0"
            minutes_word = match.group(2) or "0"
            seconds_word = match.group(3) or "0"
            
            print(f"Grupos capturados: horas='{hours_word}', minutos='{minutes_word}', segundos='{seconds_word}'")
            
            # Convertir según el idioma detectado
            if es_ingles:
                hours = convertir_palabra_a_numero_ingles(hours_word)
                minutes = convertir_palabra_a_numero_ingles(minutes_word)
                seconds = convertir_palabra_a_numero_ingles(seconds_word)
            else:
                hours = convertir_palabra_a_numero(hours_word)
                minutes = convertir_palabra_a_numero(minutes_word)
                seconds = convertir_palabra_a_numero(seconds_word)
            
            print(f"Valores convertidos: horas={hours}, minutos={minutes}, segundos={seconds}")
            
            total_time_in_hours = hours + (minutes / 60) + (seconds / 3600)
            print(f"Tiempo total en horas: {total_time_in_hours}")
        else:
            raise ValueError(f"No se pudo interpretar la descripción del tiempo: {time_description}")

    context.belly.esperar(total_time_in_hours)

@then('mi estómago debería gruñir')
def step_then_belly_should_growl(context):
    assert context.belly.esta_gruñendo(), "Se esperaba que el estómago gruñera, pero no lo hizo."

@then('mi estómago no debería gruñir')
def step_then_belly_should_not_growl(context):
    assert not context.belly.esta_gruñendo(), "Se esperaba que el estómago no gruñera, pero lo hizo."

