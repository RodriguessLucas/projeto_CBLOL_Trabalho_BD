# crud_campeonatos.py
from database import conectar
from utilidades import is_string_valida

def adicionar_campeonato():
    """
    Cadastra um novo campeonato no banco de dados.
    """
    print("\n--- ADICIONAR NOVO CAMPEONATO ---")
    try:
        nome = input("Nome do campeonato: ").strip()
        ano = input("Ano (AAAA): ").strip()
        pais = input("País de ocorrência: ").strip()
        split = input("Split (1, 2, etc.): ").strip()

        if not is_string_valida(nome) or not is_string_valida(pais):
            print("Erro: Nome e país não podem ser vazios.")
            return
        if not (len(ano) == 4 and ano.isdigit()):
            print("Erro: O ano deve ter 4 dígitos.")
            return
        if not (len(split) == 1 and split.isalnum()):
            print("Erro: O split deve ser um único caractere.")
            return

        with conectar() as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO campeonatos (nome, ano, pais_ocorrencia, split) VALUES (%s, %s, %s, %s)"
                cur.execute(sql, (nome, ano, pais, split))
                print("\nCampeonato adicionado com sucesso!")

    except Exception as e:
        print(f"\nErro ao adicionar campeonato: {e}")

def listar_campeonatos():
    """
    Busca e exibe todos os campeonatos cadastrados.
    """
    print("\n--- LISTA DE CAMPEONATOS ---")
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nome, ano, pais_ocorrencia, split FROM campeonatos ORDER BY ano DESC, nome")
                resultados = cur.fetchall()

                if not resultados:
                    print("Nenhum campeonato cadastrado.")
                    return

                print(f"{'ID':<4} | {'Nome':<40} | {'Ano':<6} | {'País':<20} | {'Split':<5}")
                print("-" * 85)
                for id_c, nome, ano, pais, split in resultados:
                    print(f"{id_c:<4} | {nome:<40} | {ano:<6} | {pais:<20} | {split:<5}")
    except Exception as e:
        print(f"\nErro ao listar campeonatos: {e}")