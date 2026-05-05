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
    
    ano = int(match.group(2))
    mes = int(match.group(3))
    dia = int(match.group(4))
    
    ano_completo = 1900 + ano if ano >= 30 else 2000 + ano
    
    try:
        datetime(ano_completo, mes, dia)
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
# PROBLEMA 4: Lista Circular + Josephus
# ---------------------------

class Lista_circular:

    class Nodo:
        def __init__(self, dato):
            self.dato = dato
            self.next = None

    def __init__(self):
        self.head = None
        self.tail = None

    def insertar(self, dato):
        nuevo = self.Nodo(dato)

        if self.head is None:
            self.head = nuevo
            self.tail = nuevo
            nuevo.next = self.head
        else:
            self.tail.next = nuevo
            self.tail = nuevo
            self.tail.next = self.head

    def __str__(self):
        if self.head is None:
            return ""

        cad = ""
        aux = self.head

        while True:
            cad += str(aux.dato) + " -> "
            aux = aux.next
            if aux == self.head:
                break

        return cad


def josephus(n, k):
    lista = Lista_circular()

    # Crear círculo de soldados
    for i in range(1, n+1):
        lista.insertar(i)

    actual = lista.head
    prev = lista.tail

    eliminados = []

    while actual.next != actual:
        # avanzar k-1 pasos
        for _ in range(k-1):
            prev = actual
            actual = actual.next

        eliminados.append(actual.dato)

        # eliminar nodo
        prev.next = actual.next
        actual = actual.next

    sobreviviente = actual.dato

    return eliminados, sobreviviente


# ---------------------------
# PROBLEMA 5: Torres de Hanoi con PILAS
# ---------------------------

class Pila:
    
    def __init__(self):
        self.pila = []
        self.tope = -1

    def push(self, elemento):
        self.pila.append(elemento)
        self.tope += 1

    def pop(self):
        if self.tope >= 0:
            ultimo = self.pila[self.tope]
            self.pila.pop()
            self.tope -= 1
            return ultimo
        else:
            return None

    def peek(self):
        if self.tope >= 0:
            return self.pila[self.tope]
        return None


def mover_disco(origen, destino, nombre_origen, nombre_destino, movimientos):
    top_origen = origen.pop()
    top_destino = destino.pop()

    if top_origen is None:
        origen.push(top_destino)
        movimientos.append(f"Mover disco de {nombre_destino} -> {nombre_origen}")
    
    elif top_destino is None:
        destino.push(top_origen)
        movimientos.append(f"Mover disco de {nombre_origen} -> {nombre_destino}")
    
    elif top_origen > top_destino:
        origen.push(top_origen)
        origen.push(top_destino)
        movimientos.append(f"Mover disco de {nombre_destino} -> {nombre_origen}")
    
    else:
        destino.push(top_destino)
        destino.push(top_origen)
        movimientos.append(f"Mover disco de {nombre_origen} -> {nombre_destino}")


def torres_Hanoi(n):
    A = Pila()
    B = Pila()
    C = Pila()

    movimientos = []

    # llenar torre A
    for i in range(n, 0, -1):
        A.push(i)

    total_movimientos = 2**n - 1

    # si n es par intercambiar destino y auxiliar
    if n % 2 == 0:
        B, C = C, B
        nombre_B, nombre_C = 'C', 'B'
    else:
        nombre_B, nombre_C = 'B', 'C'

    nombre_A = 'A'

    for i in range(1, total_movimientos + 1):
        if i % 3 == 1:
            mover_disco(A, C, nombre_A, nombre_C, movimientos)
        elif i % 3 == 2:
            mover_disco(A, B, nombre_A, nombre_B, movimientos)
        else:
            mover_disco(B, C, nombre_B, nombre_C, movimientos)

    return movimientos




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

 # Problema 4
    print("\n----------- Problema 4 -----------")

    n = 25
    k = 2

    eliminados, sobreviviente = josephus(n, k)

    print("Orden de eliminación:", eliminados)
    print("Soldado que sobrevive:", sobreviviente)
#Problema 5
    print("\n----------- Problema 5 -----------")

    n = 3 #Numero de discos
    movimientos = torres_Hanoi(n)

    for m in movimientos:
        print(m)

    print("Total de movimientos:", len(movimientos))
        
# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == '__main__':
    main()