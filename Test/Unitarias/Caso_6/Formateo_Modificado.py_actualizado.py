"""
Ejemplo de un codigo con mas de 80 caracteres en la linea, se debe formatear \
tanto codigo como comentarios. incluyendo este en dosctrig.
"""
class formato():

    # Este es un ejemplo de código que tiene líneas muy largas para probar el
# formato.
    def calcular_area_rectangulo_ancho_multiplicado_por_un_factor(base, altura,
factor):
        return (base * altura) *factor

    def funcion_para_imprimir(mensaje):  # Línea añadida
        return mensaje  # Línea añadida

    resultado = calcular_area_rectangulo_ancho_multiplicado_por_un_factor(10,
5, 1.5) + 10 * 20 - 5 * 3

    print(f"El resultado del cálculo del área del rectángulo  es: {resultado}")  # Cambios: '    print(f"El resultado del cálculo del área del rectángulo con el factor aplicado es: {resultado}")' -> '    print(f"El resultado del cálculo del área del rectángulo  es: {resultado}")'




