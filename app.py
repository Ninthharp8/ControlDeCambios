"""
Programa: Analizador de Líneas de Código
Autor: Equipo 6
Fecha: 10 de noviembre del 2024
Descripción:
    Este programa solicita al usuario la ruta de una carpeta, busca todos los archivos Python
    (.py) en dicha carpeta, y analiza cada archivo para contar las líneas físicas y lógicas
    de código. Proporciona un informe con el conteo de las líneas de código físicas y lógicas.
"""

import Analizador_De_Codigo as LOC

def main():
    while True:
        print("\nBienvenido al analizador de códigos.\n")
        print("Por favor, asegúrate de haber anexado tus archivos a la carpeta "
              "de nombre 'analizador' para poder procesarlos.")
        print("Escribe los nombres de los archivos a analizar, separados por comas.")
        print("Ejemplo: Archivo_ABC.py, Archivo_XYZ.py")

        # Leer la entrada del usuario
        entrada = input("\nIngresa el nombre del archivo: ")

        # Convertir la entrada en una lista de nombres de archivos
        archivos = [archivo.strip() for archivo in entrada.split(',')]

        # Analizar cada archivo
        for archivo in archivos:
            file_path = './analizador/' + archivo
            try:
                analyzer = LOC.AnalizadorDeCodigo(file_path)
                analyzer.analizar_archivo()
                analyzer.informe()
            except FileNotFoundError:
                print(f"Error: El archivo {archivo} no se encontró en la carpeta ./pruebas/")
            except Exception as e:
                print(f"Error al procesar el archivo {archivo}: {e}")

        print("\nAnálisis completado.")

        # Preguntar si desea realizar otro análisis o salir
        continuar = input("¿Deseas analizar más archivos? (s/n): ").strip().lower()
        if continuar != 's':
            print("Gracias por usar el analizador de códigos. ¡Hasta luego!")
            break

if __name__ == "__main__":
    main()
