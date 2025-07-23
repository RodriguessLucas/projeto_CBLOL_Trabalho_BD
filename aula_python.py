#pip install psycopg2-binary  - (codigo de instalação da biblioteca no terminal)
#!pip install psycopg2-binary - (codigo de instalação da biblioteca no codigo)

import psycopg2

def conexao():
    return psycopg2.connect(host="localhost", database="lojaveiculos", user="admin", password="admin123")

def inserirCliente(nome, cpf, cidade, idade):
    try:    
        conn = conexao()
        cur = conn.cursor()
        cur.execute(f"INSERT INTO Cliente (nome, cpf, cidade, idade) VALUES ({nome}, {cpf}, {cidade}, {idade})")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)

def atualizarCliente(id, idade):
    try:    
        conn = conexao()
        cur = conn.cursor()
        cur.execute(f"UPDATE Cliente SET idade = {idade} WHERE id = {id}")
        if cur.rowcount > 0:
            print("Dados atualizados com sucesso")
        else:
            print("Nenhuma linha foi atualizada")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)

def removerCliente():
    try:    
        conn = conexao()
        cur = conn.cursor()
        cur.execute(f"DELETE FROM Cliente WHERE id = {id}")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)

def listarClientes():
    try:    
        conn = conexao()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM Cliente")
        for linha in cur.fetchall():
            print(f"Nome: {linha[0]}, Cpf: {linha[1]}, Idade:{linha[2]}, Cidade:{linha[3]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(e)

#clientes que tem pelo menos 32 anos de cada cidade
def consultarClientesPorCidade(idade):
    try:    
        conn = conexao()
        cur = conn.cursor()
        cur.execute(f"SELECT cidade, COUNT(*) FROM Cliente WHERE idade >= {idade} GROUP BY cidade")
        for linha in cur.fetchall():
            print(f"Cidade:{linha[0]}, Quantidade:{linha[1]}")
        cur.close()
        conn.close()
    except Exception as e:
        print(e)

#inserirCliente("Renato", "12345678900", "Limoeiro", 20)
#atualizarCliente()
#removerCliente(12)
#listarClientes
#consultarClientesPorCidade(35);