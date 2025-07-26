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
