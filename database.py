import psycopg2

DB_CONFIG = {
    "dbname": "banco_cblol",
    "user": "postgres",
    "password": "postgres2025",
    "host": "localhost",
    "port": "5432"
}


SQL_CRIAR_TABELAS = """
    CREATE TABLE IF NOT EXISTS posicoes(
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS campeoes(
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS times(
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL,
        sigla VARCHAR(3) NOT NULL,
        data_fundacao DATE NOT NULL,
        nacionalidade VARCHAR(100) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS campeonatos(
        id SERIAL PRIMARY KEY,
        nome VARCHAR(150) NOT NULL,
        ano CHAR(4) NOT NULL,
        pais_ocorrencia VARCHAR(100) NOT NULL,
        split CHAR(1) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS jogadores(
        id SERIAL PRIMARY KEY,
        nome VARCHAR(150) NOT NULL,
        data_inicio_carreira DATE NOT NULL,
        data_fim_carreira DATE,
        nacionalidade VARCHAR(100) NOT NULL,
        id_posicao INTEGER NOT NULL,

        CONSTRAINT fk_id_posicao_jogador
            FOREIGN KEY(id_posicao)
            REFERENCES posicoes(id)

    );

    CREATE TABLE IF NOT EXISTS contratos(
        id SERIAL PRIMARY KEY,
        data_inicio DATE NOT NULL,
        data_fim DATE,
        id_time INTEGER NOT NULL,
        id_jogador INTEGER NOT NULL,

        CONSTRAINT fk_id_time_contrato_jogador
            FOREIGN KEY(id_time)
            REFERENCES times(id),

        CONSTRAINT fk_id_jogador_contrato
            FOREIGN KEY(id_jogador)
            REFERENCES jogadores(id)
    );

    CREATE TABLE IF NOT EXISTS partidas(
        id SERIAL PRIMARY KEY,
        duracao_partida CHAR(8) NOT NULL,
        id_campeonato INTEGER NOT NULL,
        id_time1 INTEGER NOT NULL,
        id_time2 INTEGER NOT NULL,
        id_time_vencedor INTEGER NOT NULL,

        CONSTRAINT fk_id_campeonato_partida
            FOREIGN KEY(id_campeonato)
            REFERENCES campeonatos(id),

        CONSTRAINT fk_id_time1_partida
            FOREIGN KEY(id_time1)
            REFERENCES times(id),

        CONSTRAINT fk_id_time2_partida
            FOREIGN KEY(id_time2)
            REFERENCES times(id)
    );

    CREATE TABLE IF NOT EXISTS estatisticas(
        id SERIAL PRIMARY KEY,
        qntd_abates INTEGER NOT NULL,
        qntd_mortes INTEGER NOT NULL,
        qntd_assistencias INTEGER NOT NULL,
        lado_mapa VARCHAR(8) NOT NULL
        id_partida INTEGER NOT NULL,
        id_jogador INTEGER NOT NULL
        id_posicao INTEGER NOT NULL,
        id_personagem INTERGER NOT NULL,

        CONSTRAINT fk_id_partida_estatistica
            FOREIGN KEY(id_partida)
            REFERENCES partidas(id),

        CONSTRAINT fk_id_jogador_estatistica
            FOREIGN KEY(id_jogador)
            REFERENCES jogadores(id),
        
        CONSTRAINT fk_id_posicao_estatistica
            FOREIGN KEY(id_posicao)
            REFERENCES posicoes(id),

        CONSTRAINT fk_id_personagem_estatistica
            FOREIGN KEY(id_personagem)
            REFERENCES personagens(id),
    );

"""

def conectar():
    try:
        conexao = psycopg2.connect(**DB_CONFIG)
        return conexao
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None
    

def criar_tabelas():
    print("Verificando e criando tabelas...")
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute(SQL_CRIAR_TABELAS)
        print("Tabelas prontas para uso.")
    except Exception as e:
        print(f"Ocorreu um erro ao criar as tabelas: {e}")


