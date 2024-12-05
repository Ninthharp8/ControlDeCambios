# Test para estructura 'def'
class clase:
    def sumar(a, b):
        return a + b
    def es_par(numero):
        return numero % 2 == 0
    def mostrar_mensaje(mensaje):
        print(f"Mensaje: {mensaje}")
class test:
    for i in range(5):  # Línea añadida
        if i == 2:  # Línea añadida
            continue  # Línea añadida
        print(i)  # Línea añadida

        for y in range(6):  # Línea añadida
            if y == 2:  # Línea añadida
                continue  # Línea añadida
            print(y)  # Línea añadida

