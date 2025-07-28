# crud_times.py
from database import conectar
from utilidades import is_string_valida, is_data_valida, string_to_date, date_to_string
import psycopg2

def adicionar_time():
    """
    Solicita dados do usuário para cadastrar um novo time no banco de dados.
    """
    print("\n--- CADASTRAR NOVO TIME ---")
    try:
        nome = input("Nome do time: ").strip()
        sigla = input("Sigla (3 caracteres): ").strip().upper()
        data_fundacao_str = input("Data de fundação (DD/MM/AAAA): ").strip()
        nacionalidade = input("Nacionalidade: ").strip()

        if not is_string_valida(nome) or not is_string_valida(nacionalidade):
            print("Erro: Nome e nacionalidade não podem ser vazios ou inválidos.")
            return
        
        if len(sigla) != 3 or not sigla.isalpha():
            print("Erro: A sigla deve ter exatamente 3 letras.")
            return

        if not is_data_valida(data_fundacao_str):
            print("Erro: Formato de data inválido. Use DD/MM/AAAA.")
            return

        data_fundacao = string_to_date(data_fundacao_str)

        with conectar() as conn:
            with conn.cursor() as cur:
                sql = "INSERT INTO times (nome, sigla, data_fundacao, nacionalidade) VALUES (%s, %s, %s, %s)"
                cur.execute(sql, (nome, sigla, data_fundacao, nacionalidade))
                print("\nTime adicionado com sucesso!")

    except Exception as e:
        print(f"\nErro ao adicionar time: {e}")


def listar_times():
    """
    Busca e exibe todos os times cadastrados no banco de dados.
    """
    print("\n--- LISTA DE TIMES ---")
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nome, sigla, data_fundacao, nacionalidade FROM times ORDER BY nome")
                times = cur.fetchall()

                if not times:
                    print("Nenhum time cadastrado.")
                    return

                print(f"{'ID':<4} | {'Nome':<25} | {'Sigla':<5} | {'Fundação':<12} | {'Nacionalidade':<20}")
                print("-" * 75)
                for time in times:
                    id, nome, sigla, data_fundacao, nacionalidade = time
                    data_formatada = date_to_string(data_fundacao)
                    print(f"{id:<4} | {nome:<25} | {sigla:<5} | {data_formatada:<12} | {nacionalidade:<20}")
    
    except Exception as e:
        print(f"\nErro ao listar times: {e}")


def atualizar_time():
    """
    Atualiza os dados de um time existente no banco de dados.
    """
    print("\n--- ATUALIZAR TIME ---")
    try:
        id_time = int(input("Digite o ID do time a ser atualizado: ").strip())
    except ValueError:
        print("Erro: ID inválido.")
        return

    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM times WHERE id = %s", (id_time,))
                if cur.fetchone() is None:
                    print("Erro: Time não encontrado.")
                    return

                print("Deixe o campo em branco para não alterar.")
                nome = input(f"Novo nome: ").strip() or None
                sigla = input(f"Nova sigla: ").strip().upper() or None
                data_fundacao_str = input(f"Nova data de fundação (DD/MM/AAAA): ").strip() or None
                nacionalidade = input(f"Nova nacionalidade: ").strip() or None
                
                campos = []
                valores = []

                if nome:
                    campos.append("nome = %s")
                    valores.append(nome)
                if sigla:
                    if len(sigla) != 3 or not sigla.isalpha():
                        print("Erro de validação: A sigla deve ter 3 letras.")
                        return
                    campos.append("sigla = %s")
                    valores.append(sigla)
                if data_fundacao_str:
                    if not is_data_valida(data_fundacao_str):
                        print("Erro de validação: Data inválida.")
                        return
                    campos.append("data_fundacao = %s")
                    valores.append(string_to_date(data_fundacao_str))
                if nacionalidade:
                    campos.append("nacionalidade = %s")
                    valores.append(nacionalidade)

                if not campos:
                    print("Nenhuma alteração foi fornecida.")
                    return

                valores.append(id_time)
                sql = f"UPDATE times SET {', '.join(campos)} WHERE id = %s"
                cur.execute(sql, valores)
                print("\nTime atualizado com sucesso!")

    except Exception as e:
        print(f"\nErro ao atualizar time: {e}")


def remover_time():
    """
    Remove um time do banco de dados a partir de seu ID.
    """
    print("\n--- REMOVER TIME ---")
    try:
        id_time = int(input("Digite o ID do time a ser removido: ").strip())
    except ValueError:
        print("Erro: ID inválido.")
        return

    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM times WHERE id = %s", (id_time,))
                if cur.rowcount > 0:
                    print("\nTime removido com sucesso!")
                else:
                    print("Time não encontrado ou ID inválido.")
    
    except psycopg2.errors.ForeignKeyViolation:
        print("\nErro: Este time não pode ser removido pois possui jogadores ou partidas associadas a ele.")
    except Exception as e:
        print(f"\nErro ao remover time: {e}")
