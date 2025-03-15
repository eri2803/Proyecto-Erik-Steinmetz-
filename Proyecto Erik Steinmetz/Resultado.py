class Resultado:
    """
    Representa el resultado de un experimento de laboratorio.
    """

    def __init__(self, experimento, valores_obtenidos, valores_aceptables):
        """
        Inicializa el resultado del experimento.

        :param experimento: Objeto del experimento asociado.
        :param valores_obtenidos: Diccionario con valores medidos en el experimento.
        :param valores_aceptables: Diccionario con los rangos aceptables para cada medición.
        """
        self.experimento = experimento  # Referencia al experimento asociado
        self.valores_obtenidos = valores_obtenidos  # {medición: valor obtenido}
        self.valores_aceptables = valores_aceptables  # {medición: (mínimo, máximo)}
        self.valido = self.evaluar_resultado()  # Evaluación automática al crear el objeto

    def evaluar_resultado(self):
        """
        Verifica si los valores obtenidos están dentro de los rangos aceptables.

        :return: True si todos los valores están dentro del rango, False en caso contrario.
        """
        for medicion, valor in self.valores_obtenidos.items():
            min_aceptable, max_aceptable = self.valores_aceptables.get(medicion, (None, None))
            if min_aceptable is not None and max_aceptable is not None:
                if not (min_aceptable <= valor <= max_aceptable):
                    return False  # Se encuentra fuera de los parámetros aceptables
        return True

    def __str__(self):
        """
        Devuelve una representación en cadena del resultado del experimento.
        """
        resultado_str = f"\n===== RESULTADO DEL EXPERIMENTO {self.experimento.id} =====\n"
        resultado_str += f"Receta: {self.experimento.receta.nombre}\n"
        resultado_str += f"Fecha: {self.experimento.fecha}\n"
        resultado_str += f"Responsables: {', '.join(self.experimento.responsables)}\n"
        resultado_str += f"Costo: ${self.experimento.costo:.2f}\n"
        resultado_str += f"Evaluación: {'Dentro de parámetros' if self.valido else 'Fuera de parámetros'}\n"

        # Detalles de los valores obtenidos y su comparación con los valores aceptables
        resultado_str += "\nValores obtenidos:\n"
        for medicion, valor in self.valores_obtenidos.items():
            min_aceptable, max_aceptable = self.valores_aceptables[medicion]
            dentro_de_rango = "Sí" if min_aceptable <= valor <= max_aceptable else "No"
            resultado_str += f"  - {medicion}: {valor:.2f} (Aceptable: {min_aceptable} - {max_aceptable}) [{dentro_de_rango}]\n"

        return resultado_str
