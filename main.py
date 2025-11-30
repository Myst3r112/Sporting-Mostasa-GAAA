from clase_biblioteca import Biblioteca

def main():
    biblioteca = Biblioteca("Biblioteca Central")
    biblioteca.cargar_archivos()

    while True:
        opcion = biblioteca.menu()

        match opcion:
            case 1:
                biblioteca.registrar_usuario()
            case 2:
                biblioteca.registrar_libro()
            case 3:
                biblioteca.ver_libros()
            case 4:
                biblioteca.hacer_prestamo()
            case 5:
                biblioteca.devolver_libro()
            case 6:
                biblioteca.ver_penalidades_usuario()
            case 7:
                opcion_menu = biblioteca.menu_reportes()
                match opcion_menu:
                    case 1:
                        biblioteca.libro_mas_prestado()
                    case 2:
                        biblioteca.usuario_mas_prestamos()
                    case 3:
                        biblioteca.tiempo_promedio_prestamos()
                    case 4:
                        biblioteca.recaudacion_total_penalidades()
            case 8:
                Biblioteca.cambiar_dia_actual()
            case 9:
                biblioteca.guardar_archivos()
                print("\nGracias por usar el sistema.")
                break

if __name__ == "__main__":
    main()
