class Experimento:
    """
    Representa un experimento de laboratorio basado en una receta.
    """

    def __init__(self, id, receta, responsables, fecha):
        """
        Inicializa un experimento.

        :param id: Identificador único del experimento.
        :param receta: Objeto `Receta` asociado al experimento.
        :param responsables: Lista de nombres de los responsables del experimento.
        :param fecha: Fecha en la que se realiza el experimento.
        """
        self.id = id
        self.receta = receta  # Receta en la que se basa el experimento
        self.responsables = responsables  # Lista de personas encargadas
        self.fecha = fecha  # Fecha de realización
        self.costo = self.calcular_costo()  # Cálculo automático del costo total
        self.resultado = None  # Se inicializa sin resultado hasta que sea registrado

    def calcular_costo(self):
        """
        Calcula el costo total del experimento en función de los reactivos utilizados.

        :return: Costo total del experimento.
        """
        costo_total = 0  # Inicializa el costo total en 0

        for reactivo_info in self.receta.reactivos:
            reactivo = reactivo_info["reactivo"]  # Objeto Reactivo
            cantidad = reactivo_info["cantidad"]  # Cantidad utilizada
            costo_total += reactivo.costo * cantidad  # Suma al costo total
            
        return costo_total

    def __str__(self):
        """
        Devuelve una representación en cadena del experimento.
        """
        responsables_str = ", ".join(self.responsables)  # Convierte la lista de responsables en una cadena
        resultado_str = self.resultado if self.resultado else "No registrado"

        return (f"===== EXPERIMENTO {self.id} =====\n"
                f"Receta: {self.receta.nombre}\n"
                f"Responsables: {responsables_str}\n"
                f"Fecha: {self.fecha}\n"
                f"Costo Total: ${self.costo:.2f}\n"
                f"Resultado: {resultado_str}\n")