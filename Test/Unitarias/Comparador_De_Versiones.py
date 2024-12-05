
class LectorArchivos:
    """Lee las líneas de un archivo omitiendo espacios en blanco."""
    def __init__(self, ruta_archivo):
        self.ruta_archivo = ruta_archivo

    def leer_lineas(self):
        """Lee el archivo, omite líneas en blanco y devuelve las líneas."""
        with open(self.ruta_archivo, 'r', encoding='utf-8') as archivo:
            lineas = [linea.rstrip() for linea in archivo if linea.strip()]
        return lineas


class ComparadorLineas:
    """Compara las líneas de dos archivos y detecta cambios."""
    def __init__(self, lineas_original, lineas_modificado):
        self.lineas_original = lineas_original
        self.lineas_modificado = lineas_modificado

    def _lcs(self):
        """Encuentra la subsecuencia común más larga (LCS) entre las líneas."""
        m, n = len(self.lineas_original), len(self.lineas_modificado)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Llenar la tabla LCS
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if self.lineas_original[i - 1] == self.lineas_modificado[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Reconstruir la subsecuencia común
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
        """Compara dos líneas y detecta diferencias carácter por carácter."""
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
        """Detecta líneas añadidas, eliminadas y con cambios pequeños."""
        lcs = self._lcs()

        lineas_sin_cambios = lcs
        lineas_añadidas = [linea for linea in self.lineas_modificado if linea not in lcs]
        lineas_eliminadas = [linea for linea in self.lineas_original if linea not in lcs]
        #lineas_movidas = [linea for linea in lcs if self.lineas_original.index(linea) != self.lineas_modificado.index(linea)]

        # Detectar cambios pequeños
        lineas_con_cambios_pequeños = []
        for linea_modificada in lineas_añadidas[:]:
            for linea_original in lineas_eliminadas[:]:
                diferencias = self.detectar_cambios_pequeños(linea_original, linea_modificada)
                if len(diferencias) > 0 and len(diferencias) < max(len(linea_original), len(linea_modificada)) // 2:
                    lineas_con_cambios_pequeños.append((linea_original, linea_modificada, diferencias))
                    lineas_añadidas.remove(linea_modificada)
                    lineas_eliminadas.remove(linea_original)
                    break

        return lineas_añadidas, lineas_eliminadas, lineas_sin_cambios, lineas_con_cambios_pequeños

class ReportadorCambios:
    def __init__(self, lineas_añadidas, lineas_eliminadas, lineas_cambios_pequeños):
        self.lineas_añadidas = lineas_añadidas
        self.lineas_eliminadas = lineas_eliminadas
        self.lineas_cambios_pequeños = lineas_cambios_pequeños

    def _formatear_cambios_pequeños(self, original, modificado, diferencias):
        """Formatea y muestra las diferencias entre dos líneas con cambios pequeños."""
        partes_original = []
        partes_modificado = []
        
        for c1, c2 in diferencias:
            if c1 is None:  # Caracter nuevo en el modificado
                partes_modificado.append(c2)
            elif c2 is None:  # Caracter eliminado del original
                partes_original.append(c1)
            elif c1 != c2:  # Caracter cambiado
                partes_original.append(c1)
                partes_modificado.append(c2)

        texto_original = "".join(partes_original)
        texto_modificado = "".join(partes_modificado)
        
        return f"'{original}' -> '{modificado}'"

    def _formatear_linea(self, linea, etiqueta=None):
        """
        Divide una línea que exceda los 80 caracteres en segmentos seguros:
        - Para comentarios (`#`), cada línea dividida comienza con `#`.
        - Para código, las líneas divididas terminan con diagonal (excepto la última).
        """
        max_len = 80
        es_comentario = linea.strip().startswith("#")
        
        if len(linea) <= max_len:
            return linea if etiqueta is None else f"{linea}  {etiqueta}"

        partes = []
        while len(linea) > max_len:
            # Buscar el último espacio antes del límite
            corte_seguro = linea.rfind(' ', 0, max_len)
            if corte_seguro == -1:  # Si no hay espacio, forzar corte en el límite
                corte_seguro = max_len

            # Dividir la línea en el punto seguro
            segmento = linea[:corte_seguro].rstrip()
            if es_comentario:
                partes.append(segmento)
                linea = f"# {linea[corte_seguro:].lstrip()}"  # Mantener formato de comentario
            else:
                if not segmento.endswith(('\\', ',', '(', '[', '{', '+', '-', '*', '/')):
                    segmento += " \\"
                partes.append(segmento)
                linea = linea[corte_seguro:].lstrip()

        partes.append(linea)  # Agregar la última parte
        resultado = "\n".join(partes)
        return resultado if etiqueta is None else f"{resultado}  {etiqueta}"

    def reportar_cambios(self, archivo_original, archivo_modificado):
        """Escribe comentarios en los archivos originales y modificados."""
        with open(archivo_original, 'r', encoding='utf-8') as archivo:
            lineas_original = [linea.rstrip() for linea in archivo]

        with open(archivo_modificado, 'r', encoding='utf-8') as archivo:
            lineas_modificado = [linea.rstrip() for linea in archivo]

        # Etiquetar en el archivo original
        with open(f"{archivo_original}_actualizado.py", 'w', encoding='utf-8') as archivo:
            for linea in lineas_original:
                etiqueta = None
                if linea in self.lineas_eliminadas:
                    etiqueta = "# Línea eliminada"
                elif any(linea == original for original, _, _ in self.lineas_cambios_pequeños):
                    etiqueta = "# Línea modificada (ver archivo modificado)"
                archivo.write(self._formatear_linea(linea, etiqueta) + "\n")

        # Etiquetar en el archivo modificado
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
    """Clase principal que gestiona la comparación de archivos."""
    def __init__(self, archivo_original, archivo_modificado):
        self.archivo_original = archivo_original
        self.archivo_modificado = archivo_modificado
    
    def comparar_archivos(self):
        """Realiza la comparación completa de los archivos."""
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


# Ejecución del programa con los archivos proporcionados
if __name__ == "__main__":
    ruta_archivo_original = "./Caso_6/Formateo_Original.py"
    ruta_archivo_modificado = "./Caso_6/Formateo_Modificado.py"

    comparador = ComparadorArchivos(ruta_archivo_original, ruta_archivo_modificado)
    comparador.comparar_archivos()


