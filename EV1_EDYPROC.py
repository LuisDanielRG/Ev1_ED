def RegistroNotas():
    # Opción 1. Registrar una nota.
    while True:
        nombre_cliente = input("Ingresa el nombre del cliente (Dejar vacío para regresar al menú principal): ")
        if nombre_cliente.strip() == "":
            break
        if nombre_cliente == float:
            print("Error, el caracter que usted ingreso es numerico. Vuelva a intentarlo")
            continue

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

        folio = len(notas) + 1
        #folio = max(notas.keys(), default=0) + 1

        #Modifique tantito para acomplar a lo mio, como quiera puse lo tuyo como comentario por si acaso. Atte: Daniel

        #notas[folio] = (fecha_procesada, nombre_cliente, detalles_servicios, monto_a_pagar)
        notas[folio] = {"fecha": fecha_procesada, "cliente": nombre_cliente, "detalle": detalles_servicios, "monto_a_pagar": monto_a_pagar}
        print(f"Nota registrada con éxito. Folio: {folio}")

def ConsultasReportes():

    def ConsultaPorPeriodo():
        # Opción 2.1 Consulta por período.
        fecha_inicial = input("Ingrese la fecha inicial (dd/mm/yyyy): ")
        fecha_final = input("Ingrese la fecha final (dd/mm/yyyy): ")

        try:
            fecha_inicial = datetime.datetime.strptime(fecha_inicial, "%d/%m/%Y").date()
            fecha_final = datetime.datetime.strptime(fecha_final, "%d/%m/%Y").date()
        except Exception:
            print("¡ERROR! Fecha inválida. Asegúrate de seguir el formato dd/mm/yyyy.")
            return

        notas_periodo = [nota for nota in notas.values() if fecha_inicial <= nota["fecha"] <= fecha_final]

        if notas_periodo:
            print("\nReporte de notas por período:")
            for folio, nota in notas.items():
                if nota in notas_periodo:
                    print(f"___________________________________________")
                    print(f"Folio: {folio}")
                    print(f"___________________________________________")
                    print(f"Fecha: {nota['fecha']}")
                    print(f"___________________________________________")
                    print(f"Cliente: {nota['cliente']}")
                    print(f"___________________________________________")
                    print(f"Monto a pagar: {nota['monto_a_pagar']}")
                    print(f"___________________________________________")
                    print()
        else:
            print("\nNo hay notas emitidas para el período especificado.")

    def ConsultaPorFolio():
        # Opción 2.2 Consulta por folio.
        folio = int(input("Ingrese el folio de la nota a consultar: "))

        if folio in notas:
            nota = notas[folio]
            print("\nDetalle de la nota:")
            print(f"Folio: {folio}")
            print(f"Fecha: {nota['fecha']}")
            print(f"Cliente: {nota['cliente']}")
            print(f"Monto a pagar: {nota['monto_a_pagar']}")
            print("Detalle de servicios:")
            for detalle in nota['detalle']:
                print(f"___________________________________________")
                print(f"- Servicio: {detalle['servicios']}")
                print(f"___________________________________________")
                print(f"  Costo: {detalle['costo_servicio']}")
                print(f"___________________________________________")
        else:
            print("\nLa nota no se encuentra en el sistema.")

    while True:
            print("\nMenú de Consultas y Reportes:")
            print("1. Consulta por período")
            print("2. Consulta por folio")
            print("3. Volver al menú principal")

            sub_opcion = int(input("Seleccione una opción: "))

            if sub_opcion == 1:
                ConsultaPorPeriodo()
            elif sub_opcion == 2:
                ConsultaPorFolio()
            elif sub_opcion == 3:
                break
            else:
                print("Opción no válida.")

def CancelarNota():
    folio = int(input("Ingrese el numero de folio de la nota que desea cancelar: "))

    if folio in notas:
        nota = notas[folio]
        print("\nDetalle de la nota a cancelar:")
        print(f"Folio: {folio}")
        print(f"Fecha: {nota['fecha']}")
        print(f"Cliente: {nota['cliente']}")
        print(f"Monto a pagar: {nota['monto_a_pagar']}")
        print("Detalle de servicios:")
        for detalle in nota['detalle']:
            print(f"- Servicio: {detalle['servicios']}")
            print(f"  Costo: {detalle['costo_servicio']}")
        
        confirmacion = input("¿Está seguro de que desea cancelar esta nota? (S/N): ")
        if confirmacion.lower() == "s":
            del notas[folio]
            notas_canceladas[folio] = nota
            print("Nota cancelada exitosamente.")
        else:
            print("Cancelación de nota cancelada.")
    else:
        print("\nLa nota no se encuentra en el sistema.")

def RecuperarNota():
    #para que funcione ocupa que en la parte de cancelar nota exista la lista notas_canceladas en donde se guarden todas las notas canceladas :)
    #La funcion funciona trayendo de vuelta una nota cancelada de la lista notas_canceladas y volviendola a poner en la lista de notas 
    
    while True:
        print("Desea Recuperar nota o Salir")
        opcion = input("[R]  [S]\n")
        if opcion.upper() == "S":
            
            break
        if opcion.upper() == 'R':
            clear()
            
            folio = int(input("Ingrese el folio de la nota que quieras recuperar: "))
            
            if folio in notas_canceladas:
                nota = notas_canceladas[folio]
                print("\nDetalle de la nota recuperada:")
                print(f"Folio: {folio}")
                print(f"Fecha: {nota['fecha']}")
                print(f"Cliente: {nota['cliente']}")
                print(f"Monto a pagar: {nota['monto_a_pagar']}")
                print("Detalle de servicios:")
                for detalle in nota['detalle']:
                    print(f"- Servicio: {detalle['servicios']}")
                    print(f"  Costo: {detalle['costo_servicio']}")
                del notas_canceladas[folio]
                notas[folio] = nota 
                print("La nota se recupero exitosamente .")
            else:
                print("\nEl folio ingresado no corresponde a una nota cancelada.")
        
        
        
    

notas_canceladas = {} 
    

# Menú Principal
import os
import datetime
clear = lambda: os.system('cls') 

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
            ConsultasReportes()
        case 3:
            # CancelarNota()
            CancelarNota()
        case 4:
            # RecuperarNota()
            RecuperarNota()
        case 5:
            print("\nGracias por visitar este sistema. ¡Vuelva pronto!")
            break
        case _:
            print("Opción no válida.")
