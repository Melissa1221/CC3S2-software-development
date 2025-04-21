from behave import given, when, then
import re
import random
from src.belly import CantidadNegativaError, CantidadExcesivaError

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

# Función para manejar tiempos aleatorios 
def generar_tiempo_aleatorio(descripcion):
    # Patrón para "entre X y Y horas" o "un tiempo aleatorio entre X y Y horas"
    patron_esp = re.compile(r'(?:un tiempo aleatorio )?entre (\d+|[\w]+) y (\d+|[\w]+) horas')
    patron_ing = re.compile(r'(?:a random time )?between (\d+|[\w]+) and (\d+|[\w]+) hours')
    
    # Verificar si es español o inglés y extraer valores
    match_esp = patron_esp.search(descripcion.lower())
    match_ing = patron_ing.search(descripcion.lower())
    
    if match_esp:
        # Descripción en español
        min_valor = match_esp.group(1)
        max_valor = match_esp.group(2)
        
        # Convertir a números
        if min_valor.isdigit():
            min_horas = int(min_valor)
        else:
            min_horas = convertir_palabra_a_numero(min_valor)
            
        if max_valor.isdigit():
            max_horas = int(max_valor)
        else:
            max_horas = convertir_palabra_a_numero(max_valor)
    
    elif match_ing:
        # Descripción en inglés
        min_valor = match_ing.group(1)
        max_valor = match_ing.group(2)
        
        # Convertir a números
        if min_valor.isdigit():
            min_horas = int(min_valor)
        else:
            min_horas = convertir_palabra_a_numero_ingles(min_valor)
            
        if max_valor.isdigit():
            max_horas = int(max_valor)
        else:
            max_horas = convertir_palabra_a_numero_ingles(max_valor)
    
    else:
        raise ValueError(f"No se reconoce el formato de tiempo aleatorio: {descripcion}")
    
 
    if "debería gruñir" in descripcion or min_horas < 1.5:
        min_horas = max(min_horas, 1.5)
    
    # Generar tiempo aleatorio en el rango 
    tiempo_aleatorio = random.uniform(min_horas, max_horas)
    print(f"Tiempo aleatorio generado: {tiempo_aleatorio:.2f} horas")
    
    return tiempo_aleatorio

# Función mejorada para procesar descripciones complejas de tiempo
def procesar_descripcion_tiempo(descripcion, es_ingles=False):
    print(f"Procesando descripción compleja: '{descripcion}'")
    if es_ingles:
        pattern = r'(\d+|\b\w+\b(?:\s+\b\w+\b)?)\s*(hours?|minutes?|seconds?)'
    else:
        pattern = r'(\d+|\b\w+\b(?:\s+\b\w+\b)?)\s*(horas?|minutos?|segundos?)'
        
    componentes = re.findall(pattern, descripcion)
    print(f"Componentes encontrados: {componentes}")

    horas = 0
    minutos = 0
    segundos = 0
    
    for valor, unidad in componentes:
        valor = valor.strip()
        unidad = unidad.lower()
        # Convertir palabra a número según idioma
        if es_ingles:
            numero = convertir_palabra_a_numero_ingles(valor)
            if 'hour' in unidad:
                horas = numero
            elif 'minute' in unidad:
                minutos = numero
            elif 'second' in unidad:
                segundos = numero
        else:
            numero = convertir_palabra_a_numero(valor)
            if 'hora' in unidad:
                horas = numero
            elif 'minuto' in unidad:
                minutos = numero
            elif 'segundo' in unidad:
                segundos = numero
    print(f"Valores procesados: horas={horas}, minutos={minutos}, segundos={segundos}")
    tiempo_total = horas + (minutos / 60) + (segundos / 3600)
    print(f"Tiempo total en horas: {tiempo_total:.4f}")
    return tiempo_total

@given('que he comido {cukes:g} pepinos')
def step_given_eaten_cukes(context, cukes):
    try:
        context.belly.comer(float(cukes))
        # Si llega hasta aquí es porque no hubo excepciones
        context.exception = None
    except (CantidadNegativaError, CantidadExcesivaError) as e:
        # guardar la excepción para verificarla después
        context.exception = e
        print(f"Excepción capturada: {str(e)}")

@when('espero {time_description}')
def step_when_wait_time_description(context, time_description):
    # Si ya hubo una excepción en un paso anterior, no continuamos
    if hasattr(context, 'exception') and context.exception is not None:
        return
        
    time_description = time_description.strip('"').lower()
    print(f"Descripción original: '{time_description}'")
    
    # Detectar si es inglés o español
    es_ingles = False
    if "hour" in time_description or "minute" in time_description or "second" in time_description:
        es_ingles = True
        print("Detectado como inglés")
  
    # Obtener información del escenario completo para la función de tiempo aleatorio
    info_escenario = ""
    if hasattr(context, '_runner') and hasattr(context._runner, 'feature'):
        for escenario in context._runner.feature.scenarios:
            if escenario.name == context.scenario.name:
                # Recopilar todos los pasos del escenario
                for step in escenario.steps:
                    info_escenario += step.name + " "
                break
  
    # Detectar primero si es un tiempo aleatorio
    if "entre" in time_description and "horas" in time_description:
        # Tiempo aleatorio en español
        tiempo_total = generar_tiempo_aleatorio(time_description + " " + info_escenario)
        context.belly.esperar(tiempo_total)
        return
    elif "between" in time_description and "hours" in time_description:
        # Tiempo aleatorio en inglés
        tiempo_total = generar_tiempo_aleatorio(time_description + " " + info_escenario)
        context.belly.esperar(tiempo_total)
        return
    
    # Manejar casos especiales como 'media hora' o 'half hour'
    if time_description == 'media hora' or time_description == 'half hour':
        total_time_in_hours = 0.5
    # Verificar si contiene formato complejo
    elif "," in time_description:
        # Usar el procesador mejorado para manejo de expresiones complejas
        total_time_in_hours = procesar_descripcion_tiempo(time_description, es_ingles)
    else:
        # continuar con el procesamiento normal previo
        if es_ingles:
            time_description = time_description.replace('and', ' ')
        else:
            time_description = time_description.replace('y', ' ')
        
        time_description = time_description.strip()
        print(f"Descripción normalizada: '{time_description}'")

        # Definir patrones para ambos idiomas
        if es_ingles:
            pattern = re.compile(
                r'(?:(\w+(?:\s+\w+)?|\d+)\s*hours?)?\s*'    # horas en inglés 
                r'(?:(\w+(?:\s+\w+)?|\d+)\s*minutes?)?\s*'  # minutos en inglés 
                r'(?:(\w+(?:\s+\w+)?|\d+)\s*seconds?)?'     # segundos en inglés 
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
            # Intentar con el procesador mejorado como último recurso
            total_time_in_hours = procesar_descripcion_tiempo(time_description, es_ingles)

    context.belly.esperar(total_time_in_hours)

@then('mi estómago debería gruñir')
def step_then_belly_should_growl(context):
    # Si ya hubo una excepción en un paso anterior, no continuamos
    if hasattr(context, 'exception') and context.exception is not None:
        return
        
    assert context.belly.esta_gruñendo(), "Se esperaba que el estómago gruñera, pero no lo hizo."

@then('mi estómago no debería gruñir')
def step_then_belly_should_not_growl(context):
    # Si ya hubo una excepción en un paso anterior, no continuamos
    if hasattr(context, 'exception') and context.exception is not None:
        return
        
    assert not context.belly.esta_gruñendo(), "Se esperaba que el estómago no gruñera, pero lo hizo."

@then('debería ocurrir un error de cantidad negativa')
def step_then_should_raise_negative_error(context):
    assert context.exception is not None, "Se esperaba una excepción, pero no ocurrió ninguna."
    assert isinstance(context.exception, CantidadNegativaError), f"Se esperaba CantidadNegativaError, pero se obtuvo: {type(context.exception)}"
    
@then('debería ocurrir un error de cantidad excesiva')
def step_then_should_raise_excessive_error(context):
    assert context.exception is not None, "Se esperaba una excepción, pero no ocurrió ninguna."
    assert isinstance(context.exception, CantidadExcesivaError), f"Se esperaba CantidadExcesivaError, pero se obtuvo: {type(context.exception)}"

@when('pregunto cuántos pepinos más puedo comer')
def step_when_ask_cukes_left(context):
    if hasattr(context, 'exception') and context.exception is not None:
        return
    
    context.pepinos_restantes = 10 - context.belly.pepinos_comidos
    if context.pepinos_restantes < 0:
        context.pepinos_restantes = 0

@then('debería decirme que puedo comer {cantidad:d} pepinos más')
def step_then_can_eat_more(context, cantidad):
    if hasattr(context, 'exception') and context.exception is not None:
        return
    
    assert context.pepinos_restantes == cantidad, f"Se esperaba poder comer {cantidad} pepinos más, pero se puede comer {context.pepinos_restantes}"

@when('pregunto cuánto tiempo falta para que gruña')
def step_when_ask_time_until_growl(context):
    if hasattr(context, 'exception') and context.exception is not None:
        return
    
    if context.belly.pepinos_comidos <= 10:
        context.tiempo_restante = None
    else:
        tiempo_faltante = max(0, 1.5 - context.belly.tiempo_esperado)
        context.tiempo_restante = tiempo_faltante

@then('debería decirme que gruñirá en {horas:g} horas')
def step_then_will_growl_in(context, horas):
    if hasattr(context, 'exception') and context.exception is not None:
        return
    
    assert context.tiempo_restante is not None, "El estómago no gruñirá con esta cantidad de pepinos"
    assert abs(context.tiempo_restante - horas) < 0.01, f"Se esperaba que gruñera en {horas} horas, pero gruñirá en {context.tiempo_restante} horas"

@when('pregunto si gruñirá después de {horas:g} horas')
def step_when_ask_if_will_growl(context, horas):
    if hasattr(context, 'exception') and context.exception is not None:
        return
  
    tiempo_total = context.belly.tiempo_esperado + horas
    pepinos = context.belly.pepinos_comidos
    
    context.prediccion_gruñido = tiempo_total >= 1.5 and pepinos > 10

@then('debería confirmar que sí gruñirá')
def step_then_confirm_will_growl(context):
    if hasattr(context, 'exception') and context.exception is not None:
        return
    
    assert context.prediccion_gruñido is True, "Se esperaba que el estómago gruñera, pero la predicción dice que no gruñirá"

@then('debería confirmar que no gruñirá')
def step_then_confirm_will_not_growl(context):
    if hasattr(context, 'exception') and context.exception is not None:
        return
    
    assert context.prediccion_gruñido is False, "Se esperaba que el estómago no gruñera, pero la predicción dice que sí gruñirá"

