import re
from datetime import datetime


# ---------------------------
# PROBLEMA 1: Validación de RFC
# ---------------------------
def valida_rfc(rfc):
    patron = re.compile(r'^([A-ZÑ&]{4})(\d{2})(\d{2})(\d{2})([A-Z0-9]{3})$')
    
    match = patron.match(rfc)
    if not match:
        return False
    
    anio = int(match.group(2))
    mes = int(match.group(3))
    dia = int(match.group(4))
    
    anio_completo = 1900 + anio if anio >= 30 else 2000 + anio
    
    try:
        datetime(anio_completo, mes, dia)
    except ValueError:
        return False
    
    return True


# ---------------------------
# PROBLEMA 2: Normalización de teléfonos
# ---------------------------
def normaliza_telefonos(texto):
    # Regex que captura los distintos formatos
    patron = re.compile(r'\(?(\d{3})\)?[.\-\s]?(\d{3})[.\-]?(\d{4})')
    
    # Función de reemplazo usando los grupos
    def reemplazo(match):
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    
    # Sustituir en todo el texto
    resultado = patron.sub(reemplazo, texto)
    
    return resultado



# ---------------------------
# PROBLEMA 3: Validación de código EAN
# ---------------------------
def valida_ean(codigo):
    codigo_str = str(codigo)
    
    # 1. Validar que sean solo dígitos
    if not codigo_str.isdigit():
        return False, None
    
    # 2. Validar longitud
    if len(codigo_str) not in [8, 13]:
        return False, None
    
    # 3. Separar dígito de control
    digitos = list(map(int, codigo_str))
    digito_control = digitos[-1]
    datos = digitos[:-1]
    
    # 4. Aplicar algoritmo
    suma = 0
    datos_reversa = datos[::-1]
    
    for i, d in enumerate(datos_reversa):
        if i % 2 == 0:  # posición impar (desde la derecha)
            suma += d * 3
        else:           # posición par
            suma += d * 1
    
    # 5. Calcular dígito esperado
    siguiente_multiplo_10 = ((suma + 9) // 10) * 10
    digito_esperado = siguiente_multiplo_10 - suma
    
    if digito_esperado == 10:
        digito_esperado = 0
    
    # 6. Comparar
    es_valido = (digito_control == digito_esperado)
    
    # 7. Obtener país (solo EAN-13)
    pais = None
    if es_valido and len(codigo_str) == 13:
        prefijo = int(codigo_str[:3])
        
        tabla_paises = {
            0: "EEUU",
            380: "Bulgaria",
            50: "Inglaterra",
            560: "Portugal",
            70: "Noruega",
            759: "Venezuela",
            890: "India"
        }
        
        pais = tabla_paises.get(prefijo, "Desconocido")
    
    return es_valido, pais



# ---------------------------
# MAIN
# ---------------------------
def main():
    # Problema 1
    print("----------- Problema 1 -----------")
    print(valida_rfc("XEXT990101NI4"))  # True
    print(valida_rfc("XEXT994001NI4"))  # False
    
    print("\n----------- Problema 2 -----------")
    
    texto = """Puedes contactar a Juan al (555) 123-4567 o al 555.123.4567.
También puedes llamar a Maria al 555-123-4567, o al (555) 987-6543."""
    
    resultado = normaliza_telefonos(texto)
    
    print("Texto original:\n", texto)
    print("\nTexto normalizado:\n", resultado)

    print("\n----------- Problema 3 -----------")
    
    codigos = ["29033706", "12345670", "7501031311309"]
    
    for c in codigos:
        valido, pais = valida_ean(c)
        if pais:
            print(f"{c} -> Válido: {valido}, País: {pais}")
        else:
            print(f"{c} -> Válido: {valido}")


# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == '__main__':
    main()