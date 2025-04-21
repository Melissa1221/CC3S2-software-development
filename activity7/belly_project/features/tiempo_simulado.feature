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