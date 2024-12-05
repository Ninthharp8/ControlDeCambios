import  Comparador_De_Versiones as vs

class TestComparadorArchivos:
    """
    Clase que implementa pruebas automáticas del módulo Comparador_De_Versiones.

    Esta clase valida los resultados esperados de:
        - Líneas añadidas
        - Líneas eliminadas
        - Líneas sin cambios
        - Líneas movidas
        - Líneas con cambios pequeños
    """

    def __init__(self):
        # Ejecuta automáticamente las pruebas al instanciar la clase.
        self.test_caso1_identicos()
        self.test_caso2_linea_añadida()
        self.test_caso3_linea_borrada()
        self.test_caso4_linea_movida()
        self.test_formato_80_caracteres()
        
    def assertEqual(self, valor_obtenido, valor_esperado, mensaje):
        """
        Compara si dos valores son iguales; lanza un error si no lo son.
        """
        if valor_obtenido != valor_esperado:
            raise AssertionError(f"{mensaje}: obtenido {valor_obtenido}, esperado {valor_esperado}")
    
    def assertFormato80(self, lineas, mensaje):
        """
        Verifica que todas las líneas del archivo no excedan los 80 caracteres.
        """
        for i, linea in enumerate(lineas):
            if len(linea) > 80:
                raise AssertionError(f"{mensaje} - Línea {i+1} excede los 80 caracteres: {linea[:80]}...")

    def probar_comparacion(self, ruta_original, ruta_modificado, resultados_esperados):
        """
        Realiza la comparación de archivos y verifica los resultados.
        
        Parámetros:
        - ruta_original: Ruta del archivo original.
        - ruta_modificado: Ruta del archivo modificado.
        - resultados_esperados: Diccionario con las expectativas para la comparación.
        """
        lector_original = vs.LectorArchivos(ruta_original)
        lector_modificado = vs.LectorArchivos(ruta_modificado)

        lineas_original = lector_original.leer_lineas()
        lineas_modificado = lector_modificado.leer_lineas()

        comparador = vs.ComparadorLineas(lineas_original, lineas_modificado)
        (lineas_añadidas, lineas_eliminadas, 
        lineas_sin_cambios, 
        lineas_con_cambios_pequeños) = comparador.comparar_lineas()

        # Validación de resultados
        self.assertEqual(len(lineas_añadidas), resultados_esperados['añadidas'], "Líneas añadidas incorrectas")
        self.assertEqual(len(lineas_eliminadas), resultados_esperados['eliminadas'], "Líneas eliminadas incorrectas")
        self.assertEqual(len(lineas_sin_cambios), resultados_esperados['sin_cambios'], "Líneas sin cambios incorrectas")
        self.assertEqual(len(lineas_con_cambios_pequeños), resultados_esperados['cambios_pequeños'], "Líneas con cambios pequeños incorrectas")

    def test_caso1_identicos(self):
        """
        Prueba que archivos idénticos no tengan diferencias.
        """
        print("prueba para lineas sin cambios")
        self.probar_comparacion(
            ruta_original="./Caso_1/identico_original.py",
            ruta_modificado="./Caso_1/identico_modificado.py",
            resultados_esperados={
                'añadidas': 0,
                'eliminadas': 0,
                'sin_cambios': 5,
                'cambios_pequeños': 0
            }
        )

    def test_caso2_linea_añadida(self):
        """
        Prueba que se detecte correctamente una línea añadida.
        """
        print("prueba para detectar lineas añadidas")
        self.probar_comparacion(
            ruta_original="./Caso_2/lineas_añadidas_original.py",
            ruta_modificado="./Caso_2/lineas_añadidas_modificado.py",
            resultados_esperados={
                'añadidas': 2,
                'eliminadas': 0,
                'sin_cambios': 5,
                'cambios_pequeños': 0
            }
        )
    def test_caso3_linea_borrada(self):
        """
        Prueba que se detecte correctamente una línea borrada.
        """
        print("prueba para detectar lineas borradas")
        self.probar_comparacion(
            ruta_original="./Caso_3/Eliminadas_Original.py",
            ruta_modificado="./Caso_3/Eliminadas_Modificado.py",
            resultados_esperados={
                'añadidas': 0,
                'eliminadas': 9,
                'sin_cambios': 11,
                'cambios_pequeños': 0
            }
        )
    def test_caso4_linea_movida(self):
        """
        Prueba que se detecte correctamente una línea borrada.
        """
        print("prueba para detectar lineas movidas")
        self.probar_comparacion(
            ruta_original="./Caso_4/Movidas_original.py",
            ruta_modificado="./Caso_4/Movidas_Modificado.py",
            resultados_esperados={
                'añadidas': 1,
                'eliminadas': 1,
                'sin_cambios': 9,
                'cambios_pequeños': 0
            }
        )
    def test_caso5_cambios_pequeños(self):
        """
        Prueba que se detecte correctamente una línea borrada.
        """
        print("prueba para detectar lineas movidas")
        self.probar_comparacion(
            ruta_original="./Caso_4/Movidas_original.py",
            ruta_modificado="./Caso_4/Movidas_Modificado.py",
            resultados_esperados={
                'añadidas': 1,
                'eliminadas': 1,
                'sin_cambios': 9,
                'cambios_pequeños': 0
            }
        )
    
    def test_formato_80_caracteres(self):
        """
        Prueba que todos los archivos no excedan los 80 caracteres por línea.
        """
        print("prueba para verificar que se formatea el codigo y "
              "se cuentan todos los casos anteriores ")
        
        # Aquí asegúrate de tener los archivos que deseas verificar
        ruta_original = "./Caso_6/Formateo_Original.py"
        ruta_modificado="./Caso_6/Formateo_Modificado.py"
       
        self.probar_comparacion(
            ruta_original,
            ruta_modificado,
            resultados_esperados={
                'añadidas': 2,
                'eliminadas': 2,
                'sin_cambios': 8,
                'cambios_pequeños': 1
            }
        )

if __name__ == '__main__':
    try:
        TestComparadorArchivos()
        print("Todas las pruebas pasaron correctamente.")
    except AssertionError as e:
        print(f"Prueba fallida: {e}")
