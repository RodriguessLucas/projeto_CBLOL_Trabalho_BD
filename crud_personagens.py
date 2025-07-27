# crud_personagens.py
from database import conectar
from utilidades import is_string_valida


def cadastrar_campeoes():
    try:
        conexao = conectar()
        cur = conexao.cursor()

        campeoes_lol = ['Aatrox', 'Ahri', 'Akali', 'Akshan', 'Alistar', 'Amumu', 'Anivia', 'Annie', 
                        'Aphelios', 'Ashe', 'AurelionSol', 'Aurora', 'Azir', 'Bard', 'Belveth', 'Blitzcrank', 
                        'Brand', 'Braum', 'Briar', 'Caitlyn', 'Camille', 'Cassiopeia', 'Chogath', 'Corki', 
                        'Darius', 'Diana', 'Draven', 'DrMundo', 'Ekko', 'Elise', 'Evelynn', 'Ezreal', 
                        'Fiddlesticks', 'Fiora', 'Fizz', 'Galio', 'Gangplank', 'Garen', 'Gnar', 'Gragas', 
                        'Graves', 'Gwen', 'Hecarim', 'Heimerdinger', 'Hwei', 'Illaoi', 'Irelia', 'Ivern', 
                        'Janna', 'JarvanIV', 'Jax', 'Jayce', 'Jhin', 'Jinx', 'Kaisa', 'Kalista', 'Karma', 
                        'Karthus', 'Kassadin', 'Katarina', 'Kayle', 'Kayn', 'Kennen', 'Khazix', 'Kindred',
                          'Kled', 'KogMaw', 'KSante', 'LeBlanc', 'LeeSin', 'Leona', 'Lillia', 'Lissandra', 
                          'Lucian', 'Lulu', 'Lux', 'Malphite', 'Malzahar', 'Maokai', 'MasterYi', 'Milio', 
                          'MissFortune', 'Mordekaiser', 'Morgana', 'Naafiri', 'Nami', 'Nasus', 'Nautilus', 
                          'Neeko', 'Nidalee', 'Nilah', 'Nocturne', 'Nunu', 'Olaf', 'Orianna', 'Ornn', 'Pantheon', 
                          'Poppy', 'Pyke', 'Qiyana', 'Quinn', 'Rakan', 'Rammus', 'RekSai', 'Rell', 'Renata', 
                          'Renekton', 'Rengar', 'Riven', 'Rumble', 'Ryze', 'Samira', 'Sejuani', 'Senna', 
                          'Seraphine', 'Sett', 'Shaco', 'Shen', 'Shyvana', 'Singed', 'Sion', 'Sivir', 
                          'Skarner', 'Smolder', 'Sona', 'Soraka', 'Swain', 'Sylas', 'Syndra', 'TahmKench', 
                          'Taliyah', 'Talon', 'Taric', 'Teemo', 'Thresh', 'Tristana', 'Trundle', 'Tryndamere', 
                          'TwistedFate', 'Twitch', 'Udyr', 'Urgot', 'Varus', 'Vayne', 'Veigar', 'Velkoz', 'Vex', 
                          'Vi', 'Viego', 'Viktor', 'Vladimir', 'Volibear', 'Warwick', 'Wukong', 'Xayah', 'Xerath', 
                          'XinZhao', 'Yasuo', 'Yone', 'Yorick', 'Yuumi', 'Zac', 'Zed', 'Zeri', 'Ziggs', 'Zilean', 
                          'Zoe', 'Zyra']
        

        for nome in campeoes_lol:
            cur.execute("INSERT INTO posicoes(nome) VALUES(%s)", (nome,))
            conexao.commit()

    except Exception as e:
        print(e)
    finally:
        cur.close()
        conexao.close()


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