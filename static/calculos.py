def main():
    while True:
        cota_inicial = float(input("Ingrese la cota del BM: "))
        vista_mas = float(input("Ingrese la vista (+): "))

        while True:
            tipo_punto = input("¿Qué tipo de punto va a registrar? (Delta, Cambio): ")

            altura_instrumental = vista_mas + cota_inicial

            if tipo_punto == 'Delta':
                punto = input("Punto: ")
                vista_menos = float(input("Vista (-): "))
                cota_calculada = altura_instrumental - vista_menos
                print(f"{punto}: Vista (-):{vista_menos} Cota:{cota_calculada}")
            else:
                vista_mas = None
            
            if tipo_punto == 'Cambio':
                punto = input("Punto: ")
                vista_mas = float(input("Vista (+): "))
                altura_instrumental = cota_calculada + vista_mas
                print(f"{punto}: Altura instrumental:{altura_instrumental} Vista (+):{vista_mas} Cota:{cota_calculada}")
            else:
                vista_menos = None
            
            boton_agregar = input("¿Desea agregar otro punto? (s/n): ")
            if boton_agregar.lower() != 's':
                break  # Salir del bucle interno si no se desea agregar más puntos

        print("Su cartera ha sido registrada con éxito")
        break  # Salir del bucle principal después de registrar la cartera

if __name__ == "__main__":
    main()