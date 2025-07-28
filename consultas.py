from database import * 


#CONSULTA AVANÇADA 1: Média de tempo de partidas por split de um campeonato
def mediaDuracaoPorSplit():
    conexao = conectar()
    cur = conexao.cursor()
    campeonato = input("Digite o nome do campeonato: ").strip()
    try:
        cur.execute(f"SELECT c.split, AVG(p.duracao_partida) AS media_duracao FROM partidas p JOIN campeanatos c ON p.id_campeonato = c.id AND c.nome = {campeonato} GROUP BY c.split ORDER BY media_duracao DESC")
        splits = cur.fetchall()
        
        if not splits:
            return "Esse campeonato não está cadastrado no sistema"
        
        print(f"\nMédia de duração por Split para o campeonato: {campeonato}\n")
        print(f"{'Split':<6} | {'Média de Duração':>20}")
        print("-" * 30)
        
        for split, media_segundos in splits:
            minutos = int(media_segundos // 60)
            segundos = int(media_segundos % 60)
            tempo_formatado = f"{minutos:02d}:{segundos:02d}"
            print(f"{split:<6} | {tempo_formatado:>20}")
    
    except Exception as e:
        print(e)
   
    finally:
        cur.close()
        conexao.close()

#CONSULTA AVANÇADA 2: Personagens mais usados de cada rota
def personagemMaisUsadoRotas():
    conexao = conectar()
    cur = conexao.cursor()
    try:
        cur.execute("SELECT pos.nome AS rota, per.nome AS personagem, COUNT(*) AS vezes_usado FROM estatisticas e JOIN posicoes pos ON e.id_posicao = pos.id JOIN personagens per ON e.id_personagem = per.id GROUP BY pos.nome, per.nome ORDER BY pos.nome, vezes_usado DESC")
        for rota, personagem, vezes in cur.fetchall():
            print(f"{rota:<10} | {personagem:<20} | {vezes} usos")
    
    except Exception as e:
        print(e)
   
    finally:
        cur.close()
        conexao.close()


def consultar_media_tempo_partida_por_split():
    """
    Consulta a média de tempo das partidas, agrupando por nome e split do campeonato.
    Usa: JOIN, GROUP BY, AVG, CAST.
    """
    sql = """
        SELECT
            c.nome AS campeonato,
            c.split,
            TO_CHAR(AVG(CAST(p.duracao_partida AS INTERVAL)), 'HH24:MI:SS') AS media_duracao
        FROM partidas p
        JOIN campeonatos c ON p.id_campeonato = c.id
        GROUP BY c.nome, c.split
        ORDER BY c.nome, c.split;
    """
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()

                if not resultados:
                    print("\nNenhuma partida encontrada para calcular a média de tempo.")
                    return

                print("\n--- MÉDIA DE TEMPO DE PARTIDA POR SPLIT ---")
                print(f"{'Campeonato':<40} | {'Split':<10} | {'Duração Média':<20}")
                print("-" * 75)
                for campeonato, split, media_duracao in resultados:
                    print(f"{campeonato:<40} | {split:<10} | {media_duracao:<20}")

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def consultar_personagens_mais_usados_por_rota():
    """
    Mostra o personagem mais utilizado em cada uma das rotas (posições).
    Usa: JOIN, GROUP BY, COUNT e a função de janela ROW_NUMBER().
    """
    sql = """
        WITH ContagemPersonagens AS (
            SELECT
                pos.nome AS posicao,
                pers.nome AS personagem,
                COUNT(e.id) AS vezes_jogado,
                ROW_NUMBER() OVER(PARTITION BY pos.nome ORDER BY COUNT(e.id) DESC) as rn
            FROM estatisticas e
            JOIN personagens pers ON e.id_personagem = pers.id
            JOIN posicoes pos ON e.id_posicao = pos.id
            GROUP BY pos.nome, pers.nome
        )
        SELECT 
            posicao,
            personagem,
            vezes_jogado
        FROM ContagemPersonagens
        WHERE rn = 1
        ORDER BY posicao;
    """
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()

                if not resultados:
                    print("\nNenhuma estatística de personagem por rota encontrada.")
                    return

                print("\n--- PERSONAGEM MAIS USADO POR ROTA ---")
                print(f"{'Rota':<20} | {'Personagem':<25} | {'Vezes Jogadas':<15}")
                print("-" * 70)
                for rota, personagem, vezes_jogado in resultados:
                    print(f"{rota:<20} | {personagem:<25} | {vezes_jogado:<15}")

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def consultar_time_menor_media_partida():
    """
    Encontra o time com a menor média de tempo de partida geral.
    Usa: JOIN, GROUP BY, AVG, UNION ALL para unificar os times.
    """
    sql = """
        WITH TempoPorTime AS (
            SELECT id_time, AVG(CAST(duracao_partida AS INTERVAL)) as media_duracao
            FROM (
                SELECT id_time1 as id_time, duracao_partida FROM partidas
                UNION ALL
                SELECT id_time2 as id_time, duracao_partida FROM partidas
            ) AS participacoes
            GROUP BY id_time
        )
        SELECT 
            t.nome,
            TO_CHAR(tt.media_duracao, 'HH24:MI:SS') as media_formatada
        FROM TempoPorTime tt
        JOIN times t ON tt.id_time = t.id
        ORDER BY tt.media_duracao ASC
        LIMIT 1;
    """
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultado = cur.fetchone()

                if not resultado:
                    print("\nNão foi possível calcular a média de tempo dos times.")
                    return

                time, media_duracao = resultado
                print("\n--- TIME COM MENOR MÉDIA DE TEMPO DE PARTIDA ---")
                print(f"Time: {time}")
                print(f"Duração Média: {media_duracao}")

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def consultar_jogadores_media_assistencias_alta():
    """
    Lista todos os jogadores com uma média de assistências por partida maior que 5.
    Usa: JOIN, GROUP BY, AVG, HAVING.
    """
    sql = """
        SELECT
            j.nome,
            CAST(AVG(e.qntd_assistencias) AS DECIMAL(10, 2)) as media_assistencias
        FROM estatisticas e
        JOIN jogadores j ON e.id_jogador = j.id
        GROUP BY j.nome
        HAVING AVG(e.qntd_assistencias) > 5
        ORDER BY media_assistencias DESC;
    """
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()

                if not resultados:
                    print("\nNenhum jogador encontrado com média de assistências maior que 5.")
                    return

                print("\n--- JOGADORES COM MÉDIA DE ASSISTÊNCIAS > 5 ---")
                print(f"{'Jogador':<30} | {'Média de Assistências':<25}")
                print("-" * 60)
                for jogador, media in resultados:
                    print(f"{jogador:<30} | {media:<25}")

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def consultar_jogadores_mais_de_cem_abates():
    """
    Lista todos os jogadores que possuem mais de 100 abates no total.
    Usa: JOIN, GROUP BY, SUM, HAVING.
    """
    sql = """
        SELECT
            j.nome,
            SUM(e.qntd_abates) as total_abates
        FROM estatisticas e
        JOIN jogadores j ON e.id_jogador = j.id
        GROUP BY j.nome
        HAVING SUM(e.qntd_abates) > 100
        ORDER BY total_abates DESC;
    """
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                resultados = cur.fetchall()

                if not resultados:
                    print("\nNenhum jogador encontrado com mais de 100 abates no total.")
                    return

                print("\n--- JOGADORES COM MAIS DE 100 ABATES TOTAIS ---")
                print(f"{'Jogador':<30} | {'Total de Abates':<20}")
                print("-" * 55)
                for jogador, total_abates in resultados:
                    print(f"{jogador:<30} | {total_abates:<20}")

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
