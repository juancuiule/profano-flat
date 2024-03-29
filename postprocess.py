import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

requiredKeys = ['edad-actual', 'edad-morir', 'hijes-tenes', 'gestacion-aborto', 'gestacion-persona', 'genero-coincide', 'morir-cuerpo', 'morir-redes', 'miedo-propia', 'miedo-resto', 'muerte-experiencia', 'muerte-eutanasia', 'firstTime']
optionalKeys = ['hijes-gustaria', 'hijes-volveria']

def hasAllKeys(obj):
    objectKeys = obj.keys()
    hasRequiredKeys = np.all([(key in objectKeys) for key in requiredKeys])
    hasConditionalKeys =  ('hijes-gustaria' in objectKeys) if obj['hijes-tenes'] == "0" else ('hijes-volveria' in objectKeys)
    return hasRequiredKeys and hasConditionalKeys

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
    
    columns = np.concatenate((requiredKeys, optionalKeys))
    raw = np.array([])
    for x in json["data"]:
        if hasAllKeys(x):
            if meetsConditions(x):
                d = {}
                for k in columns:
                    d[k] = x[k] if k in x.keys() else None
                raw = np.append(raw, d)
    
    csv = pd.DataFrame([row.values() for row in raw], columns=raw[0].keys())
    csv.to_csv('./profano.csv')

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

    ####

    rango = range(0, 101)

    ####

    BW_WIDTH = 0.2
    f = stats.gaussian_kde(csv['genero-coincide'], BW_WIDTH)
    plt.plot(rango, f(rango))

    plt.yticks([])
    ax = plt.gca()
    ax.set_ylabel('Frecuencia')
    plt.title('Género coincide')
    plt.savefig('4.png')
    plt.clf()

    pairs = []
    for x in rango:
        y = f(x)[0]
        pairs.append([x, y])
    pd.DataFrame(pairs).to_csv("curva-genero.csv", index=False, header=["x", "area"])

    ######

    BW_WIDTH = 0.4
    g = stats.gaussian_kde(csv.loc[csv['hijes-tenes'] == "0"]['hijes-gustaria'], BW_WIDTH)
    h = stats.gaussian_kde(csv.loc[csv['hijes-tenes'] == "1"]['hijes-volveria'], BW_WIDTH)
    plt.plot(rango, h(rango))
    plt.plot(rango, g(rango))

    plt.yticks([])
    plt.legend(["Con hijes", "Sin hijes"])
    ax = plt.gca()
    ax.set_xlabel('Gustaría o volvería')
    ax.set_ylabel('Frecuencia')
    plt.title('Hijes')
    plt.savefig('2.png')
    plt.clf()

    pairs = []
    for x in rango:
        y1 = g(x)[0]
        y2 = h(x)[0]
        pairs.append([x, y1, y2])
    pd.DataFrame(pairs).to_csv("curva-hijes.csv", index=False, header=["x", "gustaria", "volveria"])