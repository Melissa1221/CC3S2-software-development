# Actividad: Objetos mocking

**Paso 1: Preparando el entorno**
Primero creé la carpeta correspondiente a la actividad (activity13), luego creé y activé el entorno virtual en el cual se instalarán las dependencias requeridas para este caso:
```
python -m venv venv
source venv/bin/activate  # uso arch linux en wsl
```

También creé un archivo .gitignore para excluir archivos no deseados:
```
venv/
__pycache__/
.pytest_cache
```

**Paso 2: Instalando las dependencias**
El proyecto requiere la biblioteca `requests` para hacer llamadas a APIs externas y `pytest` para ejecutar las pruebas:
```
pip install pytest requests
```

**Paso 3: Entendiendo la estructura del proyecto**
El proyecto consta de:
- `models/imdb.py`: Contiene la clase IMDb que implementa tres métodos para interactuar con la API de IMDb: `search_titles()`, `movie_reviews()` y `movie_ratings()`.
- `tests/test_imbd.py`: Contiene las pruebas unitarias para la clase IMDb.
- `tests/fixtures/imdb_responses.json`: Contiene respuestas simuladas de la API de IMDb para usar en las pruebas.

**Paso 4: Implementando las pruebas con mocking**
El proceso de implementación de pruebas siguió estos pasos:

1. **Prueba de búsqueda por título (test_search_titles_success)**
   
   Primero implementé una prueba para verificar que la búsqueda de títulos funciona correctamente. Utilicé el decorador `@patch` para interceptar la llamada a `requests.get` y configurar un objeto Mock que simula una respuesta exitosa:
   
   ```python
   @patch('models.imdb.requests.get')
   def test_search_titles_success(self, mock_get):
       """Prueba que la búsqueda de títulos retorna datos correctamente"""
       mock_response = Mock(spec=Response)
       mock_response.status_code = 200
       mock_response.json.return_value = self.imdb_data['search_title']
       mock_get.return_value = mock_response

       imdb = IMDb(apikey="fake_api_key")
       resultado = imdb.search_titles("Bambi")

       assert resultado == self.imdb_data['search_title']
       mock_get.assert_called_once_with("https://imdb-api.com/API/SearchTitle/fake_api_key/Bambi")
   ```

2. **Prueba de búsqueda sin resultados (test_search_titles_failure)**
   
   Implementé una prueba para el "camino triste" donde la búsqueda no encuentra resultados, simulando un código de estado 404:
   
   ```python
   @patch('models.imdb.requests.get')
   def test_search_titles_failure(self, mock_get):
       """Prueba que la búsqueda de títulos maneja errores correctamente"""
       mock_response = Mock(spec=Response)
       mock_response.status_code = 404
       mock_response.json.return_value = {}
       mock_get.return_value = mock_response

       imdb = IMDb(apikey="fake_api_key")
       resultado = imdb.search_titles("TituloInexistente")

       assert resultado == {}
       mock_get.assert_called_once_with("https://imdb-api.com/API/SearchTitle/fake_api_key/TituloInexistente")
   ```

3. **Prueba de búsqueda por título fallida (test_search_by_title_failed)**
   
   Implementé un caso de prueba para simular una clave API inválida, donde la API responde con un código 200 pero incluye un mensaje de error:
   
   ```python
   @patch('models.imdb.requests.get')
   def test_search_by_title_failed(self, mock_get):
       """Prueba de búsqueda por título fallida"""
       mock_response = Mock(
           spec=Response,
           status_code=200,
           json=Mock(return_value=self.imdb_data["INVALID_API"])
       )
       mock_get.return_value = mock_response

       imdb = IMDb(apikey="bad-key")
       resultados = imdb.search_titles("Bambi")

       assert resultados is not None
       assert resultados["errorMessage"] == "Invalid API Key"
   ```

4. **Prueba de calificaciones de películas (test_movie_ratings_good)**
   
   Finalmente, implementé una prueba para verificar la funcionalidad de obtener calificaciones de películas, mockeando la respuesta para incluir datos específicos:
   
   ```python
   @patch('models.imdb.requests.get')
   def test_movie_ratings_good(self, mock_get):
       """Prueba de calificaciones de películas con buenas calificaciones"""
       mock_response = Mock(
           spec=Response,
           status_code=200,
           json=Mock(return_value=self.imdb_data["movie_ratings"])
       )
       mock_get.return_value = mock_response

       imdb = IMDb(apikey="fake_api_key")
       resultados = imdb.movie_ratings("tt1375666")

       assert resultados is not None
       assert resultados["title"] == "Bambi"
       assert resultados["filmAffinity"] == 3
       assert resultados["rottenTomatoes"] == 5
   ```


EL archivo final es el siguiente
```py
"""
Casos de prueba para el mocking
"""
import os
import json
import pytest
import sys

# Agregar el directorio raíz al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch, Mock
from requests import Response
from models import IMDb

# Fixture para cargar los datos de IMDb desde un archivo JSON
@pytest.fixture(scope="session")
def imdb_data():
    """Carga las respuestas de IMDb necesarias para las pruebas"""
    current_dir = os.path.dirname(__file__)
    fixture_path = os.path.join(current_dir, 'fixtures', 'imdb_responses.json')
    with open(fixture_path) as json_data:
        data = json.load(json_data)
        print("Contenido de imdb_data:", data)  # Para depuración
        return data

class TestIMDbDatabase:
    """Casos de prueba para la base de datos de IMDb"""

    @pytest.fixture(autouse=True)
    def setup_class(self, imdb_data):
        """Configuración inicial para cargar los datos de IMDb"""
        self.imdb_data = imdb_data

    ######################################################################
    #  Casos de prueba
    ######################################################################

    @patch('models.imdb.requests.get')
    def test_search_titles_success(self, mock_get):
        """Prueba que la búsqueda de títulos retorna datos correctamente"""
        # Configurar el mock para devolver una respuesta exitosa
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = self.imdb_data['search_title']
        mock_get.return_value = mock_response

        imdb = IMDb(apikey="fake_api_key")
        resultado = imdb.search_titles("Bambi")

        assert resultado == self.imdb_data['search_title']
        mock_get.assert_called_once_with("https://imdb-api.com/API/SearchTitle/fake_api_key/Bambi")

    @patch('models.imdb.requests.get')
    def test_search_titles_failure(self, mock_get):
        """Prueba que la búsqueda de títulos maneja errores correctamente"""
        # Configurar el mock para devolver una respuesta fallida con json retornando {}
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        imdb = IMDb(apikey="fake_api_key")
        resultado = imdb.search_titles("TituloInexistente")

        assert resultado == {}
        mock_get.assert_called_once_with("https://imdb-api.com/API/SearchTitle/fake_api_key/TituloInexistente")

    @patch('models.imdb.requests.get')
    def test_movie_reviews_success(self, mock_get):
        """Prueba que la obtención de reseñas retorna datos correctamente"""
        # Configurar el mock para devolver una respuesta exitosa
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = self.imdb_data['movie_reviews']
        mock_get.return_value = mock_response

        imdb = IMDb(apikey="fake_api_key")
        resultado = imdb.movie_reviews("tt1375666")

        assert resultado == self.imdb_data['movie_reviews']
        mock_get.assert_called_once_with("https://imdb-api.com/API/Reviews/fake_api_key/tt1375666")

    @patch('models.imdb.requests.get')
    def test_movie_ratings_success(self, mock_get):
        """Prueba que la obtención de calificaciones retorna datos correctamente"""
        # Configurar el mock para devolver una respuesta exitosa
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = self.imdb_data['movie_ratings']
        mock_get.return_value = mock_response

        imdb = IMDb(apikey="fake_api_key")
        resultado = imdb.movie_ratings("tt1375666")

        assert resultado == self.imdb_data['movie_ratings']
        mock_get.assert_called_once_with("https://imdb-api.com/API/Ratings/fake_api_key/tt1375666")

    @patch('models.imdb.requests.get')
    def test_search_by_title_failed(self, mock_get):
        """Prueba de búsqueda por título fallida"""
        # Configurar el mock para devolver una respuesta con API Key inválida
        mock_response = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=self.imdb_data["INVALID_API"])
        )
        mock_get.return_value = mock_response

        imdb = IMDb(apikey="bad-key")
        resultados = imdb.search_titles("Bambi")

        assert resultados is not None
        assert resultados["errorMessage"] == "Invalid API Key"

    @patch('models.imdb.requests.get')
    def test_movie_ratings_good(self, mock_get):
        """Prueba de calificaciones de películas con buenas calificaciones"""
        # Configurar el mock para devolver una respuesta exitosa con buenas calificaciones
        mock_response = Mock(
            spec=Response,
            status_code=200,
            json=Mock(return_value=self.imdb_data["movie_ratings"])
        )
        mock_get.return_value = mock_response

        imdb = IMDb(apikey="fake_api_key")
        resultados = imdb.movie_ratings("tt1375666")

        assert resultados is not None
        assert resultados["title"] == "Bambi"
        assert resultados["filmAffinity"] == 3
        assert resultados["rottenTomatoes"] == 5
```

**Paso 5: Ejecutando las pruebas**
Al ejecutar pytest después de todas las correcciones e implementaciones, todas las pruebas pasaron exitosamente:

![](https://i.imgur.com/uS9xGzy.png)


**Paso 7: Conclusiones sobre el mocking**
El mocking es una técnica poderosa que permite:
- Aislar el código que se está probando de sus dependencias externas
- Controlar el comportamiento de esas dependencias durante las pruebas
- Simular diferentes escenarios, incluyendo casos de éxito y error
- Acelerar las pruebas al evitar llamadas reales a servicios externos

La combinación de `@patch`, `Mock` y fixtures de prueba permite un control completo sobre el entorno de prueba, asegurando que solo se está probando el comportamiento del código propio, no el de servicios externos.
