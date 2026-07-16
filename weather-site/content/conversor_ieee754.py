def obtener_signo(numero):
    """Devuelve '1' si es negativo, '0' si es positivo."""
    return "1" if numero < 0 else "0"

def entero_a_binario(entero):
    """Convierte la parte entera a binario dividiendo sucesivamente para 2."""
    if entero == 0: return "0"
    binario = ""
    while entero > 0:
        binario = str(entero % 2) + binario
        entero = entero // 2
    return binario

def fraccion_a_binario(fraccion, precision=50):
    """Multiplica sucesivamente la fracción por 2 para extraer los bits."""
    binario = ""
    while fraccion > 0 and len(binario) < precision:
        fraccion *= 2
        bit = int(fraccion)
        binario += str(bit)
        fraccion -= bit
    return binario if binario else "0"

def normalizar_y_exponente(binario_entero, binario_fraccion):
    """Desplaza la coma, calcula el exponente sesgado y ajusta la mantisa a 23 bits."""
    if binario_entero == "0" and "1" not in binario_fraccion:
        return "00000000", "0" * 23

    # Desplazamiento de la coma
    if binario_entero != "0":
        exponente = len(binario_entero) - 1
        mantisa_cruda = binario_entero[1:] + binario_fraccion
    else:
        indice_uno = binario_fraccion.find("1")
        exponente = -(indice_uno + 1)
        mantisa_cruda = binario_fraccion[indice_uno + 1:]

    # Suma del sesgo (127) y formato
    bin_exponente = bin(exponente + 127)[2:].zfill(8)
    mantisa_final = mantisa_cruda.ljust(23, '0')[:23]

    return bin_exponente, mantisa_final

def convertir_a_ieee754(numero):
    """Ensambla el Signo, Exponente y Mantisa."""
    if numero == 0.0:
        return "0 00000000 00000000000000000000000"
        
    signo = obtener_signo(numero)
    num_abs = abs(numero)
    entero = int(num_abs)
    fraccion = num_abs - entero
    
    bin_entero = entero_a_binario(entero)
    bin_fraccion = fraccion_a_binario(fraccion)
    
    exponente, mantisa = normalizar_y_exponente(bin_entero, bin_fraccion)
    return f"{signo} {exponente} {mantisa}"

def consola_interactiva():
    """Bucle principal de validación y captura de datos por consola."""
    MAX_FLOAT_32 = 3.4028235e38
    MIN_FLOAT_32 = 1.17549435e-38
    
    print("--- Conversor Decimal a IEEE 754 (32 bits) ---")
    while True:
        entrada = input("Ingrese un numero decimal (o 'q' para salir): ")
        if entrada.lower() == 'q':
            break
        try:
            numero = float(entrada)
            # Validación estricta del rango
            if numero != 0.0 and (abs(numero) > MAX_FLOAT_32 or abs(numero) < MIN_FLOAT_32):
                print("Error: El numero excede los limites de 32 bits (Overflow/Underflow). Intente de nuevo.\n")
                continue
            
            resultado = convertir_a_ieee754(numero)
            print(f"IEEE 754: {resultado}\n")
        except ValueError:
            print("Error: Ingrese un valor numerico valido.\n")

if __name__ == "__main__":
    consola_interactiva()
