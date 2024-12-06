"""
Módulo: Analizador de líneas de código

Este módulo proporciona una herramienta para analizar un archivo fuente en 
Python y contar las líneas de código en dos categorías:
- Líneas físicas: cuenta las líneas de código, excluyendo comentarios y 
  líneas en blanco.
- Líneas lógicas: cuenta los bloques lógicos, como clases, funciones, bucles,
  condicionales, etc.

La clase `AnalizadorDeCodigo` procesa el archivo línea por línea, identifica 
los comentarios, las líneas en blanco y los bloques lógicos, y calcula los 
totales correspondientes. Además, maneja errores de archivo y codificación.

Funciones principales:
- `AnalizadorDeCodigo`: Clase encargada del análisis de líneas físicas y lógicas
   en archivos Python.
- `analizar_archivo`: Procesa el archivo fuente y cuenta las líneas físicas y 
   lógicas.
- `informe`: Muestra un resumen del análisis con el conteo de líneas lógicas y 
   físicas.
"""

class AnalizadorDeCodigo:
    """
    Clase para analizar archivos Python y contar líneas físicas y lógicas.

    Attributes:
        ruta_del_archivo (str): Ruta del archivo a analizar.
        lineas_fisicas (int): Contador de líneas físicas.
        lineas_logicas (int): Contador de líneas lógicas.
    """

    def __init__(self, ruta_del_archivo):
        """
        Inicializa el analizador con la ruta del archivo.

        Args:
            ruta_del_archivo (str): Ruta del archivo a analizar.
        """
        self.ruta_del_archivo = ruta_del_archivo
        self.lineas_fisicas = 0
        self.lineas_logicas = 0
        self.palabras_clave_logicas = ['if', 'for', 'while', 
                                       'def', 'class', 'try', 'with']
        # Indicador de error
        self.error = False  
        # Mensaje de error
        self.error_mensaje = ""  

    def analizar_archivo(self):
        """
        Analiza un archivo fuente para contar líneas físicas y lógicas.

        Procesa línea por línea el archivo especificado, ignorando comentarios
        y líneas en blanco. Los comentarios en bloque también se excluyen.

        Excepciones:
            FileNotFoundError: Si el archivo no existe.
            IOError: Si hay un problema al leer el archivo.
        """
        comentario_bloque = False
        try:
            with open(self.ruta_del_archivo, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    linea_sin_espacios = linea.strip()

                    # Manejo de comentarios en bloque
                    if '"""' in linea_sin_espacios or "'''" in linea_sin_espacios:
                        if linea_sin_espacios.count('"""') == 2 \
                            or linea_sin_espacios.count("'''") == 2:
                            continue
                        comentario_bloque = not comentario_bloque
                        continue
                    # Manejo de líneas en blanco y comentarios normales
                    if comentario_bloque or not linea_sin_espacios \
                        or linea_sin_espacios.startswith('#'):
                        continue

                    self.lineas_fisicas += 1

                    primera_palabra = linea_sin_espacios.split()[0]
                    if primera_palabra.rstrip(':') in self.palabras_clave_logicas:
                        self.lineas_logicas += 1

        except FileNotFoundError as e:
            self.error = True
            self.error_mensaje = f"Archivo no encontrado: {e}"
        except IOError as e:
            self.error = True
            self.error_mensaje = f"Error de E/S: {e}"
        except UnicodeDecodeError as e:
            self.error = True
            self.error_mensaje = f"Error de codificación: {e}"

    def informe(self):
        """
        Retorna un resumen tabular del análisis del archivo.

        Retorna:
            El conteo de las líneas de código físicas y lógicas.
        """
        if not self.error:
            print("-" * 60)
            print(f"{'Programa':<30} | {'LOC Lógicas':<11} | {'LOC Físicas':<11}")
            print(f"{self.ruta_del_archivo:<30} | {self.lineas_logicas:<11} | {self.lineas_fisicas:<11}")
        else:
            print(f"El análisis no pudo completarse. Motivo: {self.error_mensaje}")


if __name__ == "__main__":
    ruta_del_archivo = './pruebas/Prueba_M.py'
    analizador = AnalizadorDeCodigo(ruta_del_archivo)
    analizador.analizar_archivo()
    analizador.informe()
