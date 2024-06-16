import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np


data_dict = pickle.load(open('./data.pickle', 'rb'))

#Imprimir contenido de data.pickle
##print(data_dict.keys())
##print(data_dict)



#Queremos  convertir los datos que tenemos como lista en arrays de numpy
data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])



#Se separan los datos que tenemos en set de entrenamiento y set de testeo uno para enseñar al algoritmo y otro para comprobar

#test_size=0.2 indica que pillamos el 80% para entrenamiento y el 20 restante para testeo, shuffle=True aleatoriza la muestra y generalmente ayuda, stratify=labels mantiene una proporción equitativa en las diferentes categorias
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)


#RandomForestClassifer
model = RandomForestClassifier()

#Entrenar
model.fit(x_train, y_train)

#Predecir
y_predict = model.predict(x_test)

#Éxito?
score = accuracy_score(y_predict, y_test)

print('{}% de las muestras se clasificaron correctamente!'.format(score * 100))


##GUARDAR MODELO PARA MIRAR RENDIMIENTO CON DATOS REALES
f = open('model.p', 'wb')
pickle.dump({'model': model}, f)
f.close()
