# language: es

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