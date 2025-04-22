#!/usr/bin/env python
"""
Script para ejecutar todas las pruebas del proyecto Belly:
1. Primero las pruebas unitarias (Pytest) - más rápidas
2. Luego las pruebas BDD (Behave) - más lentas

Uso:
    python run_all_tests.py
"""

import os
import sys
import subprocess
import time


def print_header(title):
    """Imprime un encabezado con formato."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def run_unit_tests():
    """Ejecuta las pruebas unitarias con pytest."""
    print_header("EJECUTANDO PRUEBAS UNITARIAS (PYTEST)")

    start_time = time.time()
    result = subprocess.run(
        ["pytest", "tests/", "-v", "--cov=src", "--cov-report=term"],
        capture_output=True,
        text=True,
    )
    end_time = time.time()

    print(result.stdout)
    if result.stderr:
        print("ERRORES:", result.stderr)

    print(f"Tiempo total pytest: {end_time - start_time:.2f} segundos")
    return result.returncode


def run_bdd_tests():
    """Ejecuta las pruebas BDD con behave."""
    print_header("EJECUTANDO PRUEBAS BDD (BEHAVE)")

    start_time = time.time()
    result = subprocess.run(["behave"], capture_output=True, text=True)
    end_time = time.time()

    print(result.stdout)
    if result.stderr:
        print("ERRORES:", result.stderr)

    print(f"Tiempo total behave: {end_time - start_time:.2f} segundos")
    return result.returncode


def main():
    """Función principal que ejecuta todas las pruebas."""
    print_header("INICIANDO EJECUCIÓN DE TODAS LAS PRUEBAS")

    # Cambiar al directorio del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Ejecutar pruebas en orden
    total_start_time = time.time()

    # 1. Primero las pruebas unitarias
    unit_test_result = run_unit_tests()

    # 2. Luego las pruebas BDD
    bdd_test_result = run_bdd_tests()

    total_end_time = time.time()
    total_time = total_end_time - total_start_time

    # Resultado final
    print_header("RESUMEN FINAL")
    print(f"Tiempo total de ejecución: {total_time:.2f} segundos")

    if unit_test_result == 0 and bdd_test_result == 0:
        print("Todas las pruebas pasaron correctamente")
        return 0
    else:
        print("Algunas pruebas fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
