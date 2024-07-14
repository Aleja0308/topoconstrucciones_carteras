
cota = 0

def main():
    while True:
        cota_inicial = float(input("Ingrese la cota del BM: "))
        vista_mas = float(input("Inrese la vista(+): "))
        tipo_punto = input("Tipo de punto (Delta, Cambio): ")
        
        altura_instrumental = vista_mas + cota_inicial
        
        if tipo_punto == 'Delta':
            punto = input("Punto: ")
            vista_menos = float(input("Vista (-): "))
            cota_anterior = altura_instrumental - vista_menos
            print(f"{punto}: \n Vista menos:{vista_menos} \n Cota: {cota_anterior}")
        else:
            vista_mas = None
            
        if tipo_punto == 'Cambio':
            punto = input("Punto: ")
            vista_mas = float(input("Vista (+): "))
            altura_instrumental = cota_anterior + vista_mas
            print(f"{punto}: \n Altura instrumental:{altura_instrumental} \n Vista mas: {vista_mas} \n Cota: {cota_anterior}")
        else:
            vista_menos = None
        continue

if __name__ == "__main__":
    main()