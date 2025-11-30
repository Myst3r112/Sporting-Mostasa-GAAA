class Libro:
    def __init__(self, id_libro: int, titulo: str, autor: str, anio: int):
        self.__id_libro = id_libro
        self.__titulo = titulo
        self.__autor = autor
        self.__anio = anio
        self.__estado = True  # True = disponible, False = prestado

    @property
    def id_libro(self):
        return self.__id_libro

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):
        self.__titulo = valor

    @property
    def autor(self):
        return self.__autor

    @autor.setter
    def autor(self, valor):
        self.__autor = valor

    @property
    def anio(self):
        return self.__anio

    @anio.setter
    def anio(self, valor):
        self.__anio = valor

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        self.__estado = valor

    def __str__(self):
        estado_str = "Disponible" if self.__estado else "Prestado"
        return f"[{self.__id_libro}] {self.__titulo} - {self.__autor} ({self.__anio}) - {estado_str}"
