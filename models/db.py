import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    # Usuários (is_admin será 1 para admin, 0 comum)
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            cpf TEXT,
            endereco TEXT,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    # Produtos
    c.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            imagem TEXT
        )
    ''')
    # Pedidos
    c.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            total REAL NOT NULL,
            metodo_pagamento TEXT,
            endereco_entrega TEXT,
            status TEXT DEFAULT 'Pendente',
            data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')
    
    # Criar um Admin padrão se a tabela de usuários estiver vazia
    c.execute('SELECT COUNT(*) FROM usuarios')
    if c.fetchone()[0] == 0:
        from werkzeug.security import generate_password_hash
        admin_pass = generate_password_hash('admin123')
        c.execute('INSERT INTO usuarios (nome, email, senha, is_admin) VALUES (?, ?, ?, ?)', 
                  ('Administrador', 'admin@loja.com', admin_pass, 1))
             # Inserir alguns produtos mockados
        produtos_mock = [
            # Doces Famosos (18)
            ('Brigadeiro Gourmet Belga', 'Feito com chocolate 54% cacau e granulado especial de chocolate belga.', 4.50, 'https://images.unsplash.com/photo-1541783245831-57d6fb0926d3?auto=format&fit=crop&q=80&w=600'),
            ('Pudim de Leite Condensado', 'O clássico brasileiro, lisinho e cremoso com calda de caramelo artesanal.', 12.00, 'https://images.unsplash.com/photo-1528413533234-374f637caab0?auto=format&fit=crop&q=80&w=600'),
            ('Torta de Limão Siciliano', 'Massa sucrée crocante, creme cítrico e cobertura de merengue suíço maçaricado.', 15.00, 'https://images.unsplash.com/photo-1519915028121-7d3463d20b13?auto=format&fit=crop&q=80&w=600'),
            ('Brownie Belga com Nozes', 'Massa densa e molhadinha com pedaços generosos de chocolate e nozes.', 13.00, 'https://images.unsplash.com/photo-1580915411954-282cb1b0d780?auto=format&fit=crop&q=80&w=600'),
            ('Cheesecake de Frutas Vermelhas', 'Base de biscoito, creme de queijo leve e calda artesanal de morango e amora.', 16.00, 'https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&q=80&w=600'),
            ('Banoffee Pie', 'Doce de leite, banana fatiada e chantilly fresco polvilhado com cacau.', 14.00, 'https://images.unsplash.com/photo-1590422119951-6ca23cd7048f?auto=format&fit=crop&q=80&w=600'),
            ('Red Velvet Cake', 'Camadas aveludadas de bolo vibrante com frosting de cream cheese frosting.', 22.00, 'https://images.unsplash.com/photo-1586788680452-a46e1291880a?auto=format&fit=crop&q=80&w=600'),
            ('Bolo de Cenoura com Chocolate', 'Bolo fofinho de cenoura com cobertura generosa de brigadeiro gourmet.', 18.00, 'https://images.unsplash.com/photo-1576733221372-10ae4473e87d?auto=format&fit=crop&q=80&w=600'),
            ('Petit Gâteau de Chocolate', 'Bolinho quente de chocolate belga com interior derretido e aveludado.', 18.00, 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&q=80&w=600'),
            ('Tiramisù Original', 'Biscoito champagne embebido em café espresso e creme de mascarpone.', 20.00, 'https://images.unsplash.com/photo-1571877223202-536f98889bf2?auto=format&fit=crop&q=80&w=600'),
            ('Cannoli de Pistache', 'Massa frita crocante recheada com ricota doce e pistaches iranianos.', 14.00, 'https://images.unsplash.com/photo-1551462002-31d7986c757c?auto=format&fit=crop&q=80&w=600'),
            ('Macarons Selection (Caixa 6)', 'Seleção de 6 macarons franceses em sabores sortidos e refinados.', 35.00, 'https://images.unsplash.com/photo-1514517604298-cf80e0fb7f1e?auto=format&fit=crop&q=80&w=600'),
            ('Donuts Artesanais Especial', 'Donut super macio com glaçagem colorida e recheio cremoso.', 10.00, 'https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&q=80&w=600'),
            ('Quindim de Ouro', 'Doce tradicional feito com gemas selecionadas e coco fresco hidratado.', 8.00, 'https://images.unsplash.com/photo-1590005354167-6da97870c912?auto=format&fit=crop&q=80&w=600'),
            ('Sonho de Baunilha', 'Massa fofinha polvilhada com açúcar e recheada com creme patissière.', 7.00, 'https://images.unsplash.com/photo-1559599189-fe84dea4eb79?auto=format&fit=crop&q=80&w=600'),
            ('Palha Italiana Tradicional', 'Mistura irresistível de brigadeiro artesanal com biscoito triturado.', 8.00, 'https://images.unsplash.com/photo-1553452118-621e1f860f43?auto=format&fit=crop&q=80&w=600'),
            ('Alfajor de Doce de Leite', 'Biscoito macio recheado com doce de leite e banhado em chocolate.', 9.00, 'https://images.unsplash.com/photo-1594913785162-e6785b426cb7?auto=format&fit=crop&q=80&w=600'),
            ('Pão de Mel Recheado', 'Mel puro e especiarias recheado com o melhor doce de leite do mercado.', 8.00, 'https://images.unsplash.com/photo-1583095117201-1632822003c2?auto=format&fit=crop&q=80&w=600'),
            
            # Bebidas Premium (12)
            ('Milkshake Ninho com Nutella', 'O favorito absoluto: Leite Ninho batido com Nutella original.', 22.00, 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&q=80&w=600'),
            ('Milkshake Chocolate Belga', 'Batido com chocolate 54% e finalizado com chantilly fresco.', 20.00, 'https://images.unsplash.com/photo-1579954115545-a95591f28bfc?auto=format&fit=crop&q=80&w=600'),
            ('Milkshake Morango Silvestre', 'Com base de sorvete de baunilha e calda de morangos in natura.', 20.00, 'https://images.unsplash.com/photo-1553787499-6f9133860278?auto=format&fit=crop&q=80&w=600'),
            ('Cappuccino Italiano Tradicional', 'O equilíbrio perfeito entre café espresso, leite vaporizado e cacau.', 12.00, 'https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&q=80&w=600'),
            ('Café Espresso Double', 'Extração dupla de grãos selecionados 100% arábica com notas amendoadas.', 8.00, 'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?auto=format&fit=crop&q=80&w=600'),
            ('Mocha de Caramelo Salgado', 'Café espresso, leite vaporizado, chocolate e calda de caramelo salgado.', 15.00, 'https://images.unsplash.com/photo-1541167760496-1628856ab772?auto=format&fit=crop&q=80&w=600'),
            ('Soda Italiana Maçã Verde', 'Refresco leve com xarope artesanal francês e água gaseificada.', 14.00, 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&q=80&w=600'),
            ('Soda Italiana Cranberry', 'Refrescante e levemente ácido, ideal para acompanhar doces intensos.', 14.00, 'https://images.unsplash.com/photo-1546171753-97d7676e4602?auto=format&fit=crop&q=80&w=600'),
            ('Iced Tea Frutas Vermelhas', 'Chá preto gelado com infusão natural de hibisco e frutas vermelhas.', 12.00, 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&q=80&w=600'),
            ('Chocolate Quente Europeu', 'Chocolate denso e cremoso em estilo europeu, feito com blend 50% cacau.', 16.00, 'https://images.unsplash.com/photo-1544787210-2211d7c3099a?auto=format&fit=crop&q=80&w=600'),
            ('Suco de Laranja Natural', 'Suco integral 100% fruta, espremido na hora para máximo frescor.', 10.00, 'https://images.unsplash.com/photo-1613478223719-2ab802602423?auto=format&fit=crop&q=80&w=600'),
            ('Kit Degustação Doce Magia', 'Experiência completa: 4 mini doces e um mini cappuccino italiano.', 45.00, 'https://images.unsplash.com/photo-1551632432-c735e8306df9?auto=format&fit=crop&q=80&w=600')
        ]
        c.executemany('INSERT INTO produtos (nome, descricao, preco, imagem) VALUES (?, ?, ?, ?)', produtos_mock)
        
    # --- Migração simples para novas colunas (caso o banco já exista) ---
    try:
        c.execute('ALTER TABLE usuarios ADD COLUMN cpf TEXT')
    except: pass
    try:
        c.execute('ALTER TABLE usuarios ADD COLUMN endereco TEXT')
    except: pass
    try:
        c.execute('ALTER TABLE pedidos ADD COLUMN metodo_pagamento TEXT')
    except: pass
    try:
        c.execute('ALTER TABLE pedidos ADD COLUMN status TEXT DEFAULT "Pendente"')
    except: pass
    try:
        c.execute('ALTER TABLE pedidos ADD COLUMN endereco_entrega TEXT')
    except: pass

    conn.commit()
    conn.close()

# --- Helpers ---

def get_produtos(busca=None):
    conn = get_connection()
    try:
        c = conn.cursor()
        if busca:
            busca_query = f"%{busca}%"
            c.execute('SELECT * FROM produtos WHERE nome LIKE ? OR descricao LIKE ?', (busca_query, busca_query))
        else:
            c.execute('SELECT * FROM produtos')
        return c.fetchall()
    finally:
        conn.close()

def get_produto(id):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM produtos WHERE id = ?', (id,))
        return c.fetchone()
    finally:
        conn.close()

def d_insert_produto(nome, descricao, preco, imagem):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute('INSERT INTO produtos (nome, descricao, preco, imagem) VALUES (?, ?, ?, ?)', 
                  (nome, descricao, preco, imagem))
        conn.commit()
    finally:
        conn.close()

def d_update_produto(id, nome, descricao, preco, imagem):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute('UPDATE produtos SET nome=?, descricao=?, preco=?, imagem=? WHERE id=?', 
                  (nome, descricao, preco, imagem, id))
        conn.commit()
    finally:
        conn.close()

def d_delete_produto(id):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute('DELETE FROM produtos WHERE id=?', (id,))
        conn.commit()
    finally:
        conn.close()

def d_create_usuario(nome, email, senha, cpf=None, endereco=None):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO usuarios (nome, email, senha, cpf, endereco) VALUES (?, ?, ?, ?, ?)', 
                  (nome, email, senha, cpf, endereco))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_usuario_by_email(email):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        return c.fetchone()
    finally:
        conn.close()
    
def d_create_pedido(usuario_id, total, metodo_pagamento, endereco_entrega=None, status='Pago'):
    conn = get_connection()
    try:
        c = conn.cursor()
        c.execute('INSERT INTO pedidos (usuario_id, total, metodo_pagamento, endereco_entrega, status) VALUES (?, ?, ?, ?, ?)', 
                  (usuario_id, total, metodo_pagamento, endereco_entrega, status))
        conn.commit()
    finally:
        conn.close()

def get_pedidos_usuario(usuario_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT p.*, u.nome as usuario_nome 
        FROM pedidos p 
        JOIN usuarios u ON p.usuario_id = u.id 
        WHERE p.usuario_id = ? 
        ORDER BY p.data_pedido DESC
    ''', (usuario_id,))
    pedidos = c.fetchall()
    conn.close()
    return pedidos

def get_todos_pedidos():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        SELECT p.*, u.nome as usuario_nome, u.email as usuario_email 
        FROM pedidos p 
        JOIN usuarios u ON p.usuario_id = u.id 
        ORDER BY p.data_pedido DESC
    ''')
    pedidos = c.fetchall()
    conn.close()
    return pedidos
