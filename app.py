from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/ejercicio-1', methods=['GET', 'POST'])
def ejercicio_1():
    if request.method == 'GET':
        return render_template('ejercicio1.html')

    try:
        notas = [float(request.form[f'nota{i}']) for i in range(1, 4)]
        asistencia = float(request.form['asistencia'])
    except (KeyError, TypeError, ValueError):
        return render_template('ejercicio1.html', error='Completa todos los campos con valores numéricos.'), 400

    if any(nota < 10 or nota > 70 for nota in notas):
        return render_template('ejercicio1.html', error='Las notas deben estar entre 10 y 70.'), 400
    if asistencia < 0 or asistencia > 100:
        return render_template('ejercicio1.html', error='La asistencia debe estar entre 0 y 100%.'), 400

    promedio = sum(notas) / len(notas)
    aprobado = promedio >= 40 and asistencia >= 75
    return render_template(
        'resultado.html',
        titulo='Resultado del ejercicio 1',
        resultado=f'{promedio:.1f}',
        detalle=f'Asistencia: {asistencia:.1f}%',
        estado='Aprobado' if aprobado else 'Reprobado',
        aprobado=aprobado,
    )


@app.route('/ejercicio-2', methods=['GET', 'POST'])
def ejercicio_2():
    if request.method == 'GET':
        return render_template('ejercicio2.html')

    nombres = [request.form.get(f'nombre{i}', '').strip() for i in range(1, 4)]
    if any(not nombre for nombre in nombres):
        return render_template('ejercicio2.html', error='Debes completar los tres nombres.'), 400
    if len({nombre.casefold() for nombre in nombres}) != 3:
        return render_template('ejercicio2.html', error='Los tres nombres deben ser diferentes.'), 400

    nombre_mas_largo = max(nombres, key=len)
    return render_template(
        'resultado.html',
        titulo='Resultado del ejercicio 2',
        resultado=nombre_mas_largo,
        detalle=f'Cantidad de caracteres: {len(nombre_mas_largo)}',
        estado='Nombre más largo',
        aprobado=True,
    )


@app.errorhandler(404)
def pagina_no_encontrada(_error):
    return render_template('resultado.html', titulo='Página no encontrada', resultado='404', detalle='La ruta solicitada no existe.', estado='Error', aprobado=False), 404


if __name__ == '__main__':
    app.run(debug=True)
