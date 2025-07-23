import psycopg2
from datetime import datetime
DB_CONFIG = {
    "dbname": "banco_cblol",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}


SQL_CRIAR_TABELAS = """
    CREATE TABLE IF NOT EXISTS posicoes(
        id SERIAL PRIMARY KEY,
        nome VARCHAR(100) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS personagens(
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
            FOREIGN KEY (id_posicao)
            REFERENCES posicoes(id)

    );

    CREATE TABLE IF NOT EXISTS contratos(
        id SERIAL PRIMARY KEY,
        data_inicio DATE NOT NULL,
        data_fim DATE,
        id_time INTEGER NOT NULL,
        id_jogador INTEGER NOT NULL,

        CONSTRAINT fk_id_time_contrato_jogador
            FOREIGN KEY (id_time)
            REFERENCES times(id),

        CONSTRAINT fk_id_jogador_contrato
            FOREIGN KEY (id_jogador)
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
            FOREIGN KEY (id_campeonato)
            REFERENCES campeonatos(id),

        CONSTRAINT fk_id_time1_partida
            FOREIGN KEY (id_time1)
            REFERENCES times(id),

        CONSTRAINT fk_id_time2_partida
            FOREIGN KEY (id_time2)
            REFERENCES times(id)
    );

    CREATE TABLE IF NOT EXISTS estatisticas(
        id SERIAL PRIMARY KEY,
        qntd_abates INTEGER NOT NULL,
        qntd_mortes INTEGER NOT NULL,
        qntd_assistencias INTEGER NOT NULL,
        lado_mapa VARCHAR(8) NOT NULL,
        id_partida INTEGER NOT NULL,
        id_jogador INTEGER NOT NULL,
        id_posicao INTEGER NOT NULL,
        id_personagem INTEGER NOT NULL,

        CONSTRAINT fk_id_partida_estatistica
            FOREIGN KEY(id_partida)
            REFERENCES partidas(id),

        CONSTRAINT fk_id_jogador_estatistica
            FOREIGN KEY (id_jogador)
            REFERENCES jogadores(id),
        
        CONSTRAINT fk_id_posicao_estatistica
            FOREIGN KEY (id_posicao)
            REFERENCES posicoes(id),

        CONSTRAINT fk_id_personagem_estatistica
            FOREIGN KEY( id_personagem)
            REFERENCES personagens(id)
    );

"""

def conectar():
    try:
        conexao = psycopg2.connect(**DB_CONFIG)
        CONEXAO = conexao
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


# AQUI EM DIANTE SÓ SÃO FUNCOES PARA ULTILIZAR OS DADOS NO POSTGRES
# Fiz uma alteracao no loop de criar posicoes pq não estava funcionando 
def cadastrarPosicoes():
    try:
        conexao = conectar()
        cur = conexao.cursor()

        nomes= ["TOPO","MEIO","CAÇADOR","ATIRADOR","SUPORTE"]
        for nome in nomes:
            cur.execute("INSERT INTO posicoes(nome) VALUES(%s)", (nome,))
            conexao.commit()

        cur.close()
        conexao.close
    except Exception as e:
        print(e)


# FUNCÃO QUE ADICIONA DIRETO AO BANDO DE DADOS SEM O INPUT DADOS DO 
# Não passeia data 
def Adcplyr(nome,inicio_carreira,fim_carreira,nacionalidade,id_posicao):
    conexao = conectar()
    cur = conexao.cursor()
    try:
        cur.execute("insert into jogadores( nome, data_inicio_carreira,data_fim_carreira, nacionalidade,id_posicao) values (%s,%s,%s,%s,%s)", ( nome,inicio_carreira,fim_carreira, nacionalidade,id_posicao))
        conexao.commit()
        cur.close()
        print("jogador adicionado")
    except Exception as e :
        print(e)
    finally:  
     conexao.close()

#Adiciona um jogador com input de dados do user

def Adicionarjogadores():
    try:
     nome = input("Digite o nome: ")
     data_ini = input("Digite a data que este jogador começou a atuar (DD/MM/AAAA): ")
     data_fim = input("Digite a data de fim da carreira (DD/MM/AAAA ou deixe em branco se ainda estiver ativo): ")
     nacionalidade = input("Digite a nacionalidade: ")
#logo logo adicionarei pelo nome da posicao e nao pelo id
     posicao = input("Digite o ID da posicao: ")
     data_fim = datetime.strptime(data_fim,"%d/%m/%Y").date()if data_fim else None
     datainic = datetime.strptime(data_ini,"%d/%m/%Y").date()
     Adcplyr(nome,datainic,data_fim,nacionalidade,posicao)
    except Exception as e :
        print (e)

# Função para exibir a lista de jogadores

def Mostrarjogadores():
    conexao = conectar()
    cur = conexao.cursor()
    try:
        cur.execute("select id, nome, data_inicio_carreira, data_fim_carreira, nacionalidade, id_posicao from jogadores")
        jogadores = cur.fetchall()
        for jogador in jogadores:
            id_, nome, data_inicio, data_fim, nacionalidade, id_posicao = jogador
            data_fim_str = data_fim.strftime("%d/%m/%Y") if data_fim else "Ativo"
            print(f"ID: {id_} | Nome: {nome} | Início: {data_inicio.strftime('%d/%m/%Y')} | Fim: {data_fim_str} | Nacionalidade: {nacionalidade} | Posição ID: {id_posicao}")
        cur.close()
    finally:
        conexao.close()


#cadastrarPosicoes()
#("joseval","2025-07-22","brasileira",2)
#Adicionarjogadores()
Mostrarjogadores()
