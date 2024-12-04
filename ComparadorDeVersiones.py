import Analizador_De_Codigo as LOC
class ComparadorDeVersiones:
    def __init__(self, archivo_v1, archivo_v2):
        """
        Inicializa el comparador con las rutas de las versiones a comparar.

        Args:
            archivo_v1 (str): Ruta de la versión previa.
            archivo_v2 (str): Ruta de la nueva versión.
        """
        self.archivo_v1 = archivo_v1
        self.archivo_v2 = archivo_v2
        self.lineas_v1 = self.leer_y_formatear(archivo_v1)
        self.lineas_v2 = self.leer_y_formatear(archivo_v2)
        self.lineas_añadidas = []
        self.lineas_borradas = []
        self.lineas_modificadas = []

    def leer_y_formatear(self, ruta):
        """
        Lee un archivo y divide las líneas mayores a 80 caracteres.

        Args:
            ruta (str): Ruta del archivo.

        Retorna:
            list: Lista de líneas formateadas.
        """
        lineas = []
        with open(ruta, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.rstrip()
                while len(linea) > 80:
                    lineas.append(linea[:80])
                    linea = linea[80:]
                lineas.append(linea)
        return lineas

    def comparar_versiones(self):
        """
        Compara las versiones de los archivos línea por línea.
        """
        # Crear conjuntos de líneas para comparación
        conjunto_v1 = set(self.lineas_v1)
        conjunto_v2 = set(self.lineas_v2)

        # Identificar líneas añadidas y borradas
        self.lineas_añadidas = list(conjunto_v2 - conjunto_v1)
        self.lineas_borradas = list(conjunto_v1 - conjunto_v2)

        # Comparar líneas para detectar modificaciones
        for linea_añadida in self.lineas_añadidas[:]:  # Copia temporal para iterar
            for linea_borrada in self.lineas_borradas[:]:
                if self.es_modificacion(linea_añadida, linea_borrada):
                    self.lineas_modificadas.append((linea_borrada, linea_añadida))
                    self.lineas_borradas.remove(linea_borrada)
                    self.lineas_añadidas.remove(linea_añadida)
                    break

    def es_modificacion(self, linea_nueva, linea_antigua):
        """
        Determina si dos líneas son una pequeña modificación basándose en la
        distancia de edición simple.

        Args:
            linea_nueva (str): Línea nueva.
            linea_antigua (str): Línea antigua.

        Retorna:
            bool: True si son similares, False si son completamente diferentes.
        """
        return self.similitud_basica(linea_nueva, linea_antigua) > 0.7

    def similitud_basica(self, linea1, linea2):
        """
        Calcula la similitud entre dos líneas basado en el número de caracteres coincidentes.

        Args:
            linea1 (str): Primera línea.
            linea2 (str): Segunda línea.

        Retorna:
            float: Valor entre 0 y 1 indicando el grado de similitud.
        """
        coincidencias = sum(1 for a, b in zip(linea1, linea2) if a == b)
        return coincidencias / max(len(linea1), len(linea2))

    def generar_informe(self):
        """
        Genera un informe del análisis de diferencias entre las versiones.
        """
        print("Informe de cambios entre versiones:")
        print(f"Líneas añadidas: {len(self.lineas_añadidas)}")
        for linea in self.lineas_añadidas:
            print(f" + {linea}  # LÍNEA NUEVA")
        
        print(f"\nLíneas borradas: {len(self.lineas_borradas)}")
        for linea in self.lineas_borradas:
            print(f" - {linea}  # LÍNEA BORRADA")
        
        print(f"\nLíneas modificadas: {len(self.lineas_modificadas)}")
        for original, nueva in self.lineas_modificadas:
            print(f" * {original}  → {nueva}  # MODIFICADA")


# Uso del comparador
if __name__ == "__main__":
    archivo_v1 = './version1.py'
    archivo_v2 = './version2.py'
    archivo_analizado1 = LOC.AnalizadorDeCodigo(archivo_v1)
    archivo_analizado2 = LOC.AnalizadorDeCodigo(archivo_v2)

    comparador = ComparadorDeVersiones(archivo_v1, archivo_v2)
    comparador.comparar_versiones()
    comparador.generar_informe()
    archivo_analizado1.analizar_archivo()
    archivo_analizado1.informe()
    archivo_analizado2.analizar_archivo()
    archivo_analizado2.informe()
