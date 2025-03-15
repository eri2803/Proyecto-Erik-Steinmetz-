class Receta:
    """
    Representa una receta de laboratorio.
    """

    def __init__(self, id_receta, nombre, objetivo, reactivos, procedimiento, valores_a_medir):
        """
        Inicializa la receta.

        :param id_receta: Identificador de la receta.
        :param nombre: Nombre de la receta.
        :param objetivo: Objetivo del experimento.
        :param reactivos: Lista de diccionarios con reactivos, cantidades y unidades.
        :param procedimiento: Lista de pasos del experimento.
        :param valores_a_medir: Lista de objetos Medicion con fórmulas y rangos.
        """
        self.id = id_receta
        self.nombre = nombre
        self.objetivo = objetivo
        self.reactivos = reactivos  # Diccionarios con "reactivo", "cantidad" y "unidad".
        self.procedimiento = procedimiento  # Pasos a seguir.
        self.valores_a_medir = valores_a_medir  # Mediciones esperadas.

    def __str__(self):
        """
        Retorna una cadena con la información completa de la receta.
        """
        receta_str = f"\nReceta: {self.nombre} (ID: {self.id})\n"
        receta_str += f"Objetivo: {self.objetivo}\n\n"

        # Lista de reactivos
        receta_str += "Reactivos Utilizados:\n"
        for item in self.reactivos:
            reactivo = item["reactivo"]
            cantidad = item["cantidad"]
            unidad = item["unidad"]
            receta_str += f"- {reactivo.nombre}: {cantidad} {unidad}\n"

        # Procedimiento
        receta_str += "\nProcedimiento:\n"
        for i, paso in enumerate(self.procedimiento, start=1):
            receta_str += f"  {i}. {paso}\n"

        # Valores a medir
        receta_str += "\nValores a Medir:\n"
        for medicion in self.valores_a_medir:
            receta_str += f"- {medicion.nombre}: {medicion.formula} ({medicion.minimo} - {medicion.maximo})\n"

        return receta_str