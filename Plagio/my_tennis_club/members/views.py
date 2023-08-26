import os
from django.shortcuts import render
import tensorflow as tf
import random
from django.http import HttpResponse
import csv

directorio_actual = os.getcwd()
nombre_archivo = "modelo_x.h5"
ruta_archivo = os.path.join(directorio_actual, "members", nombre_archivo)
try:
    # Carga el modelo .h5 utilizando tf.keras.models.load_model
    model = tf.keras.models.load_model(ruta_archivo)
    print("Modelo cargado exitosamente:", model)
except Exception as e:
    print("Error al cargar el modelo:", e)

historial_data = []
def process_file(file):
    texto_archivo = file.read().decode('utf-8')
    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts([texto_archivo])
    secuencia_archivo = tokenizer.texts_to_sequences([texto_archivo])[0]
    if len(secuencia_archivo) > 435:
        secuencia_archivo = secuencia_archivo[:435]
    else:
        secuencia_archivo = secuencia_archivo + [0] * (435 - len(secuencia_archivo))
    secuencia_archivo = [secuencia_archivo]
    secuencia_archivo = tf.keras.preprocessing.sequence.pad_sequences(secuencia_archivo, maxlen=435, padding='post')    
    prediccion = model.predict(secuencia_archivo)
    return prediccion

def members(request):
    if request.method == 'POST':
        archivo = request.FILES['archivo1']
        # Validar la extensión del archivo
        allowed_extensions = ['py']
        file_extension = archivo.name.split('.')[-1]
        if file_extension not in allowed_extensions:
            return HttpResponse('<script>alert("Por favor, suba un archivo con extensión .py."); history.back();</script>')

        nombre_estudiante = request.POST.get('nombre_estudiante')

        prediccion = process_file(archivo)
        
        if prediccion >= 0.65:
            color_semaforo = 'red'
            calidad_palgio="Alto"
        elif prediccion< 0.65 and prediccion>=0.50:
            color_semaforo = 'yellow'
            calidad_palgio="Medio"
        else:
            color_semaforo = 'green'
            calidad_palgio="Bajo"

        
        historial_data.append({'nombre_estudiante': nombre_estudiante, 'archivo': archivo, 'calidad':calidad_palgio})
                
        return render(request, 'myfirst.html', {'archivos_obtenidos': True, 'color_semaforo': color_semaforo,'nombre_estudiante':nombre_estudiante,'calidad': calidad_palgio})

    return render(request, 'myfirst.html', {'archivos_obtenidos': False})

def descargar_reporte_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre del Estudiante', 'Archivo', 'Plagio'])

    for item in historial_data:
        writer.writerow([item['nombre_estudiante'], item['archivo'],item['calidad']])

    return response

def historial(request):
    return render(request, 'historial.html', {'historial_data': historial_data})


