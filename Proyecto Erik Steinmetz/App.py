import requests
import random
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from Reactivo import Reactivo
from Conversion import Conversion
from Receta import Receta
from Medicion import Medicion
from Experimento import Experimento
from Resultado import Resultado

class App:
    """
    Clase principal para gestionar reactivos, recetas, experimentos y resultados.
    """

    def __init__(self):
        """
        Inicializa la aplicación con listas vacías para almacenar los datos.
        """
        self.reactivos = []  # Almacena los objetos Reactivo
        self.recetas = []  # Almacena los objetos Receta
        self.experimentos = []  # Almacena los objetos Experimento
        self.resultados = []  # Almacena los objetos Resultado

    def obtener_reactivo_por_id(self, id):
        """
        Busca un reactivo por su ID.

        :param id: Identificador del reactivo.
        :return: Objeto Reactivo si se encuentra, de lo contrario None.
        """
        for reactivo in self.reactivos:
            if reactivo.id == id:
                return reactivo
        return None  # Retorna None si no se encuentra el reactivo

    def cargar_reactivos_api(self):
        """
        Carga los reactivos desde una API y los almacena en la lista de reactivos.
        """
        url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/reactivos.json"
        response = requests.get(url)

        if response.status_code == 200:
            datos = response.json()
            for dato in datos:
                # Extraer datos del reactivo
                id_reactivo = dato["id"]
                nombre = dato["nombre"]
                descripcion = dato["descripcion"]
                costo = dato["costo"]
                categoria = dato["categoria"]
                inventario_disponible = dato["inventario_disponible"]
                unidad_medida = dato["unidad_medida"]
                fecha_caducidad = dato["fecha_caducidad"]
                minimo_sugerido = dato["minimo_sugerido"]

                # Procesar conversiones de unidad
                conversiones = []
                for conversion in dato["conversiones_posibles"]:
                    unidad = conversion["unidad"]
                    factor = conversion["factor"]
                    conversion_nueva = Conversion(unidad, factor)
                    conversiones.append(conversion_nueva)

                # Crear y agregar el reactivo a la lista
                reactivo = Reactivo(
                    id_reactivo, nombre, descripcion, costo, categoria,
                    inventario_disponible, unidad_medida, fecha_caducidad,
                    minimo_sugerido, conversiones
                )
                self.reactivos.append(reactivo)

            print("Reactivos cargados correctamente desde la API.")
        else:
            print("Error: No se pudo conectar con la API de reactivos.")

    def cargar_recetas_api(self):
        """
        Carga las recetas desde una API y las almacena en la lista de recetas.
        """
        url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/recetas.json"
        response = requests.get(url)

        if response.status_code == 200:
            datos = response.json()
            for dato in datos:
                # Extraer datos de la receta
                id_receta = dato["id"]
                nombre = dato["nombre"]
                objetivo = dato["objetivo"]
                procedimiento = dato["procedimiento"]

                # Procesar reactivos necesarios para la receta
                reactivos_necesarios = []
                for reactivo_info in dato["reactivos_utilizados"]:
                    reactivo = self.obtener_reactivo_por_id(reactivo_info["reactivo_id"])
                    if reactivo:  # Solo agrega el reactivo si existe
                        reactivos_necesarios.append({
                            "reactivo": reactivo,
                            "cantidad": reactivo_info["cantidad_necesaria"],
                            "unidad": reactivo_info["unidad_medida"]
                        })

                # Procesar valores a medir
                mediciones = []
                for medicion_info in dato["valores_a_medir"]:
                    nombre_medicion = medicion_info["nombre"]
                    formula = medicion_info["formula"]
                    minimo = medicion_info["minimo"]
                    maximo = medicion_info["maximo"]

                    medicion = Medicion(nombre_medicion, formula, minimo, maximo)
                    mediciones.append(medicion)

                # Crear y agregar la receta a la lista
                receta = Receta(id_receta, nombre, objetivo, reactivos_necesarios, procedimiento, mediciones)
                self.recetas.append(receta)

            print("Recetas cargadas correctamente desde la API.")
        else:
            print("Error: No se pudo conectar con la API de recetas.")


    def obtener_receta_por_id(self, id):
        for receta in self.recetas:
            if receta.id == id:
                return receta
        return None  # Retorna None si no encuentra la receta
     

    def cargar_experimentos_api(self):
        """
        Carga los experimentos desde una API y los almacena en la lista de experimentos.
        """
        url = "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/experimentos.json"
        response = requests.get(url)

        if response.status_code == 200:
            datos = response.json()
            for dato in datos:
                # Extraer datos del experimento
                id_experimento = dato["id"]
                receta = self.obtener_receta_por_id(dato["receta_id"])  # Buscar receta asociada
                responsables = dato["personas_responsables"]
                fecha = dato["fecha"]
                resultado = dato["resultado"]

                # Solo crear el experimento si la receta existe
                if receta:
                    experimento = Experimento(id_experimento, receta, responsables, fecha)
                    experimento.resultado = resultado  # Asignar resultado si está presente
                    self.experimentos.append(experimento)

            print("Experimentos cargados correctamente desde la API.")
        else:
            print("Error: No se pudo conectar con la API de experimentos.") 

    def inicializar_datos(self):
        """
        Carga los datos de reactivos, recetas y experimentos desde la API.
        """
        print("\nCargando datos desde la API...\n")
        self.cargar_reactivos_api()
        self.cargar_recetas_api()
        self.cargar_experimentos_api()
        print("Datos cargados correctamente.")

    def borrar_datos(self):
        """
        Elimina todos los datos almacenados en la aplicación.
        """
        self.reactivos.clear()  # Vacía la lista de reactivos
        self.recetas.clear()  # Vacía la lista de recetas
        self.experimentos.clear()  # Vacía la lista de experimentos
        print("\nTodos los datos han sido eliminados.\n")


    def mostrar_menu_principal(self):
        """
        Muestra el menú principal de la aplicación y gestiona la navegación entre opciones.
        """
        while True:
            # Despliegue del menú
            print("\n===== MENÚ PRINCIPAL =====")
            print("1. Gestionar Reactivos")
            print("2. Gestionar Experimentos")
            print("3. Gestionar Resultados")
            print("4. Estadísticas")
            print("5. Salir")

            # Validación de entrada del usuario
            opcion = input("Seleccione una opción: ")
            while not opcion.isnumeric() or not int(opcion) in range(1, 6):
                print("Error")
                opcion = input("Ingrese una opción válida: ")

            # Redirección según la opción seleccionada
            if opcion == "1":
                self.menu_reactivos()
            elif opcion == "2":
                self.menu_experimentos()
            elif opcion == "3":
                self.menu_resultados()
            elif opcion == "4":
                self.menu_estadisticas()
            else:
                self.guardar_datos_json()
                self.borrar_datos()  # Limpia los datos antes de salir
                print("\nGracias por utilizar el Laboratorio.")
                break  # Sale del bucle y finaliza el programa


    import json

    def guardar_datos_json(self):
        """
        Guarda los datos de reactivos, recetas, experimentos y resultados en archivos JSON.
        """
        # Lista para almacenar los reactivos en formato JSON
        reactivos_json = []
        for r in self.reactivos:
            reactivo_data = {
                "id": r.id,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "costo": r.costo,
                "categoria": r.categoria,
                "inventario_disponible": r.inventario,
                "unidad_medida": r.unidad_medida,
                "fecha_caducidad": r.fecha_caducidad,
                "minimo_sugerido": r.minimo,
                "conversiones": []
            }
            for c in r.conversiones:
                reactivo_data["conversiones"].append({
                    "unidad": c.unidad,
                    "factor": c.factor
                })
            reactivos_json.append(reactivo_data)

        # Lista para almacenar las recetas en formato JSON
        recetas_json = []
        for r in self.recetas:
            receta_data = {
                "id": r.id,
                "nombre": r.nombre,
                "objetivo": r.objetivo,
                "procedimiento": r.procedimiento,
                "reactivos_utilizados": [],
                "valores_a_medir": []
            }
            for item in r.reactivos:
                receta_data["reactivos_utilizados"].append({
                    "reactivo_id": item["reactivo"].id,
                    "cantidad": item["cantidad"],
                    "unidad": item["unidad"]
                })
            for v in r.valores_a_medir:
                receta_data["valores_a_medir"].append({
                    "nombre": v.nombre,
                    "formula": v.formula,
                    "minimo": v.minimo,
                    "maximo": v.maximo
                })
            recetas_json.append(receta_data)

        # Lista para almacenar los experimentos en formato JSON
        experimentos_json = []
        for e in self.experimentos:
            experimento_data = {
                "id": e.id,
                "receta_id": e.receta.id,
                "personas_responsables": e.responsables,
                "fecha": e.fecha,
                "costo_asociado": e.costo,
                "resultado": e.resultado if isinstance(e.resultado, str) else None
            }
            experimentos_json.append(experimento_data)

        # Lista para almacenar los resultados en formato JSON
        resultados_json = []
        for r in self.resultados:
            resultado_data = {
                "experimento_id": r.experimento.id,
                "valores_obtenidos": r.valores_obtenidos,
                "valores_aceptables": r.valores_aceptables,
                "valido": r.valido
            }
            resultados_json.append(resultado_data)

        # Guardar cada conjunto de datos en un archivo JSON
        with open("reactivos.json", "w", encoding="utf-8") as f:
            json.dump(reactivos_json, f, indent=4, ensure_ascii=False)

        with open("recetas.json", "w", encoding="utf-8") as f:
            json.dump(recetas_json, f, indent=4, ensure_ascii=False)

        with open("experimentos.json", "w", encoding="utf-8") as f:
            json.dump(experimentos_json, f, indent=4, ensure_ascii=False)

        with open("resultados.json", "w", encoding="utf-8") as f:
            json.dump(resultados_json, f, indent=4, ensure_ascii=False)

        print("\nDatos guardados exitosamente en archivos JSON.")

    def cargar_datos_json(self):
        """
        Carga los datos de reactivos, recetas, experimentos y resultados desde archivos JSON.
        """
        # Verifica si los archivos existen antes de intentar cargarlos
        archivos = ["reactivos.json", "recetas.json", "experimentos.json", "resultados.json"]
        for archivo in archivos:
            if not os.path.exists(archivo):
                print(f"\nAdvertencia: El archivo {archivo} no existe. No se cargaron datos de este archivo.")

        # Cargar reactivos desde JSON
        if os.path.exists("reactivos.json"):
            with open("reactivos.json", "r", encoding="utf-8") as f:
                reactivos_json = json.load(f)

            self.reactivos.clear()
            for r in reactivos_json:
                conversiones = []
                for c in r["conversiones"]:
                    conversiones.append(Conversion(c["unidad"], c["factor"]))

                reactivo = Reactivo(
                    r["id"], r["nombre"], r["descripcion"], r["costo"], r["categoria"],
                    r["inventario_disponible"], r["unidad_medida"], r["fecha_caducidad"],
                    r["minimo_sugerido"], conversiones
                )
                self.reactivos.append(reactivo)

        # Cargar recetas desde JSON
        if os.path.exists("recetas.json"):
            with open("recetas.json", "r", encoding="utf-8") as f:
                recetas_json = json.load(f)

            self.recetas.clear()
            for r in recetas_json:
                reactivos_necesarios = []
                for item in r["reactivos_utilizados"]:
                    reactivo = self.obtener_reactivo_por_id(item["reactivo_id"])
                    if reactivo:
                        reactivos_necesarios.append({
                            "reactivo": reactivo,
                            "cantidad": item["cantidad"],
                            "unidad": item["unidad"]
                        })

                valores_a_medir = []
                for v in r["valores_a_medir"]:
                    medicion = Medicion(v["nombre"], v["formula"], v["minimo"], v["maximo"])
                    valores_a_medir.append(medicion)

                receta = Receta(r["id"], r["nombre"], r["objetivo"], reactivos_necesarios, r["procedimiento"], valores_a_medir)
                self.recetas.append(receta)

        # Cargar experimentos desde JSON
        if os.path.exists("experimentos.json"):
            with open("experimentos.json", "r", encoding="utf-8") as f:
                experimentos_json = json.load(f)

            self.experimentos.clear()
            for e in experimentos_json:
                receta = self.obtener_receta_por_id(e["receta_id"])
                if receta:
                    experimento = Experimento(e["id"], receta, e["personas_responsables"], e["fecha"])
                    experimento.costo = e["costo_asociado"]
                    experimento.resultado = e["resultado"]
                    self.experimentos.append(experimento)

        # Cargar resultados desde JSON
        if os.path.exists("resultados.json"):
            with open("resultados.json", "r", encoding="utf-8") as f:
                resultados_json = json.load(f)

            self.resultados.clear()
            for r in resultados_json:
                experimento = next((e for e in self.experimentos if e.id == r["experimento_id"]), None)
                if experimento:
                    resultado = Resultado(experimento, r["valores_obtenidos"], r["valores_aceptables"])
                    resultado.valido = r["valido"]
                    self.resultados.append(resultado)

        print("\nDatos cargados exitosamente desde archivos JSON.")

            
    def mostrar_menu_inicial(self):
        """
        Muestra el menú inicial para la carga de datos antes de acceder al sistema.
        """
        while True:
            print("\nBienvenido al Sistema del Laboratorio")
            print("1. Cargar datos desde la API")
            print("2. Cargar JSON")
            print("3. Salir")  # Corrección de numeración

            # Validación de la opción ingresada
            opcion = input("Seleccione una opción: ")
            while not opcion.isnumeric() or not int(opcion) in range(1, 4):
                print("Error")
                opcion = input("Ingrese una opción válida: ")

            # Manejo de opciones
            if opcion == "1":
                self.inicializar_datos()
                self.mostrar_menu_principal()
            elif opcion == "2":
                self.cargar_datos_json()
                self.mostrar_menu_principal()
            else:
                print("\nSaliendo del sistema. Hasta pronto.")
                break  # Finaliza la ejecución


    def menu_reactivos(self):
        """
        Muestra el menú de gestión de reactivos.
        """
        while True:
            print("\n===== Gestión de Reactivos =====")
            print("1. Crear Reactivo")
            print("2. Eliminar Reactivo")
            print("3. Editar Reactivo")
            print("4. Salir")

            # Validación de la opción ingresada
            opcion = input("Seleccione una opción: ")
            while not opcion.isnumeric() or not int(opcion) in range(1, 5):
                print("Error")
                opcion = input("Ingrese una opción válida: ")

            # Manejo de opciones
            if opcion == "1":
                self.crear_reactivos()
            elif opcion == "2":
                self.eliminar_reactivos()
            elif opcion == "3":
                self.editar_reactivos()
            else:
                print("\nHas salido del módulo Gestión de Reactivos.")
                break  # Regresa al menú principal


    def crear_reactivos(self):
        """
        Crea un nuevo reactivo solicitando los datos al usuario.
        """
        print("\n===== CREAR NUEVO REACTIVO =====")
        
        # Generar un ID único basado en la cantidad de reactivos existentes
        id_reactivo = len(self.reactivos) + 1  

        # Solicitar el nombre del reactivo
        nombre = input("Ingrese el nombre del reactivo: ")
        while not nombre:
            print("Error: El nombre no puede estar vacío.")
            nombre = input("Ingrese el nombre del reactivo: ")

        # Solicitar la descripción
        descripcion = input("Ingrese una breve descripción: ")
        while not descripcion:
            print("Error: La descripción no puede estar vacía.")
            descripcion = input("Ingrese una breve descripción: ")

        # Solicitar el costo del reactivo
        costo = input("Ingrese el costo del reactivo: ")
        while not costo.replace('.', '', 1).isnumeric() or float(costo) < 0:
            print("Error: Ingrese un costo válido (número positivo).")
            costo = input("Ingrese el costo del reactivo: ")
        costo = float(costo)

        # Solicitar la categoría
        categoria = input("Ingrese la categoría del reactivo: ")
        while not categoria:
            print("Error: La categoría no puede estar vacía.")
            categoria = input("Ingrese la categoría del reactivo: ")

        # Solicitar el inventario disponible
        inventario = input("Ingrese la cantidad disponible: ")
        while not inventario.replace('.', '', 1).isnumeric() or float(inventario) < 0:
            print("Error: Ingrese una cantidad válida (número positivo).")
            inventario = input("Ingrese la cantidad disponible: ")
        inventario = float(inventario)

        # Solicitar la unidad de medida
        unidad_medida = input("Ingrese la unidad de medida (ej. mL, L, g, Kg): ")
        while not unidad_medida:
            print("Error: La unidad de medida no puede estar vacía.")
            unidad_medida = input("Ingrese la unidad de medida (ej. mL, L, g, Kg): ")

        # Solicitar la fecha de caducidad (opcional)
        fecha_caducidad = input("Ingrese la fecha de caducidad (YYYY-MM-DD) o deje vacío si no aplica: ")
        if not fecha_caducidad:
            fecha_caducidad = "No aplica"

        # Solicitar el mínimo sugerido para reposición
        minimo = input("Ingrese la cantidad mínima sugerida para reposición: ")
        while not minimo.replace('.', '', 1).isnumeric() or float(minimo) < 0:
            print("Error: Ingrese un valor válido (número positivo).")
            minimo = input("Ingrese la cantidad mínima sugerida para reposición: ")
        minimo = float(minimo)

        # Agregar conversiones de unidades
        conversiones = []
        while True:
            agregar_conversion = input("¿Desea agregar una conversión de unidad? (S/N): ").lower()
            if agregar_conversion == 's':
                # Solicitar unidad de conversión
                unidad = input("Ingrese la unidad de conversión (ej. L, mg, Kg): ")
                while not unidad:
                    print("Error: La unidad de conversión no puede estar vacía.")
                    unidad = input("Ingrese la unidad de conversión (ej. L, mg, Kg): ")

                # Solicitar el factor de conversión
                factor = input(f"Ingrese el factor de conversión para {unidad}: ")
                while not factor.replace('.', '', 1).isnumeric() or float(factor) <= 0:
                    print("Error: Ingrese un factor de conversión válido (mayor a 0).")
                    factor = input(f"Ingrese el factor de conversión para {unidad}: ")
                factor = float(factor)

                conversiones.append(Conversion(unidad, factor))

            elif agregar_conversion == 'n':
                break
            else:
                print("Opción inválida, ingrese 'S' para sí o 'N' para no.")

        # Crear el objeto Reactivo y agregarlo a la lista
        nuevo_reactivo = Reactivo(
            id_reactivo, nombre, descripcion, costo, categoria,
            inventario, unidad_medida, fecha_caducidad, minimo, conversiones
        )
        
        self.reactivos.append(nuevo_reactivo)
        print("\nReactivo creado exitosamente:")
        print(nuevo_reactivo)



    def editar_reactivos(self):
        """
        Permite editar los atributos de un reactivo existente en el sistema.
        """
        while True:
            if not self.reactivos:
                print("\nNo hay reactivos en el sistema para editar.")
                break

            # Mostrar lista de reactivos disponibles
            print("\n===== EDITAR REACTIVO =====")
            for i, reactivo in enumerate(self.reactivos, start=1):
                print(f"{i}. ID:{reactivo.id} {reactivo.nombre}")

            # Validar selección del reactivo
            seleccion = input("\nSeleccione el número del reactivo a editar: ")
            while not seleccion.isnumeric() or int(seleccion) not in range(1, len(self.reactivos) + 1):
                print("Error: Ingrese un número válido de la lista.")
                seleccion = input("\nSeleccione el número del reactivo a editar: ")

            seleccion = int(seleccion) - 1  # Convertir a índice válido
            reactivo = self.reactivos[seleccion]  # Obtener el reactivo seleccionado

            print(f"\nEditando reactivo: {reactivo.nombre} (ID: {reactivo.id})")

            while True:
                # Menú de opciones de edición
                print("\n===== OPCIONES DE EDICIÓN =====")
                print("1. Editar nombre")
                print("2. Editar descripción")
                print("3. Editar costo")
                print("4. Editar categoría")
                print("5. Editar inventario disponible")
                print("6. Editar unidad de medida")
                print("7. Editar fecha de caducidad")
                print("8. Editar mínimo sugerido")
                print("9. Gestionar conversiones")
                print("10. Salir de la edición")

                # Validar opción de edición
                opcion_editar = input("\nIngrese el número de la opción a editar: ")
                while not opcion_editar.isnumeric() or int(opcion_editar) not in range(1, 11):
                    print("Error: Ingrese un número válido de la lista.")
                    opcion_editar = input("\nIngrese el número de la opción a editar: ")

                opcion_editar = int(opcion_editar)

                # Edición del atributo seleccionado
                if opcion_editar == 1:
                    reactivo.nombre = input("\nNuevo nombre: ")
                elif opcion_editar == 2:
                    reactivo.descripcion = input("\nNueva descripción: ")
                elif opcion_editar == 3:
                    nuevo_costo = input("\nNuevo costo: ")
                    while not nuevo_costo.replace('.', '', 1).isnumeric():
                        print("Error: Ingrese un número válido para el costo.")
                        nuevo_costo = input("\nNuevo costo: ")
                    reactivo.costo = float(nuevo_costo)
                elif opcion_editar == 4:
                    reactivo.categoria = input("\nNueva categoría: ")
                elif opcion_editar == 5:
                    nuevo_inventario = input("\nNuevo inventario disponible: ")
                    while not nuevo_inventario.isnumeric():
                        print("Error: Ingrese un número válido para el inventario.")
                        nuevo_inventario = input("\nNuevo inventario disponible: ")
                    reactivo.inventario = int(nuevo_inventario)
                elif opcion_editar == 6:
                    reactivo.unidad_medida = input("\nNueva unidad de medida: ")
                elif opcion_editar == 7:
                    reactivo.fecha_caducidad = input("\nNueva fecha de caducidad (YYYY-MM-DD): ")
                elif opcion_editar == 8:
                    nuevo_minimo = input("\nNuevo mínimo sugerido: ")
                    while not nuevo_minimo.isnumeric():
                        print("Error: Ingrese un número válido para el mínimo sugerido.")
                        nuevo_minimo = input("\nNuevo mínimo sugerido: ")
                    reactivo.minimo = int(nuevo_minimo)
                elif opcion_editar == 9:
                    self.gestionar_conversiones(reactivo)  # Método externo para manejar conversiones
                else:
                    print(reactivo.__str__())  # Mostrar reactivo actualizado
                    print("\nSaliendo de la edición del reactivo.")
                    break  # Termina la edición

                print("\nAtributo actualizado correctamente.")

            # Preguntar si desea editar otro reactivo
            continuar = input("\n¿Desea editar otro reactivo? (S/N): ").lower()
            while continuar not in ['s', 'n']:
                print("Error: Ingrese 'S' para sí o 'N' para no.")
                continuar = input("\n¿Desea editar otro reactivo? (S/N): ").lower()

            if continuar == 'n':
                break  # Salir del bucle


    def gestionar_conversiones(self, reactivo):
        """
        Permite gestionar las conversiones de unidad de un reactivo: agregar, editar o eliminar.
        
        :param reactivo: Objeto Reactivo al que se le aplicarán las conversiones.
        """
        while True:
            print("\n===== GESTIONAR CONVERSIONES =====")
            print("1. Agregar conversión")
            print("2. Editar conversión")
            print("3. Eliminar conversión")
            print("4. Salir")

            # Validar la opción seleccionada
            opcion = input("\nSeleccione una opción: ")
            while not opcion.isnumeric() or int(opcion) not in range(1, 5):
                print("Error: Ingrese un número válido de la lista.")
                opcion = input("\nSeleccione una opción: ")

            opcion = int(opcion)

            if opcion == 1:  # Agregar conversión
                unidad = input("\nIngrese la nueva unidad de medida: ")
                factor = input("\nIngrese el factor de conversión: ")
                while not factor.replace('.', '', 1).isnumeric() or float(factor) <= 0:
                    print("Error: Ingrese un número válido para el factor de conversión.")
                    factor = input("\nIngrese el factor de conversión: ")
                factor = float(factor)

                reactivo.conversiones.append(Conversion(unidad, factor))
                print("\nConversión agregada correctamente.")

            elif opcion == 2:  # Editar conversión
                if not reactivo.conversiones:
                    print("\nNo hay conversiones registradas para este reactivo.")
                    continue

                print("\nSeleccione la conversión a editar:")
                for i, conversion in enumerate(reactivo.conversiones, start=1):
                    print(f"{i}. {conversion.unidad} (Factor: {conversion.factor})")

                # Validar la selección
                seleccion = input("\nSeleccione el número de la conversión a editar: ")
                while not seleccion.isnumeric() or int(seleccion) not in range(1, len(reactivo.conversiones) + 1):
                    print("Error: Ingrese un número válido de la lista.")
                    seleccion = input("\nSeleccione el número de la conversión a editar: ")

                seleccion = int(seleccion) - 1
                conversion = reactivo.conversiones[seleccion]

                # Solicitar nuevos valores
                nueva_unidad = input("\nNueva unidad de medida: ")
                nuevo_factor = input("\nNuevo factor de conversión: ")
                while not nuevo_factor.replace('.', '', 1).isnumeric() or float(nuevo_factor) <= 0:
                    print("Error: Ingrese un número válido para el factor de conversión.")
                    nuevo_factor = input("\nNuevo factor de conversión: ")
                nuevo_factor = float(nuevo_factor)

                # Actualizar conversión
                conversion.unidad = nueva_unidad
                conversion.factor = nuevo_factor
                print("\nConversión editada correctamente.")

            elif opcion == 3:  # Eliminar conversión
                if not reactivo.conversiones:
                    print("\nNo hay conversiones registradas para este reactivo.")
                    continue

                print("\nSeleccione la conversión a eliminar:")
                for i, conversion in enumerate(reactivo.conversiones, start=1):
                    print(f"{i}. {conversion.unidad} (Factor: {conversion.factor})")

                # Validar la selección
                seleccion = input("\nSeleccione el número de la conversión a eliminar: ")
                while not seleccion.isnumeric() or int(seleccion) not in range(1, len(reactivo.conversiones) + 1):
                    print("Error: Ingrese un número válido de la lista.")
                    seleccion = input("\nSeleccione el número de la conversión a eliminar: ")

                seleccion = int(seleccion) - 1
                reactivo.conversiones.pop(seleccion)
                print("\nConversión eliminada correctamente.")

            elif opcion == 4:
                print("\nSaliendo de la gestión de conversiones.")
                break

    def eliminar_reactivos(self):
        """
        Permite eliminar un reactivo de la lista de reactivos.
        """
        while True:
            if not self.reactivos:
                print("\nNo hay reactivos en el sistema para eliminar.")
                break

            # Mostrar lista de reactivos disponibles
            print("\n===== ELIMINAR REACTIVO =====")
            for i, reactivo in enumerate(self.reactivos, start=1):
                print(f"{i}. ID:{reactivo.id} {reactivo.nombre}")

            # Validar selección del reactivo
            seleccion = input("\nSeleccione el número del reactivo a eliminar: ")
            while not seleccion.isnumeric() or int(seleccion) not in range(1, len(self.reactivos) + 1):
                print("Error: Ingrese un número válido de la lista.")
                seleccion = input("\nSeleccione el número del reactivo a eliminar: ")

            seleccion = int(seleccion) - 1  # Convertir a índice válido
            reactivo_eliminado = self.reactivos.pop(seleccion)  # Eliminar de la lista
            
            print(f"\nReactivo '{reactivo_eliminado.nombre}' eliminado correctamente.")

            # Preguntar si desea eliminar otro reactivo
            continuar = input("\n¿Desea eliminar otro reactivo? (S/N): ").lower()
            while continuar not in ['s', 'n']:
                print("Error: Ingrese 'S' para sí o 'N' para no.")
                continuar = input("\n¿Desea eliminar otro reactivo? (S/N): ").lower()
            
            if continuar == 'n':
                break  # Salir del bucle

    def menu_experimentos(self):
        """
        Muestra el menú de gestión de experimentos y permite realizar acciones relacionadas.
        """
        while True:
            print("\n===== Gestión de Experimentos =====")
            print("1. Crear Experimento")
            print("2. Eliminar Experimento")
            print("3. Editar Experimento")
            print("4. Realizar Experimento")
            print("5. Salir")

            # Validar entrada del usuario
            opcion = input("Seleccione una opción: ")
            while not opcion.isnumeric() or not int(opcion) in range(1, 6):
                print("Error: Ingrese una opción válida.")
                opcion = input("Seleccione una opción: ")

            # Redirigir según la opción seleccionada
            if opcion == "1":
                self.crear_experimento()
            elif opcion == "2":
                self.eliminar_experimento()
            elif opcion == "3":
                self.editar_experimento()
            elif opcion == "4":
                self.realizar_experimento()
            else:
                print("\nHas salido del módulo Gestión de Experimentos.")
                break  # Regresa al menú principal


    def crear_experimento(self):
        if not self.recetas:
            print("\nNo hay recetas registradas. Debe agregar una antes de crear un experimento.")
            return

        print("\n===== CREAR EXPERIMENTO =====")

        # Listar recetas disponibles
        for i, receta in enumerate(self.recetas, start=1):
            print(f"{i}. ID:{receta.id} {receta.nombre}")

        seleccion = input("\nSeleccione el número de la receta a usar para el experimento: ")

        while not seleccion.isnumeric() or int(seleccion) not in range(1, len(self.recetas) + 1):
            print("Error: Ingrese un número válido de la lista.")
            seleccion = input("\nSeleccione el número de la receta a usar para el experimento: ")

        seleccion = int(seleccion) - 1
        receta_seleccionada = self.recetas[seleccion]

        # Validar disponibilidad de reactivos
        for reactivo_info in receta_seleccionada.reactivos:
            reactivo = reactivo_info["reactivo"]
            cantidad_necesaria = reactivo_info["cantidad"]

            if reactivo.inventario < cantidad_necesaria:
                print(f"\nError: No hay suficiente {reactivo.nombre} en inventario para realizar el experimento.")
                return
            if reactivo.fecha_caducidad and reactivo.fecha_caducidad < str(datetime.today().date()):
                print(f"\nError: El reactivo {reactivo.nombre} ha caducado y no puede usarse.")
                return

        # Ingresar responsables del experimento
        responsables = []
        while True:
            responsable = input("\nIngrese el nombre de un responsable (o deje vacío para finalizar): ").strip()
            if not responsable:
                if responsables:
                    break
                else:
                    print("Debe ingresar al menos un responsable.")
            else:
                responsables.append(responsable)

        # Registrar la fecha actual
        fecha = str(datetime.today().date())

        # Crear el experimento y agregarlo a la lista
        nuevo_experimento = Experimento(len(self.experimentos) + 1, receta_seleccionada, responsables, fecha)
        self.experimentos.append(nuevo_experimento)

        print("\nExperimento creado exitosamente:")
        print(nuevo_experimento)


    def editar_experimento(self):
        """
        Permite editar los atributos de un experimento registrado.
        """
        if not self.experimentos:
            print("\nNo hay experimentos registrados para editar.")
            return

        while True:
            print("\n===== EDITAR EXPERIMENTO =====")

            # Mostrar lista de experimentos disponibles
            for i, experimento in enumerate(self.experimentos, start=1):
                print(f"{i}. ID:{experimento.id} - {experimento.receta.nombre}")

            # Validar selección del experimento
            seleccion = input("\nSeleccione el número del experimento a editar: ")
            while not seleccion.isnumeric() or int(seleccion) not in range(1, len(self.experimentos) + 1):
                print("Error: Ingrese un número válido de la lista.")
                seleccion = input("\nSeleccione el número del experimento a editar: ")

            seleccion = int(seleccion) - 1
            experimento = self.experimentos[seleccion]

            # Menú de edición
            while True:
                print("\n===== OPCIONES DE EDICIÓN =====")
                print("1. Cambiar receta")
                print("2. Editar responsables")
                print("3. Modificar fecha")
                print("4. Salir de la edición")

                # Validar opción ingresada
                opcion = input("\nSeleccione una opción: ")
                while not opcion.isnumeric() or int(opcion) in range(1,5):
                    print("Error: Opción no válida.")
                    opcion = input("Seleccione una opción: ")

                if opcion == "1":  # Cambiar receta
                    print("\n===== SELECCIONAR NUEVA RECETA =====")
                    for i, receta in enumerate(self.recetas, start=1):
                        print(f"{i}. {receta.nombre}")

                    # Validar selección de la nueva receta
                    nueva_receta_idx = input("\nSeleccione el número de la nueva receta: ")
                    while not nueva_receta_idx.isnumeric() or int(nueva_receta_idx) not in range(1, len(self.recetas) + 1):
                        print("Error: Seleccione un número válido.")
                        nueva_receta_idx = input("Seleccione el número de la nueva receta: ")

                    experimento.receta = self.recetas[int(nueva_receta_idx) - 1]
                    print(f"\nReceta cambiada a: {experimento.receta.nombre}")

                elif opcion == "2":  # Editar responsables
                    print("\n===== EDITAR RESPONSABLES =====")
                    print(f"Responsables actuales: {', '.join(experimento.responsables)}")
                    
                    nuevos_responsables = input("Ingrese los nombres de los responsables separados por comas: ")
                    experimento.responsables = [r.strip() for r in nuevos_responsables.split(",")]
                    print("\nResponsables actualizados correctamente.")

                elif opcion == "3":  # Modificar fecha
                    print("\n===== MODIFICAR FECHA =====")
                    nueva_fecha = input(f"Ingrese la nueva fecha (actual: {experimento.fecha}): ").strip()
                    experimento.fecha = nueva_fecha
                    print("\nFecha actualizada correctamente.")

                elif opcion == "4":  # Salir de la edición
                    print("\nSaliendo de la edición del experimento.")
                    break

            # Preguntar si desea editar otro experimento
            continuar = input("\n¿Desea editar otro experimento? (s/n): ").strip().lower()
            while continuar not in ["s", "n"]:
                continuar = input("Ingrese 's' para continuar editando o 'n' para salir: ").strip().lower()

            if continuar == "n":
                break  # Salir del bucle

    def eliminar_experimento(self):
        """
        Elimina un experimento registrado en el sistema.
        """
        if not self.experimentos:
            print("\nNo hay experimentos registrados para eliminar.")
            return

        while True:
            print("\n===== ELIMINAR EXPERIMENTO =====")
            
            # Mostrar lista de experimentos disponibles
            for i, experimento in enumerate(self.experimentos, start=1):
                print(f"{i}. ID:{experimento.id} - {experimento.receta.nombre}")

            # Validar selección del experimento
            seleccion = input("\nSeleccione el número del experimento a eliminar: ")
            while not seleccion.isnumeric() or int(seleccion) not in range(1, len(self.experimentos) + 1):
                print("Error: Ingrese un número válido de la lista.")
                seleccion = input("\nSeleccione el número del experimento a eliminar: ")

            seleccion = int(seleccion) - 1
            experimento_eliminado = self.experimentos.pop(seleccion)  # Eliminar de la lista

            print(f"\nExperimento '{experimento_eliminado.receta.nombre}' eliminado correctamente.")

            # Preguntar si desea eliminar otro experimento
            continuar = input("\n¿Desea eliminar otro experimento? (s/n): ").strip().lower()
            while continuar not in ["s", "n"]:
                continuar = input("Ingrese 's' para continuar eliminando o 'n' para salir: ").strip().lower()

            if continuar == "n":
                break  # Salir del bucle

    def realizar_experimento(self):
        """
        Ejecuta un experimento, validando reactivos, descontando inventario y generando resultados.
        """
        print("\n===== REALIZAR EXPERIMENTO =====")

        # Listar experimentos disponibles
        if not self.experimentos:
            print("No hay experimentos disponibles para realizar.")
            return

        print("Seleccione un experimento para ejecutar:")
        for i, experimento in enumerate(self.experimentos, start=1):
            print(f"{i}. {experimento.receta.nombre} (ID: {experimento.id})")

        # Validar selección del experimento
        opcion = input("> Ingrese el número del experimento: ")
        while not opcion.isnumeric() or int(opcion) not in range(1, len(self.experimentos) + 1):
            opcion = input("Ingrese una opción válida: ")

        experimento_seleccionado = self.experimentos[int(opcion) - 1]

        # Verificar disponibilidad de reactivos
        for item in experimento_seleccionado.receta.reactivos:
            reactivo = item["reactivo"]
            cantidad_necesaria = item["cantidad"]

            if reactivo.inventario < cantidad_necesaria:
                print(f"Error: No hay suficiente {reactivo.nombre} en inventario ({reactivo.inventario} disponibles, {cantidad_necesaria} requeridos).")
                return
            
            # Verificación de fecha de caducidad simulada
            if reactivo.fecha_caducidad is not None and reactivo.fecha_caducidad < "2024-03-10":  
                print(f"Error: El reactivo {reactivo.nombre} ha caducado y no puede utilizarse.")
                return

        # Descontar del inventario y aplicar error aleatorio
        for item in experimento_seleccionado.receta.reactivos:
            reactivo = item["reactivo"]
            cantidad_necesaria = item["cantidad"]
            error_porcentaje = random.uniform(0.001, 0.225)  # Error entre 0.1% y 22.5%
            cantidad_total = cantidad_necesaria * (1 + error_porcentaje)

            reactivo.inventario -= cantidad_total
            print(f"Se han descontado {cantidad_total:.2f} {reactivo.unidad_medida} de {reactivo.nombre} (incluye error de {error_porcentaje * 100:.2f}%).")

        # Calcular costo total del experimento
        costo_total = sum(item["reactivo"].costo * item["cantidad"] for item in experimento_seleccionado.receta.reactivos)
        experimento_seleccionado.costo = costo_total

        # Generar valores obtenidos con variación aleatoria
        valores_obtenidos = {}
        valores_aceptables = {}

        for medicion in experimento_seleccionado.receta.valores_a_medir:
            min_valor = medicion.minimo
            max_valor = medicion.maximo
            error_factor = random.uniform(0.0, 1.0)  # Error aleatorio entre 0% y 100%
            valor_obtenido = random.uniform(min_valor, max_valor) * (1 + error_factor)
            valores_obtenidos[medicion.nombre] = round(valor_obtenido, 2)
            valores_aceptables[medicion.nombre] = (min_valor, max_valor)

        # Crear resultado del experimento y evaluar si está dentro de los valores aceptables
        resultado = Resultado(experimento_seleccionado, valores_obtenidos, valores_aceptables)
        self.resultados.append(resultado)

        print("\nExperimento realizado con éxito.")
        print(resultado.__str__())

    
    def menu_resultados(self):
        """
        Muestra el menú de gestión de resultados y permite visualizar o graficar los datos.
        """
        while True:
            print("\n===== GESTIÓN DE RESULTADOS =====")
            print("1. Ver Resultados de Experimentos")
            print("2. Graficar Resultados")
            print("3. Salir")

            # Validar la opción ingresada
            opcion = input("\nSeleccione una opción: ")
            while not opcion.isnumeric() or int(opcion) not in range(1, 4):
                print("Error: Ingrese un número válido de la lista.")
                opcion = input("\nSeleccione una opción: ")

            opcion = int(opcion)

            # Redirección según la opción seleccionada
            if opcion == 1:
                self.ver_resultados()
            elif opcion == 2:
                self.graficar_resultados()
            else:
                print("\nSaliendo del módulo de resultados.")
                break  # Regresa al menú principal
    
    def ver_resultados(self):
        """
        Muestra la lista de resultados registrados y permite visualizar los detalles de un experimento específico.
        """
        if not self.resultados:
            print("\nNo hay resultados registrados.")
            return

        print("\n===== LISTA DE RESULTADOS =====")
        for i, resultado in enumerate(self.resultados, start=1):
            print(f"{i}. {resultado.experimento.receta.nombre} - Fecha: {resultado.experimento.fecha} - "
                f"Evaluación: {'Dentro de parámetros' if resultado.valido else 'Fuera de parámetros'}")

        # Selección de un resultado para ver detalles
        seleccion = input("\nSeleccione el número del resultado para ver detalles o '0' para salir: ")
        while not seleccion.isnumeric() or int(seleccion) not in range(0, len(self.resultados) + 1):
            print("Error: Ingrese un número válido de la lista.")
            seleccion = input("\nSeleccione el número del resultado para ver detalles o '0' para salir: ")

        if int(seleccion) > 0:
            print(self.resultados[int(seleccion) - 1])  # Muestra los detalles del resultado seleccionado

    def graficar_resultados(self):
        """
        Genera una gráfica de dispersión comparando los valores obtenidos con los valores aceptables de un experimento.
        """
        if not self.resultados:
            print("\nNo hay resultados registrados para graficar.")
            return

        print("\n===== SELECCIONAR RESULTADO A GRAFICAR =====")
        for i, resultado in enumerate(self.resultados, start=1):
            print(f"{i}. {resultado.experimento.receta.nombre} - Fecha: {resultado.experimento.fecha}")

        # Validar selección del resultado
        seleccion = input("\nSeleccione el número del resultado a graficar: ")
        while not seleccion.isnumeric() or int(seleccion) not in range(1, len(self.resultados) + 1):
            print("Error: Ingrese un número válido de la lista.")
            seleccion = input("\nSeleccione el número del resultado a graficar: ")

        resultado = self.resultados[int(seleccion) - 1]

        # Extraer datos para la gráfica
        mediciones = list(resultado.valores_obtenidos.keys())
        valores_obtenidos = [resultado.valores_obtenidos[m] for m in mediciones]
        valores_minimos = [resultado.valores_aceptables[m][0] for m in mediciones]
        valores_maximos = [resultado.valores_aceptables[m][1] for m in mediciones]

        x = range(len(mediciones))  # Índices para el eje X

        # Configuración de la gráfica
        plt.figure(figsize=(10, 5))
        plt.scatter(x, valores_obtenidos, color="blue", label="Obtenido", zorder=3)
        plt.scatter(x, valores_minimos, color="red", label="Mínimo", zorder=3)
        plt.scatter(x, valores_maximos, color="green", label="Máximo", zorder=3)

        # Personalización del gráfico
        plt.xticks(ticks=x, labels=mediciones, rotation=45)
        plt.ylabel("Valores")
        plt.title(f"Resultados de {resultado.experimento.receta.nombre}")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6, zorder=0)
        
        # Mostrar la gráfica
        plt.show()

    def menu_estadisticas(self):
        """
        Muestra el menú de estadísticas y permite acceder a diferentes análisis de uso del laboratorio.
        """
        while True:
            print("\n===== MENÚ ESTADÍSTICAS =====")
            print("1. Investigadores que más utilizan el laboratorio")
            print("2. Experimentos más y menos realizados")
            print("3. Top 5 reactivos con más alta rotación")
            print("4. Top 3 reactivos con mayor desperdicio")
            print("5. Reactivos que más se vencen")
            print("6. Veces que no se logró hacer un experimento por falta de reactivos")
            print("7. Salir")

            # Validar la opción ingresada
            opcion = input("\nSeleccione una opción: ")
            while not opcion.isnumeric() or int(opcion) not in range(1, 8):
                print("Error: Ingrese un número válido.")
                opcion = input("\nSeleccione una opción: ")

            opcion = int(opcion)

            # Redirigir según la opción seleccionada
            if opcion == 1:
                self.estadistica_investigadores()
            elif opcion == 2:
                self.estadistica_experimentos()
            elif opcion == 3:
                self.estadistica_reactivos_mas_usados()
            elif opcion == 4:
                self.estadistica_mayor_desperdicio()
            elif opcion == 5:
                self.estadistica_reactivos_vencidos()
            elif opcion == 6:
                self.estadistica_experimentos_fallidos()
            else:
                print("\nSaliendo del módulo de estadísticas.")
                break  # Regresa al menú principal

    def estadistica_investigadores(self):
        """
        Muestra los investigadores que más han realizado experimentos en el laboratorio.
        """
        investigadores = {}

        # Contar la cantidad de experimentos realizados por cada investigador
        for experimento in self.experimentos:
            for responsable in experimento.responsables:
                if responsable in investigadores:
                    investigadores[responsable] += 1
                else:
                    investigadores[responsable] = 1

        if not investigadores:
            print("\nNo hay datos de investigadores.")
            return

        # Convertir a lista de tuplas y ordenar por cantidad de experimentos en orden descendente
        top_investigadores = sorted(investigadores.items(), key=lambda x: x[1], reverse=True)

        print("\n===== INVESTIGADORES QUE MÁS USAN EL LABORATORIO =====")

        # Mostrar los 5 investigadores con más experimentos
        for i, (investigador, cantidad) in enumerate(top_investigadores[:5], start=1):
            print(f"{i}. {investigador}: {cantidad} experimentos realizados")


    def estadistica_experimentos(self):
        """
        Muestra el experimento más realizado y el menos realizado en el laboratorio.
        """
        conteo_experimentos = {}

        # Contar la cantidad de veces que se ha realizado cada experimento
        for experimento in self.experimentos:
            nombre = experimento.receta.nombre
            if nombre in conteo_experimentos:
                conteo_experimentos[nombre] += 1
            else:
                conteo_experimentos[nombre] = 1

        if not conteo_experimentos:
            print("\nNo hay datos de experimentos realizados.")
            return

        # Determinar el experimento más y menos realizado
        max_experimento = None
        min_experimento = None
        max_valor = float('-inf')
        min_valor = float('inf')

        for nombre, cantidad in conteo_experimentos.items():
            if cantidad > max_valor:
                max_valor = cantidad
                max_experimento = nombre
            if cantidad < min_valor:
                min_valor = cantidad
                min_experimento = nombre

        print("\n===== EXPERIMENTOS MÁS Y MENOS REALIZADOS =====")
        print(f"Más realizado: {max_experimento} ({max_valor} veces)")
        print(f"Menos realizado: {min_experimento} ({min_valor} veces)")


    def estadistica_reactivos_mas_usados(self):
        """
        Muestra los 5 reactivos más utilizados en los experimentos.
        """
        reactivos_usados = {}

        # Contar la cantidad total utilizada de cada reactivo
        for experimento in self.experimentos:
            for reactivo_info in experimento.receta.reactivos:
                reactivo = reactivo_info["reactivo"]
                cantidad = reactivo_info["cantidad"]
                if reactivo.nombre in reactivos_usados:
                    reactivos_usados[reactivo.nombre] += cantidad
                else:
                    reactivos_usados[reactivo.nombre] = cantidad

        if not reactivos_usados:
            print("\nNo hay datos de reactivos utilizados.")
            return

        # Convertir a lista de tuplas y ordenar por cantidad de uso en orden descendente
        top_reactivos = sorted(reactivos_usados.items(), key=lambda x: x[1], reverse=True)

        print("\n===== TOP 5 REACTIVOS CON MÁS USO =====")

        # Mostrar los 5 reactivos más utilizados
        for i, (reactivo, cantidad) in enumerate(top_reactivos[:5], start=1):
            print(f"{i}. {reactivo}: {cantidad} unidades utilizadas")

    def estadistica_mayor_desperdicio(self):
        """
        Muestra los 3 reactivos con mayor desperdicio en los experimentos.
        """
        desperdicio_reactivos = {}

        # Calcular el desperdicio de cada reactivo en los experimentos
        for experimento in self.experimentos:
            for reactivo_info in experimento.receta.reactivos:
                reactivo = reactivo_info["reactivo"]
                cantidad = reactivo_info["cantidad"]
                desperdicio = cantidad * random.uniform(0.01, 0.3)  # Simulación de desperdicio (1% a 30%)

                if reactivo.nombre in desperdicio_reactivos:
                    desperdicio_reactivos[reactivo.nombre] += desperdicio
                else:
                    desperdicio_reactivos[reactivo.nombre] = desperdicio

        if not desperdicio_reactivos:
            print("\nNo hay datos de desperdicio de reactivos.")
            return

        # Convertir a lista de tuplas y ordenar por mayor desperdicio en orden descendente
        top_despilfarro = sorted(desperdicio_reactivos.items(), key=lambda x: x[1], reverse=True)

        print("\n===== TOP 3 REACTIVOS CON MAYOR DESPERDICIO =====")

        # Mostrar los 3 reactivos con más desperdicio
        for i, (reactivo, cantidad) in enumerate(top_despilfarro[:3], start=1):
            print(f"{i}. {reactivo}: {cantidad:.2f} unidades desperdiciadas")

    def estadistica_reactivos_vencidos(self):
        """
        Muestra los reactivos que han vencido según la fecha de caducidad.
        """
        vencidos = []

        # Buscar reactivos cuya fecha de caducidad haya pasado
        for reactivo in self.reactivos:
            if reactivo.fecha_caducidad != "No aplica" and reactivo.fecha_caducidad < str(datetime.today().date()):
                vencidos.append(reactivo)

        if not vencidos:
            print("\nNo hay reactivos vencidos.")
            return

        print("\n===== REACTIVOS VENCIDOS =====")
        for reactivo in vencidos:
            print(f"{reactivo.nombre} - Venció el {reactivo.fecha_caducidad}")


    def estadistica_experimentos_fallidos(self):
        """
        Cuenta cuántos experimentos no se pudieron realizar por falta de inventario de reactivos.
        """
        fallidos = 0

        # Contar experimentos fallidos debido a falta de reactivos
        for experimento in self.experimentos:
            for reactivo_info in experimento.receta.reactivos:
                reactivo = reactivo_info["reactivo"]
                cantidad = reactivo_info["cantidad"]

                if reactivo.inventario < cantidad:
                    fallidos += 1
                    break  # Si un reactivo falta, no es necesario revisar los demás

        print(f"\n===== EXPERIMENTOS NO REALIZADOS POR FALTA DE REACTIVOS =====")
        print(f"Total: {fallidos}")

