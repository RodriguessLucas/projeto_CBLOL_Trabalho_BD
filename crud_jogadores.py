# crud_jogadores.py
from database import conectar
from utilidades import string_to_date, date_to_string, is_data_valida

def listar_todos_jogadores():
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT j.id, j.nome, j.data_inicio_carreira, j.data_fim_carreira, j.nacionalidade, p.nome FROM jogadores j JOIN posicoes p ON j.id_posicao = p.id ORDER BY j.nome")
                jogadores = cur.fetchall()
                
                if not jogadores:
                    print("\nNão há jogadores cadastrados no sistema!")
                    return

                print(f"\n--- LISTA DE JOGADORES ---")
                print(f"{'ID':<4} | {'Nome':<25} | {'Início':<12} | {'Fim':<12} | {'Nacionalidade':<20} | {'Posição':<10}")
                print("-" * 95)
                
                for jogador in jogadores:
                    id_jogador, nome, data_inicio, data_fim, nacionalidade, posicao_nome = jogador
                    
                    data_fim_str = date_to_string(data_fim) if data_fim else "Ativo"
                    data_inicio_str = date_to_string(data_inicio)
                    
                    print(f"{id_jogador:<4} | {nome:<25} | {data_inicio_str:<12} | {data_fim_str:<12} | {nacionalidade:<20} | {posicao_nome:<10}")

    except Exception as e:
        print(f"Erro ao listar jogadores: {e}")

def buscar_um_jogador():
    try:
        id_jogador_str = input("Digite o ID do jogador que busca: ").strip()
        id_jogador = int(id_jogador_str)

        with conectar() as conn:
            with conn.cursor() as cur:
                sql = """
                    SELECT j.id, j.nome, j.data_inicio_carreira, j.data_fim_carreira, j.nacionalidade, p.nome 
                    FROM jogadores j
                    JOIN posicoes p ON j.id_posicao = p.id
                    WHERE j.id = %s
                """
                cur.execute(sql, (id_jogador,))
                jogador = cur.fetchone()

                if not jogador:
                    print("\nJogador não encontrado no banco de dados.")
                    return
                
                id_j, nome, dt_inicio, dt_fim, nac, pos = jogador
                
                print("\n--- Informações do Jogador ---")
                print(f"ID: {id_j}")
                print(f"Nome: {nome}")
                print(f"Início da Carreira: {date_to_string(dt_inicio)}")
                print(f"Fim da Carreira: {date_to_string(dt_fim) if dt_fim else 'Ativo'}")
                print(f"Nacionalidade: {nac}")
                print(f"Posição: {pos}")

    except ValueError:
        print("Erro: ID inválido. Por favor, digite um número.")
    except Exception as e:
        print(f"Erro ao buscar jogador: {e}")

def cadastrar_jogador():
    try:
        nome = input("Digite o nome: ").strip()
        inicio_carreira_str = input("Digite a data de início da carreira (DD/MM/AAAA): ").strip()
        nacionalidade = input("Digite a nacionalidade: ").strip()
        id_posicao_str = input("Digite o ID da posição: ").strip()
        
        if not all([nome, inicio_carreira_str, nacionalidade, id_posicao_str]):
            print("Erro: Todos os campos são obrigatórios.")
            return

        if not is_data_valida(inicio_carreira_str):
            print("Erro: Data de início inválida.")
            return

        id_posicao = int(id_posicao_str)
        inicio_carreira = string_to_date(inicio_carreira_str)

        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT nome FROM posicoes WHERE id = %s", (id_posicao,))
                posicao = cur.fetchone()
                if not posicao:
                    print("Erro: Posição usada para cadastrar jogador é inválida!")
                    return
                
                sql = "INSERT INTO jogadores(nome, data_inicio_carreira, nacionalidade, id_posicao) VALUES (%s, %s, %s, %s)"
                cur.execute(sql, (nome, inicio_carreira, nacionalidade, id_posicao))
                
                print(f"\nNovo jogador adicionado! \nNome: {nome} - Nacionalidade: {nacionalidade} - Posição: {posicao[0]}")

    except ValueError:
        print("Erro: O ID da posição deve ser um número.")
    except Exception as e:
        print(f"Erro ao cadastrar jogador: {e}")

def remover_jogador():
    try:
        id_str = input("Digite o ID do jogador que será removido: ").strip()
        id_jogador = int(id_str)

        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM jogadores WHERE id = %s", (id_jogador,))
                if cur.rowcount > 0:
                    print("Jogador removido com sucesso!")
                else:
                    print("ID inválido ou não encontrado. Nenhum jogador foi removido.")
    except ValueError:
        print("Erro: ID digitado não é um número válido!")
    except Exception as e:
        print(f"Erro ao remover jogador: {e}")
