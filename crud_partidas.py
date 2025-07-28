# crud_partidas.py
from database import conectar

def adicionar_partida():
    """
    Cadastra uma nova partida no banco de dados.
    """
    print("\n--- ADICIONAR NOVA PARTIDA ---")
    try:
        id_campeonato = int(input("ID do Campeonato: ").strip())
        id_time1 = int(input("ID do Time 1: ").strip())
        id_time2 = int(input("ID do Time 2: ").strip())
        id_time_vencedor = int(input(f"ID do Time Vencedor ({id_time1} ou {id_time2}): ").strip())
        duracao = input("Duração da partida (HH:MM:SS): ").strip()

        if id_time1 == id_time2:
            print("Erro: Os times 1 e 2 não podem ser iguais.")
            return
        if id_time_vencedor not in [id_time1, id_time2]:
            print("Erro: O time vencedor deve ser o time 1 ou o time 2.")
            return

        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM campeonatos WHERE id = %s", (id_campeonato,))
                if not cur.fetchone(): print("Erro: ID do campeonato não existe."); return
                cur.execute("SELECT id FROM times WHERE id = %s", (id_time1,))
                if not cur.fetchone(): print("Erro: ID do time 1 não existe."); return
                cur.execute("SELECT id FROM times WHERE id = %s", (id_time2,))
                if not cur.fetchone(): print("Erro: ID do time 2 não existe."); return

                sql = "INSERT INTO partidas (id_campeonato, id_time1, id_time2, id_time_vencedor, duracao_partida) VALUES (%s, %s, %s, %s, %s)"
                cur.execute(sql, (id_campeonato, id_time1, id_time2, id_time_vencedor, duracao))
                print("\nPartida adicionada com sucesso!")

    except ValueError:
        print("Erro: IDs devem ser números inteiros.")
    except Exception as e:
        print(f"\nErro ao adicionar partida: {e}")

def listar_partidas():
    """
    Busca e exibe todas as partidas, mostrando os nomes dos times.
    """
    print("\n--- LISTA DE PARTIDAS ---")
    sql = """
        SELECT p.id, c.nome, t1.nome, t2.nome, t_venc.nome, p.duracao_partida
        FROM partidas p
        JOIN campeonatos c ON p.id_campeonato = c.id
        JOIN times t1 ON p.id_time1 = t1.id
        JOIN times t2 ON p.id_time2 = t2.id
        JOIN times t_venc ON p.id_time_vencedor = t_venc.id
        ORDER BY p.id DESC;
    """
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()
                if not resultados:
                    print("Nenhuma partida cadastrada."); return

                print(f"{'ID':<4} | {'Camp':<20} | {'Time 1':<15} | {'Time 2':<15} | {'Vencedor':<15} | {'Duração':<10}")
                print("-" * 95)
                for id_p, camp, t1, t2, t_venc, duracao in resultados:
                    print(f"{id_p:<4} | {camp[:18]:<20} | {t1:<15} | {t2:<15} | {t_venc:<15} | {duracao:<10}")
    except Exception as e:
        print(f"\nErro ao listar partidas: {e}")
