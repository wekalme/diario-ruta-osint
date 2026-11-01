# generador_variantes.py
# Genera variantes probables de nombre de usuario (ana.garcia, agarcia, anagarcia90...)
# a partir de nombre, apellido y año de nacimiento. Quita tildes y ñ, y si el año
# no es válido, avisa y genera solo las variantes sin año.
#
# Uso: python generador_variantes.py
# Uso ético: probar solo con datos propios o de personas ficticias.

tabla = str.maketrans("áéíóúñü", "aeiounu")

#CONSEGUIR
nombre = input("Nombre: ").lower().translate(tabla)
apellido = input("Apellido: ").lower().translate(tabla)
anio = input("Año de nacimiento: ")

#COMPROBAR
try:
    int(anio)
except ValueError:
    print("El año no es un número; genero las variantes sin año")
    anio_valido = False
else:
    if int(anio) <= 2026 and len(anio) == 4:
        anio_valido = True
    else:
        anio_valido = False 
        print("Año no válido, posterior a 2026 o de + o - de 4 dígitos")

#TRANSFORMAR
variantes = []

#siempre se muestran (las de sin numero)
variantes.append(nombre + "." + apellido)
variantes.append(nombre[0] + apellido)
variantes.append(nombre + apellido)

#se muestran si es_anio = True wendyalarcon98, 1998alarcon, wendy.alarcon98
if anio_valido == True:
    variantes.append(nombre + apellido + anio[-2:])
    variantes.append(anio + apellido)
    variantes.append(nombre + "." + apellido + anio[-2:])

#MOSTRAR
for variante in variantes:
    print(variante)