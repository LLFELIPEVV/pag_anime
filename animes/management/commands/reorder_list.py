import json

# Carga el archivo JSON
with open('lista_id.json', 'r') as archivo_json:
    data = json.load(archivo_json)

# Define la clave en la que deseas insertar el nuevo valor
clave_destino = 12

# Define el nuevo valor que deseas insertar
nuevo_valor = "detective-conan"

# Mueve los elementos existentes hacia abajo, empezando desde la última clave
for i in range(len(data), clave_destino, -1):
    data[str(i + 1)] = data[str(i)]

# Mueve el elemento original de la clave destino a la siguiente clave
data[str(clave_destino + 1)] = data[str(clave_destino)]

# Inserta el nuevo valor en la clave destino
data[str(clave_destino)] = nuevo_valor

# Guarda los datos actualizados en el archivo JSON
with open('lista_id.json', 'w') as archivo_json:
    json.dump(data, archivo_json, indent=4)
