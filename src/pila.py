from src.configuracion import obtener_configuracion_general


class PilaOperaciones:
    """
    Pila LIFO utilizada para almacenar el historial
    reciente de operaciones realizadas durante la
    ejecucion del sistema.
    """

    def __init__(self):
        configuracion = obtener_configuracion_general()

        self.maximo = configuracion.get(
            "maximo_historial_pila",
            20
        )

        self.elementos = []

    def esta_vacia(self):
        return len(self.elementos) == 0

    def push(self, operacion):
        """
        Inserta una operacion en el TOP de la pila.
        """
        if len(self.elementos) >= self.maximo:
            self.elementos.pop(0)

        self.elementos.append(operacion)

    def pop(self):
        """
        Elimina y devuelve la operacion ubicada
        en el TOP de la pila.
        """
        if self.esta_vacia():
            return None

        return self.elementos.pop()

    def top(self):
        """
        Devuelve la operacion ubicada en el TOP
        sin eliminarla.
        """
        if self.esta_vacia():
            return None

        return self.elementos[-1]

    def obtener_historial(self):
        """
        Devuelve el historial desde el TOP
        hasta la operacion mas antigua.
        """
        return list(reversed(self.elementos))

    def cantidad(self):
        return len(self.elementos)