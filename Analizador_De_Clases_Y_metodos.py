import sys
import time
from Analizador_De_Codigo import AnalizadorDeCodigo  

class AnalizadorEstructural(AnalizadorDeCodigo):
    """
    Analiza un archivo Python para:
    - Contar las clases y métodos.
    - Verificar si el código sigue el paradigma POO.
    - Delegar el conteo de líneas físicas y lógicas al 'AnalizadorDeCodigo'.
    """

    def __init__(self, ruta_del_archivo):
        """
        Inicializa el analizador con la ruta del archivo.
        """
        self.ruta_del_archivo = ruta_del_archivo
        self.clases = {}
        self.metodos_fuera_clases = []
        self.codigo_fuera_clases = []  # Almacena líneas de código fuera de clases
        super().__init__(ruta_del_archivo) # Instancia del analizador de líneas

    def analizar_clases_y_metodos(self):
        """
        Analiza el archivo fuente para contar clases, métodos 
        y verificar la estructura POO.
        Delegamos el conteo de líneas al AnalizadorDeCodigo.
        """
        comentario_bloque = False
        clase_actual = None  # Almacena la clase en la que estamos actualmente
        indentacion_clase = None  # Almacena la indentación de la clase actual

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

                    if comentario_bloque or not linea_sin_espacios \
                        or linea_sin_espacios.startswith('#'):
                        continue

                    # Detección de clases
                    if linea_sin_espacios.startswith('class '):
                        clase_actual = linea_sin_espacios.split()[1].split('(')[0]
                        self.clases[clase_actual] = {'lineas': 0, 'metodos': 0}
                        indentacion_clase = len(linea) - len(linea.lstrip())
                        continue

                    # Detección de métodos
                    if linea_sin_espacios.startswith('def '):
                        metodo = linea_sin_espacios.split()[1].split('(')[0]
                        indentacion_metodo = len(linea) - len(linea.lstrip())

                        if clase_actual and indentacion_metodo > indentacion_clase:
                            self.clases[clase_actual]['metodos'] += 1
                        else:
                            self.metodos_fuera_clases.append(metodo)

                    # Detección de código fuera de clases
                    if not clase_actual:
                        if not any(linea_sin_espacios.startswith(palabra) \
                                for palabra in ['import', 'from', 'class', 'def']):
                            self.codigo_fuera_clases.append(linea_sin_espacios)

                    # Sumar líneas a la clase actual si existe
                    if clase_actual:
                        indentacion_actual = len(linea) - len(linea.lstrip())
                        if indentacion_actual > indentacion_clase:
                            self.clases[clase_actual]['lineas'] += 1
                        else:
                            clase_actual = None  # Salimos del contexto de la clase

        except FileNotFoundError as e:
            print(f"Archivo no encontrado: {e}")
            time.sleep(10)
            sys.exit(1)
        except IOError as e:
            print(f"Error de E/S: {e}")
            time.sleep(10)
            sys.exit(1)
        except UnicodeDecodeError as e:
            print(f"Error de codificación: {e}")
            time.sleep(10)
            sys.exit(1)
    
    def obtener_resultados(self):
        """
        Retorna los resultados del análisis en un diccionario.
        """
        super().analizar_archivo()
        self.analizar_clases_y_metodos()
        self.verificar_poo()

        return {
            "clases": self.clases,
            "lineas_fisicas": self.lineas_fisicas,
            "lineas_logicas": self.lineas_logicas,
            "total_clases": len(self.clases),
        }

    def verificar_poo(self):
        """
        Verifica si el script sigue estrictamente el paradigma POO.
        Si no lo cumple, muestra un mensaje y sale del programa.
        """
        if self.metodos_fuera_clases or self.codigo_fuera_clases:
            print("\nERROR: El archivo **NO** sigue "\
                  "estrictamente el paradigma POO.")
            print("El programa se cerrara despues de este mensaje")
            print("Causas detectadas:")
            if self.metodos_fuera_clases:
                print(f"  - Métodos fuera de clases: \
                      {', '.join(self.metodos_fuera_clases)}")
            if self.codigo_fuera_clases:
                print("  - Código ejecutable fuera de clases:")
                for linea in self.codigo_fuera_clases:
                    print(f"    {linea}")
            time.sleep(15)
            sys.exit(1)

    def informe(self):
        """
        Muestra un informe del análisis y verifica si es POO.
        """
        resultados = self.obtener_resultados()
        print("-" * 60)
        print(f"{'Clases ':<30} | {'Métodos':<11} | {'Líneas':<11}")
        print("-" * 60)
        for clase, datos in resultados["clases"].items():
            print(f"{clase:<30} | {datos['metodos']:<11} | {datos['lineas']:<11}")
        print("-" * 60)
        print(f"{'Total líneas físicas':<30} | {resultados['lineas_fisicas']:<11}")
        print(f"{'Total líneas lógicas':<30} | {resultados['lineas_logicas']:<11}")
        print(f"{'Total de clases':<30} | {resultados['total_clases']:<11}")


if __name__ == "__main__":
    ruta_del_archivo = './Test/test_archivo_integral.py'
    analizador = AnalizadorEstructural(ruta_del_archivo)
    analizador.informe()        
