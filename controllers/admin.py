from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models.db import get_produtos, get_produto, d_insert_produto, d_update_produto, d_delete_produto, get_todos_pedidos

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorador de Autenticação Admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('is_admin') != 1:
            flash('Acesso restrito a administradores.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_required
@admin_bp.route('/')
@admin_bp.route('/dashboard')
def dashboard():
    produtos = get_produtos()
    return render_template('admin.html', produtos=produtos)

@admin_required
@admin_bp.route('/produto/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco', 0))
        imagem = request.form.get('imagem')
        
        d_insert_produto(nome, descricao, preco, imagem)
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin.html', action='novo', produtos=get_produtos())

@admin_required
@admin_bp.route('/produto/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    p = get_produto(id)
    if not p:
        flash('Produto não encontrado.', 'warning')
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco', 0))
        imagem = request.form.get('imagem')
        
        d_update_produto(id, nome, descricao, preco, imagem)
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin.html', action='editar', p_edit=p, produtos=get_produtos())

@admin_required
@admin_bp.route('/produto/deletar/<int:id>')
def deletar_produto(id):
    d_delete_produto(id)
    flash('Produto removido do catálogo.', 'info')
    return redirect(url_for('admin.dashboard'))
@admin_required
@admin_bp.route('/pedidos')
def pedidos():
    vendas = get_todos_pedidos()
    return render_template('pedidos.html', pedidos=vendas, view_type='admin')
