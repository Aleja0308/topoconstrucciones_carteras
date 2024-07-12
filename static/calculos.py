cota_anterior = 0
cota = 0

def main():
    while True:
        cota_inicial = float(input("Ingrese la cota del BM:"))
        tipo_punto = input("Tipo de punto (BM, Delta, Cambio): ")
        punto = int(input("Punto: "))

        if tipo_punto == 'BM':
            vista_mas = float(input("Vista (+): "))
        else:
            vista_menos = None
        
        if tipo_punto == 'Delta':
            vista_menos = float(input("Vista (-): "))
        else:
            vista_mas = None
            
        if tipo_punto == 'Cambio':
            vista_mas = float(input("Vista (+): "))
        else:
            vista_menos = None

        # Calcular altura instrumental:
        if tipo_punto == 'BM':
            altura_instrumental = cota_inicial + vista_mas
        else:
            altura_instrumental = None

        if tipo_punto == 'Cambio':
            altura_instrumental = cota_anterior + vista_mas
        else:
            altura_instrumental = None

        # Calcular cota para punto delta:
        if tipo_punto == 'Delta':
            cota_anterior = altura_instrumental - vista_menos
        else:
            cota_anterior = None
        
        # Mostrar resultados
        print("\nResultados:")
        print(f"Tipo de punto: {tipo_punto}")
        print(f"Punto: {punto}")
        if tipo_punto == 'BM' or tipo_punto == 'Cambio':
            print(f"Vista (+): {vista_mas}")
        if tipo_punto == 'Delta':
            print(f"Vista (-): {vista_menos}")
        print(f"Cota: {cota}")
        
        if tipo_punto == 'BM' or tipo_punto == 'Cambio':
            print(f"Altura instrumental: {altura_instrumental}")
        if tipo_punto == 'Delta':
            print(f"Nueva cota para delta: {cota_anterior}")

        # Preguntar si se desea agregar otro punto:
        respuesta = input("\n¿Desea agregar otro punto? (s/n): ").strip().lower()
        if respuesta != 's':
            break

if __name__ == "__main__":
    main()