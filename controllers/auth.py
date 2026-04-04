from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import get_usuario_by_email, d_create_usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        usuario = get_usuario_by_email(email)
        
        if usuario and check_password_hash(usuario['senha'], senha):
            session['usuario_id'] = usuario['id']
            session['nome'] = usuario['nome']
            session['email'] = usuario['email']
            session['is_admin'] = usuario['is_admin']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('shop.index'))
        else:
            flash('E-mail ou senha incorretos.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        cpf = request.form.get('cpf')
        endereco = request.form.get('endereco')
        
        if not nome or not email or not senha or not cpf or not endereco:
            flash('Preencha todos os campos.', 'warning')
            return redirect(url_for('auth.cadastro'))
            
        senha_hash = generate_password_hash(senha)
        
        if d_create_usuario(nome, email, senha_hash, cpf, endereco):
            flash('Conta criada! Agora você pode entrar.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('E-mail já cadastrado.', 'danger')
            
    return render_template('cadastro.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('shop.index'))
