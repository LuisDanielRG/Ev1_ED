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
    # Aqui va todo el código correspondiente a NOTAS. Quitar esta línea.
    print("")


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
    

def Servicios():
    def ConsultasReportesServicios():
        def ListadoServicios():
            def OrdenadoClave():
                try:
                    with sqlite3.connect("TallerMecanico.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Servicios ORDER BY Identificador;")
                        datos_servicios = cursor.fetchall()

                        if datos_servicios:
                            encabezado = ["Clave", "Nombre", "Costo"]
                            reporte_clave = tabulate(datos_servicios, encabezado, tablefmt="grid")
                            print("\n               REPORTE DE SERVICIOS ORDENADOS POR CLAVE")
                            print(reporte_clave)
                        else:
                            print("**** No hay servicios en la base de datos. ****")

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
                                            opcion_exportar = int(opcion_capturada)
                                        except ValueError:
                                            print("*** ¡ERROR! La opción debe ser un número entero. ***")
                                            continue

                                        fecha_actual = datetime.datetime.today().strftime("%m_%d_%Y")
                                        if opcion_exportar == 1:
                                            archivo_csv = f"ReporteServiciosPorClave_{fecha_actual}.csv"
                                            ExportarDatos(datos_servicios, archivo_csv, encabezado=encabezado)
                                            print(f"Información exportada correctamente con el nombre {archivo_csv}")
                                        elif opcion_exportar == 2:
                                            archivo_excel = f"ReporteServiciosPorClave_{fecha_actual}.xlsx"
                                            ExportarDatos(datos_servicios, archivo_excel, encabezado=encabezado)
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
                try:
                    with sqlite3.connect("TallerMecanico.db") as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT * FROM Servicios ORDER BY Nombre;")
                        datos_servicios = cursor.fetchall()

                        if datos_servicios:
                            encabezado = ["Clave", "Nombre", "Costo"]
                            reporte_nombre = tabulate(datos_servicios, encabezado, tablefmt="grid")
                            print("\n               REPORTE DE SERVICIOS ORDENADOS POR NOMBRE")
                            print(reporte_nombre)
                        else:
                            print("**** No hay servicios en la base de datos. ****")

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
                                            opcion_exportar = int(opcion_capturada)
                                        except ValueError:
                                            print("*** ¡ERROR! La opción debe ser un número entero. ***")
                                            continue

                                        fecha_actual = datetime.datetime.today().strftime("%m_%d_%Y")
                                        if opcion_exportar == 1:
                                            archivo_csv = f"ReporteServiciosPorNombre_{fecha_actual}.csv"
                                            ExportarDatos(datos_servicios, archivo_csv, encabezado=encabezado)
                                            print(f"Información exportada correctamente con el nombre {archivo_csv}")
                                        elif opcion_exportar == 2:
                                            archivo_excel = f"ReporteServiciosPorNombre_{fecha_actual}.xlsx"
                                            ExportarDatos(datos_servicios, archivo_excel, encabezado=encabezado)
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
                print("\n*************************************************")
                print("  Menú de Listado de Servicios  ")
                print("*************************************************")
                print("1. Ordenado por clave.")
                print("2. Ordenado por nombre.")
                print("3. Volver al menú de consultas y reportes.")
                print("*************************************************")

                sub_opcion_capturada = input("\nSeleccione una opción: ")

                if sub_opcion_capturada.strip() == "":
                    print("**** ¡ERROR! No puede quedarse vacío. ****")
                    continue
                else:
                    try:
                        sub_opcion_listado = int(sub_opcion_capturada)
                    except Exception:
                        print("***** ¡ERROR! La opción debe ser un número entero. *****")
                        continue

                    if sub_opcion_listado == 1:
                        OrdenadoClave()
                    elif sub_opcion_listado == 2:
                        OrdenadoNombre()
                    elif sub_opcion_listado == 3:
                        print("Volviendo al menú de consultas y reportes...")
                        break
                    else:
                        print("***** Opción no válida. *****")

        while True:
            print("\n************************************")
            print("           Menú de servicios          ")
            print("************************************")
            print("1. Agregar un nuevo servicio.")
            print("2. Consultas y reportes de servicios.")
            print("3. Volver al menú principal.")
            print("************************************")

            sub_opcion_capturada = input("\nSeleccione una opción: ")

            if sub_opcion_capturada.strip() == "":
                print("**** ¡ERROR! No puede quedarse vacío. ****")
                continue
            else:
                try:
                    sub_opcion_servicios = int(sub_opcion_capturada)
                except Exception:
                    print("***** ¡ERROR! La opción debe ser un número entero. *****")
                    continue

                if sub_opcion_servicios == 1:
                    AgregarServicio()
                elif sub_opcion_servicios == 2:
                    ConsultasReportesServicios()
                elif sub_opcion_servicios == 3:
                    print("Volviendo al menú principal...")
                    break
                else:
                    print("***** Opción no válida. *****")

   


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
