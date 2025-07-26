# crud_contratos.py
from database import conectar
from utilidades import is_data_valida, string_to_date, date_to_string
import psycopg2

def adicionar_contrato():
    """
    Cria um novo contrato entre um jogador e um time.
    """
    print("\n--- ADICIONAR NOVO CONTRATO ---")
    try:
        id_jogador = int(input("Digite o ID do jogador: ").strip())
        id_time = int(input("Digite o ID do time: ").strip())
        data_inicio_str = input("Data de início do contrato (DD/MM/AAAA): ").strip()
        data_fim_str = input("Data de fim (DD/MM/AAAA) [deixe em branco se for indeterminado]: ").strip()

        if not is_data_valida(data_inicio_str):
            print("Erro: Data de início inválida.")
            return

        data_inicio = string_to_date(data_inicio_str)
        data_fim = None
        if data_fim_str:
            if not is_data_valida(data_fim_str):
                print("Erro: Data de fim inválida.")
                return
            data_fim = string_to_date(data_fim_str)
            if data_fim <= data_inicio:
                print("Erro: A data de fim deve ser posterior à data de início.")
                return

        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM jogadores WHERE id = %s", (id_jogador,))
                if cur.fetchone() is None:
                    print(f"Erro: Jogador com ID {id_jogador} não encontrado.")
                    return
                
                cur.execute("SELECT id FROM times WHERE id = %s", (id_time,))
                if cur.fetchone() is None:
                    print(f"Erro: Time com ID {id_time} não encontrado.")
                    return

                sql = "INSERT INTO contratos (id_jogador, id_time, data_inicio, data_fim) VALUES (%s, %s, %s, %s)"
                cur.execute(sql, (id_jogador, id_time, data_inicio, data_fim))
                print("\nContrato adicionado com sucesso!")

    except ValueError:
        print("Erro: IDs devem ser números inteiros.")
    except Exception as e:
        print(f"\nErro ao adicionar contrato: {e}")


def listar_contratos():
    """
    Busca e exibe todos os contratos, mostrando nomes dos jogadores e times.
    """
    print("\n--- LISTA DE CONTRATOS ---")
    sql = """
        SELECT 
            c.id,
            j.nome AS nome_jogador,
            t.nome AS nome_time,
            c.data_inicio,
            c.data_fim
        FROM contratos c
        JOIN jogadores j ON c.id_jogador = j.id
        JOIN times t ON c.id_time = t.id
        ORDER BY c.data_inicio DESC;
    """
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                contratos = cur.fetchall()

                if not contratos:
                    print("Nenhum contrato cadastrado.")
                    return

                print(f"{'ID':<4} | {'Jogador':<30} | {'Time':<30} | {'Início':<12} | {'Fim':<12}")
                print("-" * 95)
                for contrato in contratos:
                    id_contrato, nome_jogador, nome_time, data_inicio, data_fim = contrato
                    
                    inicio_str = date_to_string(data_inicio)
                    fim_str = date_to_string(data_fim) if data_fim else "Vigente"
                    
                    print(f"{id_contrato:<4} | {nome_jogador:<30} | {nome_time:<30} | {inicio_str:<12} | {fim_str:<12}")
    
    except Exception as e:
        print(f"\nErro ao listar contratos: {e}")


def atualizar_data_fim_contrato():
    """
    Atualiza a data de término de um contrato existente.
    """
    print("\n--- ATUALIZAR DATA DE FIM DO CONTRATO ---")
    try:
        id_contrato = int(input("Digite o ID do contrato a ser atualizado: ").strip())
    except ValueError:
        print("Erro: ID inválido.")
        return

    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT data_inicio FROM contratos WHERE id = %s", (id_contrato,))
                resultado = cur.fetchone()
                if resultado is None:
                    print("Erro: Contrato não encontrado.")
                    return
                data_inicio = resultado[0]

                data_fim_str = input(f"Nova data de fim (DD/MM/AAAA): ").strip()
                if not is_data_valida(data_fim_str):
                    print("Erro de validação: Data inválida.")
                    return
                
                nova_data_fim = string_to_date(data_fim_str)
                if nova_data_fim <= data_inicio:
                    print("Erro: A nova data de fim deve ser posterior à data de início.")
                    return

                sql = "UPDATE contratos SET data_fim = %s WHERE id = %s"
                cur.execute(sql, (nova_data_fim, id_contrato))
                print("\nContrato atualizado com sucesso!")

    except Exception as e:
        print(f"\nErro ao atualizar contrato: {e}")


def remover_contrato():
    """
    Remove um contrato do banco de dados a partir de seu ID.
    """
    print("\n--- REMOVER CONTRATO ---")
    try:
        id_contrato = int(input("Digite o ID do contrato a ser removido: ").strip())
    except ValueError:
        print("Erro: ID inválido.")
        return

    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM contratos WHERE id = %s", (id_contrato,))
                if cur.rowcount > 0:
                    print("\nContrato removido com sucesso!")
                else:
                    print("Contrato não encontrado ou ID inválido.")
    
    except Exception as e:
        print(f"\nErro ao remover contrato: {e}")