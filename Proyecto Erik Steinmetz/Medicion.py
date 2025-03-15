class Medicion:
    """
    Representa una medición en un experimento de laboratorio.
    """

    def __init__(self, nombre, formula, minimo, maximo):
        """
        Inicializa una medición.

        :param nombre: Nombre de la medición.
        :param formula: Fórmula utilizada para calcular la medición.
        :param minimo: Valor mínimo aceptable.
        :param maximo: Valor máximo aceptable.
        """
        self.nombre = nombre  # Nombre de la medición
        self.formula = formula  # Expresión o referencia utilizada en el cálculo
        self.minimo = minimo  # Límite inferior aceptable
        self.maximo = maximo  # Límite superior aceptable

    def __str__(self):
        """
        Devuelve una representación en cadena de la medición.
        """
        return (f"Nombre: {self.nombre}\n"
                f"Fórmula: {self.formula}\n"
                f"Mínimo: {self.minimo}\n"
                f"Máximo: {self.maximo}")
