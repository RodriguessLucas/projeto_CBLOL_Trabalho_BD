import psycopg2
from datetime import datetime, date


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




# FUNÇÕES AUXILIARES PARA VERIFICAR ENTRADAS E CONVERTER PARA O PADRAO DO POSTGRES
def verificarNome(nome:str):
    if not nome or not isinstance(nome,str):
        return False
    
    verificar = nome.replace(' ','').replace('-','').replace("'","")
    return verificar.isalnum()


def verificarEntradaData(data)->bool:
    if not data or not isinstance(data,str):
        return False

    try:
        datetime.strptime(data, '%d/%m/%Y')
        return True
    except ValueError:
        return False
    

def converterDataPostgresParaString(data_obj: date) -> str:
    if data_obj is None:
        return "não definido"
    if not isinstance(data_obj, (date, datetime)):
        raise TypeError("A data não é válida.")    
    return data_obj.strftime('%d/%m/%Y')
    

def converterStringParaData(data_str: str) -> date | None:
    try:
        return datetime.strptime(data_str, '%d/%m/%Y').date()
    except (ValueError, TypeError):
        return None

def verificarEntradaNacionalidade(nacionalidade):
    if not nacionalidade or not isinstance(nacionalidade,str):
        return False
    
    verificar = nacionalidade.replace(' ','').replace('-','').replace("'","")
    return verificar.isalnum()



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

    except Exception as e:
        print(e)
    finally:
        cur.close()
        conexao.close()


# FUNCÃO QUE ADICIONA DIRETO AO BANCO DE DADOS SEM O INPUT DADOS DO user 
def cadastrarJogador():
    nome = input("Digite o nome: ").strip()
    inicio_carreira = input("Digite a data que este jogador começou a atuar (DD/MM/AAAA): ").strip()
    nacionalidade = input("Digite a nacionalidade: ").strip()
    id_posicao = input("Digite o ID da posicao: ").strip()
    
    conexao = conectar()
    cur = conexao.cursor()
    try:    
        id_posicao = int(id_posicao)

        verificarNome(nome)
        if(verificarEntradaData(inicio_carreira)):
            inicio_carreira = converterStringParaData(inicio_carreira)

        verificarEntradaNacionalidade(nacionalidade)

        cur.execute(f"SELECT * FROM posicoes WHERE id = {id_posicao};")
        obterPosicao = cur.fetchone()
        print(obterPosicao)
        if(obterPosicao[0] == None) :
            raise ValueError("Posicao usada para cadastrar jogador é inválida!")
        
        cur.execute(
            "insert into jogadores( nome, data_inicio_carreira, nacionalidade,id_posicao) values (%s,%s,%s,%s)", 
            ( nome,inicio_carreira, nacionalidade,id_posicao))  
        conexao.commit()

        return f"Novo jogador adicionado! \nNome: {nome} - Nacionalidade: {nacionalidade} - Posição: {obterPosicao[1]} "
    
    except Exception as e :
        print(e)
    finally:  
        cur.close()
        conexao.close()



# FUNCAO PARA LISTAR TODOS OS JOGADORES CADASTRADOS 
def listarTodosJogadores():
    conexao = conectar()
    cur = conexao.cursor()
    try:
        cur.execute("SELECT id, nome, data_inicio_carreira, data_fim_carreira, nacionalidade, id_posicao FROM jogadores")
        jogadores = cur.fetchall()
        
        if not jogadores:
            return "Não há jogadores cadastrados no sistema!"

        resultado = f"{'ID':<4} | {'Nome':<25} | {'Início':<10} | {'Fim':<10} | {'Nacionalidade':<20} | {'Posição':<8}\n"
        resultado += "-" * 90 + "\n"
        
        for jogador in jogadores:
            id, nome, data_inicio, data_fim, nacionalidade, id_posicao = jogador
            data_fim_str = data_fim.strftime("%d/%m/%Y") if data_fim else "Ativo"
            resultado += f"{id:<4} | {nome:<25} | {data_inicio.strftime('%d/%m/%Y'):<10} | {data_fim_str:<10} | {nacionalidade:<20} | {id_posicao:<8}\n"
        
        return resultado
    
    finally:
        cur.close()
        conexao.close()


def buscrUmJogador():
    conexao = conectar()
    cur = conexao.cursor()

    try:
        id_jogador = int(input("Digite o ID do jogador que busca: ").strip())

        cur.execute(f"SELECT * FROM jogadores WHERE id = {id_jogador}")
        jogador = cur.fetchone()
        if(jogador[0] == None):
            raise ValueError("Jogador não encontrado no banco de dados")
        
        cur.execute(f"SELECT nome FROM posicoes WHERE id = {jogador[5]}")
        obterPosicao = cur.fetchone()
        
        mensagem = (f"Informações do jogador:\n" +
                    "ID:{jogador[0]} \nNome: {jogador[1]} \nInicio da carreira: {jogador[2]} \nFim de carreira: {jogador[3]}"+
                    "\nNacionalidade: {jogador[4]} \nPosição:{obterposicao[0]}"
                    )
        return mensagem  
    except Exception as e:
        print(e)

    finally:
        cur.close()
        conexao.close()


#Funcao que remove jogadores 
def Removerjogadores():
    id_str = input("Digite o id do jogador que sera removido: ").strip()
    conexao = conectar()
    cur = conexao.cursor()
    try:
        auxId= int(id_str)
        cur.execute("delete from jogadores where id =%s ",(auxId,))
        conexao.commit()
        if cur.rowcount > 0:
             print ("Jogador removido com sucesso")
        else:
            print("\tID invalido!\n\tVeja os IDs validos na lista de jogadores") 
    except ValueError:
        print("ID digitado não é um número válido!")
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conexao.close()


def atualizarDadosJogador():
    # Coleta de dados
    id_jogador = input("Digite o ID do jogador: ").strip()
    id_jogador = int(id_jogador) if id_jogador.isdigit() else None

    print("Digite os dados atualizados \nCASO NÃO QUEIRA ATUALIZAR APENAS DEIXE VAZIO")

    nome = input("Digite o novo nome: ").strip() or None
    inicio_carreira = input("Digite a nova data que este jogador começou a atuar (DD/MM/AAAA): ").strip() or None
    fim_carreira = input("Digite a nova data que este jogador se aposentou (DD/MM/AAAA): ").strip() or None
    nacionalidade = input("Digite a nova nacionalidade: ").strip() or None
    id_posicao = input("Digite o novo ID da posicao: ").strip()
    id_posicao = int(id_posicao) if id_posicao.isdigit() else None

    conexao = conectar()
    cur = conexao.cursor()
    
    try:
        # Verificações básicas
        if id_jogador is None:
            raise ValueError("ID do jogador inválido, insira o dado corretamente")

        # Verifica se jogador existe
        cur.execute("SELECT * FROM jogadores WHERE id = %s", (id_jogador,))
        jogador = cur.fetchone()
        if not jogador:
            raise ValueError("Jogador não encontrado!")

        # Validações dos dados
        if nome is not None:
            verificarNome(nome)
        
        if inicio_carreira is not None:
            if verificarEntradaData(inicio_carreira):
                inicio_carreira = converterStringParaData(inicio_carreira)
            else:
                inicio_carreira = None

        if fim_carreira is not None:
            if verificarEntradaData(fim_carreira):
                fim_carreira = converterStringParaData(fim_carreira)
            else:
                fim_carreira = None

        if nacionalidade is not None:
            verificarEntradaNacionalidade(nacionalidade)

        if id_posicao is not None:
            cur.execute("SELECT * FROM posicoes WHERE id = %s", (id_posicao,))
            obterPosicao = cur.fetchone()
            if not obterPosicao:
                raise ValueError("Posição usada para jogador é inválida!")
            nome_posicao = obterPosicao[1]
        else:
            # Se não foi informada nova posição, obtém a atual
            cur.execute("SELECT nome FROM posicoes WHERE id = %s", (jogador[5],))
            nome_posicao = cur.fetchone()[0]

        # Construção da query de atualização
        campos = []
        valores = []
        
        if nome is not None:
            campos.append("nome = %s")
            valores.append(nome)
            
        if inicio_carreira is not None:
            campos.append("data_inicio_carreira = %s")
            valores.append(inicio_carreira)
            
        if fim_carreira is not None:
            campos.append("data_fim_carreira = %s")
            valores.append(fim_carreira)
            
        if nacionalidade is not None:
            campos.append("nacionalidade = %s")
            valores.append(nacionalidade)
            
        if id_posicao is not None:
            campos.append("id_posicao = %s")
            valores.append(id_posicao)

        
        if campos:
            valores.append(id_jogador)
            query = f"UPDATE jogadores SET {', '.join(campos)} WHERE id = %s"
            cur.execute(query, valores)
            conexao.commit()
            
            # Obtém o nome do jogador atualizado (ou o antigo se não foi modificado)
            nome_exibicao = nome if nome is not None else jogador[1]
            nacionalidade_exibicao = nacionalidade if nacionalidade is not None else jogador[4]
            
            return (f"Jogador atualizado com sucesso!\n"
                    f"Nome: {nome_exibicao}\n"
                    f"Nacionalidade: {nacionalidade_exibicao}\n"
                    f"Posição: {nome_posicao}")
        else:
            return "Nenhum dado foi alterado."
            
    except Exception as e:
        conexao.rollback()
        return f"Erro ao atualizar jogador: {str(e)}"
    finally:
        cur.close()
        conexao.close()






# Funcao de aposentar jogadores no futuro tera um trigger para encerrar io contrato assim q o joagdor se aposentar
def Aposentarjogador():
   conexao = conectar()
   cur = conexao.cursor()
   id = input("Digte o id do jogador: ").strip()
   data_str = input("Digite a data de fim da carreira (DD/MM/AAAA ): ").strip()
   
   try:
     data_fim = datetime.strptime(data_str, "%d/%m/%Y").date()
     cur.execute("UPDATE jogadores SET data_fim_carreira = %s WHERE id = %s",(data_fim, int(id)) )
     conexao.commit()
   except ValueError:
       print("Erro: Data inválida. Use o formato DD/MM/AAAA.")
   except Exception as e:
    print(e)
   finally:
       cur.close()
       conexao.close()

# Funcao de atualizar contrato pode ser usada pra iniciar, terminar ou renovar um contrato
def Atualizarcontrato():
    conexao = conectar()
    cur = conexao.cursor()
    data_inicio_str = input("Data início (DD/MM/AAAA): ").strip()
    data_fim_str = input("Data fim (DD/MM/AAAA) : ").strip()
    id_time = int(input("ID do time: ").strip())
    id_jogador = int(input("ID do jogador: ").strip())
    data_inicio = datetime.strptime(data_inicio_str, "%d/%m/%Y").date()
    data_fim = datetime.strptime(data_fim_str, "%d/%m/%Y").date()
    try:
        cur.execute(" INSERT INTO contratos (data_inicio, data_fim, id_time, id_jogador) VALUES (%s, %s, %s, %s)", (data_inicio, data_fim, id_time, id_jogador))
        conexao.commit()
        print("Contrato adicionado com sucesso!")
    except Exception as e:
        print("Erro ao adicionar contrato:", e)
    finally:
        cur.close()
        conexao.close()

# Funcao de adicionar um time
def Adicionartime():
    conexao = conectar()
    cur = conexao.cursor()
    nome = input("Nome do time: ").strip()
    sigla = input("Sigla (3 caracteres): ").strip().upper()
    data_fundacao_str = input("Data de fundação (DD/MM/AAAA): ").strip()
    data_fundacao = datetime.strptime(data_fundacao_str, "%d/%m/%Y").date()
    nacionalidade = input("Nacionalidade: ").strip()
    if len(sigla) != 3:
            print("Erro: A sigla deve ter exatamente 3 caracteres.")
            return
    try:
        cur.execute("INSERT INTO times (nome, sigla, data_fundacao, nacionalidade) VALUES (%s, %s, %s, %s)", (nome, sigla, data_fundacao, nacionalidade))
        conexao.commit()
        print("Time adicionado com sucesso!.")
    except ValueError:
        print("Erro: Data inválida. Use o formato DD/MM/AAAA.")
    except Exception as e:
        print("Erro ao adicionar time:", e)
    finally:
        cur.close()
        conexao.close()

# Funcao de exibir os times
def Exibirtimes():
    conexao = conectar()
    cur = conexao.cursor()
    try:
        cur.execute("SELECT id, nome, sigla, data_fundacao, nacionalidade FROM times ORDER BY id")
        times = cur.fetchall()
        if not times:
            print("Nenhum time cadastrado.")
            return
        print(f"{'ID':<4} | {'Nome':<25} | {'Sigla':<5} | {'Fundação':<10} | {'Nacionalidade':<20}")
        print("-" * 75)
        for t in times:
            id, nome, sigla, data_fundacao, nacionalidade = t
            print(f"{id:<4} | {nome:<25} | {sigla:<5} | {data_fundacao.strftime('%d/%m/%Y'):<10} | {nacionalidade:<20}")
    except Exception as e :
        print(e)
    finally:
        cur.close()
        conexao.close()


  









