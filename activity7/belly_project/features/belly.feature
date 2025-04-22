# language: es

Característica: Característica del estómago

  @core_logic @language_spanish
  Escenario: comer muchos pepinos y gruñir
    Dado que he comido 42 pepinos
    Cuando espero 2 horas
    Entonces mi estómago debería gruñir

  @core_logic @language_spanish
  Escenario: comer pocos pepinos y no gruñir
    Dado que he comido 10 pepinos
    Cuando espero 2 horas
    Entonces mi estómago no debería gruñir

  @core_logic @language_spanish
  Escenario: comer muchos pepinos y esperar menos de una hora
    Dado que he comido 50 pepinos
    Cuando espero media hora
    Entonces mi estómago no debería gruñir

  @language_spanish
  Escenario: comer pepinos y esperar en minutos
    Dado que he comido 30 pepinos
    Cuando espero 90 minutos
    Entonces mi estómago debería gruñir

  @language_spanish
  Escenario: comer pepinos y esperar en diferentes formatos
    Dado que he comido 25 pepinos
    Cuando espero "dos horas y treinta minutos"
    Entonces mi estómago debería gruñir

  @complex_time @language_spanish
  Escenario: Comer pepinos y esperar con horas, minutos y segundos
    Dado que he comido 35 pepinos
    Cuando espero "1 hora y 30 minutos y 45 segundos"
    Entonces mi estómago debería gruñir

  @fractional
  Escenario: Comer una cantidad fraccionaria de pepinos
    Dado que he comido 0.5 pepinos
    Cuando espero 2 horas
    Entonces mi estómago no debería gruñir

  @language_english
  Escenario: Esperar usando horas en inglés
    Dado que he comido 20 pepinos
    Cuando espero two hours and thirty minutes
    Entonces mi estómago debería gruñir

  @complex_time @language_english
  Escenario: Esperar usando minutos y segundos en inglés
    Dado que he comido 25 pepinos
    Cuando espero one hour and forty five minutes and thirty seconds
    Entonces mi estómago debería gruñir

  @random_time @language_spanish
  Escenario: Comer pepinos y esperar un tiempo aleatorio
    Dado que he comido 25 pepinos
    Cuando espero un tiempo aleatorio entre 1 y 3 horas
    Entonces mi estómago debería gruñir

  @random_time @language_english
  Escenario: Comer pepinos y esperar un tiempo aleatorio en inglés
    Dado que he comido 25 pepinos
    Cuando espero a random time between 2 and 5 hours
    Entonces mi estómago debería gruñir

  @error_handling
  Escenario: Manejar una cantidad negativa de pepinos
    Dado que he comido -5 pepinos
    Entonces debería ocurrir un error de cantidad negativa

  @error_handling
  Escenario: Manejar una cantidad excesiva de pepinos
    Dado que he comido 150 pepinos
    Entonces debería ocurrir un error de cantidad excesiva

  @performance @language_spanish
  Escenario: Comer 1000 pepinos y esperar 10 horas
    Dado que he comido 1000 pepinos
    Cuando espero 10 horas
    Entonces mi estómago debería gruñir

  @performance @language_spanish
  Escenario: Prueba de rendimiento con grandes cantidades
    Dado que he comido 5000 pepinos
    Cuando espero 20 horas
    Entonces mi estómago debería gruñir

  @complex_time @language_spanish
  Escenario: Manejar tiempos complejos con comas
    Dado que he comido 50 pepinos
    Cuando espero "1 hora, 30 minutos y 45 segundos"
    Entonces mi estómago debería gruñir

  @complex_time @language_spanish
  Escenario: Manejar tiempos complejos con diferentes separadores
    Dado que he comido 40 pepinos
    Cuando espero "2 horas, 15 minutos, 30 segundos"
    Entonces mi estómago debería gruñir

  @complex_time @language_english
  Escenario: Manejar tiempos complejos en inglés con comas
    Dado que he comido 45 pepinos
    Cuando espero "3 hours, 10 minutes, 20 seconds"
    Entonces mi estómago debería gruñir

  @core_logic @language_spanish
  Escenario: Comer muchos pepinos y esperar el tiempo suficiente
    Dado que he comido 15 pepinos
    Cuando espero 2 horas
    Entonces mi estómago debería gruñir

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
    
  @nueva_funcionalidad @language_spanish
  Escenario: Calcular el tiempo de digestión de pepinos
    Dado que he comido 20 pepinos
    Cuando consulto el tiempo de digestión
    Entonces me debería informar que faltan 4 horas para digerir completamente
    
  @nueva_funcionalidad @language_spanish  
  Escenario: Calcular el tiempo de digestión después de esperar
    Dado que he comido 15 pepinos
    Cuando espero 2 horas
    Y consulto el tiempo de digestión
    Entonces me debería informar que faltan 1 horas para digerir completamente
    
  @nueva_funcionalidad @language_spanish
  Escenario: Tiempo de digestión con el estómago vacío
    Dado que he comido 0 pepinos
    Cuando consulto el tiempo de digestión
    Entonces me debería informar que faltan 0 horas para digerir completamente
    