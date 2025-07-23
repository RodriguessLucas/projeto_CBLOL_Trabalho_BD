import psycopg2

DB_CONFIG = {
    "dbname": "banco_cblol",
    "user": "postgres",
    "password": "postgres2025",
    "host": "localhost",
    "port": "5432"
}

def conectar():
    try:
        conexao = psycopg2.connect(**DB_CONFIG)
        return conexao
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    

SQL_CRIAR_TABELAS = """



"""