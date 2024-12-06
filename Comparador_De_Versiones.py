"""
Módulo : Comparador De versiones

Este modulo implementa la soluciopa para leer dos archivos de python y comparar
ambos archivos  de texto  para identificar y señalar  las lineas que han sido 
modificadas,  añadidas,  eliminadas,  cambiadas y  generar además de formatear 
aquellas lineas  que sobrepasan  los 80 carcateres para por ultimo generar dos 
archivos nuevos con ambas versiones del codigo pero formateados y etiquetados 
con los cambios en las lineas detectados. 


Este módulo contiene varias clases para leer archivos, comparar líneas entre 
archivos y detectar cambios,  incluyendo  diferencias  menores  entre líneas. 
Los cambios detectados se categorizan  en  líneas  añadidas, eliminadas, sin 
cambios y con cambios pequeños. Posteriormente, se generan reportes con los 
resultados de la comparación, donde se etiquetan las líneas modificadas.

Clases:
    - LectorArchivos: Lee las líneas de un archivo omitiendo las vacías.
    - ComparadorLineas: Compara las líneas de dos archivos y detecta cambios.
    - ReportadorCambios: Genera un reporte con los cambios detectados entre dos
      archivos.
    - ComparadorArchivos: Gestiona la comparación de dos archivos y la 
      generación de reportes.

Uso:
    Se puede utilizar el módulo para comparar dos archivos de texto, detectar 
    las diferencias y generar reportes con las líneas modificadas, añadidas o 
    eliminadas, así como los detalles de cambios pequeños.
"""

class LectorArchivos:
    """
    Clase para leer las líneas de un archivo omitiendo aquellas que están vacías.

    Attributes:
        ruta_archivo (str): Ruta al archivo a procesar.
    """
    def __init__(self, ruta_archivo):
        """
        Inicializa la clase con la ruta del archivo.

        Args:
            ruta_archivo (str): Ruta al archivo que se va a leer.
        """
        self.ruta_archivo = ruta_archivo

    def leer_lineas(self):
        """
        Lee todas las líneas de un archivo, omitiendo aquellas que están en blanco.

        Returns:
            list: Una lista con las líneas no vacías del archivo.
        """
        with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
            lineas = [linea.rstrip() for linea in archivo if linea.strip()]
        return lineas


class ComparadorLineas:
    """
    Clase para comparar las líneas de dos listas de texto y detectar cambios.

    Attributes:
        lineas_original (list): Líneas del archivo original.
        lineas_modificado (list): Líneas del archivo modificado.
    """
    def __init__(self, lineas_original, lineas_modificado):
        """
        Inicializa la clase con las líneas de los archivos original y modificado.

        Args:
            lineas_original (list): Líneas del archivo original.
            lineas_modificado (list): Líneas del archivo modificado.
        """
        self.lineas_original = lineas_original
        self.lineas_modificado = lineas_modificado

    def _lcs(self):
        """
        Calcula la subsecuencia común más larga (LCS) entre dos listas de líneas.

        Returns:
            list: La subsecuencia común más larga entre las dos listas.
        """
        m, n = len(self.lineas_original), len(self.lineas_modificado)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.lineas_original[i - 1] == self.lineas_modificado[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        i, j = m, n
        lcs = []
        while i > 0 and j > 0:
            if self.lineas_original[i - 1] == self.lineas_modificado[j - 1]:
                lcs.append(self.lineas_original[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return lcs[::-1]

    def detectar_cambios_pequeños(self, linea1, linea2):
        """
        Detecta diferencias carácter por carácter entre dos líneas.

        Args:
            linea1 (str): Línea del archivo original.
            linea2 (str): Línea del archivo modificado.

        Returns:
            list: Lista de tuplas con diferencias (carácter_original, carácter_modificado).
        """
        diferencias = []
        for c1, c2 in zip(linea1, linea2):
            if c1 != c2:
                diferencias.append((c1, c2))
        if len(linea1) > len(linea2):
            diferencias.extend((c, None) for c in linea1[len(linea2):])
        elif len(linea2) > len(linea1):
            diferencias.extend((None, c) for c in linea2[len(linea1):])
        return diferencias

    def comparar_lineas(self):
        """
        Compara las líneas de los dos archivos y categoriza los cambios.

        Returns:
            tuple: Contiene cuatro elementos:
                - Líneas añadidas.
                - Líneas eliminadas.
                - Líneas sin cambios.
                - Líneas con cambios pequeños (detalladas).
        """
        lcs = self._lcs()

        lineas_sin_cambios = lcs
        lineas_añadidas = [linea for linea in self.lineas_modificado if linea not in lcs]
        lineas_eliminadas = [linea for linea in self.lineas_original if linea not in lcs]

        lineas_con_cambios_pequeños = []
        for linea_modificada in lineas_añadidas[:]:
            for linea_original in lineas_eliminadas[:]:
                diferencias = self.detectar_cambios_pequeños(linea_original, linea_modificada)
                if len(diferencias) > 0 and len(diferencias) < max(len(linea_original), len(linea_modificada)) // 2:
                    lineas_con_cambios_pequeños.append((linea_original, linea_modificada, diferencias))
                    lineas_añadidas.remove(linea_modificada)
                    lineas_eliminadas.remove(linea_original)
                    break

        return (lineas_añadidas, lineas_eliminadas, lineas_sin_cambios, lineas_con_cambios_pequeños)


class ReportadorCambios:
    """
    Clase para generar reportes de los cambios detectados entre dos archivos.

    Attributes:
        lineas_añadidas (list): Líneas añadidas en el archivo modificado.
        lineas_eliminadas (list): Líneas eliminadas del archivo original.
        lineas_cambios_pequeños (list): Líneas con cambios menores detectados.
    """
    def __init__(self, lineas_añadidas, lineas_eliminadas, lineas_cambios_pequeños):
        """
        Inicializa el reportador con los cambios detectados.

        Args:
            lineas_añadidas (list): Líneas añadidas en el archivo modificado.
            lineas_eliminadas (list): Líneas eliminadas del archivo original.
            lineas_cambios_pequeños (list): Líneas con cambios menores detectados.
        """
        self.lineas_añadidas = lineas_añadidas
        self.lineas_eliminadas = lineas_eliminadas
        self.lineas_cambios_pequeños = lineas_cambios_pequeños

    def _formatear_cambios_pequeños(self, original, modificado, diferencias):
        """
        Formatea los cambios pequeños detectados entre dos líneas.

        Args:
            original (str): Línea original.
            modificado (str): Línea modificada.
            diferencias (list): Diferencias detectadas carácter por carácter.

        Returns:
            str: Texto formateado que describe los cambios.
        """
        partes_original = []
        partes_modificado = []

        for c1, c2 in diferencias:
            if c1 is None:
                partes_modificado.append(c2)
            elif c2 is None:
                partes_original.append(c1)
            elif c1 != c2:
                partes_original.append(c1)
                partes_modificado.append(c2)

        texto_original = "".join(partes_original)
        texto_modificado = "".join(partes_modificado)

        return f"'{texto_original}' -> '{texto_modificado}'"

    def _formatear_linea(self, linea, etiqueta=None):
        """
        Formatea una línea, añadiendo etiquetas de cambios si corresponde.

        Args:
            linea (str): Línea a formatear.
            etiqueta (str, optional): Etiqueta de cambio asociada a la línea.

        Returns:
            str: Línea formateada con etiquetas.
        """
        max_len = 80
        es_comentario = linea.strip().startswith("#")

        if len(linea) <= max_len:
            return linea if etiqueta is None else f"{linea}  {etiqueta}"

        partes = []
        while len(linea) > max_len:
            corte_seguro = linea.rfind(' ', 0, max_len)
            if corte_seguro == -1:
                corte_seguro = max_len

            segmento = linea[:corte_seguro].rstrip()
            if es_comentario:
                partes.append(segmento)
                linea = f"# {linea[corte_seguro:].lstrip()}"
            else:
                if not segmento.endswith(('\\', ',', '(', '[', '{', '+', '-', '*', '/')):
                    segmento += " \\"
                partes.append(segmento)
                linea = linea[corte_seguro:].lstrip()

        partes.append(linea)
        resultado = "\n".join(partes)
        return resultado if etiqueta is None else f"{resultado}  {etiqueta}"

    def reportar_cambios(self, archivo_original, archivo_modificado):
        """
        Genera un reporte de los cambios y actualiza los archivos originales y modificados.

        Args:
            archivo_original (str): Ruta del archivo original.
            archivo_modificado (str): Ruta del archivo modificado.
        """
        with open(archivo_original, 'r', encoding='utf-8') as archivo:
            lineas_original = [linea.rstrip() for linea in archivo]

        with open(archivo_modificado, 'r', encoding='utf-8') as archivo:
            lineas_modificado = [linea.rstrip() for linea in archivo]

        with open(f"{archivo_original}_actualizado.py", 'w', encoding='utf-8') as archivo:
            for linea in lineas_original:
                etiqueta = None
                if linea in self.lineas_eliminadas:
                    etiqueta = "# Línea eliminada"
                elif any(linea == original for original, _, _ in self.lineas_cambios_pequeños):
                    etiqueta = "# Línea modificada (ver archivo modificado)"
                archivo.write(self._formatear_linea(linea, etiqueta) + "\n")

        with open(f"{archivo_modificado}_actualizado.py", 'w', encoding='utf-8') as archivo:
            for linea in lineas_modificado:
                etiqueta = None
                if linea in self.lineas_añadidas:
                    etiqueta = "# Línea añadida"
                elif any(linea == modificado for _, modificado, _ in self.lineas_cambios_pequeños):
                    original, modificado, diferencias = next(
                        (original, modificado, diferencias)
                        for original, modificado, diferencias in self.lineas_cambios_pequeños
                        if modificado == linea
                    )
                    diferencias_formateadas = self._formatear_cambios_pequeños(original, modificado, diferencias)
                    etiqueta = f"# Cambios: {diferencias_formateadas}"
                archivo.write(self._formatear_linea(linea, etiqueta) + "\n")


class ComparadorArchivos:
    """
    Clase principal para gestionar la comparación de archivos y generar reportes.

    Attributes:
        archivo_original (str): Ruta al archivo original.
        archivo_modificado (str): Ruta al archivo modificado.
    """
    def __init__(self, archivo_original, archivo_modificado):
        """
        Inicializa la clase con las rutas de los archivos.

        Args:
            archivo_original (str): Ruta al archivo original.
            archivo_modificado (str): Ruta al archivo modificado.
        """
        self.archivo_original = archivo_original
        self.archivo_modificado = archivo_modificado
    
    def comparar_archivos(self):
        """
        Compara los archivos, detecta cambios y genera reportes actualizados.
        """
        lector_original = LectorArchivos(self.archivo_original)
        lector_modificado = LectorArchivos(self.archivo_modificado)

        lineas_original = lector_original.leer_lineas()
        lineas_modificado = lector_modificado.leer_lineas()

        comparador = ComparadorLineas(lineas_original, lineas_modificado)
        
        (lineas_añadidas, lineas_eliminadas, 
        lineas_sin_cambios, 
        lineas_con_cambios_pequeños) = comparador.comparar_lineas()

        print(f"Líneas añadidas: {len(lineas_añadidas)}")
        print(f"Líneas eliminadas: {len(lineas_eliminadas)}")
        print(f"Líneas sin cambios: {len(lineas_sin_cambios)}")
        print(f"Líneas con cambios pequeños: {len(lineas_con_cambios_pequeños)}")

        reportador = ReportadorCambios(lineas_añadidas, lineas_eliminadas, lineas_con_cambios_pequeños)
        reportador.reportar_cambios(self.archivo_original, self.archivo_modificado)


if __name__ == "__main__":
    """
    Punto de entrada principal del programa. Compara dos archivos especificados y genera un reporte.
    """
    ruta_archivo_original = "./analizador/Comparador_De_Versiones.py"
    ruta_archivo_modificado = "./analizador/Comparador_De_Versiones_Copy.py"

    comparador = ComparadorArchivos(ruta_archivo_original, ruta_archivo_modificado)
    comparador.comparar_archivos()
