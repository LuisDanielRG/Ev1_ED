def BaseDeDatos():
    # Creación de la base de datos.
    try:
        with sqlite3.connect("TallerMecanico.db") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Clientes (Clave INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, RFC TEXT NOT NULL, Correo TEXT NOT NULL);")
            cursor.execute("CREATE TABLE IF NOT EXISTS Servicios (Identificador INTEGER PRIMARY KEY, Nombre TEXT NOT NULL, Costo REAL NOT NULL);")
            cursor.execute("CREATE TABLE IF NOT EXISTS Notas (Folio INTEGER PRIMARY KEY, Fecha TIMESTAMP NOT NULL, ClienteID INTEGER NOT NULL, MontoPago REAL NOT NULL, Estado TEXT NOT NULL, FOREIGN KEY(ClienteID) REFERENCES Clientes(Clave));")
            cursor.execute("CREATE TABLE IF NOT EXISTS DetalleNotas (DetalleID INTEGER PRIMARY KEY, NotaID INTEGER NOT NULL, ServicioID INTEGER NOT NULL, FOREIGN KEY(NotaID) REFERENCES Notas(Folio), FOREIGN KEY(ServicioID) REFERENCES Servicios(Identificador));")
    except Error as error:
        print(error)
    except Exception:
        print(f"Ha ocurrido el siguiente error: {sys.exc_info()[0]}")



def Notas():

                def registrar_nota():
                    while True: 
                        with sqlite3.connect("TallerMecanico.db") as conn:
                            cursor = conn.cursor()

                            # Recopila información necesaria para la nota.
                            cliente_clave = input("Clave del cliente al cual se expedirá la nota: ")
                            if cliente_clave.strip() == '':
                                print("**** ¡Espacio vacio, regresando al menu. ****")
                                return
                            
        
                            detalle = input("Detalle de la nota: ")
                            if detalle.strip() == '':
                                print("**** ¡Espacio vacio. Regresando al menu.  ****")
                                return
                                

                                

                            # Verifica si el cliente ya está registrado.
                            cursor.execute("SELECT * FROM Clientes WHERE clave = ?", (cliente_clave,))
                            cliente = cursor.fetchone()

                            if cliente is None:
                                print("El cliente no está registrado. Registre al cliente primero.")
                                return
                            

                            # Ahora puedes insertar la nota en la base de datos.
                            cursor.execute("INSERT INTO Notas (cliente_clave, detalle) VALUES (?, ?)", (cliente_clave, detalle))
                            conn.commit()
                            print("Nota registrada exitosamente.")
              



            

                def mostrar_notas():
                    with sqlite3.connect("TallerMecanico.db") as conn:
                        cursor = conn.cursor()

                        cursor.execute("SELECT * FROM Notas")
                        notas = cursor.fetchall()

                        if not notas:
                            print("No hay notas registradas.")
                        else:
                            headers = ["ID", "Clave del Cliente", "Detalle"]
                            data = [(nota[0], nota[1], nota[2]) for nota in notas]
                            print(tabulate(data, headers=headers, tablefmt="grid"))

                        volver = input('Presione "Enter" para volver al menu ')
                        if volver.strip() == '':
                                return


                def cancelar_nota():
                    while True:
                        with sqlite3.connect("TallerMecanico.db") as conn:
                            cursor = conn.cursor()

                            folio_nota = input("Ingrese el folio de la nota a cancelar: ")
                            if folio_nota.strip() == '':
                                    print("**** Regresando al menu.  ****")
                                    return
                            if isinstance(folio_nota, str):
                                print("***Valor no valido, debe ser numero entero***")
                                print("Recuerde presionar 'Enter' para volver al menu")
                                continue

                            # Verifica si la nota existe y no está cancelada.
                            cursor.execute("SELECT * FROM Notas WHERE id = ? AND cancelada = 0", (folio_nota,))
                            nota = cursor.fetchone()

                            if nota is None:
                                print("La nota no existe o ya está cancelada en el sistema.")
                                return
                            
                            
                                

                            # Muestra los detalles de la nota.
                            print("\nDetalles de la nota a cancelar:")
                            print(f"Folio: {nota[0]}")
                            print(f"Clave del Cliente: {nota[1]}")
                            print(f"Detalle: {nota[2]}")

                            confirmacion = input("¿Desea cancelar esta nota? (Sí/No): ")

                            if confirmacion.lower() == "si":
                                # Realiza la cancelación de la nota.
                                cursor.execute("UPDATE Notas SET cancelada = 1 WHERE id = ?", (folio_nota,))
                                conn.commit()
                                print("La nota ha sido cancelada exitosamente.")
                            else:
                                print("La nota no ha sido cancelada.")

                def recuperar_nota():
                    while True:

                        with sqlite3.connect("TallerMecanico.db") as conn:
                            cursor = conn.cursor()

                            # Obtiene todas las notas canceladas.
                            cursor.execute("SELECT * FROM Notas WHERE cancelada = 1")
                            notas_canceladas = cursor.fetchall()

                            if not notas_canceladas:
                                print("No hay notas canceladas en el sistema.")
                                return

                            # Muestra un listado tabular de las notas canceladas sin su detalle.
                            headers = ["Folio", "Clave del Cliente"]
                            data = [(nota[0], nota[1]) for nota in notas_canceladas]
                            print(tabulate(data, headers=headers, tablefmt="grid"))

                            folio_nota_recuperar = input("Ingrese el folio de la nota que desea recuperar (o presione 'Enter' para cancelar): ")
                            

                            if folio_nota_recuperar() == "":
                                print("Regresando al menu.")
                                return

                            # Verifica si el folio ingresado corresponde a una nota cancelada.
                            cursor.execute("SELECT * FROM Notas WHERE id = ? AND cancelada = 1", (folio_nota_recuperar,))
                            nota = cursor.fetchone()

                            if nota is None:
                                print("El folio ingresado no corresponde a una nota cancelada en el sistema.")
                                return

                            # Muestra los detalles de la nota y solicita confirmación para recuperarla.
                            print("\nDetalles de la nota a recuperar:")
                            print(f"Folio: {nota[0]}")
                            print(f"Clave del Cliente: {nota[1]}")

                            confirmacion = input("¿Desea recuperar esta nota? (Sí/No): ")
                            if confirmacion == "":
                                print("No se detecto una respuesta, intente de nuevo.")
                                continue

                            if confirmacion.lower() == "si":
                                # Realiza la recuperación de la nota.
                                cursor.execute("UPDATE Notas SET cancelada = 0 WHERE id = ?", (folio_nota_recuperar,))
                                conn.commit()
                                print("La nota ha sido recuperada exitosamente.")
                            else:
                                print("La nota no ha sido recuperada.")

                def consulta_por_periodo():
                    while True:

                        with sqlite3.connect("TallerMecanico.db") as conn:
                            cursor = conn.cursor()

                            fecha_inicial = input("Ingrese la fecha inicial (en formato mm/dd/aaaa o presione Enter para usar 01/01/2000): ")
                            fecha_final = input("Ingrese la fecha final (en formato mm/dd/aaaa o presione Enter para usar la fecha actual): ")

                            # Validación de las fechas.
                            if not fecha_inicial:
                                fecha_inicial = "01/01/2000"
                                print("Fecha inicial asumida como 01/01/2000.")
                            if not fecha_final:
                                fecha_final = datetime.datetime.now().strftime("%m/%d/%Y")
                                print(f"Fecha final asumida como {fecha_final}.")

                            # Convertir fechas a objetos datetime.
                            try:
                                fecha_inicial = datetime.datetime.strptime(fecha_inicial, "%m/%d/%Y")
                                fecha_final = datetime.datetime.strptime(fecha_final, "%m/%d/%Y")
                            except ValueError:
                                print("Formato de fecha incorrecto. Utilice mm/dd/aaaa.")
                                return

                            # Verificar que la fecha final sea igual o posterior a la fecha inicial.
                            if fecha_final < fecha_inicial:
                                print("La fecha final debe ser igual o posterior a la fecha inicial.")
                                return

                            # Consultar notas en el período especificado.
                            cursor.execute("SELECT id, cliente_clave, fecha FROM Notas WHERE fecha >= ? AND fecha <= ? AND cancelada = 0", (fecha_inicial, fecha_final))
                            notas_periodo = cursor.fetchall()

                            if not notas_periodo:
                                print("No hay notas emitidas para el período especificado.")
                                return

                            # Calcular el monto promedio de las notas del período.
                            cursor.execute("SELECT AVG(total) FROM Notas WHERE fecha >= ? AND fecha <= ? AND cancelada = 0", (fecha_inicial, fecha_final))
                            monto_promedio = cursor.fetchone()[0]

                            # Muestra el reporte tabular de notas y el monto promedio.
                            headers = ["Folio", "Clave del Cliente", "Fecha"]
                            data = [(nota[0], nota[1], nota[2]) for nota in notas_periodo]
                            print("\nReporte de Notas por Período:")
                            print(tabulate(data, headers=headers, tablefmt="grid"))
                            print(f"Monto Promedio de las Notas en el Período: ${monto_promedio:.2f}")

                            # Ofrece la opción de exportar el resultado.
                            print('¿Desea exportar el reporte a CSV, Excel o regresar al menú de reportes?')
                            exportar_reporte = input(f" [1] CSV\n [2] Excel\n [3] Regresar \n :")

                            if exportar_reporte() == 1:
                                exportar_a_csv(data, fecha_inicial, fecha_final)
                            elif exportar_reporte() == 2:
                                exportar_a_excel(data, fecha_inicial, fecha_final)
                            elif exportar_reporte() == 3:
                                return
                            if isinstance(exportar_reporte, str):
                                print("valor no valido. Intente de nuevo.")
                                continue
                            else:
                                print("Opción no válida.")
                                continue

                def consulta_por_folio():
                    while True:
                        
                        with sqlite3.connect("TallerMecanico.db") as conn:
                            cursor = conn.cursor()

                            # Obtener y mostrar un listado tabular de los folios, fechas y nombres de clientes.
                            cursor.execute("SELECT N.id, N.fecha, C.nombre FROM Notas N JOIN Clientes C ON N.cliente_clave = C.clave WHERE N.cancelada = 0 ORDER BY N.id")
                            notas = cursor.fetchall()

                            if not notas:
                                print("No hay notas no canceladas en el sistema.")
                                return

                            headers = ["Folio", "Fecha", "Nombre del Cliente"]
                            data = [(nota[0], nota[1], nota[2]) for nota in notas]
                            print("\nListado de Notas no Canceladas:")
                            print(tabulate(data, headers=headers, tablefmt="grid"))

                            folio_nota_consultar = input("Ingrese el folio de la nota a consultar (o escriba 'No' para cancelar): ")

                            if folio_nota_consultar.lower() == "no":
                                return
                            elif folio_nota_consultar.lower() == "n":
                                return
                            elif isinstance(folio_nota_consultar, int):
                                print("Valor no valido, intente de nuevo")
                                continue
                            elif isinstance(folio_nota_consultar, float):
                                print("Valor no valido, intente de nuevo")
                                continue
                                
                            # Verifica si el folio ingresado corresponde a una nota no cancelada.
                            cursor.execute("SELECT N.id, N.cliente_clave, N.detalle, C.* FROM Notas N JOIN Clientes C ON N.cliente_clave = C.clave WHERE N.id = ? AND N.cancelada = 0", (folio_nota_consultar,))
                            nota = cursor.fetchone()

                            if nota is None:
                                print("El folio ingresado no corresponde a una nota no cancelada en el sistema.")
                                return

                            # Muestra los detalles de la nota y sus servicios.
                            print("\nDetalles de la Nota:")
                            print(f"Folio: {nota[0]}")
                            print(f"Clave del Cliente: {nota[1]}")
                            print(f"Detalle de la Nota: {nota[2]}")
                            print("\nDatos del Cliente:")
                            print(f"Nombre: {nota[4]}")
                            print(f"Dirección: {nota[5]}")
                            print(f"Teléfono: {nota[6]}")
                            print("\nServicios:")




                def consultas_y_reportes():
                    while True:
                        print("\n*************************************************")
                        print("                    NOTAS                        ")
                        print("*************************************************")
                        print("(1) Consulta por folio.")
                        print("(2) Consulta por periodo.")
                        print("(3) Volver al menu principal.")
                        print("*************************************************")
                        tipo_consul = input("Que tipo de consulta desea?: ")
                        if tipo_consul.strip() == "":
                            print("**** ¡ERROR! No puede quedarse vacío. ****")
                            continue
                        else:
                            try:
                                # Convierte la opcion capturada a tipo de dato int.
                                 consul = int(tipo_consul)
                            except Exception:
                                print("***** ¡ERROR! La opción debe ser un número entero. *****")
                                continue

                            if consul == 1:
                                consulta_por_folio()
                            elif consul == 2:
                                consulta_por_periodo()
                            elif consul == 3:
                                return
                            else:
                                 print("**** Opción no válida. ****")
                                 
                            




                while True:
                                print("\n*************************************************")
                                print("                    NOTAS                        ")
                                print("*************************************************")
                                print("(1) Registrar nota.")
                                print("(2) Mostrar nota.")
                                print("(3) Cancelar nota.")
                                print("(4) Recuperar nota.")
                                print("(5) Consultas y reportes.")
                                print("(6) Volver al menu principal.")
                                print("*************************************************")
                                opcion_nota = input("Seleccione su opcion: ")
                                if opcion_nota.strip() == "":
                                    print("**** ¡ERROR! No puede quedarse vacío. ****")
                                    continue
                                else:
                                    try:
                                        # Convierte la opcion capturada a tipo de dato int.
                                        Nota = int(opcion_nota)
                                    except Exception:
                                        print("***** ¡ERROR! La opción debe ser un número entero. *****")
                                        continue

                                    if Nota == 1:
                                        registrar_nota()
                                    elif Nota == 2:
                                        mostrar_notas()
                                    elif Nota == 3:
                                        cancelar_nota()
                                    elif Nota == 4:
                                        recuperar_nota()
                                    elif Nota == 5:
                                        consultas_y_reportes()
                                    elif Nota == 6:
                                        return
                                    
                                        


def Clientes():
    # Opción 2. Clientes.

    def AgregarCliente():
        # Opción 2.1. Agregar un cliente.
        while True:
            # Solicita el nombre y valida que no quede vacío.
            while True:
                nombre_cliente = input("\nIngresa el nombre del cliente: ")
                if nombre_cliente.strip() == "":
                    print("**** ¡ERROR! El nombre no puede quedar vacío. ****")
                else:
                    break
            
            # Solicita el RFC del cliente, y valida que este en un formato valido.
            patron_rfc = r'^[A-ZÑ&]{3,4}[0-9]{6}[A-Z0-9]{3}$'

            while True:
                rfc_captura = input("\nIngrese el RFC del cliente: ")
                rfc_cliente = rfc_captura.strip().upper()

                if not re.match(patron_rfc, rfc_cliente):
                    print("**** ¡ERROR! El RFC no cumple con el patrón asignado. ****")
                else:
                    letras_iniciales = rfc_cliente[:4] if len(rfc_cliente) == 13 else rfc_cliente[:3]
                    fecha_str = rfc_cliente[len(letras_iniciales):len(letras_iniciales) + 6]

                    try:
                        fecha_rfc = datetime.datetime.strptime(fecha_str, "%y%m%d").date()
                        if fecha_rfc > datetime.date.today():
                            print("**** ¡ERROR! El RFC no es válido. ****")
                            continue
                        else:
                            if len(rfc_cliente) == 13:
                                print("El RFC ingresado es de persona física.")
                                break
                            else:
                                print("El RFC ingresado es de persona moral.")
                                break
                    except Exception:
                        print("**** ¡ERROR! La fecha del RFC no es válida. ****")
                        continue
            
            # Solicita el correo electrónico del cliente y hace las respectivas validaciones.
            patron_correo = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

            while True:
                correo = input("\nIngrese el correo del cliente: ").lower()

                if not re.match(patron_correo,correo):
                    print("**** ¡ERROR! El correo no cumple con el patrón asignado. ****")
                    continue
                else:
                    dominio = correo.split('@')[1]
                    try:
                        socket.gethostbyname(dominio)
                        break
                    except Exception:
                        print("**** ¡ERROR! El dominio no existe, intenta de nuevo. ****")
                        continue
            
            try:
                with sqlite3.connect("TallerMecanico.db") as conn:
                    cursor = conn.cursor()
                    datos_cliente = (nombre_cliente, rfc_cliente, correo)
                    cursor.execute("INSERT INTO Clientes (Nombre, RFC, Correo) VALUES (?,?,?)", datos_cliente)
                    print(f"Cliente registrado exitosamente con la clave {cursor.lastrowid}")
                    break
            except Error as error:
                print(error)
            except Exception:
                print(f"Ha ocurrido el siguiente error: {sys.exc_info()[0]}")


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
                            encabezado = ["Clave", "Nombre", "RFC", "Correo"]
                            reporte_clave = tabulate(datos_clientes, encabezado, tablefmt="grid")
                            print("\n               REPORTE DE CLIENTES ORDENADOS POR CLAVE")
                            print(reporte_clave)
                        else:
                            print("**** No hay clientes en la base de datos. ****")
                            
                        while True:
                            exportacion = input("\n¿Deseas exportar la información anterior? [SI/NO] >> ")
                            if exportacion.upper() == "SI":
                                while True:
                                    print("\n*************************************************")
                                    print("                    Opciones                   ")
                                    print("*************************************************")
                                    print("(1) Archivo CSV.")
                                    print("(2) Excel.")
                                    print("(3) Regresar al menú de consultas y reportes.")
                                    print("*************************************************")

                                    opcion_capturada = input("\nSeleccione una opción: ")

                                    if opcion_capturada.strip() == "":
                                        print("*** ¡ERROR! No puede quedarse vacío. ***")
                                        continue
                                    else:
                                        try:
                                            # Convierte la opción capturada a tipo de dato int.
                                            opcion_exportar = int(opcion_capturada)
                                        except ValueError:
                                            print("*** ¡ERROR! La opción debe ser un número entero. ***")
                                            continue

                                        fecha_actual = datetime.datetime.today().strftime("%m_%d_%Y")
                                        if opcion_exportar == 1:
                                            # Exportar información a CSV
                                            archivo_csv = f"ReporteClientesActivosPorClave_{fecha_actual}.csv"
                                            ExportarDatos(datos_clientes, archivo_csv, encabezado=encabezado)
                                            print(f"Información exportada correctamente con el nombre {archivo_csv}")
                                        elif opcion_exportar == 2:
                                            # Exportar información a EXCEL
                                            archivo_excel = f"ReporteClientesActivosPorClave_{fecha_actual}.xlsx"
                                            ExportarDatos(datos_clientes, archivo_excel, encabezado=encabezado)
                                            print(f"Información exportada correctamente con el nombre {archivo_excel}")
                                        elif opcion_exportar == 3:
                                            return
                                        else:
                                            print("*** Opción no válida. ***")                          
                            elif exportacion.upper() == "NO":
                                print("**** La información no fue exportada. ****")
                                break
                            else:
                                print("**** ¡ERROR! Ingresa una respuesta válida [SI / NO]. ****")
                                continue
                except Error as error:
                    print(error)
                except Exception:
                    print(f"Ha ocurrido el siguiente error: {sys.exc_info()[0]}")


            def OrdenadoNombre():
                # Opción 2.2.1.2. Listado de clientes ordenado por nombre.
                try:
                    with sqlite3.connect("TallerMecanico.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Clientes ORDER BY Nombre;")
                        datos_clientes = cursor.fetchall()

                        if datos_clientes:
                            encabezado = ["Clave", "Nombre", "RFC", "Correo"]
                            reporte_nombre= tabulate(datos_clientes, encabezado, tablefmt="grid")
                            print("\n               REPORTE DE CLIENTES ORDENADOS POR NOMBRES")
                            print(reporte_nombre)
                        else:
                            print("**** No hay clientes en la base de datos. ****")

                        while True:
                            exportacion = input("\n¿Deseas exportar la información anterior? [SI/NO] >> ")
                            if exportacion.upper() == "SI":
                                while True:
                                    print("\n*************************************************")
                                    print("                    Opciones                   ")
                                    print("*************************************************")
                                    print("(1) Archivo CSV.")
                                    print("(2) Excel.")
                                    print("(3) Regresar al menú de consultas y reportes.")
                                    print("*************************************************")

                                    opcion_capturada = input("\nSeleccione una opción: ")

                                    if opcion_capturada.strip() == "":
                                        print("*** ¡ERROR! No puede quedarse vacío. ***")
                                        continue
                                    else:
                                        try:
                                            # Convierte la opción capturada a tipo de dato int.
                                            opcion_exportar = int(opcion_capturada)
                                        except ValueError:
                                            print("*** ¡ERROR! La opción debe ser un número entero. ***")
                                            continue
                                                
                                        fecha_actual = datetime.datetime.today().strftime("%m_%d_%Y")
                                        if opcion_exportar == 1:
                                            # Exportar información a CSV
                                            archivo_csv = f"ReporteClientesActivosPorNombre_{fecha_actual}.csv"
                                            ExportarDatos(datos_clientes, archivo_csv, encabezado=encabezado)
                                            print(f"Información exportada correctamente con el nombre {archivo_csv}")
                                        elif opcion_exportar == 2:
                                            # Exportar información a EXCEL
                                            archivo_excel = f"ReporteClientesActivosPorNombre_{fecha_actual}.xlsx"
                                            ExportarDatos(datos_clientes, archivo_excel, encabezado=encabezado)
                                            print(f"Información exportada correctamente con el nombre {archivo_excel}")
                                        elif opcion_exportar == 3:
                                            return
                                        else:
                                            print("*** Opción no válida. ***")
                            elif exportacion.upper() == "NO":
                                print("**** La información no fue exportada. ****")
                                break
                            else:
                                print("**** ¡ERROR! Ingresa una respuesta válida [SI / NO]. ****")
                                continue
                except Error as error:
                    print(error)
                except Exception:
                    print(f"Ha ocurrido el siguiente error: {sys.exc_info()[0]}")


            while True:
                # Submenú de listado de clientes.
                print("\n************************************")
                print("  Menú de Listado de Clientes  ")
                print("************************************")
                print("1. Ordenado por clave.")
                print("2. Ordenado por nombre.")
                print("3. Volver al menú anterior.")
                print("************************************")

                sub_opcion_capturada = input("\nSeleccione una opción: ")

                if sub_opcion_capturada.strip() == "":
                    print("**** ¡ERROR! No puede quedarse vacío. ****")
                    continue
                else:
                    try:
                        # Convierte la opcion capturada a tipo de dato int.
                        sub_opcion_listado = int(sub_opcion_capturada)
                    except Exception:
                        print("***** ¡ERROR! La opción debe ser un número entero. *****")
                        continue

                    if sub_opcion_listado == 1:
                        OrdenadoClave()
                    elif sub_opcion_listado == 2:
                        OrdenadoNombre()
                    elif sub_opcion_listado == 3:
                        print("Volviendo al menú anterior...")
                        break
                    else:
                        print("***** Opción no válida. *****") 


        def BusquedaClave():
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
                            print(f"\n           BÚSQUEDA DE CLIENTES POR LA CLAVE {clave_consulta}")
                            print(busqueda_clave)
                        else:
                            print(f"*** No se encontró ningún cliente con la clave {clave_consulta} ***")

                    break
                except ValueError:
                    print("**** ¡ERROR! La clave debe ser un número entero. ****")
                except Error as error:
                    print(error)
                except Exception:
                    print(f"Ha ocurrido el siguiente error: {sys.exc_info()[0]}")


        def BusquedaNombre():
            # Opción 2.2.3. Búsqueda de clientes por nombre.
            while True:
                # Solicita el nombre a consultar.
                nombre_consulta = input("\nIngrese el nombre del cliente a consultar: ")
                if nombre_consulta.strip() == "":
                    print("**** ¡ERROR! El nombre no puede quedar vacío. ****")
                else:
                    break
            
            try:
                with sqlite3.connect("TallerMecanico.db") as conn:
                    cursor = conn.cursor()
                    dato = {"nombre":nombre_consulta.upper()}
                    cursor.execute("SELECT * FROM Clientes WHERE UPPER(Nombre) = :nombre", dato)
                    datos_consulta_nombre = cursor.fetchall()

                    if datos_consulta_nombre:
                        encabezado = ["CLAVE", "NOMBRE", "RFC", "CORREO"]
                        busqueda_nombre = tabulate(datos_consulta_nombre, encabezado, tablefmt="grid")
                        print(f"\n          BÚSQUEDA DE CLIENTES POR EL NOMBRE '{nombre_consulta.upper()}'")
                        print(busqueda_nombre)
                    else:
                        print(f"*** No se encontró ningún cliente con el nombre '{nombre_consulta}' ***")
            except Error as error:
                print(error)
            except Exception:
                print(f"Ha ocurrido el siguiente error: {sys.exc_info()[0]}")


        while True:
            # Submenú de consultas y reportes.
            print("\n************************************")
            print("Menú de Consultas y Reportes de Clientes")
            print("************************************")
            print("1. Listado de clientes registrados.")
            print("2. Búsqueda por clave.")
            print("3. Búsqueda por nombre.")
            print("4. Volver al menú de clientes.")
            print("************************************")

            sub_opcion_capturada = input("\nSeleccione una opción: ")

            if sub_opcion_capturada.strip() == "":
                print("**** ¡ERROR! No puede quedarse vacío. ****")
                continue
            else:
                try:
                    # Convierte la opcion capturada a tipo de dato int.
                    sub_opcion_consultas = int(sub_opcion_capturada)
                except Exception:
                    print("***** ¡ERROR! La opción debe ser un número entero. *****")
                    continue

                if sub_opcion_consultas == 1:
                    ListadoClientes()
                elif sub_opcion_consultas == 2:
                    BusquedaClave()
                elif sub_opcion_consultas == 3:
                    BusquedaNombre()
                elif sub_opcion_consultas == 4:
                    print("Volviendo al menú de clientes...")
                    break
                else:
                    print("***** Opción no válida. *****")    


    while True:
        # Submenú de clientes.
        print("\n************************************")
        print("           Menú de Clientes          ")
        print("************************************")
        print("1. Agregar un cliente.")
        print("2. Consultas y reportes.")
        print("3. Volver al menú principal")
        print("************************************")

        sub_opcion_capturada = input("\nSeleccione una opción: ")

        if sub_opcion_capturada.strip() == "":
            print("**** ¡ERROR! No puede quedarse vacío. ****")
            continue
        else:
            try:
                # Convierte la opcion capturada a tipo de dato int.
                sub_opcion_clientes = int(sub_opcion_capturada)
            except Exception:
                print("***** ¡ERROR! La opción debe ser un número entero. *****")
                continue

            if sub_opcion_clientes == 1:
                AgregarCliente()
            elif sub_opcion_clientes == 2:
                ConsultasReportesCliente()
            elif sub_opcion_clientes == 3:
                print("Volviendo al menú principal...")
                break
            else:
                print("***** Opción no válida. *****")    


def Servicios():
    def agregar_servicio():
        while True:
         nom_serv_nuevo =input("Dime el nombre que describe el nuevo servicio: ")
         
         if nom_serv_nuevo.strip() == "":
            print("**** ¡ERROR! No puede quedarse vacío. ****")
         else:
             pass
         
         mont_serv_nuevo = float(input("dime cuanto va a cosar el nuevo servicio (Tiene que ser mayor a $0.00): "))
         if mont_serv_nuevo == " ":
             print("***** El campo no puede quedar vacio ")
         else:
             try:
                mont_serv_nuevo = float(mont_serv_nuevo)
                if mont_serv_nuevo <= 0:
                    print("**** ¡ERROR! El monto debe ser mayor a $0.00. ****")
                else:
                    print("[green]Servicio agregado correctamente [/green]")
                    break
             except ValueError:
                print("**** ¡ERROR! Ingresa un valor numérico válido. ****")
            
         try:
            with sqlite3.connect("TallerMecanico.db") as conn:
                datos_nuev_servicios =(nom_serv_nuevo, mont_serv_nuevo)
                mi_cursor= conn.cursor()
                mi_cursor.execute("INSERT INTO Servicios(Nombre, Costo) VALUES(?,?)", (datos_nuev_servicios))
                conn.commit()
         except Error as e:
                print(f"[red]{e}[/red]")
         except Exception:
             print(f"[red]Se produjo el siguiente error: {sys.exc_info()[0]}[/red]")
         
             
         
         
         
        
        

    while True:
        # Aqui va todo el código correspondiente a SERVICIOS. Quitar esta línea.
        print("\n************************************")
        print("           Menú de servicios          ")
        print("************************************")
        print("1. agregar un nuevo servicio")
        print("2. Consultas y reportes de los servicios ")
        print("3. volver al menu principal")
        opcion_servicios = int(input("Selecciona una opcion "))
        
        if opcion_capturada.strip() == "":
            print("**** ¡ERROR! No puede quedarse vacío. ****")
        elif opcion_servicios == 1:
            agregar_servicio()
    


   


def Salir():
    # Opción 4. Salida del sistema.
    while True:
        confirmacion_salida = input("\n¿Estas seguro de salir del sistema [SI / NO]? >> ")
        if confirmacion_salida.upper() == "SI":
            print("Gracias por visitar este sistema. ¡Vuelva pronto!\n")
            exit()
        elif confirmacion_salida.upper() == "NO":
            print("Volviendo al menú principal...")
            return
        else:
            print("**** ¡ERROR! Ingresa una respuesta válida [SI / NO]. ****")
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
        print("*** Formato de archivo no compatible, debe ser CSV o EXCEL. ***")

def exportar_a_csv(data, fecha_inicial, fecha_final):
    file_name = f"ReportePorPeriodo_{fecha_inicial.strftime('%m_%d_%Y')}_{fecha_final.strftime('%m_%d_%Y')}.csv"

    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Escribe los encabezados.
        csv_writer.writerow(["Folio", "Clave del Cliente", "Fecha"])
        # Escribe los datos.
        csv_writer.writerows(data)

def exportar_a_excel(data, fecha_inicial, fecha_final):
    file_name = f"ReportePorPeriodo_{fecha_inicial.strftime('%m_%d_%Y')}_{fecha_final.strftime('%m_%d_%Y')}.xlsx"

    workbook = Workbook()
    sheet = workbook.active
    # Escribe los encabezados.
    sheet.append(["Folio", "Clave del Cliente", "Fecha"])
    # Escribe los datos.
    for row in data:
        sheet.append(row)

    workbook.save(file_name)
    print(f"El reporte se ha exportado a {file_name} en formato Excel.")





# Menú Principal
import datetime
import re
import socket
from tabulate import tabulate
import openpyxl
import numpy as np
import csv
import os
import sqlite3
from sqlite3 import Error
import sys
import rich
from rich import print as print 
from openpyxl import Workbook

BaseDeDatos() # Se manda llamar a la base de datos, en caso de que no exista, se crea.

print("\n  ¡BIENVENIDO/A AL SISTEMA DEL TALLER MECÁNICO!  ")
while True:
    print("\n*************************************************")
    print("  [bold blue]      ¿Qué desea realizar el día de hoy?  [/bold blue]     ")
    print("*************************************************")
    print("(1) Notas.")
    print("(2) Clientes.")
    print("(3) Servicios.")
    print("(4) Salir.")
    print("*************************************************")

    opcion_capturada = input("\nSeleccione una opción: ")

    if opcion_capturada.strip() == "":
        print("**** ¡ERROR! No puede quedarse vacío. ****")
        continue
    else:
        try:
            # Convierte la opcion capturada a tipo de dato int.
            opcion = int(opcion_capturada)
        except Exception:
            print("***** ¡ERROR! La opción debe ser un número entero. *****")
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
            print("**** Opción no válida. ****")
