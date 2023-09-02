def RegistroNotas():
    # Opción 1. Registrar una nota.
    while True:
        nombre_cliente = input("Ingresa el nombre del cliente (Dejar vacío para regresar al menú principal): ")
        if nombre_cliente.strip() == "":
            break

        detalles_servicios = []

        while True:
            fecha_capturada = input("Ingresa la fecha (dd/mm/yyyy): ")
            try:
                fecha_procesada = datetime.datetime.strptime(fecha_capturada,"%d/%m/%Y").date()
            except Exception:
                print("¡ERROR! Fecha inválida. Asegurate de seguir el formato dd/mm/yyyy.")
            else:
                if fecha_procesada < datetime.date.today():
                    break
                else:
                    print("¡ERROR! La fecha ingresada es posterior a la fecha actual del sistema, por favor ingrese una fecha válida.")   
                    continue

        while True:
            servicios = input("Ingrese el nombre del servicio: ")
            if servicios.strip() == "":
                print("¡ERROR! El nombre del servicio no puede quedar vacío. Intenta de nuevo.")
                continue

            while True:
                costo = input("Ingrese el costo del servicio: ")
                if costo.strip() == "":
                    print("¡ERROR! El costo del servicio no puede quedar vacío. Intenta de nuevo.")
                    continue

                try:
                    costo_servicio = float(costo)
                except Exception:
                    print("¡ERROR! El costo de servicio solamente acepta dígitos. Intenta de nuevo.")
                    continue
                else:
                    if costo_servicio > 0:
                        break
                    else:
                        print("¡ERROR! El costo de servicio debe ser mayor a 0. Intenta de nuevo.")
                        continue

            detalles_servicios.append({"servicios": servicios, "costo_servicio": costo_servicio})

            respuesta = input("¿Deseas seguir agregando servicios [SI / NO]? >> ")
            if respuesta.upper() != "SI":
                break
        
        monto_a_pagar = sum(detalle["costo_servicio"] for detalle in detalles_servicios)

        folio = max(notas.keys(), default=0) + 1

        notas[folio] = (fecha_procesada, nombre_cliente, detalles_servicios, monto_a_pagar)

# Menú Principal
import datetime

notas = {}

print("¡Bienvenido/a!")
while True:
    print("\n¿Qué desea realizar el día de hoy?\n(1) Registrar una nota / (2) Consultas y reportes / (3) Cancelar una nota / (4) Recuperar una nota / (5) Salir del sistema")
    opcion = int(input(">> "))

    match opcion:
        case 1:
            RegistroNotas()
        case 2:
            # ConsultasReportes()
            print("Aquí va la parte de consultas y reportes. Quitar esta línea.")
        case 3:
            # CancelarNota()
            print("Aquí va la parte de cancelar notas. Quitar esta línea.")
        case 4:
            # RecuperarNota()
            print("Aquí va la parte de recuperar notas. Quitar esta línea.")
        case 5:
            print("\nGracias por visitar este sistema. ¡Vuelva pronto!")
            break
        case _:
            print("Opción no válida.")