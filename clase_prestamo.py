class Prestamo:
    def __init__(self, libro, usuario, dia_inicio: int, dia_fin: int = None, penalidad: float = 0.0):
        self.__libro = libro
        self.__usuario = usuario
        self.__dia_inicio = dia_inicio
        self.__dia_fin = dia_fin
        self.__penalidad = penalidad

    @property
    def libro(self):
        return self.__libro

    @property
    def usuario(self):
        return self.__usuario

    @property
    def dia_inicio(self):
        return self.__dia_inicio

    @property
    def dia_fin(self):
        return self.__dia_fin

    @property
    def penalidad(self):
        return self.__penalidad

    def esta_activo(self):
        return self.__dia_fin is None

    def cerrar(self, dia_devolucion: int, penalidad_por_dia: float):
        self.__dia_fin = dia_devolucion
        dias_transcurridos = dia_devolucion - self.__dia_inicio

        if dias_transcurridos > 7:
            self.__penalidad = (dias_transcurridos - 7) * penalidad_por_dia
        else:
            self.__penalidad = 0.0

        return dias_transcurridos, self.__penalidad
