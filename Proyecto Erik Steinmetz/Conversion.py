class Conversion:
    """
    Representa una conversión de unidad de medida.
    """

    def __init__(self, unidad, factor):
        """
        Inicializa la conversión de unidad.

        :param unidad: Unidad de medida destino (ejemplo: 'L', 'mg', 'kg').
        :param factor: Factor de conversión con respecto a la unidad base.
        """
        self.unidad = unidad  # Unidad de medida a la que se convertirá
        self.factor = factor  # Relación de conversión con la unidad base del reactivo

    def convertir(self, cantidad):
        """
        Convierte una cantidad desde la unidad base a la unidad destino.

        :param cantidad: Valor en la unidad base.
        :return: Valor convertido a la unidad de destino.
        """
        return cantidad * self.factor  # Aplicación del factor de conversión

    def __str__(self):
        """
        Representación en cadena de la conversión.
        """
        return f"{self.unidad} (Factor: {self.factor})"
