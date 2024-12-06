import unittest
from unittest.mock import patch, MagicMock
import os
import tempfile
from app import App  # Ajustar si el archivo tiene otro nombre o ruta

class TestApp(unittest.TestCase):
    def setUp(self):
        # Crear carpeta temporal para pruebas
        self.temp_dir = tempfile.TemporaryDirectory()
        self.app = App(carpeta=self.temp_dir.name)

        # Crear archivos temporales de prueba
        self.file1 = os.path.join(self.temp_dir.name, "test1.py")
        self.file2 = os.path.join(self.temp_dir.name, "test2.py")
        with open(self.file1, "w") as f:
            f.write("def func1(): pass\nclass Test1: pass")
        with open(self.file2, "w") as f:
            f.write("def func2(): pass\nclass Test2: pass")

    def tearDown(self):
        # Eliminar carpeta temporal
        self.temp_dir.cleanup()

    @patch('app.AnalizadorEstructural')
    @patch('app.ComparadorArchivos')
    @patch('builtins.input', side_effect=["test1.py, test2.py", "no"])
    def test_ejecutar(self, mock_input, MockComparador, MockAnalizador):
        # Configurar los mocks para los análisis y comparación
        analizador_mock = MagicMock()
        MockAnalizador.return_value = analizador_mock
        comparador_mock = MagicMock()
        MockComparador.return_value = comparador_mock

        # Ejecutar el flujo principal
        self.app.ejecutar()

        # Verificar que los análisis fueron llamados con los archivos correctos
        MockAnalizador.assert_any_call(self.file1)
        MockAnalizador.assert_any_call(self.file2)
        MockComparador.assert_called_once_with(self.file1, self.file2)

        # Verificar que se llamaron los métodos esperados
        analizador_mock.obtener_resultados.assert_called()
        analizador_mock.informe.assert_called()
        comparador_mock.comparar_archivos.assert_called_once()

if __name__ == '__main__':
    unittest.main()
