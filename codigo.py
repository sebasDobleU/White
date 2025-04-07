import random

###########################
# Funciones básicas
###########################

def pertenece_a_L(w):
    """
    Verifica si w tiene la forma: a^k b^s a^r y cumple: (k+s) ≡ r (mod 3)
    """
    if set(w) - {"a", "b"}:
        return False
    # Encuentra el final del bloque inicial de a's
    i = 0
    while i < len(w) and w[i] == "a":
        i += 1
    k = i
    # Luego, contar b's
    j = i
    while j < len(w) and w[j] == "b":
        j += 1
    s = j - i
    # El resto son a's finales
    r = len(w) - j
    return (k + s) % 3 == r % 3

def obtener_particiones(w):
    """
    Retorna todas las particiones (u, v, x) de w con v no vacío.
    """
    particiones = []
    for i in range(len(w)):
        for j in range(i+1, len(w)+1):
            u, v, x = w[:i], w[i:j], w[j:]
            if v:
                particiones.append((u, v, x))
    return particiones

###########################
# Opción 1: Juego interactivo (Usuario ingresa w y m)
###########################

def juego_interactivo():
    print("=== Juego interactivo ===")
    # Elegir n aleatorio entre 8 y 30
    n = random.randint(8, 30)
    print(f"Se ha fijado n = {n}. Debes ingresar una cadena con longitud >= {n} que pertenezca a L.")
    
    w = input("Ingresa la cadena (solo 'a' y 'b'): ").strip()
    if len(w) < n:
        print(f"Error: la cadena debe tener al menos {n} caracteres.")
        return
    if not set(w) <= {"a", "b"}:
        print("Error: la cadena debe contener solo 'a' y 'b'.")
        return
    if not pertenece_a_L(w):
        print("La cadena no pertenece a L.")
        return
    try:
        m = int(input("Ingresa un número natural m (puede ser 0): "))
    except ValueError:
        print("Entrada inválida.")
        return

    particiones = obtener_particiones(w)
    total = len(particiones)
    user_wins = 0
    machine_wins = 0

    for u, v, x in particiones:
        bombeada = u + v * m + x
        if pertenece_a_L(bombeada):
            user_wins += 1
        else:
            machine_wins += 1

    print("\n=== Resultados (Juego interactivo) ===")
    print(f"Total de particiones evaluadas: {total}")
    print(f"Usuario ganó: {user_wins} veces ({user_wins/total*100:.2f}%)")
    print(f"Máquina ganó: {machine_wins} veces ({machine_wins/total*100:.2f}%)")
    if machine_wins > user_wins:
        print("💻 Ganó la máquina.")
    else:
        print("🎉 Ganó el usuario.")

###########################
# Opción 2: Simulación insesgada
###########################

def generar_cadena_valida(n):
    """
    Genera una cadena w = a^k b^s a^r que pertenece a L.
    Aquí n es la longitud mínima deseada.
    """
    while True:
        k = random.randint(1, n//2)
        s = random.randint(1, n//3)
        # Elegimos r de forma que (k+s) ≡ r (mod 3)
        r = random.randint(1, n//3 + 2)
        if (k + s) % 3 == r % 3:
            w = "a" * k + "b" * s + "a" * r
            if len(w) >= n:
                return w

def simulacion_insesgada(cantidad=30):
    total_machine = 0
    total_user = 0
    total_particiones_global = 0
    # Se fija n = 19 para esta simulación
    n = 19
    for idx in range(1, cantidad + 1):
        w = generar_cadena_valida(n)
        m = 4  # Valor fijo
        particiones = obtener_particiones(w)
        user_wins = 0
        machine_wins = 0
        for u, v, x in particiones:
            bombeada = u + v * m + x
            if pertenece_a_L(bombeada):
                user_wins += 1
            else:
                machine_wins += 1
        total_particiones_global += len(particiones)
        total_user += user_wins
        total_machine += machine_wins

        print(f"\n--- Cadena {idx} ---")
        print(f"n = {n}, m = {m}")
        print(f"w = {w}")
        print(f"Particiones evaluadas: {len(particiones)}")
        print(f"Usuario ganó: {user_wins} veces ({user_wins/len(particiones)*100:.2f}%)")
        print(f"Máquina ganó: {machine_wins} veces ({machine_wins/len(particiones)*100:.2f}%)")

    print("\n=== Resultados Globales (Insesgada) ===")
    print(f"Total de particiones evaluadas: {total_particiones_global}")
    print(f"Promedio de victorias del usuario: {total_user/total_particiones_global*100:.2f}%")
    print(f"Promedio de victorias de la máquina: {total_machine/total_particiones_global*100:.2f}%")

###########################
# Opción 3: Simulación sesgada
###########################
# En esta opción se fija la partición de forma injusta:
# Sea w = a^k b^s a^r, con k > 3. Se define:
#   u = a^(k - l), v = a^l, x = b^s a^r.
# Se bombea: z = u + v^m + x.
# z pertenece a L si y solo si l*(m-1) ≡ 0 (mod 3).
# Se escoge l de forma sesgada: de un arreglo de 10 valores, 9 de ellos con l % 3 != 0 y 1 con l % 3 == 0.
# Además, se fija n = 19 para todas las palabras, y m se fija para toda la simulación.
    
def generar_cadena_valida_k_mayor_3(n):
    """
    Genera una cadena w = a^k b^s a^r perteneciente a L, con k > 3.
    """
    while True:
        k = random.randint(4, n//2+2)  # k > 3
        s = random.randint(1, n//3+1)
        r = random.randint(1, n//3+2)
        if (k + s) % 3 == r % 3:
            w = "a" * k + "b" * s + "a" * r
            if len(w) >= n:
                return w

def evaluacion_sesgada(w, m):
    """
    Dada una cadena w = a^k b^s a^r con k > 3,
    se fija la partición:
       u = a^(k - l), v = a^l, x = b^s a^r.
    Se elige l de forma sesgada: de un arreglo con 10 valores,
      9 de ellos con l % 3 != 0 y 1 con l % 3 == 0.
    Se bombea: z = u + v^m + x.
    z pertenece a L si y solo si l*(m-1) ≡ 0 (mod 3).
    """
    # Extraer k, s, r de w:
    i = 0
    while i < len(w) and w[i] == "a":
        i += 1
    k = i
    j = i
    while j < len(w) and w[j] == "b":
        j += 1
    s = j - i
    r = len(w) - j

    # Crear arreglo sesgado de posibles l (1 <= l <= k)
    sesgado = []
    for l in range(1, k+1):
        if l % 3 != 0:
            sesgado.extend([l] * 9)
        else:
            sesgado.append(l)
    l_val = random.choice(sesgado)
    if l_val > k:
        l_val = 1

    # Partición fija:
    u = "a" * (k - l_val)
    v = "a" * l_val
    x = w[k:]  # x = b^s a^r
    z = u + v * m + x
    return pertenece_a_L(z)

def simulacion_sesgada(cantidad=30):
    total_machine = 0
    total_user = 0
    # Se fija n = 19 para la simulación
    n = 19
    # Se pide un único m para toda la simulación:
    try:
        m = int(input("Ingrese un valor natural m para la simulación sesgada: "))
    except ValueError:
        print("Valor inválido. Se usará m = 4.")
        m = 4

    for idx in range(1, cantidad + 1):
        w = generar_cadena_valida_k_mayor_3(n)
        resultado = evaluacion_sesgada(w, m)
        if resultado:
            total_user += 1
            res = "Usuario gana (z ∈ L)"
        else:
            total_machine += 1
            res = "Máquina gana (z ∉ L)"
        print(f"\n--- Caso {idx} (Sesgada) ---")
        print(f"n = {n}")
        print(f"w = {w}")
        print(f"Con m = {m} y partición sesgada, {res}")

    total = total_machine + total_user
    print("\n=== Resultados Globales (Sesgada) ===")
    print(f"Total de casos: {total}")
    print(f"Usuario gana: {total_user} veces ({total_user/total*100:.2f}%)")
    print(f"Máquina gana: {total_machine} veces ({total_machine/total*100:.2f}%)")

###########################
# Menú principal
###########################

def main_menu():
    while True:
        print("\nMenú:")
        print("  J - Juego interactivo (Opción 1)")
        print("  S - Simulación insesgada (Opción 2)")
        print("  I - Simulación sesgada (Opción 3)")
        print("  X - Salir")
        opcion = input("Selecciona una opción (J, S, I, X): ").strip().upper()
        if opcion == "J":
            juego_interactivo()
        elif opcion == "S":
            try:
                cant = int(input("¿Cuántas palabras deseas simular? "))
            except ValueError:
                print("Valor inválido, se simularán 30 casos.")
                cant = 30
            simulacion_insesgada(cantidad=cant)
        elif opcion == "I":
            try:
                cant = int(input("¿Cuántos casos deseas simular en la opción sesgada? "))
            except ValueError:
                print("Valor inválido, se simularán 30 casos.")
                cant = 30
            simulacion_sesgada(cantidad=cant)
        elif opcion == "X":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intenta nuevamente.")

if __name__ == "__main__":
    main_menu()
