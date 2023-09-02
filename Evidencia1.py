
notas = [
    {"folio": 1, "fecha": "2023-08-15", "monto": 100.00, "detalle": "Compra de libros"},
    {"folio": 2, "fecha": "2023-08-20", "monto": 50.00, "detalle": "Compra de alimentos"},
    {"folio": 3, "fecha": "2023-08-25", "monto": 200.00, "detalle": "Compra de ropa"},
]

def consulta_periodo():
    fecha_inicial = input("Ingrese la fecha inicial (YYYY-MM-DD): ")
    fecha_final = input("Ingrese la fecha final (YYYY-MM-DD): ")

    print(f'{fecha_inicial:4}')

    notas_periodo = []

    for nota in notas:
        if fecha_inicial <= nota["fecha"] <= fecha_final:
            notas_periodo.append(nota)

    if notas_periodo:
        print("\nReporte de notas por período:")
        print("{:<10} {:<15} {:<10}".format("Folio", "Fecha", "Monto"))
        for nota in notas_periodo:
            print("{:<10} {:<15} {:<10}".format(nota["folio"], nota["fecha"], nota["monto"]))
    else:
        print("\nNo hay notas emitidas para el período especificado.")

        # Función para consultar por folio
def consulta_folio():
    folio = int(input("Ingrese el folio de la nota a consultar: "))
    nota_encontrada = None

    for nota in notas:
        if nota["folio"] == folio:
            nota_encontrada = nota
            break

    if nota_encontrada:
        print("\nDetalle de la nota:")
        print("Folio:", nota_encontrada["folio"])
        print("Fecha:", nota_encontrada["fecha"])
        print("Monto:", nota_encontrada["monto"])
        print("Detalle:", nota_encontrada["detalle"])
    else:
        print("\nLa nota no se encuentra en el sistema o está cancelada.")

# Menú principal
while True:
    print("\nMenú de Consultas y Reportes:")
    print("1. Consulta por período")
    print("2. Consulta por folio")
    print("3. Salir")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        consulta_periodo()
    elif opcion == "2":
        consulta_folio()
    elif opcion == "3":
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")








