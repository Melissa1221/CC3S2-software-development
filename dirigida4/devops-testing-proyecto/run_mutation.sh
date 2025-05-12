#!/bin/bash

set -e

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Ejecutando pruebas de mutación en services.py${NC}"
echo "=============================================="

# Ejecutar mutmut
mutmut run --paths-to-mutate src/devops_testing/services.py

# Obtener resultados
echo -e "\n${YELLOW}Resultados de mutación:${NC}"
echo "=============================================="
mutmut results

# Obtener estadísticas
total=$(mutmut results 2>/dev/null | grep "Mutants" | cut -d ' ' -f 2)
killed=$(mutmut results 2>/dev/null | grep "killed" | cut -d ' ' -f 3)
survived=$(mutmut results 2>/dev/null | grep "survived" | cut -d ' ' -f 3)
timeout=$(mutmut results 2>/dev/null | grep "timeout" | cut -d ' ' -f 3)

# Calcular score
if [ -z "$total" ] || [ "$total" -eq 0 ]; then
    score=0
else
    score=$(echo "scale=2; ($killed * 100) / $total" | bc)
fi

# Imprimir resumen
echo -e "\n${YELLOW}Resumen:${NC}"
echo "=============================================="
echo -e "Total mutantes: ${total}"
echo -e "Mutantes eliminados: ${GREEN}${killed}${NC}"
if [ -n "$survived" ] && [ "$survived" -gt 0 ]; then
    echo -e "Mutantes sobrevivientes: ${RED}${survived}${NC}"
else
    echo -e "Mutantes sobrevivientes: ${GREEN}0${NC}"
fi
if [ -n "$timeout" ] && [ "$timeout" -gt 0 ]; then
    echo -e "Timeout: ${YELLOW}${timeout}${NC}"
else
    echo -e "Timeout: ${GREEN}0${NC}"
fi
echo -e "Score: ${score}%"

# Verificar umbral
if (( $(echo "$score < 95" | bc -l) )); then
    echo -e "\n${RED}¡Error! El score de mutación es menor al 95%.${NC}"
    echo -e "Revise los mutantes sobrevivientes con 'mutmut show <id>'"
    exit 1
else
    echo -e "\n${GREEN}¡Éxito! El score de mutación es >= 95%.${NC}"
fi 