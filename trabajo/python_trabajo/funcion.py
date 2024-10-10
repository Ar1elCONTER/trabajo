from flask import Flask, render_template, request, redirect, url_for, session
import qrcode

app = Flask(__name__)
app.secret_key = 'secret_key'


users = {
    'admin': {'role': 'admin', 'password': 'admin123'},
    'user1': {'role': 'user', 'password': 'user123'}
}

objects = [
    {'name': 'Mesa', 'category': 'Muebles', 'status': 'Disponible'},
    {'name': 'Silla', 'category': 'Muebles', 'status': 'Alquilada'},
    {'name': 'Computadora', 'category': 'Electrónica', 'status': 'Disponible'}
]

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['user'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrectos"
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        if session['role'] == 'admin':
            return render_template('admin_dashboard.html', users=users)
        else:
            return render_template('user_dashboard.html', objects=objects)
    return redirect(url_for('login'))


@app.route('/admin/modify_user/<username>', methods=['POST'])
def modify_user(username):
    if 'user' in session and session['role'] == 'admin':
        action = request.form.get('action')
        if action == 'delete':
            users.pop(username, None)
        elif action == 'suspend':
            users[username]['status'] = 'suspended'
        return redirect(url_for('dashboard'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        
        results = [obj for obj in objects if query.lower() in obj['name'].lower() or query.lower() in obj['category'].lower()]
        return render_template('search_results.html', results=results)
    return render_template('search.html')


@app.route('/register_qr')
def register_qr():
    if 'user' in session:
        user = session['user']
        qr_code = qrcode.make(user)
        qr_code.save(f'static/{user}_qr.png')
        return render_template('register_qr.html', qr_code=f'{user}_qr.png')
    return redirect(url_for('login'))

if __name__ == 'main':
    app.run(debug=True)