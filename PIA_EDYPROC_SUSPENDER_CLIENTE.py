def BaseDeDatos():
    try:
        with sqlite3.connect("TallerMecanico.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Clientes (Clave INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, RFC TEXT NOT NULL, Correo TEXT NOT NULL);")
            cursor.execute("CREATE TABLE IF NOT EXISTS ClientesSuspendidos (Clave INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, RFC TEXT NOT NULL, Correo TEXT NOT NULL);")
            cursor.execute("CREATE TABLE IF NOT EXISTS Servicios (Clave INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, Costo REAL NOT NULL, Suspendido TEXT NOT NULL);")
            cursor.execute("CREATE TABLE IF NOT EXISTS Notas (Folio INTEGER PRIMARY KEY, Fecha TIMESTAMP NOT NULL, ClienteID INTEGER NOT NULL, MontoPago REAL NOT NULL, \
                           Estado TEXT NOT NULL, FOREIGN KEY(ClienteID) REFERENCES Clientes(Clave));")
            cursor.execute("CREATE TABLE IF NOT EXISTS DetalleNotas (DetalleID INTEGER PRIMARY KEY, NotaID INTEGER NOT NULL, ServicioID INTEGER NOT NULL, \
                           FOREIGN KEY(NotaID) REFERENCES Notas(Folio), FOREIGN KEY(ServicioID) REFERENCES Servicios(Clave));")
    except Error as error:
        print(f"[red]*** {error} ***[/red]")
    except Exception:
        print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")



def Notas():
    def RegistrarNota():
        try:
            with sqlite3.connect("TallerMecanico.db") as conn:
                cursor = conn.cursor()

                while True:
                    fecha_capturada = input("\nIngresa la fecha en la que se está expidiendo la nota (dd/mm/yyyy): ")
                    try:
                        fecha_nota = datetime.datetime.strptime(fecha_capturada,"%d/%m/%Y").date()
                    except Exception:
                        print("[red]*** ¡ERROR! Fecha inválida. Asegurate de seguir el formato dd/mm/yyyy. ***[/red]")
                    else:
                        # Una vez que la fecha se haya convertido, valida que no sea una fecha futura.
                        if fecha_nota <= datetime.date.today():
                            break
                        else:
                            print("[red]*** ¡ERROR! La fecha ingresada es posterior a la fecha actual del sistema, por favor ingrese una fecha válida. ***[/red]")   
                            continue
                
                cursor.execute("SELECT Clave, Nombre FROM Clientes")
                clientes_registrados = cursor.fetchall()

                if clientes_registrados:
                    encabezado = ["CLAVE", "NOMBRE"]
                    clientes = tabulate(clientes_registrados, encabezado, tablefmt="grid")
                    print(f"\n[bold light_pink1]     CLIENTES REGISTRADOS     [/bold light_pink1]")
                    print(clientes)

                    while True:
                        cliente_clave = input("\nIngrese la clave del cliente al cual se le expedirá la nota: ")
                        if cliente_clave.strip() == "":
                            print("[red]*** ¡ERROR! No puede quedar vacío. ***[/red]")
                        else:
                            try:
                                cliente_clave = int(cliente_clave)
                                cursor.execute("SELECT * FROM Clientes WHERE Clave = ?", (cliente_clave,))
                                cliente = cursor.fetchone()

                                if cliente is None:
                                    print("[dark_orange]*** El cliente no está registrado. Registre al cliente primero. ***[/dark_orange]")
                                    return
                                else:
                                    break
                            except Exception:
                                print("[red]*** ¡ERROR! La clave debe ser un número entero. ***[/red]")
                else:
                    print("[dark_orange]*** No se han encontrado clientes registrados. Registre al menos a un cliente para poder expedir notas. ***[/dark_orange]")
                    return

                cursor.execute("SELECT * FROM Servicios")
                servicios_registrados = cursor.fetchall()

                if servicios_registrados:
                    encabezado = ["CLAVE", "NOMBRE", "MONTO","SUSPENIDO" ]
                    servicios = tabulate(servicios_registrados, encabezado, tablefmt="grid")
                    print(f"\n[bold light_pink1]        SERVICIOS REGISTRADOS       [/bold light_pink1]")
                    print(servicios)

                    detalle_nota = [] 
                    while True:
                        servicio_clave = input("\nIngrese la clave del servicio a solicitar: ")
                        if servicio_clave.strip() == "":
                            print("[red]*** ¡ERROR! No puede quedar vacío. ***[/red]")
                        else:
                            try:
                                servicio_clave = int(servicio_clave)
                                cursor.execute("SELECT * FROM Servicios WHERE Clave = ?", (servicio_clave,))
                                servicio = cursor.fetchone()

                                
                                if servicio is None:
                                    print("[dark_orange]*** El servicio no está registrado. Registre el servicio primero. ***[/dark_orange]")
                                    return
                                elif servicio[3] == "Si": 
                                    print("[dark_orange]*** El servicio está suspendido. No puede registrar más notas. ***[/dark_orange]")
                                    return
                                else:
                                    detalle_nota.append(servicio_clave)
                                    respuesta = input("\n¿Deseas seguir agregando servicios [SI / NO]? >> ")
                                    if respuesta.upper() != "SI":
                                        break
                            except ValueError:
                                print("[red]*** ¡ERROR! La clave debe ser un número entero. ***[/red]")
                else:
                    print("[dark_orange]*** No se han encontrado servicios registrados. Registre al menos a un servicio para poder expedir notas. ***[/dark_orange]")
                    return
                
                # Insertar la nota a la tabla de "Notas"
                cursor.execute("INSERT INTO Notas (Fecha, ClienteID, MontoPago, Estado) VALUES (?, ?, ?, ?)", (fecha_nota, cliente_clave, 0.00, "ACTIVA"))
                id_nota = cursor.lastrowid

                # Insertar los servicios a la tabla de "DetalleNotas"
                for clave_servicio in detalle_nota:
                    cursor.execute("INSERT INTO DetalleNotas (NotaID, ServicioID) VALUES (?, ?)", (id_nota, clave_servicio))

                # Calcular el monto de pago y actualizar en la tabla de "Notas"
                cursor.execute("SELECT Servicios.Costo FROM Servicios INNER JOIN DetalleNotas ON Servicios.Clave = DetalleNotas.ServicioID WHERE DetalleNotas.NotaID = ?", (id_nota,))
                costos_servicios = cursor.fetchall()
                monto_a_pagar = sum(costo[0] for costo in costos_servicios)

                cursor.execute("UPDATE Notas SET MontoPago = ? WHERE Folio = ?", (monto_a_pagar, id_nota))

                print(f"[green]*** Nota registrada exitosamente con el folio {id_nota} ***[/green]")
        except Error as error:
            print(f"[red]*** {error} ***[/red]")
        except Exception:
            print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


    def CancelarNota():
        # Opción 1.3. Cancelar notas.
        try:
            with sqlite3.connect("TallerMecanico.db") as conn:
                cursor = conn.cursor()

                while True:
                    # Solicitar folio a cancelar.
                    folio = input("\nIngrese el folio de la nota que desea cancelar: ")
                    
                    try:
                        # Convierte a tipo de dato int.
                        folio_a_cancelar = int(folio)
                        break
                    except ValueError:
                        print("[red]*** ¡ERROR! El folio debe ser un número entero. ***[/red]")
                
                # Verifica si la nota existe y no está cancelada.
                cursor.execute("SELECT * FROM Notas WHERE Folio = ? AND Estado = 'ACTIVA'", (folio_a_cancelar,))
                nota = cursor.fetchone()

                if nota is None:
                    print("[dark_orange]*** La nota no existe o ya ha sido cancelada. ***[/dark_orange]")
                else:
                    cursor.execute("SELECT Notas.Folio, Notas.Fecha, Notas.ClienteID, Clientes.Nombre, DetalleNotas.ServicioID, \
                                   Servicios.Nombre, Servicios.Costo, Notas.MontoPago FROM Notas INNER JOIN Clientes ON \
                                   Notas.ClienteID = Clientes.Clave INNER JOIN DetalleNotas ON Notas.Folio = DetalleNotas.NotaID \
                                   INNER JOIN Servicios ON DetalleNotas.ServicioID = Servicios.Clave WHERE Notas.Folio = ?", (folio_a_cancelar,))
                    detalle_nota = cursor.fetchall()

                    print("\n\t[bold]DETALLE DE LA NOTA A CANCELAR:[/bold]")
                    print("\t","- "*20)
                    print(f"\t\tFolio de la Nota        : {detalle_nota[0][0]}")
                    print(f"\t\tFecha de la Nota        : {detalle_nota[0][1]}")
                    print(f"\t\tClave del Cliente       : {detalle_nota[0][2]}")
                    print(f"\t\tNombre del Cliente      : {detalle_nota[0][3]}")
                    print("\t\t[bold]Servicios:[/bold]")
                    for detalle in detalle_nota:
                        print(f"\t\t- Clave del Servicio    : {detalle[4]}")
                        print(f"\t\t  Nombre del Servicio   : {detalle[5]}")
                        print(f"\t\t  Costo del Servicio    : ${detalle[6]:.2f}")
                    print(f"\t\tMonto a Pagar             : ${detalle_nota[0][7]:.2f}")

                    while True:
                        # Se pide la confirmación de la cancelación.
                        confirmacion = input("\n¿Estas seguro de que deseas cancelar la nota [SI / NO]? >> ")
                        if confirmacion.upper() == "SI":
                            # Se cancela.
                            cursor.execute("UPDATE Notas SET Estado = 'CANCELADA' WHERE Folio = ?", (folio_a_cancelar,))
                            print(f"[dark_orange]*** La nota con el folio {folio_a_cancelar} ha sido cancelada exitosamente. ***[/dark_orange]")
                            break
                        elif confirmacion.upper() == "NO":
                            print(f"[dark_orange]*** La nota con el folio {folio_a_cancelar} no fue cancelada. ***[/dark_orange]")
                            break
                        else:
                            print("[red]*** ¡ERROR! Ingresa una respuesta válida [SI / NO]. ***[/red]")
                            continue
        except Error as error:
            print(f"[red]*** {error} ***[/red]")
        except Exception:
            print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")
    

    def RecuperarNota():
        # Opción 1.3. Recuperar notas.
        try:
            with sqlite3.connect("TallerMecanico.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Notas.Folio, strftime('%d/%m/%Y', Notas.Fecha), Notas.ClienteID, Clientes.Nombre, \
                               Notas.MontoPago FROM Notas INNER JOIN Clientes ON Notas.ClienteID = Clientes.Clave WHERE Estado = 'CANCELADA'")
                notas_canceladas = cursor.fetchall()

                if not notas_canceladas:
                    print(f"[dark_orange]*** No hay notas canceladas en el sistema. ***[/dark_orange]")
                    return
                else:
                    encabezado = ["FOLIO", "FECHA", "CLAVE DEL CLIENTE", "NOMBRE DEL CLIENTE", "MONTO A PAGAR"]
                    print(f"\n[bold light_pink1]{('NOTAS CANCELADAS').center(85)}[/bold light_pink1]")
                    print(tabulate(notas_canceladas, encabezado, tablefmt="grid"))

                while True:
                    # Solicita el folio de la nota a recuperar.
                    folio = input("\nIngresa el folio de la que nota que deseas recuperar (Presiona ENTER si no deseas recuperar ninguna nota de las presentadas): ")
                
                    if folio.strip() == "":
                        # Regresa al menú principal si así se desea.
                        print("[yellow]Volviendo al menú principal...[/yellow]")
                        return
                    else:
                        if folio.isdigit():
                            # Convierte el folio ingresado a tipo de dato int.
                            folio_a_recuperar = int(folio)

                            cursor.execute("SELECT * FROM Notas WHERE Folio = ? AND Estado = 'CANCELADA'", (folio_a_recuperar,))
                            nota = cursor.fetchone()

                            if nota is None:
                                print("[red]*** ¡ERROR! El folio ingresado no corresponde a una nota cancelada. ***[/red]")
                            else:
                                break
                        else:
                            print("[red]*** ¡ERROR! El folio debe ser un número entero. ***[/red]")
                
                cursor.execute("SELECT Servicios.Nombre, Servicios.Costo FROM Servicios INNER JOIN DetalleNotas \
                               ON Servicios.Clave = DetalleNotas.ServicioID INNER JOIN Notas ON DetalleNotas.NotaID = Notas.Folio \
                               WHERE Notas.Folio = ?", (folio_a_recuperar,))
                detalle_nota = cursor.fetchall()
                print("\n\t[bold]DETALLE DE LA NOTA:[/bold]")
                print("\t","- "*20)
                for detalle in detalle_nota:
                    print(f"\t\t- Servicio: {detalle[0]}")
                    print(f"\t\t  Costo: ${detalle[1]:.2f}")

                while True:
                    # Se confirma si se desea recuperar la nota o no.
                    confirmacion = input("\n¿Esta seguro de recuperar esta nota [SI / NO]? >> ")
                    if confirmacion.upper() == "SI":
                        # Recupera la nota.
                        cursor.execute("UPDATE Notas SET Estado = 'ACTIVA' WHERE Folio = ?", (folio_a_recuperar,))
                        print(f"[dark_orange]*** La nota con el folio {folio_a_recuperar} ha sido recuperada exitosamente. ***[/dark_orange]")
                        break
                    elif confirmacion.upper() == "NO":
                        print(f"[dark_orange]*** La nota con el folio {folio_a_recuperar} no fue recuperada. ***[/dark_orange]")
                        break
                    else:
                        print("[red]*** ¡ERROR! Ingresa una respuesta válida [SI / NO]. ***[/red]")
                        continue
        except Error as error:
            print(f"[red]*** {error} ***[/red]")
        except Exception:
            print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")
    

    def ConsultasReportesNotas():
        # Opción 1.4. Consultas y reportes de notas.

        def ConsultaPorPeriodo():
            # Opción 1.4.1. Consultas por período.
            try:
                with sqlite3.connect("TallerMecanico.db") as conn:
                    cursor = conn.cursor()

                    while True:
                        # Solicita la fecha de inicio y si esta en el formato correcto, la convierte a tipo de dato date.
                        fecha_capturadaInicial = input("\nIngresa la fecha de inicio (dd/mm/yyyy) o presiona Enter para usar la fecha predefinida (01/01/2000): ")
                        if fecha_capturadaInicial == "":
                            fecha_inicial = datetime.date(2000, 1, 1)
                            print("[light_goldenrod2]*** Se usó la fecha predefinida (01/01/2000) ***[/light_goldenrod2]")
                        else:
                            try:
                                fecha_inicial = datetime.datetime.strptime(fecha_capturadaInicial, "%d/%m/%Y").date()
                            except ValueError:
                                print("[red]*** ¡ERROR! Fecha inválida. Asegúrate de seguir el formato dd/mm/yyyy. ***[/red]")
                                continue

                        # Solicita la fecha final y si está en el formato correcto, la convierte a tipo de dato date.
                        fecha_capturadaFinal = input("\nIngresa la fecha final (dd/mm/yyyy) o presiona Enter para usar la fecha actual: ")
                        if fecha_capturadaFinal == "":
                            fecha_final = datetime.date.today()
                            print(f"[light_goldenrod2]*** Usando la fecha actual ({fecha_final.strftime('%d/%m/%Y')}) ***[/light_goldenrod2]")
                        else:
                            try:
                                fecha_final = datetime.datetime.strptime(fecha_capturadaFinal, "%d/%m/%Y").date()
                            except ValueError:
                                print("[red]*** ¡ERROR! Fecha inválida. Asegúrate de seguir el formato dd/mm/yyyy. ***[/red]")
                                continue

                        # Comprueba si la fecha final es igual o posterior a la fecha inicial.
                        if fecha_final < fecha_inicial:
                            print("[red]*** ¡ERROR! La fecha final debe ser igual o posterior a la fecha inicial. ***[/red]")
                        else:
                            break

                    cursor.execute("SELECT Notas.Folio, strftime('%d/%m/%Y', Notas.Fecha), Notas.ClienteID, Clientes.Nombre, Notas.MontoPago, AVG(Notas.MontoPago) \
                        FROM Notas INNER JOIN Clientes ON Notas.ClienteID = Clientes.Clave WHERE Estado = 'ACTIVA' AND (Fecha BETWEEN ? AND ?)", (fecha_inicial, fecha_final))
                    notas_periodo = cursor.fetchall()

                    if all(nota is None for nota in notas_periodo[0]):
                        print("[dark_orange]*** No hay notas emitidas para el período especificado. ***[/dark_orange]")
                    else:
                        encabezado = ["FOLIO", "FECHA", "CLAVE DEL CLIENTE", "NOMBRE DEL CLIENTE", "MONTO A PAGAR", "MONTO PROMEDIO"]
                        print(f"\n[bold light_pink1]{('REPORTE DE NOTAS POR PERÍODO').center(110)}[/bold light_pink1]")
                        print(tabulate(notas_periodo, encabezado, tablefmt="grid"))

                        opcion_exportar = MenuExportacion()

                        if opcion_exportar == 1:
                            # Exportar información a CSV
                            archivo_csv = f"ReportePorPeriodo_{fecha_inicial.strftime('%m_%d_%Y')}_{fecha_final.strftime('%m_%d_%Y')}.csv"
                            ExportarDatos(notas_periodo, archivo_csv, encabezado=encabezado)
                            print(f"\n[green]*** Información exportada correctamente con el nombre [u]{archivo_csv}[/u] ***[/green]")
                        elif opcion_exportar == 2:
                            # Exportar información a EXCEL
                            archivo_excel = f"ReportePorPeriodo_{fecha_inicial.strftime('%m_%d_%Y')}_{fecha_final.strftime('%m_%d_%Y')}.xlsx"
                            ExportarDatos(notas_periodo, archivo_excel, encabezado=encabezado)
                            print(f"\n[green]*** Información exportada correctamente con el nombre [u]{archivo_excel}[/u] ***[/green]")
                        elif opcion_exportar == 3:
                            print("[yellow]Volviendo al menú anterior...[/yellow]")
                            return
            except Error as error:
                print(f"[red]*** {error} ***[/red]")
            except Exception:
                print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


        def ConsultaPorFolio():
            # Opción 1.4.2. Consultas por folio.
            try:
                with sqlite3.connect("TallerMecanico.db") as conn:
                    cursor = conn.cursor()

                cursor.execute("SELECT Notas.Folio, strftime('%d/%m/%Y', Notas.Fecha), Clientes.Nombre FROM Notas INNER JOIN Clientes \
                               ON Notas.ClienteID = Clientes.Clave WHERE Notas.Estado = 'ACTIVA' ORDER BY Notas.Folio")
                notas = cursor.fetchall()

                if notas:
                    encabezado = ["FOLIO", "FECHA", "NOMBRE DEL CLIENTE"]
                    print(f"\n[bold light_pink1]{('NOTAS').center(50)}[/bold light_pink1]")
                    print(tabulate(notas, encabezado, tablefmt="grid"))
                else:
                    print(f"[dark_orange]*** No hay notas en el sistema. ***[/dark_orange]")
                    return

                while True:
                    # Solicita el folio a consultar.
                    folio = input("\nIngrese el folio de la nota a consultar: ")

                    try:
                        # Convierte el folio a tipo de dato int.
                        folio_a_consultar = int(folio)

                        cursor.execute("SELECT * FROM Notas WHERE Folio = ? AND Estado = 'ACTIVA'", (folio_a_consultar,))
                        nota = cursor.fetchone()

                        if nota is None:
                            print("[red]*** ¡ERROR! El folio ingresado no corresponde a una nota existente. ***[/red]")
                        else:
                            break
                    except Exception:
                        print("[red]*** ¡ERROR! El folio debe ser un número entero. ***[/red]")

                cursor.execute("SELECT Notas.Folio, strftime('%d/%m/%Y', Notas.Fecha), Clientes.Nombre, Clientes.RFC, Clientes.Correo, \
                               Servicios.Nombre, Servicios.Costo, Notas.MontoPago FROM Notas INNER JOIN Clientes \
                               ON Notas.ClienteID = Clientes.Clave INNER JOIN DetalleNotas ON Notas.Folio = DetalleNotas.NotaID \
                               INNER JOIN Servicios ON DetalleNotas.ServicioID = Servicios.Clave WHERE Notas.Estado = 'ACTIVA'")
                datos_nota = cursor.fetchall()

                datos_combinados = []
                if datos_nota:
                    for fila in datos_nota:
                        folio, fecha, nombre, rfc, correo, servicio, costo, monto = fila
                        if not datos_combinados:
                            datos_combinados.append([folio, fecha, nombre, rfc, correo, servicio, costo, monto])
                        else:
                            datos_combinados.append(["", "", "", "", "", servicio, costo, ""])
                    
                    encabezado = ["FOLIO", "FECHA", "NOMBRE DEL CLIENTE", "RFC DEL CLIENTE", "CORREO DEL CLIENTE", "NOMBRE DEL SERVICIO", "COSTO DEL SERVICIO", "MONTO A PAGAR"]
                    print(f"\n[bold light_pink1]{('DETALLE DE LA NOTA:').center(160)}[/bold light_pink1]")
                    print(tabulate(datos_combinados, encabezado, tablefmt="grid"))
            except Error as error:
                print(f"[red]*** {error} ***[/red]")
            except Exception:
                print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


        while True:
            # Menú de consultas y reportes de notas.
            print("\n***************************************")
            print("[bold light_salmon1] Menú de Consultas y Reportes de Notas[/bold light_salmon1]")
            print("***************************************")
            print("(1). Consulta por período.")
            print("(2). Consulta por folio.")
            print("(3). Volver al menú de notas.")
            print("***************************************")

            tipo_consulta = input("\nSeleccione una opción: ")

            if tipo_consulta.strip() == "":
                print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
                continue
            else:
                try:
                    # Convierte la opcion capturada a tipo de dato int.
                    consulta = int(tipo_consulta)
                except Exception:
                    print("[red]*** ¡ERROR! La opción debe ser un número entero. ***[/red]")
                    continue

                if consulta == 1:
                    ConsultaPorPeriodo()
                elif consulta == 2:
                    ConsultaPorFolio()
                elif consulta == 3:
                    print("[yellow]Volviendo al menú de notas...[/yellow]")
                    break
                else:
                    print("[red]*** Opción no válida. ***[/red]")    


    while True:
        # Menú de notas.
        print("\n************************************")
        print(f"[bold sandy_brown]{('Menú de Notas').center(37)}[/bold sandy_brown]")
        print("************************************")
        print("(1). Registrar una nota.")
        print("(2). Cancelar una nota.")
        print("(3). Recuperar una nota.")
        print("(4). Consultas y reportes.")
        print("(5). Volver al menú principal.")
        print("************************************")

        sub_opcion_notas = input("\nSeleccione una opción: ")

        if sub_opcion_notas.strip() == "":
            print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
            continue
        else:
            try:
                # Convierte la opcion capturada a tipo de dato int.
                opcion_notas = int(sub_opcion_notas)
            except Exception:
                print("[red]*** ¡ERROR! La opción debe ser un número entero. ***[/red]")
                continue

            if opcion_notas == 1:
                RegistrarNota()
            elif opcion_notas == 2:
                CancelarNota()
            elif opcion_notas == 3:
                RecuperarNota()
            elif opcion_notas == 4:
                ConsultasReportesNotas()
            elif opcion_notas == 5:
                print("[yellow]Volviendo al menú principal...[/yellow]")
                break
            else:
                print("[red]*** Opción no válida. ***[/red]")    



def Clientes():
    # Opción 2. Clientes.

    def AgregarCliente():
        # Opción 2.1. Agregar un cliente.
        while True:
            # Solicita el nombre y valida que no quede vacío.
            while True:
                nombre_cliente = input("\nIngresa el nombre del cliente: ")
                if nombre_cliente.strip() == "":
                    print("[red]*** ¡ERROR! El nombre no puede quedar vacío. ***[/red]")
                else:
                    break
            
            # Solicita el RFC del cliente, y valida que este en un formato valido.
            patron_rfc = r'^[A-ZÑ&]{3,4}[0-9]{6}[A-Z0-9]{3}$'

            while True:
                rfc_captura = input("\nIngrese el RFC del cliente: ")
                rfc_cliente = rfc_captura.strip().upper()

                if not re.match(patron_rfc, rfc_cliente):
                    print("[red]*** ¡ERROR! El RFC no cumple con el patrón asignado. ***[/red]")
                else:
                    letras_iniciales = rfc_cliente[:4] if len(rfc_cliente) == 13 else rfc_cliente[:3]
                    fecha_str = rfc_cliente[len(letras_iniciales):len(letras_iniciales) + 6]

                    try:
                        fecha_rfc = datetime.datetime.strptime(fecha_str, "%y%m%d").date()
                        if fecha_rfc > datetime.date.today():
                            print("[red]*** ¡ERROR! El RFC no es válido. ***[/red]")
                            continue
                        else:
                            if len(rfc_cliente) == 13:
                                print("[orange1]El RFC ingresado es de persona física.[/orange1]")
                                break
                            else:
                                print("[orange1]El RFC ingresado es de persona moral.[/orange1]")
                                break
                    except Exception:
                        print("[red]*** ¡ERROR! La fecha del RFC no es válida. ***[/red]")
                        continue
            
            # Solicita el correo electrónico del cliente y hace las respectivas validaciones.
            patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            while True:
                correo = input("\nIngrese el correo del cliente: ").lower()

                if not re.match(patron_correo,correo):
                    print("[red]*** ¡ERROR! El correo no cumple con el patrón asignado. ***[/red]")
                    continue
                else:
                    dominio = correo.split('@')[1]
                    try:
                        socket.gethostbyname(dominio)
                        break
                    except Exception:
                        print("[red]*** ¡ERROR! El dominio no existe, intenta de nuevo. ***[/red]")
                        continue
            
            try:
                with sqlite3.connect("TallerMecanico.db") as conn:
                    cursor = conn.cursor()
                    datos_cliente = (nombre_cliente, rfc_cliente, correo)
                    cursor.execute("INSERT INTO Clientes (Nombre, RFC, Correo) VALUES (?,?,?)", datos_cliente)
                    print(f"[green]*** Cliente registrado exitosamente con la clave {cursor.lastrowid} ***[/green]")
                    break
            except Error as error:
                print(f"[red]*** {error} ***[/red]")
            except Exception:
                print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


    def ConsultasReportesCliente():
        # Opción 2.2. Consultas y Reportes de Clientes.
        
        def ListadoClientes():
            # Opción 2.2.1. Listado de clientes registrados.
            
            def OrdenadoClave():
                # Opción 2.2.1.1. Listado de clientes ordenado por clave.
                try:
                    with sqlite3.connect("TallerMecanico.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Clientes ORDER BY Clave;")
                        datos_clientes = cursor.fetchall()

                        if datos_clientes:
                            encabezado = ["CLAVE", "NOMBRE", "RFC", "CORREO"]
                            reporte_clave = tabulate(datos_clientes, encabezado, tablefmt="grid")
                            print(f"\n[bold light_pink1]{('REPORTE DE CLIENTES ORDENADOS POR CLAVE').center(75)}[/bold light_pink1]")
                            print(reporte_clave)
                        else:
                            print("[red]*** No hay clientes en la base de datos. ***[/red]")
                            
                        opcion_exportar = MenuExportacion()

                        fecha_actual = datetime.datetime.today().strftime("%m_%d_%Y")
                        if opcion_exportar == 1:
                            # Exportar información a CSV
                            archivo_csv = f"ReporteClientesActivosPorClave_{fecha_actual}.csv"
                            ExportarDatos(datos_clientes, archivo_csv, encabezado=encabezado)
                            print(f"\n[green]*** Información exportada correctamente con el nombre [u]{archivo_csv}[/u] ***[/green]")
                        elif opcion_exportar == 2:
                            # Exportar información a EXCEL
                            archivo_excel = f"ReporteClientesActivosPorClave_{fecha_actual}.xlsx"
                            ExportarDatos(datos_clientes, archivo_excel, encabezado=encabezado)
                            print(f"\n[green]*** Información exportada correctamente con el nombre [u]{archivo_excel}[/u] ***[/green]")
                        elif opcion_exportar == 3:
                            print("[yellow]Volviendo al menú anterior...[/yellow]")
                            return
                except Error as error:
                    print(f"[red]*** {error} ***[/red]")
                except Exception:
                    print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


            def OrdenadoNombre():
                # Opción 2.2.1.2. Listado de clientes ordenado por nombre.
                try:
                    with sqlite3.connect("TallerMecanico.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Clientes ORDER BY Nombre;")
                        datos_clientes = cursor.fetchall()

                        if datos_clientes:
                            encabezado = ["CLAVE", "NOMBRE", "RFC", "CORREO"]
                            reporte_nombre= tabulate(datos_clientes, encabezado, tablefmt="grid")
                            print(f"\n[bold light_pink1]{('REPORTE DE CLIENTES ORDENADOS POR NOMBRES').center(75)}[/bold light_pink1]")
                            print(reporte_nombre)
                        else:
                            print("[red]*** No hay clientes en la base de datos. ***[/red]")

                        opcion_exportar = MenuExportacion()

                        fecha_actual = datetime.datetime.today().strftime("%m_%d_%Y")
                        if opcion_exportar == 1:
                            # Exportar información a CSV
                            archivo_csv = f"ReporteClientesActivosPorNombre_{fecha_actual}.csv"
                            ExportarDatos(datos_clientes, archivo_csv, encabezado=encabezado)
                            print(f"\n[green]*** Información exportada correctamente con el nombre [u]{archivo_csv}[/u] ***[/green]")
                        elif opcion_exportar == 2:
                            # Exportar información a EXCEL
                            archivo_excel = f"ReporteClientesActivosPorNombre_{fecha_actual}.xlsx"
                            ExportarDatos(datos_clientes, archivo_excel, encabezado=encabezado)
                            print(f"\n[green]*** Información exportada correctamente con el nombre [u]{archivo_excel}[/u] ***[/green]")
                        elif opcion_exportar == 3:
                            print("[yellow]Volviendo al menú anterior...[/yellow]")
                            return
                except Error as error:
                    print(f"[red]*** {error} ***[/red]")
                except Exception:
                    print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


            while True:
                # Menú de listado de clientes.
                print("\n************************************")
                print(f"[bold turquoise4]{('Menú de Listado de Clientes').center(35)}[/bold turquoise4]")
                print("************************************")
                print("(1). Ordenado por clave.")
                print("(2). Ordenado por nombre.")
                print("(3). Volver al menú anterior.")
                print("************************************")

                sub_opcion_listado = input("\nSeleccione una opción: ")

                if sub_opcion_listado.strip() == "":
                    print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
                    continue
                else:
                    try:
                        # Convierte la opcion capturada a tipo de dato int.
                        opcion_listado = int(sub_opcion_listado)
                    except Exception:
                        print("[red]*** ¡ERROR! La opción debe ser un número entero. ***[/red]")
                        continue

                    if opcion_listado == 1:
                        OrdenadoClave()
                    elif opcion_listado == 2:
                        OrdenadoNombre()
                    elif opcion_listado == 3:
                        print("[yellow]Volviendo al menú anterior...[/yellow]")
                        break
                    else:
                        print("[red]*** Opción no válida. ***[/red]") 


        def BusquedaClaveCliente():
            # Opción 2.2.2. Búsqueda de clientes por clave.
            while True:
                # Solicita la clave a consultar.
                clave_cliente = input("\nIngrese la clave del cliente a consultar: ")

                try:
                    # Convierte la clave a tipo de dato int.
                    clave_consulta = int(clave_cliente)

                    with sqlite3.connect("TallerMecanico.db") as conn:
                        cursor = conn.cursor()
                        dato = {"clave":clave_consulta}
                        cursor.execute("SELECT * FROM Clientes WHERE Clave = :clave", dato)
                        datos_consulta_clave = cursor.fetchall()

                        if datos_consulta_clave:
                            encabezado = ["CLAVE", "NOMBRE", "RFC", "CORREO"]
                            busqueda_clave = tabulate(datos_consulta_clave, encabezado, tablefmt="grid")
                            print(f"\n[bold light_pink1]{('BÚSQUEDA DE CLIENTES POR LA CLAVE ' + str(clave_consulta)).center(65)}[/bold light_pink1]")
                            print(busqueda_clave)
                        else:
                            print(f"[red]*** No se encontró ningún cliente con la clave {clave_consulta} ***[/red]")

                    break
                except ValueError:
                    print("[red]*** ¡ERROR! La clave debe ser un número entero. ***[/red]")
                except Error as error:
                    print(f"[red]*** {error} ***[/red]")
                except Exception:
                    print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


        def BusquedaNombreCliente():
            # Opción 2.2.3. Búsqueda de clientes por nombre.
            while True:
                # Solicita el nombre a consultar.
                nombre_consulta = input("\nIngrese el nombre del cliente a consultar: ")
                if nombre_consulta.strip() == "":
                    print("[red]*** ¡ERROR! El nombre no puede quedar vacío. ***[/red]")
                else:
                    break
            
            try:
                with sqlite3.connect("TallerMecanico.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM Clientes WHERE UPPER(Nombre) LIKE ?", ('%' + nombre_consulta.upper() + '%',))
                    datos_consulta_nombre = cursor.fetchall()

                    if datos_consulta_nombre:
                        encabezado = ["CLAVE", "NOMBRE", "RFC", "CORREO"]
                        busqueda_nombre = tabulate(datos_consulta_nombre, encabezado, tablefmt="grid")
                        print(f"\n[bold light_pink1]{('BÚSQUEDA DE CLIENTES POR EL NOMBRE ' + nombre_consulta.upper()).center(65)}[/bold light_pink1]")
                        print(busqueda_nombre)
                    else:
                        print(f"[red]*** No se encontró ningún cliente con el nombre '{nombre_consulta}' ***[/red]")
            except Error as error:
                print(f"[red]*** {error} ***[/red]")
            except Exception:
                print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


        while True:
            # Menú de consultas y reportes de clientes.
            print("\n******************************************")
            print("[bold spring_green4] Menú de Consultas y Reportes de Clientes[/bold spring_green4]")
            print("******************************************")
            print("(1). Listado de clientes registrados.")
            print("(2). Búsqueda por clave.")
            print("(3). Búsqueda por nombre.")
            print("(4). Volver al menú de clientes.")
            print("******************************************")

            tipo_consulta = input("\nSeleccione una opción: ")

            if tipo_consulta.strip() == "":
                print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
                continue
            else:
                try:
                    # Convierte la opcion capturada a tipo de dato int.
                    consulta = int(tipo_consulta)
                except Exception:
                    print("[red]*** ¡ERROR! La opción debe ser un número entero. ***[/red]")
                    continue

                if consulta == 1:
                    ListadoClientes()
                elif consulta == 2:
                    BusquedaClaveCliente()
                elif consulta == 3:
                    BusquedaNombreCliente()
                elif consulta == 4:
                    print("[yellow]Volviendo al menú de clientes...[/yellow]")
                    break
                else:
                    print("[red]*** Opción no válida. ***[/red]")    

    def SuspenderCliente():
        try:
            with sqlite3.connect("TallerMecanico.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Clave, Nombre FROM Clientes;")
                clientes_activos = cursor.fetchall()

                if not clientes_activos:
                    print("No hay clientes activos en este momento.")
                    return

                headers = ["Clave", "Nombre"]
                print(tabulate(clientes_activos, headers=headers, tablefmt="pretty"))

                while True:
                    clave_cliente = input("Ingrese la clave del cliente que desea suspender (o 0 para volver al menú anterior): ")

                    if clave_cliente == '0':
                        break
                    elif clave_cliente.strip() == "":
                        print("[yellow]Ingrese un valor válido[/yellow]")
                    else:
                        cursor.execute("SELECT * FROM Clientes WHERE Clave=?", (clave_cliente,))
                        cliente = cursor.fetchone()

                        if not cliente:
                            print("[yellow]No se encontró ningún cliente con esa clave.[/yellow]")
                            continue

                        print("[blue]*****Detalles del cliente*****[/blue]")
                        detalle_cliente = [
                            ("Clave", cliente[0]),
                            ("Nombre", cliente[1]),
                            ("RFC", cliente[2]),
                            ("Correo", cliente[3])
                        ]

                        print(tabulate(detalle_cliente, tablefmt="pretty"))

                        while True:
                            confirmacion = input("¿Está seguro que desea suspender a este cliente? (si o no): ")

                            if confirmacion.lower() == "si":
                                cursor.execute("INSERT INTO ClientesSuspendidos (Nombre, RFC, Correo) VALUES (?, ?, ?)", (cliente[1], cliente[2], cliente[3]))
                                cursor.execute("DELETE FROM Clientes WHERE Clave=?", (clave_cliente,))
                                conn.commit()
                                print(f"El cliente con clave {clave_cliente} ha sido suspendido.")
                                break
                            elif confirmacion.lower() == "no":
                                print("No se ha suspendido al cliente.")
                                break
                            else:
                                print("Ingrese 'si' o 'no")
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")

    def RecuperarCliente():
        try:
            with sqlite3.connect("TallerMecanico.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Clave, Nombre FROM ClientesSuspendidos;")
                clientes_suspendidos = cursor.fetchall()

                if not clientes_suspendidos:
                    print("No hay clientes suspendidos en este momento.")
                    return

                headers = ["Clave", "Nombre"]
                print(tabulate(clientes_suspendidos, headers=headers, tablefmt="pretty"))

                while True:
                    clave_cliente = input("Ingrese la clave del cliente que desea recuperar (o 0 para volver al menú anterior): ")

                    if clave_cliente == '0':
                        break
                    elif clave_cliente.strip() == "":
                        print("[yellow]Ingrese un valor válido[/yellow]")
                    else:
                        cursor.execute("SELECT * FROM ClientesSuspendidos WHERE Clave=?", (clave_cliente,))
                        cliente = cursor.fetchone()

                        if not cliente:
                            print("[yellow]No se encontró ningún cliente suspendido con esa clave.[/yellow]")
                            continue

                        print("[blue]*****Detalles del cliente suspendido*****[/blue]")
                        detalle_cliente = [
                            ("Clave", cliente[0]),
                            ("Nombre", cliente[1]),
                            ("RFC", cliente[2]),
                            ("Correo", cliente[3])
                        ]

                        print(tabulate(detalle_cliente, tablefmt="pretty"))

                        confirmacion = input("¿Está seguro que desea recuperar a este cliente? (si o no): ")

                        if confirmacion.lower() == "si":
                            cursor.execute("INSERT INTO Clientes (Nombre, RFC, Correo) VALUES (?, ?, ?)", (cliente[1], cliente[2], cliente[3]))
                            cursor.execute("DELETE FROM ClientesSuspendidos WHERE Clave=?", (clave_cliente,))
                            conn.commit()
                            print(f"El cliente con clave {clave_cliente} ha sido recuperado.")
                        elif confirmacion.lower() == "no":
                            print("No se ha recuperado al cliente.")
                        else:
                            print("Ingrese 'si' o 'no")
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")


    while True:
        # Menú de clientes.
        print("\n************************************")
        print(f"[bold dark_cyan]{('Menú de Clientes').center(35)}[/bold dark_cyan]")
        print("************************************")
        print("(1). Agregar un cliente.")
        print("(2). Suspender un cliente.")
        print("(3). Recuperar un cliente.")
        print("(4). Consultas y reportes.")
        print("(5). Volver al menú principal.")
        print("************************************")

        sub_opcion_clientes= input("\nSeleccione una opción: ")

        if sub_opcion_clientes.strip() == "":
            print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
            continue
        else:
            try:
                # Convierte la opcion capturada a tipo de dato int.
                opcion_clientes = int(sub_opcion_clientes)
            except Exception:
                print("[red]*** ¡ERROR! La opción debe ser un número entero. ***[/red]")
                continue

            if opcion_clientes == 1:
                AgregarCliente()
            elif opcion_clientes == 2:
                SuspenderCliente()
            elif opcion_clientes == 3:
                RecuperarCliente()
            elif opcion_clientes == 4:
                ConsultasReportesCliente()
            elif opcion_clientes == 5:
                print("[yellow]Volviendo al menú principal...[/yellow]")
                break
            else:
                print("[red]*** Opción no válida. ***[/red]")    



def Servicios():

    def AgregarServicio():
        while True:
            while True:
                nombre_servicio = input("\nIngresa el nombre que describe el nuevo servicio: ")
                if nombre_servicio.strip() == "":
                    print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
                else:
                    break
            
            while True:
                costo_servicio = input("\nIngresa el costo del nuevo servicio (Asegúrate que sea mayor a $0.00): ")
                if costo_servicio.strip() == "":
                    print("[red]*** ¡ERROR! El campo no puede quedar vacío. ***[/red]")
                else:
                    try:
                        costo_servicio = float(costo_servicio)
                        if costo_servicio <= 0:
                            print("[red]*** ¡ERROR! El costo debe ser mayor a $0.00 ***[/red]")
                        else:
                            break
                    except ValueError:
                        print("[red]*** ¡ERROR! Ingresa un valor numérico válido. ***[/red]")

            try:
                with sqlite3.connect("TallerMecanico.db") as conn:
                    cursor = conn.cursor()
                    datos_servicios = (nombre_servicio, costo_servicio, "No")
                    cursor.execute("INSERT INTO Servicios (Nombre, Costo, Suspendido) VALUES (?,?,?)", datos_servicios)
                    print(f"[green]*** Servicio registrado exitosamente con la clave {cursor.lastrowid} ***[/green]")
                    break
            except Error as error:
                print(f"[red]*** {error} ***[/red]")
            except Exception:
                print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


    def ConsultasReportesServicios():
        # Opción 3.2. Consultas y Reportes de Servicios.

        def BusquedaClaveServicio(): 
            # Opción 3.2.1. Búsqueda de servicios por clave.
            try:
                with sqlite3.connect("TallerMecanico.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT Clave, Nombre FROM Servicios")
                    datos_servicios = cursor.fetchall()

                    if datos_servicios:
                        encabezado = ["CLAVE", "NOMBRE", "COSTO"]
                        reporte_servicos = tabulate(datos_servicios, encabezado, tablefmt="grid")
                        print(f"\n[bold light_pink1]      SERVICIOS REGISTRADOS      [/bold light_pink1]")
                        print(reporte_servicos)

                        while True:
                            # Solicita la clave a consultar.
                            clave = input("\nIngrese la clave del servicio a consultar: ")
                            if clave.strip() == "":
                                print("[red]*** ¡ERROR! La clave no puede quedar vacía. ***[/red]")
                            else:
                                try:
                                    clave_cliente = int(clave)
                                    dato = {"clave":clave_cliente}
                                    cursor.execute("SELECT * FROM Servicios WHERE Clave = :clave", dato)
                                    datos_clave = cursor.fetchall()

                                    if datos_clave:
                                        encabezado = ["CLAVE", "NOMBRE", "COSTO"]
                                        reporte_clave = tabulate(datos_clave, encabezado, tablefmt="grid")
                                        print(f"\n[bold light_pink1]  DETALLE DEL SERVICIO CON LA CLAVE {clave_cliente}  [/bold light_pink1]")
                                        print(reporte_clave)
                                        break
                                    else:
                                        print("[red]*** ¡ERROR! La clave ingresada aún no ha sido registrada. ***[/red]")
                                except ValueError:
                                    print("[red]*** ¡ERROR! La clave debe ser un número entero. ***[/red]")
                    else:
                        print(f"[red]*** No se encontró ningún servicio. ***[/red]")
            except Error as error:
                print(f"[red]*** {error} ***[/red]")
            except Exception:
                print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


        def BusquedaNombreServicio(): 
            # Opción 3.2.2. Búsqueda de servicios por nombre.
            while True:
                # Solicita el nombre a consultar.
                nombre_consulta = input("\nIngrese el nombre del servicio a consultar: ")
                if nombre_consulta.strip() == "":
                    print("[red]*** ¡ERROR! El nombre no puede quedar vacío. ***[/red]")
                else:
                    break
            
            try:
                with sqlite3.connect("TallerMecanico.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM Servicios WHERE UPPER(Nombre) LIKE ?", ('%' + nombre_consulta.upper() + '%',))
                    datos_consulta_nombre = cursor.fetchall()

                    if datos_consulta_nombre:
                        encabezado = ["CLAVE", "NOMBRE", "COSTO"]
                        busqueda_nombre = tabulate(datos_consulta_nombre, encabezado, tablefmt="grid")
                        print(f"\n[bold light_pink1]BÚSQUEDA DE SERVICIOS POR EL NOMBRE '{nombre_consulta.upper()}'[/bold light_pink1]")
                        print(busqueda_nombre)
                    else:
                        print(f"[red]*** No se encontró ningún servicio con el nombre '{nombre_consulta}' ***[/red]")
            except Error as error:
                print(f"[red]*** {error} ***[/red]")
            except Exception:
                print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


        def ListadoServicios():
            # Opción. 3.2.3. Listado de servicios registrados.

            def OrdenadoPorClave():
                # Opción 3.2.3.1. Listado de servicios ordenados por clave.
                try:
                    with sqlite3.connect("TallerMecanico.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Servicios ORDER BY Clave;")
                        datos_servicios = cursor.fetchall()

                        if datos_servicios:
                            encabezado = ["CLAVE", "NOMBRE", "COSTO"]
                            reporte_por_clave = tabulate(datos_servicios, encabezado, tablefmt="grid")
                            print("\n[bold light_pink1] REPORTE DE SERVICIOS ORDENADOS POR CLAVE [/bold light_pink1]")
                            print(reporte_por_clave)
                        else:
                            print("[red]*** No hay servicios en la base de datos. ***[/red]")
                            
                        opcion_exportar = MenuExportacion()

                        fecha_actual = datetime.datetime.today().strftime("%m_%d_%Y")
                        if opcion_exportar == 1:
                            # Exportar información a CSV
                            archivo_csv = f"ReporteServiciosPorClave_{fecha_actual}.csv"
                            ExportarDatos(datos_servicios, archivo_csv, encabezado=encabezado)
                            print(f"\n[green]*** Información exportada correctamente con el nombre [u]{archivo_csv}[/u] ***[/green]")
                        elif opcion_exportar == 2:
                            # Exportar información a EXCEL
                            archivo_excel = f"ReporteServiciosPorClave_{fecha_actual}.xlsx"
                            ExportarDatos(datos_servicios, archivo_excel, encabezado=encabezado)
                            print(f"\n[green]*** Información exportada correctamente con el nombre [u]{archivo_excel}[/u] ***[/green]")
                        elif opcion_exportar == 3:
                            print("[yellow]Volviendo al menú anterior...[/yellow]")
                            return
                except Error as error:
                    print(f"[red]*** {error} ***[/red]")
                except Exception:
                    print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


            def OrdenadoPorNombre():
                # Opción 3.2.3.2. Listado de servicios ordenados por nombre.
                try:
                    with sqlite3.connect("TallerMecanico.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Servicios ORDER BY Nombre;")
                        datos_servicios = cursor.fetchall()

                        if datos_servicios:
                            encabezado = ["CLAVE", "NOMBRE", "COSTO"]
                            reporte_por_nombre= tabulate(datos_servicios, encabezado, tablefmt="grid")
                            print("\n[bold light_pink1]REPORTE DE SERVICIOS ORDENADOS POR NOMBRES[/bold light_pink1]")
                            print(reporte_por_nombre)
                        else:
                            print("[red]*** No hay servicios en la base de datos. ***[/red]")

                        opcion_exportar = MenuExportacion()

                        fecha_actual = datetime.datetime.today().strftime("%m_%d_%Y")
                        if opcion_exportar == 1:
                            # Exportar información a CSV
                            archivo_csv = f"ReporteServiciosPorNombre_{fecha_actual}.csv"
                            ExportarDatos(datos_servicios, archivo_csv, encabezado=encabezado)
                            print(f"\n[green]*** Información exportada correctamente con el nombre [u]{archivo_csv}[/u] ***[/green]")
                        elif opcion_exportar == 2:
                            # Exportar información a EXCEL
                            archivo_excel = f"ReporteServiciosPorNombre_{fecha_actual}.xlsx"
                            ExportarDatos(datos_servicios, archivo_excel, encabezado=encabezado)
                            print(f"\n[green]*** Información exportada correctamente con el nombre [u]{archivo_excel}[/u] ***[/green]")
                        elif opcion_exportar == 3:
                            print("[yellow]Volviendo al menú anterior...[/yellow]")
                            return
                except Error as error:
                    print(f"[red]*** {error} ***[/red]")
                except Exception:
                    print(f"[red]*** Ha ocurrido el siguiente error: {sys.exc_info()[0]} ***[/red]")


            while True:
                # Menú de listado de servicios.
                print("\n************************************")
                print(f"[bold medium_purple2]{('Menú de Listado de Servicios').center(35)}[/bold medium_purple2]")
                print("************************************")
                print("(1). Ordenado por clave.")
                print("(2). Ordenado por nombre.")
                print("(3). Volver al menú anterior.")
                print("************************************")

                sub_opcion_listado = input("\nSeleccione una opción: ")

                if sub_opcion_listado.strip() == "":
                    print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
                    continue
                else:
                    try:
                        # Convierte la opcion capturada a tipo de dato int.
                        opcion_listado = int(sub_opcion_listado)
                    except Exception:
                        print("[red]*** ¡ERROR! La opción debe ser un número entero. ***[/red]")
                        continue

                    if opcion_listado == 1:
                        OrdenadoPorClave()
                    elif opcion_listado == 2:
                        OrdenadoPorNombre()
                    elif opcion_listado == 3:
                        print("[yellow]Volviendo al menú anterior...[/yellow]")
                        break
                    else:
                        print("[red]*** Opción no válida. ***[/red]") 


        while True:
            # Menú de consultas y reportes de servicios.
            print("\n*******************************************")
            print("[bold grey63] Menú de Consultas y Reportes de Servicios[/bold grey63]")
            print("*******************************************")
            print("(1). Búsqueda por clave.")
            print("(2). Búsqueda por nombre.")
            print("(3). Listado de servicios registrados.")
            print("(4). Volver al menú de servicios.")
            print("*******************************************")

            tipo_consulta = input("\nSeleccione una opción: ")

            if tipo_consulta.strip() == "":
                print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
                continue
            else:
                try:
                    # Convierte la opcion capturada a tipo de dato int.
                    consulta = int(tipo_consulta)
                except Exception:
                    print("[red]*** ¡ERROR! La opción debe ser un número entero. ***[/red]")
                    continue

                if consulta == 1:
                    BusquedaClaveServicio()
                elif consulta == 2:
                    BusquedaNombreServicio()
                elif consulta == 3:
                    ListadoServicios()
                elif consulta == 4:
                    print("[yellow]Volviendo al menú de servicios...[/yellow]")
                    break
                else:
                    print("[red]*** Opción no válida. ***[/red]")    

    def SuspenderServicio():
        try:
            with sqlite3.connect("TallerMecanico.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Clave, Nombre FROM Servicios WHERE suspendido='No';")
                servicios_activos = cursor.fetchall()
                if not servicios_activos:
                    print("No hay servicios activos en este momento.")
                    return

                headers = ["Clave", "Nombre"]
                print(tabulate(servicios_activos, headers=headers, tablefmt="pretty"))
                
            while True:
                clave_servicio = input("Ingrese la clave del servicio que desea suspender (o 0 para volver al menú anterior): ")
                if clave_servicio == '0':
                    break
                elif clave_servicio.strip() == "":
                        print("[yellow]ingrese un valor valido[/yellow]")
                else:
                        cursor.execute("SELECT * FROM Servicios WHERE Clave=?", (clave_servicio,))
                        servicio = cursor.fetchone()
                        if not servicio:
                            print("[yellow]No se encontró ningún servicio con esa clave.[/yellow]")
                            continue
                        print("[blue]*****Detalles de servicio*****[/blue]")
                        detalle_servicio = [(f"Clave", servicio[0]),
                                            (f"Nombre", servicio[1]),
                                            (f"Costo", servicio[2]),
                                            (f"Suspendido", servicio[3])]

                        print(tabulate(detalle_servicio, tablefmt="pretty"))
                        while True:
                            confi_sus = input("¿Está seguro que desea suspender este servicio? (si o no): ")
                            if confi_sus.lower() == "si":
                                cursor.execute("UPDATE Servicios SET suspendido='Si' WHERE Clave=?", (clave_servicio,))
                                conn.commit()
                                print(f"El servicio con clave {clave_servicio} ha sido suspendido.")
                                break
                            elif confi_sus.lower()== "no":
                                print("No se ha suspendido el servicio.")
                                break
                            else:
                                print("Ingrese un si o un no")

        except Exception as e:
            print(f"Ha ocurrido un error: {e}")
 
    def RecuperarServicio():
        try:
            with sqlite3.connect("TallerMecanico.db") as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Clave, Nombre FROM Servicios WHERE suspendido='Si';")
                servicios_suspendidos = cursor.fetchall()
                if not servicios_suspendidos:
                    print("No hay servicios suspendidos en este momento.")
                    return

                headers = ["Clave", "Nombre"]
                print(tabulate(servicios_suspendidos, headers=headers, tablefmt="pretty"))
                while True:
                    clave_servicio = input("Ingrese la clave del servicio que desea suspender (o 0 para volver al menú anterior): ")
                    if clave_servicio == '0':
                        break
                    elif clave_servicio.strip() == "":
                        print("[yellow]ingrese un valor valido[/yellow]")
                    else:
                        clave_servicio = int(clave_servicio)
                        cursor.execute("SELECT * FROM Servicios WHERE Clave=?", (clave_servicio,))
                        servicio = cursor.fetchone()

                        if not servicio:
                            print("No se encontró ningún servicio con esa clave.")
                            continue

                        print("[blue]*****Detalles de servicio*****[/blue]")
                        detalle_servicio = [(f"Clave", servicio[0]),
                                            (f"Nombre", servicio[1]),
                                            (f"Costo", servicio[2]),
                                            (f"Suspendido", servicio[3])]

                        print(tabulate(detalle_servicio, tablefmt="pretty"))

                        confi_sus = input("¿Está seguro que desea recuperar este servicio? (si o no): ")

                        if confi_sus.lower() == "si":
                            cursor.execute("UPDATE Servicios SET suspendido='No' WHERE Clave=?", (clave_servicio,))
                            conn.commit()
                        elif confi_sus.lower()== "no":
                            print("No se ha suspendido el servicio.")
                            break
                        else:
                            print("Ingrese un si o un no")
        except Exception as e:
            print(f"Ha ocurrido un error: {e}")

    while True:
        print("\n************************************")
        print(f"[bold rosy_brown]{('Menú de Servicios').center(37)}[/bold rosy_brown]")
        print("************************************")
        print("(1). Agregar un servicio.")
        print("(2). Consultas y reportes.")
        print("(3). Suspender servicios.")
        print("(4). Recuperar servicios.")
        print("(5). volver al menú principal.")

        print("************************************")

        sub_opcion_servicios = input("\nSeleccione una opción: ")

        if sub_opcion_servicios.strip() == "":
            print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
            continue
        else:
            try:
                opcion_servicios = int(sub_opcion_servicios)
            except Exception:
                print("[red]*** ¡ERROR! La opción debe ser un número entero. ***[/red]")
                continue

            if opcion_servicios == 1:
                AgregarServicio()
            elif opcion_servicios == 2:
                ConsultasReportesServicios()
            elif opcion_servicios == 3:
                SuspenderServicio()
            elif opcion_servicios == 4:
                RecuperarServicio()
            elif opcion_servicios == 5:
                print("[yellow]Volviendo al menú principal...[/yellow]")
                break
            else:
                print("[red]*** Opción no válida. ***[/red]")    



def Salir():
    # Opción 4. Salida del sistema.
    while True:
        confirmacion_salida = input("\n¿Estas seguro de salir del sistema [SI / NO]? >> ")
        if confirmacion_salida.upper() == "SI":
            print("[light_pink3]Gracias por visitar este sistema. ¡Vuelva pronto!\n[/light_pink3]")
            exit()
        elif confirmacion_salida.upper() == "NO":
            print("[yellow]Volviendo al menú principal...[/yellow]")
            return
        else:
            print("[red]*** ¡ERROR! Ingresa una respuesta válida [SI / NO]. ***[/red]")
            continue



def ExportarDatos(datos, nombre_archivo, encabezado):
    if nombre_archivo.endswith(".csv"):
        with open(nombre_archivo, "w", newline="") as archivo:
            grabador_csv = csv.writer(archivo)
            if encabezado:
                grabador_csv.writerow(encabezado)
            grabador_csv.writerows(datos)
    elif nombre_archivo.endswith(".xlsx"):
        libro = openpyxl.Workbook()
        hoja_trabajo = libro.active
        if encabezado:
            hoja_trabajo.append(encabezado)
        for fila in datos:
            hoja_trabajo.append(fila)
        libro.save(nombre_archivo)
    else:
        print("[red]*** Formato de archivo no compatible, debe ser CSV o EXCEL. ***[/red]")



def MenuExportacion():
    while True:
        exportacion = input("\n¿Deseas exportar la información anterior? [SI/NO] >> ")
        if exportacion.upper() == "SI":
            while True:
                print("\n*************************************************")
                print("[bold light_sea_green]                    Opciones     [/bold light_sea_green]")
                print("*************************************************")
                print("(1) Archivo CSV.")
                print("(2) Excel.")
                print("(3) Regresar al menú anterior.")
                print("*************************************************")

                opcion_capturada = input("\nSeleccione una opción: ")

                if opcion_capturada.strip() == "":
                    print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
                    continue
                else:
                    try:
                        # Convierte la opción capturada a tipo de dato int.
                        opcion_exportar = int(opcion_capturada)
                        
                        if 1 <= opcion_exportar <= 3:
                            return opcion_exportar
                        else:
                            print("[red]*** ¡ERROR! Opción no válida, debe estar en un rango de 1 a 3. ***[/red]")
                            continue
                    except ValueError:
                        print("[red]*** ¡ERROR! La opción debe ser un número entero. ***[/red]")
                        continue                         
        elif exportacion.upper() == "NO":
            print("[dark_orange]*** La información no fue exportada. ***[/dark_orange]")
            break
        else:
            print("[red]*** ¡ERROR! Ingresa una respuesta válida [SI / NO]. ***[/red]")
            continue



# Menú Principal
import datetime
import re
import socket
from tabulate import tabulate
import openpyxl
import csv
import sqlite3
from sqlite3 import Error
import sys
from rich import print as print

BaseDeDatos() # Se manda llamar a la base de datos, en caso de que no exista, se crea.

print("\n[bold dark_goldenrod]  ¡BIENVENIDO/A AL SISTEMA DEL TALLER MECÁNICO!  [/bold dark_goldenrod]")
while True:
    print("\n*************************************************")
    print(f"[bold cyan]{('Menú Principal').center(48)}[/bold cyan]")
    print("*************************************************")
    print("(1). Notas.")
    print("(2). Clientes.")
    print("(3). Servicios.")
    print("(4). Salir.")
    print("*************************************************")

    opcion_capturada = input("\nSeleccione una opción: ")

    if opcion_capturada.strip() == "":
        print("[red]*** ¡ERROR! No puede quedarse vacío. ***[/red]")
        continue
    else:
        try:
            # Convierte la opcion capturada a tipo de dato int.
            opcion = int(opcion_capturada)
        except Exception:
            print("[red]*** ¡ERROR! La opción debe ser un número entero. ***[/red]")
            continue

        if opcion == 1:
            Notas()
        elif opcion == 2:
            Clientes()
        elif opcion == 3:
            Servicios()
        elif opcion == 4:
            Salir()
        else:
            print("[red]*** Opción no válida. ***[/red]")
