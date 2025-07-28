# crud_estatisticas.py
from database import conectar

def adicionar_estatistica():
    """
    Cadastra uma nova linha de estatística para um jogador em uma partida.
    """
    print("\n--- ADICIONAR ESTATÍSTICA DE JOGADOR EM PARTIDA ---")
    try:
        id_partida = int(input("ID da Partida: ").strip())
        id_jogador = int(input("ID do Jogador: ").strip())
        id_personagem = int(input("ID do Personagem utilizado: ").strip())
        id_posicao = int(input("ID da Posição jogada: ").strip())
        lado_mapa = input("Lado do mapa (Azul/Vermelho): ").strip().capitalize()
        abates = int(input("Quantidade de Abates: ").strip())
        mortes = int(input("Quantidade de Mortes: ").strip())
        assistencias = int(input("Quantidade de Assistências: ").strip())
        
        if lado_mapa not in ['Azul', 'Vermelho']:
            print("Erro: Lado do mapa deve ser 'Azul' or 'Vermelho'."); return

        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM partidas WHERE id = %s", (id_partida,)); 
                if not cur.fetchone(): print("Erro: ID da partida não existe."); return
                cur.execute("SELECT id FROM jogadores WHERE id = %s", (id_jogador,)); 
                if not cur.fetchone(): print("Erro: ID do jogador não existe."); return
                cur.execute("SELECT id FROM personagens WHERE id = %s", (id_personagem,)); 
                if not cur.fetchone(): print("Erro: ID do personagem não existe."); return
                cur.execute("SELECT id FROM posicoes WHERE id = %s", (id_posicao,)); 
                if not cur.fetchone(): print("Erro: ID da posição não existe."); return

                sql = """
                    INSERT INTO estatisticas 
                    (id_partida, id_jogador, id_personagem, id_posicao, lado_mapa, qntd_abates, qntd_mortes, qntd_assistencias) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql, (id_partida, id_jogador, id_personagem, id_posicao, lado_mapa, abates, mortes, assistencias))
                print("\nEstatística adicionada com sucesso!")

    except ValueError:
        print("Erro: IDs, abates, mortes e assistências devem ser números inteiros.")
    except Exception as e:
        print(f"\nErro ao adicionar estatística: {e}")


def listar_estatisticas_por_partida():
    """
    Lista as estatísticas de todos os jogadores de uma partida específica.
    """
    print("\n--- ESTATÍSTICAS DA PARTIDA ---")
    try:
        id_partida = int(input("Digite o ID da Partida para ver as estatísticas: ").strip())
    except ValueError:
        print("Erro: ID inválido."); return
    
    sql = """
        SELECT j.nome, pers.nome, pos.nome, e.qntd_abates, e.qntd_mortes, e.qntd_assistencias
        FROM estatisticas e
        JOIN jogadores j ON e.id_jogador = j.id
        JOIN personagens pers ON e.id_personagem = pers.id
        JOIN posicoes pos ON e.id_posicao = pos.id
        WHERE e.id_partida = %s;
    """
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (id_partida,))
                resultados = cur.fetchall()
                if not resultados:
                    print("Nenhuma estatística encontrada para esta partida."); return
                
                print(f"\nEstatísticas da Partida ID: {id_partida}")
                print(f"{'Jogador':<25} | {'Personagem':<20} | {'Posição':<10} | {'K/D/A':<10}")
                print("-" * 75)
                for jog, pers, pos, k, d, a in resultados:
                    kda = f"{k}/{d}/{a}"
                    print(f"{jog:<25} | {pers:<20} | {pos:<10} | {kda:<10}")

    except Exception as e:
        print(f"\nErro ao listar estatísticas: {e}")
