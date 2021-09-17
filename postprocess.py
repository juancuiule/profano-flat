import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# from scipy import stats

requiredKeys = ['edad-actual', 'edad-morir', 'hijes-tenes', 'gestacion-aborto', 'gestacion-persona', 'genero-coincide', 'morir-cuerpo', 'morir-redes', 'miedo-propia', 'miedo-resto', 'muerte-experiencia', 'muerte-eutanasia', 'firstTime']

def hasAllKeys(obj):
    objectKeys = obj.keys()
    hasRequiredKeys = np.all([(key in objectKeys) for key in requiredKeys])
    hasConditionalKeys =  ('hijes-gustaria' in objectKeys) if obj['hijes-tenes'] == 0 else ('hijes-volveria' in objectKeys)

def between(low, high):
    return lambda x: x >= low and x <= high

conditions = {
    "edad-actual": lambda x: True,
    "edad-morir": between(0, 130),
    "hijes-tenes": lambda value: value == "0" or value == "1",
    "hijes-gustaria": between(0, 100),
    "hijes-volveria": between(0, 100),
    "gestacion-aborto": between(0, 42),
    "gestacion-persona": between(0, 42),
    "genero-coincide": between(0, 100),
    "morir-cuerpo": between(0, 100),
    "morir-redes": between(0, 100),
    "miedo-propia": between(0, 100),
    "miedo-resto": between(0, 100),
    "muerte-experiencia": between(0, 100),
    "muerte-eutanasia": between(0, 100),
    "firstTime": lambda x: x
}

def meetsConditions(obj):
    values = [conditions[key](obj[key]) for key in obj.keys()]
    return np.all(values)

if __name__ == "__main__":
    json = pd.read_json('./profano-data.json')
    
    raw = np.array([])
    for x in json["data"]:
        if hasAllKeys(x):
            if meetsConditions(x):
                raw = np.append(raw, x)
    
    csv = pd.DataFrame([row.values() for row in raw], columns=raw[0].keys())
    csv.to_csv('./profano.csv')
    # csv.head()
    
    plt.title("La longitud del camino")
    plt.xlabel('Edad hasta la que queremos vivir')
    plt.ylabel('Edad actual')
    ax = plt.gca()
    ax.set_xlim([0, 130])
    plt.scatter(csv['edad-morir'], csv['edad-actual'], color="#0069B4", alpha=0.4, s=4)
    plt.savefig('1.png')
    plt.clf()

    plt.title("Respecto al punto de partida")
    plt.xlabel('¿En qué momento de tu gestación creés que apareciste vos como persona?')
    plt.ylabel('¿Hasta cuando hacer un aborto?')
    ax = plt.gca()
    ax.set_xlim([0, 42])
    ax.set_ylim([0, 42])
    plt.scatter(csv['gestacion-persona'], csv['gestacion-aborto'], color="#0069B4", alpha=0.4, s=4)
    plt.savefig('3.png')
    plt.clf()

    plt.title("El final")
    plt.xlabel('¿Te interesa qué pase con tus redes sociales luego de morir?')
    plt.ylabel('¿Te interesa que pase con tu cuerpo luego de morir? ')
    ax = plt.gca()
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])
    plt.scatter(csv['morir-redes'], csv['morir-cuerpo'], color="#0069B4", alpha=0.4, s=4)
    plt.savefig('5.png')
    plt.clf()

    plt.title("Los abismos")
    plt.xlabel('¿Cuánto miedo le tenés a la muerte de les demás?')
    plt.ylabel('¿Cuánto miedo le tenés a la muerte?')
    ax = plt.gca()
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])
    plt.scatter(csv['miedo-resto'], csv['miedo-propia'], color="#0069B4", alpha=0.4, s=4)
    plt.savefig('6.png')
    plt.clf()

    plt.title("La interrupción del viaje")
    plt.xlabel('¿Debe una persona tener derecho a acceder a una eutanasia? ')
    plt.ylabel('¿Hay experiencia despues de la muerte? ')
    ax = plt.gca()
    ax.set_xlim([0, 100])
    ax.set_ylim([0, 100])
    plt.scatter(csv['muerte-eutanasia'], csv['muerte-experiencia'], color="#0069B4", alpha=0.4, s=4)
    plt.savefig('7.png')
    plt.clf()
