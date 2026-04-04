from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.db import get_produtos, get_produto, d_create_pedido, get_pedidos_usuario

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def index():
    busca = request.args.get('busca')
    produtos = get_produtos(busca)
    return render_template('index.html', produtos=produtos, busca=busca)

@shop_bp.route('/produto/<int:id>')
def produto(id):
    p = get_produto(id)
    if not p:
        flash('Produto não encontrado.', 'warning')
        return redirect(url_for('shop.index'))
    return render_template('produto.html', produto=p)

@shop_bp.route('/carrinho')
def carrinho():
    # Estrutura do carrinho na sessão: {produto_id: quantidade}
    c_session = session.get('carrinho', {})
    itens = []
    total = 0
    
    for p_id, qtd in c_session.items():
        p = get_produto(int(p_id))
        if p:
            subtotal = p['preco'] * qtd
            itens.append({
                'produto': p,
                'quantidade': qtd,
                'subtotal': subtotal
            })
            total += subtotal
            
    return render_template('carrinho.html', itens=itens, total=total)

@shop_bp.route('/add_carrinho/<int:produto_id>', methods=['POST'])
def add_carrinho(produto_id):
    if 'carrinho' not in session:
        session['carrinho'] = {}
    
    c = session['carrinho']
    p_id_str = str(produto_id)
    
    if p_id_str in c:
        c[p_id_str] += 1
    else:
        c[p_id_str] = 1
        
    session['carrinho'] = c # Forçar atualização da sessão
    flash('Produto adicionado ao carrinho!', 'success')
    return redirect(url_for('shop.index'))

@shop_bp.route('/update_carrinho', methods=['POST'])
def update_carrinho():
    p_id = request.form.get('produto_id')
    try:
        qtd = int(request.form.get('quantidade', 0))
    except ValueError:
        qtd = 0
    
    if 'carrinho' in session:
        c = session['carrinho']
        if qtd <= 0:
            if p_id in c: del c[p_id]
        else:
            c[p_id] = qtd
        session['carrinho'] = c
        
    return redirect(url_for('shop.carrinho'))

@shop_bp.route('/remove_carrinho/<int:produto_id>')
def remove_carrinho(produto_id):
    if 'carrinho' in session:
        c = session['carrinho']
        p_id_str = str(produto_id)
        if p_id_str in c:
            del c[p_id_str]
            session['carrinho'] = c
            flash('Produto removido.', 'info')
            
    return redirect(url_for('shop.carrinho'))

@shop_bp.route('/checkout')
def checkout():
    if not session.get('usuario_id'):
        flash('Faça login para finalizar a compra.', 'warning')
        return redirect(url_for('auth.login'))
        
    c_session = session.get('carrinho', {})
    if not c_session:
        flash('Seu carrinho está vazio.', 'warning')
        return redirect(url_for('shop.index'))
        
    total = 0
    itens = []
    for p_id, qtd in c_session.items():
        p = get_produto(int(p_id))
        if p:
            subtotal = p['preco'] * qtd
            itens.append({'produto': p, 'quantidade': qtd, 'subtotal': subtotal})
            total += subtotal
            
    return render_template('pagamento.html', itens=itens, total=total)

@shop_bp.route('/processar_pagamento', methods=['POST'])
def processar_pagamento():
    if not session.get('usuario_id'):
        return redirect(url_for('auth.login'))

    metodo = request.form.get('metodo_pagamento')
    total = float(request.form.get('total', 0))
    
    # Extração do endereço
    cep = request.form.get('cep')
    rua = request.form.get('rua')
    numero = request.form.get('numero')
    complemento = request.form.get('complemento', '')
    bairro = request.form.get('bairro')
    cidade = request.form.get('cidade')
    
    endereco_completo = f"{rua}, {numero} {complemento} - {bairro}, {cidade} - CEP: {cep}"
    
    # Criação do pedido final com método de pagamento e endereço
    d_create_pedido(session['usuario_id'], total, metodo, endereco_entrega=endereco_completo, status='Pago')
    
    # Limpar carrinho
    session.pop('carrinho', None)
    
    flash(f'Pedido no valor de R$ {total:.2f} via {metodo} processado com sucesso! Obrigado pela compra.', 'success')
    return redirect(url_for('shop.meus_pedidos'))

@shop_bp.route('/meus-pedidos')
def meus_pedidos():
    if not session.get('usuario_id'):
        flash('Faça login para ver seu histórico.', 'warning')
        return redirect(url_for('auth.login'))
        
    pedidos = get_pedidos_usuario(session['usuario_id'])
    return render_template('pedidos.html', pedidos=pedidos, view_type='user')
