import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')

sexos = ["Masculino", "Femenino"]

def nombre_por_sexo(sexo):
    return fake.name_male() if sexo == "Masculino" else fake.name_female()

def muestrea_edad():
    # Distribución sencilla: 0-17 (20%), 18-64 (60%), 65+ (20%)
    r = random.random()
    if r < 0.20:
        return random.randint(0, 17)
    elif r < 0.80:
        return random.randint(18, 64)
    else:
        return random.randint(65, 100)

def prob_vacunado(edad):
    if edad >= 65:
        return 0.9
    elif edad >= 18:
        return 0.75
    else:
        return 0.5  # menores con menos probabilidad de tener esquema completo

def prob_asintomatico(edad):
    if edad < 18:
        return 0.4
    elif edad < 65:
        return 0.25
    else:
        return 0.15

def prob_muerte(edad, vacunado, asintomatico):
    # Base baja; sube con edad, baja con vacuna y si fue asintomático
    base = 0.002  # 0.2%
    if edad >= 80:
        base = 0.05
    elif edad >= 65:
        base = 0.02
    elif edad >= 40:
        base = 0.005
    elif edad >= 18:
        base = 0.002
    else:
        base = 0.001

    if vacunado == "Sí":
        base *= 0.4
    if asintomatico == "Sí":
        base *= 0.2

    return min(base, 0.3)  # techo de seguridad

def prob_secuelas(edad, vacunado, asintomatico, vive):
    if vive == "No":
        return 0.0
    if asintomatico == "Sí":
        return 0.05
    # sintomáticos: más riesgo con edad y sin vacuna
    p = 0.08
    if edad >= 65:
        p += 0.10
    elif edad >= 40:
        p += 0.05
    if vacunado == "No":
        p += 0.05
    return min(p, 0.4)

pacientes = []
for _ in range(100):
    sexo = random.choice(sexos)
    edad = muestrea_edad()

    # Vacunación y asintomático según edad
    vacunado = "Sí" if random.random() < prob_vacunado(edad) else "No"
    asintomatico = "Sí" if random.random() < prob_asintomatico(edad) else "No"

    # Mortalidad según edad, vacuna y síntomas
    vive = "No" if random.random() < prob_muerte(edad, vacunado, asintomatico) else "Sí"

    # Secuelas solo si vive y no fue asintomático (aunque puede haber raro, lo bajamos)
    secuelas = "Sí" if random.random() < prob_secuelas(edad, vacunado, asintomatico, vive) else "No"

    pacientes.append({
        "Nombre": nombre_por_sexo(sexo),
        "Sexo": sexo,
        "Edad": edad,
        "Vive": vive,
        "Asintomático": asintomatico if vive == "Sí" else "No",
        "Secuelas": secuelas if vive == "Sí" else "No",
        "Vacunado": vacunado
    })

df = pd.DataFrame(pacientes)
df.to_csv("Pacientes_covid.csv", index=False, encoding="utf-8")
print("Archivo 'Pacientes_covid.csv' creado con reglas de coherencia.")
print(df.head(10))
