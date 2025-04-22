# Actividad 7

Inicializar el proyecto con la estructura dada
![](https://i.imgur.com/lDZ1RsP.png)

#### Ejercicio 1: **Añadir soporte para minutos y segundos en tiempos de espera**

1. Modificamos el archivo belly_steps.py
```py
@when('espero {time_description}')
def step_when_wait_time_description(context, time_description):
    # código anterior
    else:
        # Expresión regular para extraer horas ,minutos y segundos
        pattern = re.compile(
            r'(?:(\w+|\d+)\s*horas?)?\s*'    # horas
            r'(?:(\w+|\d+)\s*minutos?)?\s*'  # minutos
            r'(?:(\w+|\d+)\s*segundos?)?'   # segundos
        )
        match = pattern.match(time_description)
        if match:
            hours_word = match.group(1) or "0"
            minutes_word = match.group(2) or "0"
            seconds_word = match.group(3) or "0"
            hours = convertir_palabra_a_numero(hours_word)
            minutes = convertir_palabra_a_numero(minutes_word)
            seconds = convertir_palabra_a_numero(seconds_word)
            total_time_in_hours = hours + (minutes / 60) + (seconds / 3600)
        else:
            raise ValueError(f"No se pudo interpretar la descripción del tiempo: {time_description}")
    context.belly.esperar(total_time_in_hours)
```

2. Implementar un escenario Gherkin en `belly.feature`

```gherkin
  Escenario: Comer pepinos y esperar con horas, minutos y segundos
    Dado que he comido 35 pepinos
    Cuando espero "1 hora y 30 minutos y 45 segundos"
    Entonces mi estómago debería gruñir
```

El resultado de los test: 
![](https://i.imgur.com/RtZMB0N.png)

#### Ejercicio 2: **Manejo de cantidades fraccionarias de pepinos**

**Objetivo**: Permitir que el sistema acepte cantidades fraccionarias de pepinos (decimales).

Usar general number format 
```py
@given('que he comido {cukes:g} pepinos')
def step_given_eaten_cukes(context, cukes):
    context.belly.comer(float(cukes))
```

**Implementar** un nuevo escenario en Gherkin
```gherkin
  Escenario: Comer una cantidad fraccionaria de pepinos
    Dado que he comido 0.5 pepinos
    Cuando espero 2 horas
    Entonces mi estómago no debería gruñir
```

El resultado:
![](https://i.imgur.com/ZjJmtgN.png)

#### Ejercicio 3: **Soporte para idiomas múltiples (Español e Inglés)**

Función para convertir palabras numéricas en inglés a números

```py
def convertir_palabra_a_numero_ingles(palabra):
    try:
        return int(palabra)
    except ValueError:
        numeros_en_ingles = {
            "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11,
            "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16,
            "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20,
            "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70,
            "eighty": 80, "ninety": 90, "half": 0.5
        }
        return numeros_en_ingles.get(palabra.lower(), 0)
```

Modificamos when para casos en inglés
```py
@when('espero {time_description}')
def step_when_wait_time_description(context, time_description):
    time_description = time_description.strip('"').lower()
    # Detectar si es inglés o español
    es_ingles = False
    if "hour" in time_description or "minute" in time_description or "second" in time_description:
        es_ingles = True
    if es_ingles:
        time_description = time_description.replace('and', ' ')
    else:
        time_description = time_description.replace('y', ' ')
    time_description = time_description.strip()
```

```py
    # Manejar casos especiales como 'media hora' o 'half hour'
    if time_description == 'media hora' or time_description == 'half hour':
        total_time_in_hours = 0.5
    else:
        # Definir patrones para ambos idiomas
        if es_ingles:
            pattern = re.compile(
                r'(?:(\w+|\d+)\s*hours?)?\s*'    # horas en inglés
                r'(?:(\w+|\d+)\s*minutes?)?\s*'  # minutos en inglés
                r'(?:(\w+|\d+)\s*seconds?)?'     # segundos en inglés
            )
        else:
            pattern = re.compile(
                r'(?:(\w+|\d+)\s*horas?)?\s*'    # horas en español
                r'(?:(\w+|\d+)\s*minutos?)?\s*'  # minutos en español
                r'(?:(\w+|\d+)\s*segundos?)?'    # segundos en español
            )
        match = pattern.match(time_description)
```

Dos escenarios

```gherkins
  Escenario: Esperar usando horas en inglés
    Dado que he comido 20 pepinos
    Cuando espero "two hours and thirty minutes"
    Entonces mi estómago debería gruñir

  Escenario: Esperar usando minutos y segundos en inglés
    Dado que he comido 25 pepinos
    Cuando espero "one hour and forty five minutes and thirty seconds"
    Entonces mi estómago debería gruñir
```

El resultado
![](https://i.imgur.com/iZ6uvQ8.png)


#### Ejercicio 4: **Manejo de tiempos aleatorios**

Función para tiempos aleatorios
```py
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
    # Generar tiempo aleatorio en el rango
    tiempo_aleatorio = random.uniform(min_horas, max_horas)
    print(f"Tiempo aleatorio generado: {tiempo_aleatorio:.2f} horas")
    return tiempo_aleatorio
```

Dos escenarios
```gherkins
  Escenario: Comer pepinos y esperar un tiempo aleatorio
    Dado que he comido 25 pepinos
    Cuando espero "un tiempo aleatorio entre 1 y 3 horas"
    Entonces mi estómago debería gruñir

  Escenario: Comer pepinos y esperar un tiempo aleatorio en inglés
    Dado que he comido 25 pepinos
    Cuando espero "a random time between 2 and 5 hours"
    Entonces mi estómago debería gruñir
```

El resultado:
![](https://i.imgur.com/R41OHDW.png)

#### Ejercicio 5: **Validación de cantidades no válidas**

Modificamos la clase Belly
```py
class CantidadNegativaError(Exception):
    """Excepción lanzada cuando se intenta comer una cantidad negativa de pepinos."""
    pass
class CantidadExcesivaError(Exception):
    """Excepción lanzada cuando se intenta comer demasiados pepinos."""
    pass
```

![](https://i.imgur.com/JtH4Iwn.png)

Se modificó para capturar las excepciones
![](https://i.imgur.com/PnPqCUe.png)
dos nuevos steps de verificación:

![](https://i.imgur.com/Bicoa1g.png)

Nuevos escenarios

```gherkins
  Escenario: Manejar una cantidad negativa de pepinos
    Dado que he comido -5 pepinos
    Entonces debería ocurrir un error de cantidad negativa

  Escenario: Manejar una cantidad excesiva de pepinos
    Dado que he comido 150 pepinos
    Entonces debería ocurrir un error de cantidad excesiva
```

El resultado
![](https://i.imgur.com/aBQErvZ.png)

#### Ejercicio 6: **Escalabilidad con grandes cantidades de pepinos**

modificar la clase Belly para permitir un mayor límite de pepinos en modo de prueba
![](https://i.imgur.com/cQxpr42.png)

![](https://i.imgur.com/FYoVKf1.png)

modificar environment.py para activar el modo de prueba de escalabilidad:
![](https://i.imgur.com/dGcZmtV.png)

![](https://i.imgur.com/19nTeha.png)


Nuevos escenarios:
```gherkins
  Escenario: Comer 1000 pepinos y esperar 10 horas
    Dado que he comido 1000 pepinos
    Cuando espero 10 horas
    Entonces mi estómago debería gruñir
    
  Escenario: Prueba de rendimiento con grandes cantidades
    Dado que he comido 5000 pepinos
    Cuando espero 20 horas
    Entonces mi estómago debería gruñir
```

El resultado:
![](https://i.imgur.com/bHetRHU.png)

  

#### Ejercicio 7: **Descripciones de tiempo complejas**

- Ampliar la lógica para manejar descripciones avanzadas tipo `"1 hora, 30 minutos y 45 segundos"`.

1. **Refuerza** la expresión regular y parsing para que soporte múltiples separadores (comas, "y", espacios, etc.).

![](https://i.imgur.com/kdeg4eM.png)

Nuevos escenarios
```gherkins
  Escenario: Manejar tiempos complejos con comas
    Dado que he comido 50 pepinos
    Cuando espero "1 hora, 30 minutos y 45 segundos"
    Entonces mi estómago debería gruñir
    
  Escenario: Manejar tiempos complejos con diferentes separadores
    Dado que he comido 40 pepinos
    Cuando espero "2 horas, 15 minutos, 30 segundos"
    Entonces mi estómago debería gruñir
    
  Escenario: Manejar tiempos complejos en inglés con comas
    Dado que he comido 45 pepinos
    Cuando espero "3 hours, 10 minutes, 20 seconds"
    Entonces mi estómago debería gruñir
```

El resultado
![](https://i.imgur.com/H0NFvYB.png)

#### Ejercicio 8: **De TDD a BDD – Convertir requisitos técnicos a pruebas en Gherkin**

Practicar el paso de una prueba unitaria técnica a un escenario BDD comprensible por el negocio.

1. **Escribe** un test unitario básico con Pytest que valide que si se han comido más de 10 pepinos y se espera 2 horas, el estómago gruñe.

```py
def test_gruñir_si_comido_muchos_pepinos():
    belly = Belly()
    belly.comer(15)
    belly.esperar(2)
    assert belly.esta_gruñendo() == True
```

2. **Convierte** ese test unitario en un escenario Gherkin, con la misma lógica, pero más orientado al usuario.

```gherkin
  Escenario: Comer muchos pepinos y esperar el tiempo suficiente
    Dado que he comido 15 pepinos
    Cuando espero 2 horas
    Entonces mi estómago debería gruñir
```

El resultado
![](https://i.imgur.com/2lGm3Dj.png)


![](https://i.imgur.com/AZ5tHcY.png)

#### Ejercicio 9: **Identificación de criterios de aceptación para historias de usuario**

**Objetivo**  
- Traducir una historia de usuario en criterios de aceptación claros y escenarios BDD.

estos son los criterios de aceptación :
1. saber cuántos pepinos más puedo comer sin que mi estómago gruña
2. conocer cuánto tiempo más puedo esperar sin que gruña
3. predecir si el estómago gruñirá en una hora específica

```gherkins
  @historia_usuario @language_spanish
  Escenario: Saber cuántos pepinos puedo comer antes de gruñir
    Dado que he comido 8 pepinos
    Cuando pregunto cuántos pepinos más puedo comer
    Entonces debería decirme que puedo comer 2 pepinos más

  @historia_usuario @language_spanish
  Escenario: Conocer cuánto tiempo falta para que gruña
    Dado que he comido 15 pepinos
    Cuando pregunto cuánto tiempo falta para que gruña
    Entonces debería decirme que gruñirá en 1.5 horas

  @historia_usuario @language_spanish 
  Escenario: Predecir si el estómago gruñirá después de un tiempo
    Dado que he comido 12 pepinos
    Cuando pregunto si gruñirá después de 2 horas
    Entonces debería confirmar que sí gruñirá
    
```

En belly_steps.py
```py
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
```

para el ci.yml

```yml

    - name: Run User Story BDD tests
      run: |
        cd belly_project
        behave features/ --tags=@historia_usuario
```

El resultado:
Con ``behave features/ --tags=@historia_usuario``

```bash
  @historia_usuario @language_spanish
  Escenario: Saber cuántos pepinos puedo comer antes de gruñir  # features/belly.feature:118
    Dado que he comido 8 pepinos                                # features/steps/belly_steps.py:139 0.000s
    Cuando pregunto cuántos pepinos más puedo comer             # features/steps/belly_steps.py:272 0.000s
    Entonces debería decirme que puedo comer 2 pepinos más      # features/steps/belly_steps.py:281 0.000s
Escenario 'Saber cuántos pepinos puedo comer antes de gruñir' tomó 1.08 ms en ejecutarse

  @historia_usuario @language_spanish
  Escenario: Conocer cuánto tiempo falta para que gruña  # features/belly.feature:124
    Dado que he comido 15 pepinos                        # features/steps/belly_steps.py:139 0.000s
    Cuando pregunto cuánto tiempo falta para que gruña   # features/steps/belly_steps.py:288 0.000s
    Entonces debería decirme que gruñirá en 1.5 horas    # features/steps/belly_steps.py:299 0.000s
Escenario 'Conocer cuánto tiempo falta para que gruña' tomó 0.48 ms en ejecutarse

  @historia_usuario @language_spanish
  Escenario: Predecir si el estómago gruñirá después de un tiempo  # features/belly.feature:130
    Dado que he comido 12 pepinos                                  # features/steps/belly_steps.py:139 0.000s
    Cuando pregunto si gruñirá después de 2 horas                  # features/steps/belly_steps.py:307 0.000s
    Entonces debería confirmar que sí gruñirá                      # features/steps/belly_steps.py:317 0.000s
Escenario 'Predecir si el estómago gruñirá después de un tiempo' tomó 0.68 ms en ejecutarse

1 feature passed, 0 failed, 0 skipped
3 scenarios passed, 0 failed, 19 skipped
9 steps passed, 0 failed, 55 skipped, 0 undefined
Took 0m0.001s

melissa  …/CC3S2-software-development/activity7/belly_project   feature/activity7 $?  ♥ 15:35  
```


#### Ejercicio 10: **Escribir pruebas unitarias antes de escenarios BDD**

pruebas unitarias en ``tests/test_belly.py``

**Objetivo**  

- Demostrar la secuencia TDD (tests unitarios) → BDD (escenarios).

Se desarrollaron dos pruebas unitarias

```py
def test_pepinos_restantes():
    belly = Belly()
    belly.comer(15)
    assert belly.pepinos_restantes() == 15
    belly.comer(7)
    assert belly.pepinos_restantes() == 22
    
def test_pepinos_disponibles():
    belly = Belly()
    belly.comer(8)
    assert belly.pepinos_disponibles() == 2
    belly.comer(3)
    assert belly.pepinos_disponibles() == 0
```

Se agregaron dos funciones a la clase Belly

```py
    def pepinos_restantes(self):
        return self.pepinos_comidos

    def pepinos_disponibles(self):
        limite_gruñido = 10
        disponibles = max(0, limite_gruñido - self.pepinos_comidos)
        return disponibles
```

Se crearon dos escenarios BDD
```gherkins
  @tdd_sequence @language_spanish
  Escenario: Conocer cuántos pepinos he comido
    Dado que he comido 15 pepinos
    Cuando consulto los pepinos que he comido
    Entonces debería informarme que he comido 15 pepinos
    
  @tdd_sequence @language_spanish
  Escenario: Saber cuántos pepinos puedo comer sin llegar al límite
    Dado que he comido 7 pepinos
    Cuando consulto los pepinos disponibles
    Entonces debería informarme que puedo comer 3 pepinos más
    
```

Métodos para implementar 
![](https://i.imgur.com/OAryKcb.png)

El resultado con `behave features/ --tags=@tdd_sequence`

![](https://i.imgur.com/66HjSdV.png)

#### Ejercicio 11: **Refactorización guiada por TDD y BDD**

**Objetivo**  

- Refactorizar código existente sin romper funcionalidades, validado por pruebas unitarias y escenarios BDD.

para `esta_gruñendo()` se realizan los tests

![](https://i.imgur.com/ch9Qf59.png)

Ahora refactorizando Belly
![](https://i.imgur.com/k9Rl4QG.png)

Nuevos escenarios específicos
```gherkins
 
  @refactorizacion @language_spanish
  Escenario: Verificar el comportamiento de gruñido en el límite exacto
    Dado que he comido 11 pepinos
    Cuando espero 1.5 horas
    Entonces mi estómago debería gruñir
    
  @refactorizacion @language_spanish
  Escenario: Verificar el comportamiento de gruñido con tiempo exacto
    Dado que he comido 15 pepinos
    Cuando espero 1.5 horas
    Entonces mi estómago debería gruñir
    
  @refactorizacion @language_spanish
  Escenario: Verificar que no gruñe cuando ambos límites fallan
    Dado que he comido 10 pepinos
    Cuando espero 1.4 horas
    Entonces mi estómago no debería gruñir
```

En el pipeline
```yml
 - name: Run Refactoring tests with coverage
      run: |
        cd belly_project
        python -m pytest tests/test_belly.py::test_esta_gruñendo_limite_exacto tests/test_belly.py::test_esta_gruñendo_tiempo_exacto tests/test_belly.py::test_esta_gruñendo_ambos_limites_fallan -v --cov=src.belly --cov-report=term
        behave features/ --tags=@refactorizacion
```

El resultado
![](https://i.imgur.com/MugbWvj.png)

En behave
![](https://i.imgur.com/ZR8WqKZ.png)

#### Ejercicio 12: **Ciclo completo de TDD a BDD – Añadir nueva funcionalidad**

**Objetivo**  

- Desarrollar una nueva funcionalidad *desde cero* con TDD (prueba unitaria) y BDD (escenarios Gherkin).

una nueva funcionalidad
```py
    def tiempo_digestion(self):
        if self.pepinos_comidos <= 0:
            return 0.0
        tiempo_total = self.pepinos_comidos * self.TIEMPO_DIGESTION_POR_PEPINO
        tiempo_restante = max(0.0, tiempo_total - self.tiempo_esperado)
        return round(tiempo_restante, 1)
```

La prueba unitaria:

![](https://i.imgur.com/wGRJIY8.png)

Escenario BDD:
![](https://i.imgur.com/YDjNM8R.png)

El resultado con `behave features/ --tags=@nueva_funcionalidad`

![](https://i.imgur.com/cG0Gxl5.png)

#### Ejercicio 13: **Añadir criterios de aceptación claros**

**Objetivo**  
- Definir con precisión los criterios de aceptación de una nueva funcionalidad y plasmarlos en Gherkin.

una nueva feature digestion.feature
```gherkins

@criterio_nuevo
Característica: Ver el estado de digestión de pepinos

  Escenario: Ver el tiempo de digestión restante después de comer pepinos
    Dado que he comido 10 pepinos
    Cuando consulto el tiempo de digestión
    Entonces me debería informar que faltan 2 horas para digerir completamente

  Escenario: Ver el tiempo de digestión después de esperar un tiempo
    Dado que he comido 20 pepinos
    Cuando espero 1 hora
    Y consulto el tiempo de digestión
    Entonces me debería informar que faltan 3 horas para digerir completamente

  Escenario: Indicar digestión completa cuando ya ha pasado suficiente tiempo
    Dado que he comido 5 pepinos
    Cuando espero 2 horas
    Y consulto el tiempo de digestión
    Entonces me debería informar que faltan 0 horas para digerir completamente 
```

El resultado 
![](https://i.imgur.com/f6O6Knh.png)

#### Ejercicio 14: **Integración con Mocking, Stubs y Fakes (para DevOps)**

**Objetivo**  
- Demostrar cómo inyectar dependencias simuladas en tu clase `Belly` y usarlas en pruebas BDD y TDD.

```py
    def tiempo_transcurrido_real(self):
        """Devuelve el tiempo real transcurrido desde la creación del objeto en horas"""
        tiempo_actual = self.clock_service()
        return (tiempo_actual - self.tiempo_inicio) / 3600  # convertir segundos a horas
```

![](https://i.imgur.com/GySjmNy.png)

```gherkins
# language: es

@fake_clock
Característica: Pruebas con tiempo simulado

  Escenario: El estómago gruñe con hora simulada
    Dado que he comido 15 pepinos
    Cuando espero 2 horas
    Entonces mi estómago debería gruñir

  Escenario: El tiempo de digestión se calcula correctamente con hora simulada
    Dado que he comido 10 pepinos
    Cuando espero 1 hora
    Y consulto el tiempo de digestión
    Entonces me debería informar que faltan 1 horas para digerir completamente 
```

El resultado
![](https://i.imgur.com/8DfRU4s.png)
![](https://i.imgur.com/tolCnOq.png)

#### Ejercicio 15: **Despliegue y validación continua en un entorno de integración (CI/CD)**
**Objetivo**  
- Completar el ciclo DevOps: Cada push al repositorio **desencadena** pruebas automáticas BDD y TDD.



Formateamos con black
![](https://i.imgur.com/FZoSBok.png)
![](https://i.imgur.com/oH0Bj1i.png)

