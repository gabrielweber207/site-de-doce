"""
Script para atualizar as imagens dos produtos no banco de dados
com URLs de alta qualidade e mais relevantes.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

# Mapeamento: nome do produto -> URL de imagem de alta qualidade
# Usando Unsplash com IDs específicos verificados e resolução maior (800px)
IMAGENS_ATUALIZADAS = {
    # ========================
    # DOCES
    # ========================
    'Brigadeiro Gourmet Belga': (
        'https://images.unsplash.com/photo-1548365328-8c6db3220e4c'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Pudim de Leite Condensado': (
        'https://images.unsplash.com/photo-1528413533234-374f637caab0'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Torta de Limão Siciliano': (
        'https://images.unsplash.com/photo-1519915028121-7d3463d20b13'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Brownie Belga com Nozes': (
        'https://images.unsplash.com/photo-1564355808539-22fda35bed7e'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Cheesecake de Frutas Vermelhas': (
        'https://images.unsplash.com/photo-1578775887804-699de7086ff9'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Banoffee Pie': (
        'https://images.unsplash.com/photo-1541599540903-216a46ca1dc0'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Red Velvet Cake': (
        'https://images.unsplash.com/photo-1616690248240-9b01f28ed9b3'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Bolo de Cenoura com Chocolate': (
        'https://images.unsplash.com/photo-1587668178277-295251f900ce'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Petit Gâteau de Chocolate': (
        'https://images.unsplash.com/photo-1606313564200-e75d5e30476c'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Tiramisù Original': (
        'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Cannoli de Pistache': (
        'https://images.unsplash.com/photo-1551462002-31d7986c757c'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Macarons Selection (Caixa 6)': (
        'https://images.unsplash.com/photo-1569864358642-9d1684040f43'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Donuts Artesanais Especial': (
        'https://images.unsplash.com/photo-1499636136210-6f4ee915583e'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Quindim de Ouro': (
        'https://images.unsplash.com/photo-1590005354167-6da97870c912'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Sonho de Baunilha': (
        'https://images.unsplash.com/photo-1508737027454-e6454ef45afd'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Palha Italiana Tradicional': (
        'https://images.unsplash.com/photo-1549007994-cb92caebd54b'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Alfajor de Doce de Leite': (
        'https://images.unsplash.com/photo-1558961363-fa8fdf82db35'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Pão de Mel Recheado': (
        'https://images.unsplash.com/photo-1549903072-7e6e0bedb7fb'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    # ========================
    # BEBIDAS
    # ========================
    'Milkshake Ninho com Nutella': (
        'https://images.unsplash.com/photo-1572490122747-3968b75cc699'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Milkshake Chocolate Belga': (
        'https://images.unsplash.com/photo-1579954115545-a95591f28bfc'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Milkshake Morango Silvestre': (
        'https://images.unsplash.com/photo-1553787499-6f9133860278'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Cappuccino Italiano Tradicional': (
        'https://images.unsplash.com/photo-1572442388796-11668a67e53d'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Café Espresso Double': (
        'https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Mocha de Caramelo Salgado': (
        'https://images.unsplash.com/photo-1541167760496-1628856ab772'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Soda Italiana Maçã Verde': (
        'https://images.unsplash.com/photo-1622483767028-3f66f32aef97'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Soda Italiana Cranberry': (
        'https://images.unsplash.com/photo-1582656531310-7f7a8e06528f'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Iced Tea Frutas Vermelhas': (
        'https://images.unsplash.com/photo-1556679343-c7306c1976bc'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Chocolate Quente Europeu': (
        'https://images.unsplash.com/photo-1517578239113-b03992dcdd25'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Suco de Laranja Natural': (
        'https://images.unsplash.com/photo-1600271886742-f049cd451bba'
        '?auto=format&fit=crop&q=85&w=800'
    ),
    'Kit Degustação Doce Magia': (
        'https://images.unsplash.com/photo-1488477181946-6428a0291777'
        '?auto=format&fit=crop&q=85&w=800'
    ),
}

def update_images():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('SELECT id, nome FROM produtos ORDER BY id')
    produtos = c.fetchall()
    
    updated = 0
    not_found = []
    
    for produto in produtos:
        pid = produto['id']
        nome = produto['nome']
        
        if nome in IMAGENS_ATUALIZADAS:
            nova_url = IMAGENS_ATUALIZADAS[nome]
            c.execute('UPDATE produtos SET imagem = ? WHERE id = ?', (nova_url, pid))
            print(f'  OK [{pid}] {nome}')
            updated += 1
        else:
            not_found.append(f'  SKIP [{pid}] {nome} - sem mapeamento')
    
    conn.commit()
    conn.close()
    
    print(f'\n{updated} imagens atualizadas com sucesso!')
    if not_found:
        print(f'{len(not_found)} produtos sem mapeamento:')
        for nf in not_found:
            print(nf)

if __name__ == '__main__':
    print('Atualizando imagens dos produtos...\n')
    update_images()
