# Actividad: Testing y DevOps con SOLID

Esta actividad se centra en la aplicación de los principios SOLID en el contexto de testing y DevOps. Se divide en tres partes: un nivel teórico sobre SOLID, implementación de código y fixtures, y extensiones completas a nivel de proyecto.

## Nivel teórico (SRP -> DIP)

### 1. Clasificación de responsabilidades en PaymentService

El módulo `services.py` concentra la orquestación de pagos a través de la clase `PaymentService`. Se pueden identificar cuatro responsabilidades principales:

1. **Gestión de usuarios**: Recuperar y validar el usuario antes de procesar el pago.
2. **Procesamiento de pagos**: Orquestar el proceso completo de pago, conectando con la pasarela.
3. **Persistencia de pagos**: Guardar el pago una vez procesado correctamente.
4. **Política de reintentos**: Manejar fallos transitorios en la pasarela de pagos.

De estas, las candidatas a extraerse serían:

- **Política de reintentos**: Ya la he extraído a una clase `RetryPolicy` que se encarga específicamente de reintentar operaciones que pueden fallar.
- **Validación de pagos**: Podría extraerse una clase `PaymentValidator` que centralice la validación del monto y otros aspectos del pago.

Para implementar estas extracciones, deberían crearse los siguientes fixtures:

- `retry_policy`: Para inyectar la política de reintentos configurable.
- `payment_validator`: Para inyectar un validador de pagos.

### 2. Mapa de dependencias con DIP

La arquitectura ideal después de aplicar DIP para introducir `NotificationService` y `RetryPolicy` sería:

```
interfaces/ <--- models/
    ^           ^   ^
    |           |   |
repositories/   |   |
    ^           |   |
    |           |   |
services/ ----> |   |
    ^           |   |
    |           |   |
policies/ ------+   |
    ^               |
    |               |
notifications/ -----+
```

Justificación:
- `interfaces/`: Contiene abstracciones de las que dependen las capas superiores (siguiendo DIP).
- `models/`: Define entidades de dominio independientes.
- `repositories/`, `services/`, `policies/` y `notifications/`: Implementan las interfaces y dependen de abstracciones.

### 3. Análisis de sustitución (LSP y Mock)

Un `Mock` cumple con el Principio de Sustitución de Liskov (LSP) aunque acepte métodos inexistentes porque:

1. **Comportamiento de caja negra**: Desde la perspectiva de un cliente, un mock puede responder a cualquier método que se le invoque, igual que lo haría una implementación real.
2. **Contrato funcional**: El contrato fundamental se mantiene: se llama a un método, se reciben parámetros y se devuelve un valor o efecto.

Sin embargo, este comportamiento puede llevar a errores sutiles si cambia la interfaz real y las pruebas siguen pasando con un mock desactualizado.

Para mitigar este problema, `unittest.mock.create_autospec` es esencial:

```python
from unittest.mock import create_autospec
from devops_testing.services import PaymentGateway

# Mock normal (peligroso)
dangerous_mock = Mock()
dangerous_mock.non_existent_method()  # ¡No falla!

# Mock con autospec (seguro)
safe_mock = create_autospec(PaymentGateway)
safe_mock.non_existent_method()  # Falla con AttributeError
```

### 4. Cobertura ≠ calidad

Aunque la cobertura del 100% parece ideal, hay muchos defectos que no detecta:

1. **Lógica de negocio incorrecta pero consistente**: El código puede implementar requisitos mal entendidos pero de manera coherente. Las property-based tests pueden encontrar estos casos al generar datos aleatorios que prueben propiedades invariantes del sistema.

2. **Casos extremos no contemplados**: Valores en los límites, situaciones excepcionales o combinaciones inusuales de parámetros. Las pruebas de fuzzing pueden encontrar estos casos al generar entradas impredecibles.

3. **Condiciones de carrera**: Problemas de concurrencia que solo ocurren en determinadas situaciones. Las pruebas de estrés y concurrencia pueden revelar estos problemas.

4. **Fallos de integración entre componentes**: Aunque cada componente funcione correctamente de forma aislada, pueden fallar al integrarse. Las contract tests verifican que las interfaces entre componentes se respeten.

### 5. Ventajas y riesgos de monkeypatch

**Constructor-like DI vs Setter-like DI**

La inyección de dependencias constructor-like utiliza el constructor para proporcionar todas las dependencias, mientras que setter-like permite modificarlas después de la creación del objeto.

**Constructor-like (vía fixtures de fábrica)**:
- *Casos apropiados*:
  - Cuando las dependencias son inmutables durante el ciclo de vida del objeto
  - Para garantizar que un objeto siempre tiene todas sus dependencias
  - En tests que prueban el sistema completo integrado
- *Smells*:
  - Constructores con demasiados parámetros
  - Tests frágiles que dependen de muchas dependencias al mismo tiempo
  - Dificultad para aislar comportamientos específicos

**Setter-like (vía monkeypatch)**:
- *Casos apropiados*:
  - Pruebas unitarias aisladas que solo necesitan mockear una parte específica
  - Cuando se necesita cambiar una dependencia después de la inicialización
  - Para simular fallos o comportamientos excepcionales en puntos específicos
- *Smells*:
  - Estado mutable difícil de rastrear
  - Riesgo de pruebas contaminadas cuando el estado no se restablece
  - Acoplamiento a detalles de implementación internos

## Nivel implementación, código y fixtures

### 6. Fixture condicional por entorno

**Objetivo**: Permitir que los mismos tests usen `DummyGateway` localmente y un gateway real en integración.

Para implementar esto, creé una clase `RealGateway` que simula latencia en el archivo `tests/fakes.py`:

```python
class RealGateway:
    """Gateway que simula latencia como si fuera un servicio real externo."""
    def __init__(self, latency: float = 0.5, succeed: bool = True):
        self._latency = latency
        self._succeed = succeed
        self.calls: list[tuple[Decimal, str, str]] = []
    
    def charge(self, amount: Decimal, currency: str, user: User):
        time.sleep(self._latency)  # Simula latencia de red
        self.calls.append((amount, currency, user.id))
        return self._succeed
```

Luego, en `conftest.py`, configuré un fixture condicional que lee la variable de entorno:

```python
@pytest.fixture
def conditional_gateway():
    """
    Gateway condicional por entorno. Si USE_REAL_GATEWAY está activo,
    usa el gateway real con latencia. Caso contrario usa DummyGateway.
    """
    use_real = os.environ.get("USE_REAL_GATEWAY", "").lower() in ("1", "true", "yes")
    
    if use_real:
        # Marcamos estos tests como lentos
        pytest.mark.slow
        return RealGateway(latency=0.5)
    else:
        return DummyGateway()
```

Finalmente, actualicé el fixture `payment_service` para usar `conditional_gateway` y creé un test con el marcador `slow`:

```python
@pytest.mark.slow
def test_payment_with_conditional_gateway(payment_service, test_user):
    """
    Este test usará el RealGateway con latencia cuando se ejecute con 
    USE_REAL_GATEWAY=1, o el DummyGateway cuando se ejecute normalmente.
    """
    # Test implementation...
```

### 7. Custom marker @pytest.mark.contract

**Objetivo**: Señalar tests que verifiquen invariantes de dominio.

Primero, definí el marcador en `pytest.ini`:

```ini
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    contract: tests that verify domain invariants
```

Luego, creé dos casos de prueba etiquetados con este marcador en `tests/test_contract.py`:

```python
@pytest.mark.contract
def test_payment_requires_valid_user(payment_service, test_user):
    """Verifica que no se puede procesar un pago sin un usuario válido."""
    with pytest.raises(KeyError):
        payment_service.process_payment("usuario_inexistente", Decimal("50"), "USD")

@pytest.mark.contract
def test_payment_requires_positive_amount(payment_service, test_user):
    """Verifica que el monto del pago debe ser positivo."""
    with pytest.raises(ValueError):
        payment_service.process_payment(test_user.username, Decimal("-10"), "USD")
```

### 8. Policy de reintentos

**Objetivo**: Implementar `RetryPolicy` configurado con `Config.retries`.

Implementé la clase `RetryPolicy` en `src/devops_testing/retry.py`:

```python
class RetryPolicy:
    """Política que permite reintentar operaciones que pueden fallar transitoriamente."""
    
    def __init__(self, max_retries: int = 3, delay: float = 0.01):
        """
        Inicializa la política de reintentos.
        """
        self.max_retries = max_retries
        self.delay = delay
        
    def execute(self, operation: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        """
        Ejecuta una operación con reintentos según la política configurada.
        """
       
```

Luego, integré esta política en `PaymentService.process_payment`:

```python
def __init__(self, gateway: PaymentGateway, payment_repo, user_repo,
             config: Optional[Config] = None, logger=None):
    # ...
    self._retry_policy = RetryPolicy(max_retries=self._cfg.retries)

def process_payment(self, username: str, amount: Decimal, currency: str) -> str:
    # ...
    success = self._retry_policy.execute(
        self._gw.charge, amount, currency, user
    )
    # ...
```

Finalmente, implementé tests parametrizados para verificar diferentes escenarios de reintento:

```python
@pytest.mark.parametrize("retries,fail_times", [
    (1, 0),  # Success on first try (no failures)
    (2, 1),  # Success on second try (1 failure)
    (3, 2),  # Success on third try (2 failures)
])
def test_retry_policy_execution(retries, fail_times):
    """Prueba parametrizada que verifica que la política reintenta correctamente."""
    # Test implementation...
```

### 9. Property-based testing con Hypothesis

**Objetivo**: Generar montos aleatorios positivos y verificar que siempre se persiste el pago.

Primero, añadí `hypothesis` a `requirements.txt`:

```
pytest
requests
hypothesis
```

Luego, creé un archivo `test_payment_property.py` con dos pruebas property-based:

```python
@given(amount=st.decimals(min_value="0.01", max_value="1000000.00"))
def test_payment_persists_with_random_amounts(property_service):
    """
    Verifica que cualquier monto positivo válido genere un pago persistido.
    """
    # Test implementation...

@given(
    amounts=st.lists(
        st.decimals(min_value="0.01", max_value="1000.00"),
        min_size=1,
        max_size=10
    )
)
def test_multiple_payments_persist_correctly(property_service):
    """
    Verifica que múltiples pagos con montos aleatorios se persistan correctamente.
    
```

### 10. Observabilidad: logging configurable

**Objetivo**: Permitir inyectar un logger en `PaymentService`.

Añadí un parámetro opcional `logger` al constructor de `PaymentService` y registré eventos clave:

```python
def __init__(self, gateway: PaymentGateway, payment_repo, user_repo,
             config: Optional[Config] = None, logger=None):
    # ...
    self._logger = logger

def process_payment(self, username: str, amount: Decimal, currency: str) -> str:
    # ...
    if self._logger:
        self._logger.info(f"start-payment: user={username} amount={amount} currency={currency}")
    # ...
    if self._logger:
        self._logger.info(f"payment-ok: id={payment.id}")
    # ...
```

Implementé pruebas en `test_logging.py` que verifican los mensajes de log:

```python
def test_logging_emitted(self, payment_repo, user_repo, dummy_gateway, test_user, capsys):
    """Verifica que los mensajes de log se emiten correctamente."""
    # Test implementation...
    assert "start-payment" in captured.err
    assert "payment-ok" in captured.err
```

## Nivel proyecto - extensiones completas

### 11. Gateway de terceros simulado (FASTAPI)

**Objetivo**: Reemplazar el Mock por un microservicio HTTP local.

Implementé una aplicación FastAPI en `src/external_gateway/app.py`:

```python
app = FastAPI(title="Payment Gateway API")

@app.post("/charge", response_model=ChargeResponse)
async def charge(request: ChargeRequest):
    """
    Simula un cargo en una pasarela de pagos externa.
    """
    # Implementation...
```

Creé un cliente HTTP en `src/external_gateway/client.py`:

```python
class HttpPaymentGateway:
    """
    Gateway que realiza llamadas HTTP a un servicio externo.
    """
    # Implementation...
```

Añadí fixtures para el servidor en `conftest.py`:

```python
@pytest.fixture(scope="session")
def gateway_server(free_port):
    """
    Levanta el servidor FastAPI en un thread separado.
    """
    # Implementation...
```

Y creé pruebas de integración en `tests/integration/test_http_gateway.py`:

```python
@pytest.mark.http
def test_http_gateway_success(http_gateway, test_user):
    """Verifica que el gateway HTTP funciona correctamente en caso de éxito."""
    # Test implementation...
```

### 12. Persistencia en SQLite

**Objetivo**: Sustituir `InMemoryPaymentRepository` por `SQLitePaymentRepository`.

Creé un módulo para los repositorios SQLite en `src/devops_testing/persistence/sqlite_repo.py`:

```python
class SQLitePaymentRepository:
    """Repositorio de pagos que usa SQLite."""
    # Implementation...

class SQLiteUserRepository:
    """Repositorio de usuarios que usa SQLite."""
    # Implementation...
```

Añadí fixtures para SQLite en `conftest.py`:

```python
@pytest.fixture
def sqlite_db_path(tmp_path):
    """
    Genera una ruta temporal para la base de datos SQLite.
    """
    return str(tmp_path / "test.db")

@pytest.fixture
def sqlite_user_repo(sqlite_db_path):
    """Repositorio de usuarios SQLite."""
    return SQLiteUserRepository(sqlite_db_path)
```

Y creé pruebas parametrizadas que funcionan con ambos tipos de repositorios:

```python
@pytest.mark.parametrize(
    "user_repo_fixture,payment_repo_fixture,test_user_fixture",
    [
        ("user_repo", "payment_repo", "test_user"),  # In-Memory
        ("sqlite_user_repo", "sqlite_payment_repo", "sqlite_test_user"),  # SQLite
    ],
    indirect=True
)
def test_repo_agnostic_payment_flow(user_repo_fixture, payment_repo_fixture, 
                                   test_user_fixture, dummy_gateway):
    """
    Test parametrizado que demuestra que PaymentService funciona
    con cualquier implementación de repositorio.
    """
    # Test implementation...
```

### 13. Pipeline local con Make + tox

**Objetivo**: Simular la matriz del CI en equipos de los estudiantes.

Definí un archivo `tox.ini` con diferentes entornos:

```ini
[tox]
isolated_build = True
envlist = py310, py311, lint, type

[testenv]
deps =
    pytest
    requests
    hypothesis
    fastapi
    uvicorn
    sqlalchemy
commands =
    pytest {posargs:tests}
```

Creé un `Makefile` con diferentes targets:

```make
test:
	$(PYTEST) $(PYTEST_ARGS)

coverage:
	$(COVERAGE)

format:
	$(BLACK) src tests

lint:
	$(TOX) -e lint

type:
	$(TOX) -e type

ci:
	$(TOX)
```

Y actualicé el README con documentación detallada:

```markdown
#### Ejecución del pipeline CI local

Este proyecto incluye un pipeline de CI local que puedes ejecutar con:

```bash
make ci
```
```

### 14. Mutación guiada (mutmut)

**Objetivo**: Demostrar que la suite detecta mutaciones.

Configuré mutmut para analizar `services.py` en `.mutmut`:

```
paths_to_exclude=[]
paths_to_mutate=["src/devops_testing/services.py"]
runner="python -m pytest"
tests_dir="tests/"
```

Creé un script `run_mutation.sh` para ejecutar y mostrar el resumen:

```bash
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

# ... Más código para mostrar resultados ...
```

Y actualicé el Makefile para incluir este paso:

```make
mutation:
	$(MUTATION)
```

### 15. Informe de reporte de pruebas en Markdown

**Objetivo**: Generar reporte automático post-pytest.

Añadí `pytest-md-report` a los requisitos:

```
pytest-md-report
```

Configuré las opciones del informe en `pytest.ini`:

```ini
md_report_options =
    output_path=reports/latest.md
    report_title=Test Results
    tables=slowest_tests, summary, stats
    show_slowest=3
```

Y agregué un nuevo target al Makefile:

```make
report:
	$(REPORT)
```

Con esto, se genera automáticamente un informe Markdown con estadísticas de las pruebas, incluyendo la sección de "Slowest tests" con el top 3 de pruebas más lentas.
