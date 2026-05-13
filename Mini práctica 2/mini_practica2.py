class ArbolBinario:

    class Nodo:
        def __init__(self, dato):
            self.dato = dato
            self.izq = None
            self.der = None

        def _display_aux(self):
            # No child.
            if self.der is None and self.izq is None:
                line = '%s' % self.dato
                width = len(line)
                height = 1
                middle = width // 2
                return [line], width, height, middle

            # Only left child.
            if self.der is None:
                lines, n, p, x = self.izq._display_aux()
                s = '%s' % self.dato
                u = len(s)
                first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
                second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
                shifted_lines = [line + u * ' ' for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

            # Only right child.
            if self.izq is None:
                lines, n, p, x = self.der._display_aux()
                s = '%s' % self.dato
                u = len(s)
                first_line = s + x * '_' + (n - x) * ' '
                second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
                shifted_lines = [u * ' ' + line for line in lines]
                return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

            # Two children.
            left, n, p, x = self.izq._display_aux()
            right, m, q, y = self.der._display_aux()
            s = '%s' % self.dato
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
            second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '

            if p < q:
                left += [n * ' '] * (q - p)
            elif q < p:
                right += [m * ' '] * (p - q)

            zipped_lines = zip(left, right)
            lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
            return lines, n + m + u, max(p, q) + 2, n + u // 2

    def __init__(self):
        self.raiz = None

    def display(self):
        if self.raiz is None:
            print("Árbol vacío")
            return

        lines, *_ = self.raiz._display_aux()
        for line in lines:
            print(line)


# =====================================================
# EJERCICIO 1
# CONSTRUIR ÁRBOL DE EXPRESIÓN
# =====================================================


def arbol_expresion(expresion):

    pila = []

    operadores = ['+', '-', '*', '/']

    for c in expresion:

        if c == ' ':
            continue

        if c == '(':
            pila.append(c)

        elif c.isdigit():
            nodo = ArbolBinario.Nodo(int(c))
            pila.append(nodo)

        elif c in operadores:
            pila.append(c)

        elif c == ')':

            der = pila.pop()
            operador = pila.pop()
            izq = pila.pop()

            pila.pop()

            nuevo = ArbolBinario.Nodo(operador)
            nuevo.izq = izq
            nuevo.der = der

            pila.append(nuevo)

    arbol = ArbolBinario()
    arbol.raiz = pila.pop()

    return arbol


# =====================================================
# EJERCICIO 2
# EVALUAR ÁRBOL DE EXPRESIÓN
# =====================================================


def evaluar_arbol(nodo):

    if nodo is None:
        return 0

    if nodo.izq is None and nodo.der is None:
        return nodo.dato

    izq = evaluar_arbol(nodo.izq)
    der = evaluar_arbol(nodo.der)

    if nodo.dato == '+':
        return izq + der

    if nodo.dato == '-':
        return izq - der

    if nodo.dato == '*':
        return izq * der

    if nodo.dato == '/':
        return izq / der


# =====================================================
# EJERCICIO 3
# CAMINO MÁS LARGO
# =====================================================


def camino_mas_largo(raiz):

    if raiz is None:
        return []

    camino_izq = camino_mas_largo(raiz.izq)
    camino_der = camino_mas_largo(raiz.der)

    if len(camino_izq) > len(camino_der):
        return [raiz.dato] + camino_izq
    else:
        return [raiz.dato] + camino_der


# =====================================================
# PRUEBAS
# =====================================================

expresion = "(((3+1)*4)/((9-5)+2))"

arbol = arbol_expresion(expresion)

print("ÁRBOL DE EXPRESIÓN")
arbol.display()

print()

resultado = evaluar_arbol(arbol.raiz)
print("Resultado:", resultado)

print()

camino = camino_mas_largo(arbol.raiz)
print("Camino más largo:", camino)