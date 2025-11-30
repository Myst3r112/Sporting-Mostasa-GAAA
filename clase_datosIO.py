import pandas as pd
from clase_libro import Libro
from clase_usuario import Usuario
from clase_prestamo import Prestamo

class DatosIO:
    def __init__(self):
        self.__archivo_libros = "excel_libros.xlsx"
        self.__archivo_usuarios = "excel_usuarios.xlsx"
        self.__archivo_prestamos = "excel_prestamos.xlsx"

    # ========= LIBROS =========
    def cargar_libros(self):
        lista_libros = []
        try:
            df = pd.read_excel(self.__archivo_libros)
        except:
            return lista_libros

        for _, fila in df.iterrows():
            try:
                libro = Libro(
                    int(fila["id_libro"]),
                    str(fila["titulo"]),
                    str(fila["autor"]),
                    int(fila["anio"])
                )
                libro.estado = bool(fila["estado"])
                lista_libros.append(libro)
            except:
                continue

        return lista_libros

    def guardar_libros(self, lista_libros):
        datos = []
        for libro in lista_libros:
            datos.append({
                "id_libro": libro.id_libro,
                "titulo": libro.titulo,
                "autor": libro.autor,
                "anio": libro.anio,
                "estado": libro.estado
            })

        df = pd.DataFrame(datos)
        df.to_excel(self.__archivo_libros, index=False)

    # ========= USUARIOS =========
    def cargar_usuarios(self):
        lista_usuarios = []
        try:
            df = pd.read_excel(self.__archivo_usuarios)
        except:
            return lista_usuarios

        for _, fila in df.iterrows():
            try:
                usuario = Usuario(
                    int(fila["id_usuario"]),
                    str(fila["nombre"]),
                    str(fila["clave"])
                )
                lista_usuarios.append(usuario)
            except:
                continue

        return lista_usuarios

    def guardar_usuarios(self, lista_usuarios):
        datos = []
        for usuario in lista_usuarios:
            datos.append({
                "id_usuario": usuario.id_usuario,
                "nombre": usuario.nombre,
                "clave": usuario.clave
            })

        df = pd.DataFrame(datos)
        df.to_excel(self.__archivo_usuarios, index=False)

    # ========= PRESTAMOS =========
    def cargar_prestamos(self, lista_libros, lista_usuarios):
        lista_prestamos = []
        try:
            df = pd.read_excel(self.__archivo_prestamos)
        except:
            return lista_prestamos

        for _, fila in df.iterrows():
            libro = next((l for l in lista_libros if l.id_libro == fila["id_libro"]), None)
            usuario = next((u for u in lista_usuarios if u.id_usuario == fila["id_usuario"]), None)

            if libro is None or usuario is None:
                continue

            prestamo = Prestamo(
                libro,
                usuario,
                int(fila["dia_inicio"]),
                None if pd.isna(fila["dia_fin"]) else int(fila["dia_fin"]),
                float(fila["penalidad"])
            )
            lista_prestamos.append(prestamo)

        return lista_prestamos

    def guardar_prestamos(self, lista_prestamos):
        datos = []
        for prestamo in lista_prestamos:
            datos.append({
                "id_libro": prestamo.libro.id_libro,
                "id_usuario": prestamo.usuario.id_usuario,
                "dia_inicio": prestamo.dia_inicio,
                "dia_fin": prestamo.dia_fin,
                "penalidad": prestamo.penalidad
            })

        df = pd.DataFrame(datos)
        df.to_excel(self.__archivo_prestamos, index=False)
