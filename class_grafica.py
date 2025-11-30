from matplotlib import pyplot as plt

class Graficos:

    def grafico_libros_prestados(self, conteo, lista_libros):
        ids = list(conteo.keys())
        valores = list(conteo.values())
        nombres = [next(l.titulo for l in lista_libros if l.id_libro == i) for i in ids]

        plt.figure(figsize=(10,5))
        plt.bar(nombres, valores)
        plt.xticks(rotation=45, ha="right")
        plt.title("Préstamos por libro")
        plt.ylabel("Cantidad de préstamos")
        plt.tight_layout()
        plt.show()

    def grafico_usuarios_prestamos(self, conteo, lista_usuarios):
        ids = list(conteo.keys())
        valores = list(conteo.values())
        nombres = [next(u.nombre for u in lista_usuarios if u.id_usuario == i) for i in ids]

        plt.figure(figsize=(10,5))
        plt.bar(nombres, valores)
        plt.xticks(rotation=45, ha="right")
        plt.title("Préstamos por usuario")
        plt.ylabel("Cantidad de préstamos")
        plt.tight_layout()
        plt.show()

    def grafico_tiempos_prestamos(self, lista_prestamos):
        valores = []
        indices = []

        for i, prestamo in enumerate(lista_prestamos):
            if prestamo.dia_fin is not None:
                duracion = prestamo.dia_fin - prestamo.dia_inicio
                valores.append(duracion)
                indices.append(i+1)

        plt.figure(figsize=(10,5))
        plt.plot(indices, valores, marker="o")
        plt.title("Variación del tiempo de préstamo")
        plt.xlabel("Número de préstamo finalizado")
        plt.ylabel("Días del préstamo")
        plt.grid()
        plt.tight_layout()
        plt.show()

    def grafico_penalidades(self, lista_prestamos, lista_usuarios):
        conteo = {}
        for i in lista_prestamos:
            if i.penalidad > 0:
                id_user = i.usuario.id_usuario
                conteo[id_user] = conteo.get(id_user, 0) + i.penalidad

        if not conteo:
            print("\n(No hay penalidades registradas)")
            return

        ids = list(conteo.keys())
        valores = list(conteo.values())

        nombres = [next(j.nombre for j in lista_usuarios if j.id_usuario == i) for i in ids]

        total = sum(valores)

        etiquetas = [f"{n} - S/{v}" for n, v in zip(nombres, valores)]

        plt.figure(figsize=(8, 6))
        plt.pie(valores, labels=etiquetas, autopct='%1.1f%%')
        plt.title("Penalidad total por usuario")

        plt.figtext(0.5, 0.02, f"TOTAL RECAUDADO: S/{total}", ha="center", fontsize=12)

        plt.tight_layout()
        plt.show()