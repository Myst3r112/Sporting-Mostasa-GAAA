from clase_datosIO import DatosIO
from clase_libro import Libro
from clase_usuario import Usuario
from clase_prestamo import Prestamo
from clase_grafica import Graficos

def leer_texto(mensaje: str):
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("\t*El campo es obligatorio*")

def leer_numero(mensaje: str, minimo: int, maximo: int):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and minimo <= int(valor) <= maximo:
            return int(valor)
        print("\t*Ingrese un número válido*")

class Biblioteca:
    __dia_actual = 1
    __penalidad_dia = 10

    def __init__(self, nombre: str):
        self.__nombre = nombre
        self.__lista_libros = []
        self.__lista_usuarios = []
        self.__lista_prestamos = []
        self.__io = DatosIO()
        self.__graficos = Graficos()

    # ======== GETTERS Y SETTERS ========
    @classmethod
    def obtener_dia_actual(cls):
        return cls.__dia_actual

    @classmethod
    def cambiar_dia_actual(cls):
        nuevo_dia = leer_numero("Nuevo día actual: ", 1, 365)
        cls.__dia_actual = nuevo_dia
        print(f"\t*Día actual cambiado a {nuevo_dia}*")

    @classmethod
    def obtener_penalidad_por_dia(cls):
        return cls.__penalidad_dia

    # ======== CARGAR Y GUARDAR ========
    def cargar_archivos(self):
        self.__lista_libros = self.__io.cargar_libros()
        self.__lista_usuarios = self.__io.cargar_usuarios()
        self.__lista_prestamos = self.__io.cargar_prestamos(self.__lista_libros, self.__lista_usuarios)

        for usuario in self.__lista_usuarios:
            usuario.prestamos_activos.clear()

        for libro in self.__lista_libros:
            libro.estado = True

        for prestamo in self.__lista_prestamos:
            if prestamo.esta_activo():
                prestamo.usuario.prestamos_activos.append(prestamo)
                prestamo.libro.estado = False

        print("Datos cargados correctamente.\n")

    def guardar_archivos(self):
        self.__io.guardar_libros(self.__lista_libros)
        self.__io.guardar_usuarios(self.__lista_usuarios)
        self.__io.guardar_prestamos(self.__lista_prestamos)
        print("\t*Datos guardados en Excel*")

    # ======== BUSCAR ========
    def buscar_usuario_por_nombre(self, nombre):
        return next((u for u in self.__lista_usuarios if u.nombre == nombre), None)

    def buscar_usuario_por_id(self, id_usuario):
        return next((u for u in self.__lista_usuarios if u.id_usuario == id_usuario), None)

    def buscar_libro_por_id(self, id_libro):
        return next((l for l in self.__lista_libros if l.id_libro == id_libro), None)

    # ======== LOGIN ========
    def iniciar_sesion(self):
        print("\n===== Iniciar Sesión =====")
        nombre = leer_texto("Usuario: ")
        clave = leer_texto("Clave: ")

        usuario = self.buscar_usuario_por_nombre(nombre)

        if usuario and usuario.clave == clave:
            return usuario

        print("\t*Credenciales incorrectas*")
        return None

    # ======== REGISTRO ========
    def registrar_usuario(self):
        print("\n===== Registro de Usuario =====")
        nombre = leer_texto("Nombre: ")
        clave = leer_texto("Clave: ")

        if self.buscar_usuario_por_nombre(nombre):
            print("\t*El usuario ya existe*")
            return

        nuevo_id = len(self.__lista_usuarios) + 1
        usuario = Usuario(nuevo_id, nombre, clave)
        self.__lista_usuarios.append(usuario)

        print("\t*Usuario registrado exitosamente*")

    def registrar_libro(self):
        print("\n===== Registro de Libro =====")
        titulo = leer_texto("Título: ")
        autor = leer_texto("Autor: ")
        anio = leer_numero("Año: ", 1, 2025)

        nuevo_id = len(self.__lista_libros) + 1
        libro = Libro(nuevo_id, titulo, autor, anio)
        self.__lista_libros.append(libro)

        print("\t*Libro registrado exitosamente*")

    # ======== LISTAR LIBROS ========
    def ver_libros(self):
        if not self.__lista_libros:
            print("\n*No hay libros registrados*")
            return

        print("\n===== Lista de Libros =====")
        print(f"{'ID':^4} {'Título':^25} {'Autor':^20} {'Año':^6} {'Estado':^10}")

        for libro in self.__lista_libros:
            estado = "Disponible" if libro.estado else "Prestado"
            print(f"{libro.id_libro:^4} {libro.titulo[:25]:^25} {libro.autor[:20]:^20} {libro.anio:^6} {estado:^10}")

    # ======== PRESTAR ========
    def hacer_prestamo(self):
        print("\n===== Nuevo Préstamo =====")
        usuario = self.iniciar_sesion()

        if usuario is None:
            return

        if len(usuario.prestamos_activos) >= 3:
            print("\t*El usuario ya tiene 3 préstamos activos*")
            return

        self.ver_libros()
        id_libro = leer_numero("ID del libro a prestar: ", 1, 999999)

        libro = self.buscar_libro_por_id(id_libro)

        if libro is None:
            print("\t*El libro no existe*")
            return

        if not libro.estado:
            print("\t*El libro no está disponible*")
            return

        dia_actual = Biblioteca.obtener_dia_actual()
        prestamo = Prestamo(libro, usuario, dia_actual)

        self.__lista_prestamos.append(prestamo)
        usuario.prestamos_activos.append(prestamo)
        libro.estado = False

        print("\t*Préstamo registrado exitosamente*")

    # ======== DEVOLVER ========
    def devolver_libro(self):
        print("\n===== Devolver Libro =====")
        usuario = self.iniciar_sesion()

        if usuario is None:
            return

        prestamos_activos = [p for p in usuario.prestamos_activos if p.esta_activo()]

        if not prestamos_activos:
            print("\t*El usuario no tiene préstamos activos*")
            return

        print("\nPréstamos Activos:")
        print(f"{'Nro':^4} {'ID Libro':^8} {'Título':^25} {'Día inicio':^10}")

        for indice, prestamo in enumerate(prestamos_activos):
            print(f"{indice+1:^4} {prestamo.libro.id_libro:^8} {prestamo.libro.titulo[:25]:^25} {prestamo.dia_inicio:^10}")

        opcion = leer_numero("Seleccione número: ", 1, len(prestamos_activos))
        prestamo_seleccionado = prestamos_activos[opcion - 1]

        dia_devolucion = leer_numero(
            f"Día de devolución (>= {prestamo_seleccionado.dia_inicio}): ",
            prestamo_seleccionado.dia_inicio,
            365
        )

        dias, penalidad = prestamo_seleccionado.cerrar(
            dia_devolucion, Biblioteca.obtener_penalidad_por_dia()
        )

        usuario.prestamos_activos.remove(prestamo_seleccionado)
        prestamo_seleccionado.libro.estado = True

        print(f"\n*Devolución registrada*")
        print(f"Días del préstamo: {dias}")
        print(f"Penalidad: S/ {penalidad}")

    # ======== PENALIDADES ========
    def ver_penalidades_usuario(self):
        print("\n===== Penalidades del Usuario =====")
        usuario = self.iniciar_sesion()

        if usuario is None:
            return

        print(f"\nHistorial de préstamos de {usuario.nombre}:")
        print(f"{'ID Libro':^10} {'Título':^25} {'Inicio':^10} {'Fin':^10} {'Penalidad':^10}")

        total = 0

        for prestamo in self.__lista_prestamos:
            if prestamo.usuario.id_usuario == usuario.id_usuario and prestamo.dia_fin is not None:
                print(f"{prestamo.libro.id_libro:^10} {prestamo.libro.titulo[:25]:^25} "
                      f"{prestamo.dia_inicio:^10} {prestamo.dia_fin:^10} {prestamo.penalidad:^10}")
                total += prestamo.penalidad

        print(f"\nPenalidad total: S/ {total}")

    # ======== REPORTES ========
    def libro_mas_prestado(self):
        if not self.__lista_prestamos:
            print("\n*No hay préstamos registrados*")
            return

        conteo = {}
        for prestamo in self.__lista_prestamos:
            id_libro = prestamo.libro.id_libro
            conteo[id_libro] = conteo.get(id_libro, 0) + 1

        id_top = max(conteo, key=conteo.get)
        libro = self.buscar_libro_por_id(id_top)

        print(f'\nLibro más prestado: "{libro.titulo}" (ID {libro.id_libro}) con {conteo[id_top]} préstamos')
        self.__graficos.grafico_libros_prestados(conteo, self.__lista_libros)

    def usuario_mas_prestamos(self):
        if not self.__lista_prestamos:
            print("\n*No hay préstamos registrados*")
            return

        conteo = {}
        for prestamo in self.__lista_prestamos:
            id_usuario = prestamo.usuario.id_usuario
            conteo[id_usuario] = conteo.get(id_usuario, 0) + 1

        id_top = max(conteo, key=conteo.get)
        usuario = self.buscar_usuario_por_id(id_top)

        print(f'\nUsuario con más préstamos: "{usuario.nombre}" (ID {usuario.id_usuario}) con {conteo[id_top]} préstamos')
        self.__graficos.grafico_usuarios_prestamos(conteo, self.__lista_usuarios)

    def tiempo_promedio_prestamos(self):
        suma = 0
        cantidad_prestamos = 0

        for prestamo in self.__lista_prestamos:
            if prestamo.dia_fin is not None:
                suma += prestamo.dia_fin - prestamo.dia_inicio
                cantidad_prestamos += 1

        if cantidad_prestamos == 0:
            print("\n*No hay préstamos finalizados*")
            return

        promedio = suma / cantidad_prestamos
        print(f"\nTiempo promedio de préstamo: {promedio:.2f} días")
        self.__graficos.grafico_tiempos_prestamos(self.__lista_prestamos)

    def recaudacion_total_penalidades(self):
        total = sum(p.penalidad for p in self.__lista_prestamos)
        print(f"\nRecaudación total por penalidades: S/ {total}")
        self.__graficos.grafico_penalidades(self.__lista_prestamos, self.__lista_usuarios)

    # ======== MENU REPORTES ========
    def menu_reportes(self):
        print("\n===== MENÚ DE REPORTES =====")
        print("[1] Libro más prestado")
        print("[2] Usuario con más préstamos")
        print("[3] Tiempo promedio de préstamos")
        print("[4] Recaudación por penalidades")
        print("[5] Volver")

        opcion = leer_numero("Opción: ", 1, 5)
        return opcion

    # ======== MENU PRINCIPAL ========
    def menu(self):
        print(f"\nDía actual: {Biblioteca.obtener_dia_actual()}")
        print(f"===== Biblioteca: {self.__nombre} =====")
        print("[1] Registrar usuario")
        print("[2] Registrar libro")
        print("[3] Ver libros")
        print("[4] Hacer préstamo")
        print("[5] Devolver libro")
        print("[6] Ver penalidades por usuario")
        print("[7] Reportes")
        print("[8] Cambiar día actual")
        print("[9] Guardar y salir")

        opcion = leer_numero("Opción: ", 1, 9)
        return opcion
