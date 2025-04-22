# Actividad 9: Red-Green-Refactor con UserManager

## Iteración 1: Agregar usuario (Funcionalidad básica)

Se implementó la funcionalidad básica para agregar usuarios

### Red: primera prueba

```python
# tests/test_user_manager.py
import pytest
from src.user_manager import UserManager, UserAlreadyExistsError

def test_agregar_usuario_exitoso():
    # Arrange
    manager = UserManager()
    username = "kapu"
    password = "securepassword"

    # Act
    manager.add_user(username, password)

    # Assert
    assert manager.user_exists(username), "El usuario debería existir después de ser agregado."
```

Al ejecutar esta prueba, falló porque aún no había implementado la clase `UserManager`.

### Green: clase UserManager

Versión mínima de `UserManager` para que la prueba pasara:

```python
# src/user_manager.py
class UserAlreadyExistsError(Exception):
    pass

class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password):
        if username in self.users:
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        self.users[username] = password

    def user_exists(self, username):
        return username in self.users
```

### Resultado del test:

```bash

Ejemplo/tests/test_user_manager.py .                                                                                              [100%]

=========================================================== 1 passed in 0.01s ===========================================================
```

## Iteración 2: Autenticación de usuario (Inyección de dependencia para Hashing)

Se añade autenticación de usuarios y se usa inyección de dependencias para gestionar el hashing de contraseñas.

Red:

 `FakeHashService` para simular el comportamiento del hashing:

```python
class FakeHashService:
    """
    Servicio de hashing 'falso' (Fake) que simplemente simula el hashing
    devolviendo la cadena con un prefijo "fakehash:" para fines de prueba.
    """
    def hash(self, plain_text: str) -> str:
        return f"fakehash:{plain_text}"

    def verify(self, plain_text: str, hashed_text: str) -> bool:
        return hashed_text == f"fakehash:{plain_text}"

def test_autenticar_usuario_exitoso_con_hash():
    # Arrange
    hash_service = FakeHashService()
    manager = UserManager(hash_service=hash_service)

    username = "usuario1"
    password = "mypassword123"
    manager.add_user(username, password)

    # Act
    autenticado = manager.authenticate_user(username, password)

    # Assert
    assert autenticado, "El usuario debería autenticarse correctamente con la contraseña correcta."
```

### Green: hashing y autenticación

Se modifica la clase `UserManager` para usar el servicio de hashing:

```python
class UserNotFoundError(Exception):
    pass

class UserAlreadyExistsError(Exception):
    pass

class UserManager:
    def __init__(self, hash_service=None):
        """
        Si no se provee un servicio de hashing, se asume un hash trivial por defecto
        (simplemente para no romper el código).
        """
        self.users = {}
        self.hash_service = hash_service
        if not self.hash_service:
            # Si no pasamos un hash_service, usamos uno fake por defecto.
            # En producción, podríamos usar bcrypt o hashlib.
            class DefaultHashService:
                def hash(self, plain_text: str) -> str:
                    return plain_text  # Pésimo, pero sirve de ejemplo.

                def verify(self, plain_text: str, hashed_text: str) -> bool:
                    return plain_text == hashed_text

            self.hash_service = DefaultHashService()

    def add_user(self, username, password):
        if username in self.users:
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        hashed_pw = self.hash_service.hash(password)
        self.users[username] = hashed_pw

    def user_exists(self, username):
        return username in self.users

    def authenticate_user(self, username, password):
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        stored_hash = self.users[username]
        return self.hash_service.verify(password, stored_hash)
```

### Resultado del test:

```bash
platform linux -- Python 3.12.8, pytest-8.3.5, pluggy-1.5.0
rootdir: /home/melissa/documents/uni/software-development/CC3S2-software-development/activity9/Ejemplo
configfile: pytest.ini
collected 2 items                                                                                                                       

Ejemplo/tests/test_user_manager.py ..                                                                                             [100%]

=========================================================== 2 passed in 0.01s ===========================================================

```

## Iteración 3: Uso de un Mock para verificar llamadas (Spy/Mock)

En esta iteración se quiere verificar que el método `hash` del servicio de hashing se llamara correctamente al agregar un usuario. Para esto, se usa un Mock que actúa como un espía.

### Red: Prueba con mock para verificar la llamada

```python
from unittest.mock import MagicMock

def test_hash_service_es_llamado_al_agregar_usuario():
    # Arrange
    mock_hash_service = MagicMock()
    manager = UserManager(hash_service=mock_hash_service)
    username = "spyUser"
    password = "spyPass"

    # Act
    manager.add_user(username, password)

    # Assert
    mock_hash_service.hash.assert_called_once_with(password)
```



### Resultado del test:

```bash
========================================================== test session starts ==========================================================
platform linux -- Python 3.12.8, pytest-8.3.5, pluggy-1.5.0
rootdir: /home/melissa/documents/uni/software-development/CC3S2-software-development/activity9/Ejemplo
configfile: pytest.ini
collected 3 items                                                                                                                       

Ejemplo/tests/test_user_manager.py ...                                                                                            [100%]

=========================================================== 3 passed in 0.02s ===========================================================
```

## Iteración 4: Excepción al agregar usuario existente (Stubs)

Se usa un stub para forzar que `user_exists` siempre devuelva `True`.

### Red: Prueba con stub para usuarios duplicados

```python
def test_no_se_puede_agregar_usuario_existente_stub():
    # Este stub forzará que user_exists devuelva True
    class StubUserManager(UserManager):
        def user_exists(self, username):
            return True

    stub_manager = StubUserManager()
    with pytest.raises(UserAlreadyExistsError) as exc:
        stub_manager.add_user("cualquier", "1234")

    assert "ya existe" in str(exc.value)
```

Esta prueba fallaba porque `add_user` verificaba si el usuario existía mediante `username in self.users` en lugar de usar el método `user_exists`.

### Green: Modificar add_user para usar user_exists

```python
def add_user(self, username, password):
    if self.user_exists(username):  # <- Cambio aquí
        raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
    hashed_pw = self.hash_service.hash(password)
    self.users[username] = hashed_pw
```

### Resultado del test:

```bash
========================================== test session starts ==========================================
platform linux -- Python 3.12.8, pytest-8.3.5, pluggy-1.5.0 -- /home/melissa/documents/uni/software-devel
opment/CC3S2-software-development/activity9/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/melissa/documents/uni/software-development/CC3S2-software-development/activity9/Ejemplo
configfile: pytest.ini
collected 4 items                                                                                       

tests/test_user_manager.py::test_agregar_usuario_exitoso PASSED                                   [ 25%]
tests/test_user_manager.py::test_autenticar_usuario_exitoso_con_hash PASSED                       [ 50%]
tests/test_user_manager.py::test_hash_service_es_llamado_al_agregar_usuario PASSED                [ 75%]
tests/test_user_manager.py::test_no_se_puede_agregar_usuario_existente_stub PASSED                [100%]

=========================================== 4 passed in 0.03s ===========================================

```

## Iteración 5: Agregar un "Fake" repositorio de datos (Inyección de Dependencias)

En esta iteración se implementa una abstracción del almacenamiento de usuarios mediante la inyección de un repositorio, lo que permite reemplazar el diccionario interno por cualquier otro sistema de almacenamiento.

### Red: Prueba con un repositorio fake

```python
class InMemoryUserRepository:
    """Fake de un repositorio de usuarios en memoria."""
    def __init__(self):
        self.data = {}

    def save_user(self, username, hashed_password):
        if username in self.data:
            raise UserAlreadyExistsError(f"'{username}' ya existe.")
        self.data[username] = hashed_password

    def get_user(self, username):
        return self.data.get(username)

    def exists(self, username):
        return username in self.data

def test_inyectar_repositorio_inmemory():
    repo = InMemoryUserRepository()
    manager = UserManager(repo=repo)  # inyectamos repo
    username = "fakeUser"
    password = "fakePass"

    manager.add_user(username, password)
    assert manager.user_exists(username)
```

### Green: Implementación de la inyección de repositorio

Se reescribió `UserManager` para aceptar un repositorio de usuarios

```python
class UserManager:
    def __init__(self, hash_service=None, repo=None):
        self.hash_service = hash_service or self._default_hash_service()
        self.repo = repo or self._default_repo()
    
    def _default_hash_service(self):
        class DefaultHashService:
            def hash(self, plain_text: str) -> str:
                return plain_text
            def verify(self, plain_text: str, hashed_text: str) -> bool:
                return plain_text == hashed_text
        return DefaultHashService()

    def _default_repo(self):
        # Un repositorio en memoria muy básico
        class InternalRepo:
            def __init__(self):
                self.data = {}
            def save_user(self, username, hashed_password):
                if username in self.data:
                    raise UserAlreadyExistsError(f"'{username}' ya existe.")
                self.data[username] = hashed_password
            def get_user(self, username):
                return self.data.get(username)
            def exists(self, username):
                return username in self.data
        return InternalRepo()

    def add_user(self, username, password):
        if self.user_exists(username):
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        hashed = self.hash_service.hash(password)
        self.repo.save_user(username, hashed)

    def user_exists(self, username):
        return self.repo.exists(username)

    def authenticate_user(self, username, password):
        stored_hash = self.repo.get_user(username)
        if stored_hash is None:
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        return self.hash_service.verify(password, stored_hash)
```

### Resultado del test:

```bash
========================================== test session starts ==========================================
platform linux -- Python 3.12.8, pytest-8.3.5, pluggy-1.5.0 -- /home/melissa/documents/uni/software-devel
opment/CC3S2-software-development/activity9/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/melissa/documents/uni/software-development/CC3S2-software-development/activity9/Ejemplo
configfile: pytest.ini
collected 5 items                                                                                       

tests/test_user_manager.py::test_agregar_usuario_exitoso PASSED                                   [ 20%]
tests/test_user_manager.py::test_autenticar_usuario_exitoso_con_hash PASSED                       [ 40%]
tests/test_user_manager.py::test_hash_service_es_llamado_al_agregar_usuario PASSED                [ 60%]
tests/test_user_manager.py::test_no_se_puede_agregar_usuario_existente_stub PASSED                [ 80%]
tests/test_user_manager.py::test_inyectar_repositorio_inmemory PASSED                             [100%]

=========================================== 5 passed in 0.02s ===========================================
```

## Iteración 6: Introducir un "Spy" de notificaciones (Envío de correo)

Se implementó una funcionalidad para enviar un correo de bienvenida al registrar un usuario. Para probar esto sin enviar correos reales se usa un spy

### Red: Prueba con spy para el servicio de correo

```python
def test_envio_correo_bienvenida_al_agregar_usuario():
    # Arrange
    mock_email_service = MagicMock()
    manager = UserManager(email_service=mock_email_service)
    username = "nuevoUsuario"
    password = "NuevaPass123!"

    # Act
    manager.add_user(username, password)

    # Assert
    mock_email_service.send_welcome_email.assert_called_once_with(username)
```

### Green: Implementación del servicio de correo

Modifiqué `UserManager` para aceptar un servicio de correo:

```python
class UserManager:
    def __init__(self, hash_service=None, repo=None, email_service=None):
        self.hash_service = hash_service or self._default_hash_service()
        self.repo = repo or self._default_repo()
        self.email_service = email_service


    def add_user(self, username, password):
        if self.user_exists(username):
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        hashed = self.hash_service.hash(password)
        self.repo.save_user(username, hashed)
        if self.email_service:
            self.email_service.send_welcome_email(username)
```

### Resultado del test:

```bash
========================================== test session starts ==========================================
platform linux -- Python 3.12.8, pytest-8.3.5, pluggy-1.5.0 -- /home/melissa/documents/uni/software-devel
opment/CC3S2-software-development/activity9/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/melissa/documents/uni/software-development/CC3S2-software-development/activity9/Ejemplo
configfile: pytest.ini
collected 6 items                                                                                       

tests/test_user_manager.py::test_agregar_usuario_exitoso PASSED                                   [ 16%]
tests/test_user_manager.py::test_autenticar_usuario_exitoso_con_hash PASSED                       [ 33%]
tests/test_user_manager.py::test_hash_service_es_llamado_al_agregar_usuario PASSED                [ 50%]
tests/test_user_manager.py::test_no_se_puede_agregar_usuario_existente_stub PASSED                [ 66%]
tests/test_user_manager.py::test_inyectar_repositorio_inmemory PASSED                             [ 83%]
tests/test_user_manager.py::test_envio_correo_bienvenida_al_agregar_usuario PASSED                [100%]

=========================================== 6 passed in 0.03s ===========================================

```
