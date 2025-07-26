# crud_personagens.py
from database import conectar
from utilidades import is_string_valida

def adicionar_personagem():
    """
    Cadastra um novo personagem no banco de dados.
    """
    print("\n--- ADICIONAR NOVO PERSONAGEM ---")
    try:
        nome = input("Nome do personagem: ").strip()

        if not is_string_valida(nome):
            print("Erro: Nome não pode ser vazio.")
            return

        with conectar() as conn:
            with conn.cursor() as cur:
                # Evita duplicatas
                cur.execute("SELECT id FROM personagens WHERE nome = %s", (nome,))
                if cur.fetchone():
                    print("Erro: Personagem já cadastrado.")
                    return
                
                sql = "INSERT INTO personagens (nome) VALUES (%s)"
                cur.execute(sql, (nome,))
                print("\nPersonagem adicionado com sucesso!")
    except Exception as e:
        print(f"\nErro ao adicionar personagem: {e}")

def listar_personagens():
    """
    Busca e exibe todos os personagens cadastrados.
    """
    print("\n--- LISTA DE PERSONAGENS ---")
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nome FROM personagens ORDER BY nome")
                resultados = cur.fetchall()

                if not resultados:
                    print("Nenhum personagem cadastrado.")
                    return

                print(f"{'ID':<5} | {'Nome':<30}")
                print("-" * 40)
                for id_p, nome in resultados:
                    print(f"{id_p:<5} | {nome:<30}")
    except Exception as e:
        print(f"\nErro ao listar personagens: {e}")