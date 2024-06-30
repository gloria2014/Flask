from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *

PATH_URL = "public/empleados"


@app.route('/registrar-empleado', methods=['GET'])
def viewFormEmpleado():
    if 'conectado' in session:
        seguroSalud = sql_lista_segurosSaludBD()
        regiones = sql_lista_regionesBD()
        roles = sql_lista_rolesBD()

        return render_template(f'{PATH_URL}/form_empleado.html',
        seguroSalud=seguroSalud, regiones=regiones, roles=roles) 
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))

@app.route('/registrar-empleado', methods=['GET'])

#Crea un nuevo empleado
@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        resp_usuariosBD = lista_usuariosBD()
        return render_template('public/usuarios/lista_usuarios.html', resp_usuariosBD=resp_usuariosBD)
    else:
        return redirect(url_for('inicioCpanel'))


@app.route('/form-registrar-empleado', methods=['POST'])
def formEmpleado():
    if 'conectado' in session:
        resultado = procesar_form_empleado(request.form)
        resultado = int(resultado)
        print('resultado :: ',resultado)
        if resultado > 0 :
            return redirect(url_for('lista_empleados'))

        else:
            flash('El empleado NO fue registrado.', 'error')
            return render_template(f'{PATH_URL}/form_empleado.html')
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route('/lista-de-empleados', methods=['GET'])
def lista_empleados():
    if 'conectado' in session:
        return render_template(f'{PATH_URL}/lista_empleados.html', empleados=sql_lista_empleadosBD())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/detalles-empleado/", methods=['GET'])
@app.route("/detalles-empleado/<int:Id_Trab>", methods=['GET'])
def detalleEmpleado(Id_Trab=None):
    if 'conectado' in session:
        # Verificamos si el parámetro idEmpleado es None o no está presente en la URL
        if Id_Trab is None:
            return redirect(url_for('inicio'))
        else:
            detalle_empleado = sql_detalles_empleadosBD(Id_Trab) or []
            return render_template(f'{PATH_URL}/detalles_empleado.html', detalle_empleado=detalle_empleado)
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


# Buscadon de empleados
@app.route("/buscando-empleado", methods=['POST'])
def viewBuscarEmpleadoBD():
    resultadoBusqueda = buscarEmpleadoBD(request.json['busqueda'])
    if resultadoBusqueda:
        return render_template(f'{PATH_URL}/resultado_busqueda_empleado.html', dataBusqueda=resultadoBusqueda)
    else:
        return jsonify({'fin': 0})

# Viene de hacer clic del boton Actualizar de la tabla LISTA EMPELADOS 
# este método carga el formulario con datos para luego actualizar
@app.route("/editar-empleado/<int:id>", methods=['GET'])
def viewEditarEmpleado(id):
    if 'conectado' in session:
        respuestaEmpleado = buscarEmpleadoUnico(id)
        if respuestaEmpleado:
            return render_template(f'{PATH_URL}/form_empleado_update.html', respuestaEmpleado=respuestaEmpleado)
        else:
            flash('El empleado no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


@app.route("/editar-empleado/<string:email>", methods=['GET'])
def viewEditarEmpleadoEmail(email):
    if 'conectado' in session:
        respuestaEmpleado = info_datos_personales(email)
        if respuestaEmpleado:
            return render_template(f'{PATH_URL}/form_empleado_update.html', respuestaEmpleado=respuestaEmpleado)
        else:
            flash('El empleado no existe.', 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))



# Recibir formulario para actualizar INFO de empleado con el ROL 2
@app.route('/actualizar-empleado', methods=['POST'])
def actualizarEmpleado():
    if session['rol'] == 2 :
        resultData = procesar_actualizacion_form(request)
        if resultData:
            return redirect(url_for('lista_empleados'))
            
    elif session['rol'] == 3 :        
        resultData = procesar_actualizacion_formTrabajador(request)
        if resultData:
            return redirect(url_for('inicio'))



# 
# acac s eguarda resplado
# @app.route('/actualizar-empleado', methods=['POST'])
# def actualizarEmpleado():
#     resultData = procesar_actualizacion_form(request)
     
#     if resultData:
#         return redirect(url_for('lista_empleados'))
#     else:
#         print('resultData :: ', resultData)
#         flash('NO SE PUDO ACTUALIZAE LOS DATOS.', 'error')
#         return redirect(url_for('inicio'))


@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))


@app.route('/borrar-empleado/<string:Id_Trab>/<string:email_user>', methods=['GET'])
def borrarEmpleado(Id_Trab, email_user):
    Id_Trab = int(Id_Trab)
    
    resp = eliminarEmpleado(Id_Trab,email_user)
    if resp:
        flash('El Empleado fue eliminado correctamente', 'success')
        return redirect(url_for('lista_empleados'))


@app.route("/descargar-informe-empleados/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))


