# language: es

Característica: Característica del estómago

  Escenario: comer muchos pepinos y gruñir
    Dado que he comido 42 pepinos
    Cuando espero 2 horas
    Entonces mi estómago debería gruñir

  Escenario: comer pocos pepinos y no gruñir
    Dado que he comido 10 pepinos
    Cuando espero 2 horas
    Entonces mi estómago no debería gruñir

  Escenario: comer muchos pepinos y esperar menos de una hora
    Dado que he comido 50 pepinos
    Cuando espero media hora
    Entonces mi estómago no debería gruñir

  Escenario: comer pepinos y esperar en minutos
    Dado que he comido 30 pepinos
    Cuando espero 90 minutos
    Entonces mi estómago debería gruñir

  Escenario: comer pepinos y esperar en diferentes formatos
    Dado que he comido 25 pepinos
    Cuando espero "dos horas y treinta minutos"
    Entonces mi estómago debería gruñir

  Escenario: Comer pepinos y esperar con horas, minutos y segundos
    Dado que he comido 35 pepinos
    Cuando espero "1 hora y 30 minutos y 45 segundos"
    Entonces mi estómago debería gruñir

  Escenario: Comer una cantidad fraccionaria de pepinos
    Dado que he comido 0.5 pepinos
    Cuando espero 2 horas
    Entonces mi estómago no debería gruñir

  Escenario: Esperar usando horas en inglés
    Dado que he comido 20 pepinos
    Cuando espero two hours and thirty minutes
    Entonces mi estómago debería gruñir

  Escenario: Esperar usando minutos y segundos en inglés
    Dado que he comido 25 pepinos
    Cuando espero one hour and forty five minutes and thirty seconds
    Entonces mi estómago debería gruñir

  Escenario: Comer pepinos y esperar un tiempo aleatorio
    Dado que he comido 25 pepinos
    Cuando espero un tiempo aleatorio entre 1 y 3 horas
    Entonces mi estómago debería gruñir

  Escenario: Comer pepinos y esperar un tiempo aleatorio en inglés
    Dado que he comido 25 pepinos
    Cuando espero a random time between 2 and 5 hours
    Entonces mi estómago debería gruñir

  Escenario: Manejar una cantidad negativa de pepinos
    Dado que he comido -5 pepinos
    Entonces debería ocurrir un error de cantidad negativa

  Escenario: Manejar una cantidad excesiva de pepinos
    Dado que he comido 150 pepinos
    Entonces debería ocurrir un error de cantidad excesiva
    
  Escenario: Comer 1000 pepinos y esperar 10 horas
    Dado que he comido 1000 pepinos
    Cuando espero 10 horas
    Entonces mi estómago debería gruñir
    
  Escenario: Prueba de rendimiento con grandes cantidades
    Dado que he comido 5000 pepinos
    Cuando espero 20 horas
    Entonces mi estómago debería gruñir

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
    
  Escenario: Comer muchos pepinos y esperar el tiempo suficiente
    Dado que he comido 15 pepinos
    Cuando espero 2 horas
    Entonces mi estómago debería gruñir
    