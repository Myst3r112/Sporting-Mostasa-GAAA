class Usuario:
    def __init__(self, id_usuario: int, nombre: str, clave: str):
        self.__id_usuario = id_usuario
        self.__nombre = nombre
        self.__clave = clave
        self.__prestamos_activos = []
        self.__historial = []

    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def nombre(self):
        return self.__nombre

    @property
    def clave(self):
        return self.__clave

    @property
    def prestamos_activos(self):
        return self.__prestamos_activos

    @property
    def historial(self):
        return self.__historial

    def __str__(self):
        return f"[{self.__id_usuario}] {self.__nombre}"
