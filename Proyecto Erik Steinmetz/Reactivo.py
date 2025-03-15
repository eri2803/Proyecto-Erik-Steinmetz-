class Reactivo:
    """
    Representa un reactivo de laboratorio con sus características y conversiones de unidad.
    """

    def __init__(self, id, nombre, descripcion, costo, categoria, inventario, unidad_medida, fecha_caducidad, minimo, conversiones):
        """
        Inicializa un reactivo de laboratorio.

        :param id: Identificador único del reactivo.
        :param nombre: Nombre del reactivo.
        :param descripcion: Descripción del reactivo.
        :param costo: Costo por unidad base del reactivo.
        :param categoria: Categoría a la que pertenece el reactivo.
        :param inventario: Cantidad disponible en inventario.
        :param unidad_medida: Unidad base del reactivo.
        :param fecha_caducidad: Fecha de caducidad del reactivo.
        :param minimo: Cantidad mínima recomendada en inventario.
        :param conversiones: Lista de objetos `Conversion` para cambios de unidad.
        """
        self.id = id
        self.nombre = nombre  
        self.descripcion = descripcion  
        self.costo = costo  # Costo por unidad
        self.categoria = categoria  
        self.inventario = inventario  # Cantidad disponible en la unidad base
        self.unidad_medida = unidad_medida  # Unidad base (ej. 'g', 'mL')
        self.fecha_caducidad = fecha_caducidad  # Fecha en formato YYYY-MM-DD
        self.minimo = minimo  # Mínimo recomendado antes de requerir reposición
        self.conversiones = conversiones  # Lista de objetos `Conversion`

    def __str__(self):
        """
        Devuelve una representación en string del reactivo.
        """
        info = (f"ID: {self.id}\n"
                f"Nombre: {self.nombre}\n"
                f"Descripción: {self.descripcion}\n"
                f"Costo: ${self.costo:.2f}\n"
                f"Categoría: {self.categoria}\n"
                f"Inventario Disponible: {self.inventario} {self.unidad_medida}\n"
                f"Fecha de Caducidad: {self.fecha_caducidad}\n"
                f"Mínimo Sugerido: {self.minimo} {self.unidad_medida}\n"
                "Conversiones Posibles:\n")

        # Verifica si hay conversiones registradas y las agrega al string
        if self.conversiones:
            for conversion in self.conversiones:
                info += f"- {conversion.unidad} (Factor: {conversion.factor})\n"
        else:
            info += "No tiene conversiones registradas.\n"

        return info