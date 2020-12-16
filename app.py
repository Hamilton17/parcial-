from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'spbYO0JJOPUFLUikKYbKrpS5w3KUEnab5KcYDdYb'
db = sqlite3.connect('data.db', check_same_thread=False)
def base():
    global categories
    categories=db.execute("""select * from Categorias where ID_USUARIO = ?""",(session['Usuarios'][0],)).fetchall()
  

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('paginas/login.html')

    Correo=request.form.get('LCorreo')
    Contraseña=request.form.get('LContraseña')
    
    cursor=db.cursor()
    
    Usuarios = cursor.execute("""select * from Usuarios where
    Email = ? and Contraseña = ?""", (Correo,Contraseña,)).fetchone()
    
    db.commit()
    
    if  Usuarios is None:
        flash('Las Credenciales No Son Validas.','error')
        return redirect(request.url)
    
    session['Usuarios'] = Usuarios
    print(session['Usuarios'])
    
    return redirect(url_for('inicio'))

@app.route('/Logout')
def Logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/Inicio')
def inicio():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    return render_template('paginas/inicio.html')

@app.route('/Productos')
def productos():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    productos = db.execute('select * from Productos')
    productos = productos.fetchall()
    return render_template('paginas/mostrarproductos.html', productos=productos)


@app.route('/Usuarios')
def usuarios():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    usuarios = db.execute('select * from Usuarios')
    usuarios = usuarios.fetchall()
    return render_template('paginas/mostrarusuarios.html', usuarios=usuarios)


@app.route('/Categorias')
def categorias():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    categorias = db.execute('select * from Categorias')
    categorias = categorias.fetchall()
    return render_template('paginas/mostrarcategorias.html', categorias = categorias)

@app.route('/Crear Categoria', methods=['GET','POST'])
def crearcategoria():
    if request.method == 'GET':
        return render_template('paginas/crearcategoria.html')
    
    Categoria=request.form.get('NuevaCategoria')
    cursor=db.cursor()
    
    cursor.execute("""insert into Categorias (
            Categoria,
            ID_USUARIO
        )values (?,?)
    """, (Categoria,session['Usuarios'][0],))
    
    db.commit()
    
    return redirect(url_for('categorias'))

@app.route('/Crear Usuario', methods=['GET','POST'])
def registrarse():
    if request.method == 'GET':
        return render_template('paginas/crearusuario.html')
    
    Nombre=request.form.get('RUsuario')
    Email=request.form.get('RCorreo')
    Contraseña=request.form.get('RContraseña')
    
    cursor=db.cursor()
    
    cursor.execute("""insert into Usuarios (
            Nombre, 
            Email,
            Contraseña
        )values (?,?,?)
    """, (Nombre,Email,Contraseña))
    
    db.commit()
    
    return redirect(url_for('login'))

@app.route('/Crear Producto', methods=['GET','POST'])
def crearproducto():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        base()
        return render_template('paginas/crearproducto.html', Categorias=categories)
    
    Nombre=request.form.get('Nombre')
    Precio=request.form.get('Precio')
    Categoria=request.form.get('Categoria')
    
    cursor=db.cursor()
    
    cursor.execute("""insert into Productos (
            Nombre, 
            Precio,
            Categoria,
            ID_USUARIO
        )values (?,?,?,?)
    """, (Nombre,Precio,Categoria,session['Usuarios'][0],))
    
    db.commit()
    
    return redirect(url_for('productos'))

@app.route('/Eliminar Producto', methods=['GET','POST'])
def borrarproducto():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return render_template('paginas/borrarproducto.html')
    
    ID=request.form.get('EIDP')
    cursor = db.cursor()
    cursor.execute("""delete from Productos where ID = ?""",(ID))
    
    db.commit()
    
    return redirect(url_for('productos'))

@app.route('/Eliminar Usuarios', methods=['GET','POST'])
def borrarusuario():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return render_template('paginas/borrarusuario.html')
    
    DNombre=request.form.get('DNombre')
    cursor = db.cursor()
    cursor.execute("""delete from Usuarios where ID = ?""",(DNombre))
    
    db.commit()
    
    return redirect(url_for('usuarios'))    

@app.route('/Eliminar Categoria', methods=['GET','POST'])
def borrarcategoria():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return render_template('paginas/borrarcategoria.html')
    
    Categoria=request.form.get('EIDC')
    cursor = db.cursor()
    cursor.execute("""delete from Categorias where ID = ?""",(Categoria))
    
    db.commit()
    
    return redirect(url_for('categorias'))  

@app.route('/Editar usuario', methods=['GET','POST'])
def modificarusuario():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return render_template('paginas/modificarusuario.html')
    
    ID=request.form.get('IdP')
    Nombre=request.form.get('EditarNombreP')
    Correo=request.form.get('EditarCorreoP')
    Contraseña=request.form.get('EditarContraseñaP')
    
    cursor = db.cursor()
    cursor.execute("""update Usuarios set
                Nombre=?,
                Email=?, 
                Contraseña=?
                WHERE ID=?
    """,(Nombre,Correo,Contraseña,ID))
    
    db.commit()
    
    return redirect(url_for('usuarios'))

@app.route('/Editar Producto', methods=['GET','POST'])
def modificarproducto():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        base()
        return render_template('paginas/modificarproducto.html', Categorias=categories )
    
    ID=request.form.get('EID')
    Nombre=request.form.get('ENombre')
    Precio=request.form.get('EPrecio')
    Categoria=request.form.get('ECategoria')
    
    cursor = db.cursor()
    cursor.execute("""update Productos set
                Nombre=?,
                Precio=?, 
                Categoria=?
                WHERE ID=?
    """,(Nombre,Precio,Categoria,ID))
    
    db.commit()
    
    return redirect(url_for('productos'))

@app.route('/Editar Categoria', methods=['GET','POST'])
def modificarcategoria():
    if not 'Usuarios' in session:
        return redirect(url_for('login'))
    
    if request.method == 'GET':
        return render_template('paginas/modificarcategoria.html')
    
    ID=request.form.get('IDC')
    Nombre=request.form.get('EditarNombreC')
    
    cursor = db.cursor()
    cursor.execute("""update Categorias set
                Categoria=?
                WHERE ID=?
    """,(Nombre,ID))
    
    db.commit()
    
    return redirect(url_for('categorias'))

app.run(debug=True)


