# main.py
import database
from crud_jogadores import listar_todos_jogadores, buscar_um_jogador, cadastrar_jogador, remover_jogador
from crud_times import listar_times, adicionar_time, atualizar_time, remover_time
from crud_contratos import adicionar_contrato, listar_contratos, atualizar_data_fim_contrato, remover_contrato
from crud_campeonatos import adicionar_campeonato, listar_campeonatos
from crud_personagens import adicionar_personagem, listar_personagens
from crud_partidas import adicionar_partida, listar_partidas
from crud_estatisticas import adicionar_estatistica, listar_estatisticas_por_partida

from consultas import (
    consultar_media_tempo_partida_por_split,
    consultar_personagens_mais_usados_por_rota,
    consultar_time_menor_media_partida,
    consultar_jogadores_media_assistencias_alta,
    consultar_jogadores_mais_de_cem_abates
)

def menu_consultas():
    """Exibe o submenu de consultas avançadas."""
    while True:
        print("\n--- MENU DE CONSULTAS AVANÇADAS ---")
        print("1. Ver média de tempo de partida por split")
        print("2. Ver personagens mais usados por rota")
        print("3. Ver time com menor média de tempo de partida")
        print("4. Ver jogadores com média de assistências > 5")
        print("5. Ver jogadores com mais de 100 abates no total")
        print("0. Voltar ao Menu Principal")

        opcao = input("Escolha uma opção de consulta: ").strip()

        if opcao == '1':
            consultar_media_tempo_partida_por_split()
        elif opcao == '2':
            consultar_personagens_mais_usados_por_rota()
        elif opcao == '3':
            consultar_time_menor_media_partida()
        elif opcao == '4':
            consultar_jogadores_media_assistencias_alta()
        elif opcao == '5':
            consultar_jogadores_mais_de_cem_abates()
        elif opcao == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")
        


def menu_Crud_jogadores():
    print("\n[Gerenciamento de Jogadores]")
    print("1. Listar todos os jogadores")
    print("2. Buscar um jogador por ID")
    print("3. Cadastrar novo jogador")
    print("4. Remover jogador")
    print("0. Voltar")

    opcao = input("Escolha uma opção: ").strip()
    # CRUD Jogadores

    if opcao == '1': listar_todos_jogadores()
    elif opcao == '2': buscar_um_jogador()
    elif opcao == '3': cadastrar_jogador()
    elif opcao == '4': remover_jogador()
    elif opcao == '0': return
    else:
            print("Opção inválida. Tente novamente.")

def menu_crud_times():

    print("\n[Gerenciamento de times]")
    print("1. Listar todos os times")
    print("2. Buscar um time por ID")
    print("3. Cadastrar novo time")
    print("4. Remover time")
    print("0. Voltar")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == '1': listar_times()
    elif opcao == '2': adicionar_time()
    elif opcao == '3': atualizar_time()
    elif opcao == '4': remover_time()
    elif opcao == '0': return
    else:
            print("Opção inválida. Tente novamente.")


def menu_crud_contratos():
    print("\n[Gerenciamento de Contratos]")
    print("1. Listar todos os contratos")
    print("2. Adicionar novo contrato")
    print("3. Atualizar data de fim de um contrato")
    print("4. Remover contrato")
    print("0. Voltar")

    opcao = input("Escolha uma opção: ").strip()

    
    if opcao == '1': listar_contratos()
    elif opcao == '2': adicionar_contrato()
    elif opcao == '3': atualizar_data_fim_contrato()
    elif opcao == '4': remover_contrato()
    elif opcao == '0': return
    else:
            print("Opção inválida. Tente novamente.")

def menu_crud_dados_geral():
    print("\n[Gerenciamento de Dados Gerais]")
    print("1. Listar Campeonatos")
    print("2. Adicionar Campeonato")
    print("3. Listar Personagens")
    print("4. Adicionar Personagem")
    print("5. Listar Partidas")
    print("6. Adicionar Partida")
    print("7. Listar Estatísticas de uma Partida")
    print("8. Adicionar Estatística de uma Partida")
    print("0. Voltar")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == '1': listar_campeonatos()
    elif opcao == '2': adicionar_campeonato()
    elif opcao == '3': listar_personagens()
    elif opcao == '4': adicionar_personagem()
    elif opcao == '5': listar_partidas()
    elif opcao == '6': adicionar_partida()
    elif opcao == '7': listar_estatisticas_por_partida()
    elif opcao == '8': adicionar_estatistica()
    elif opcao == '0': return
    else:
            print("Opção inválida. Tente novamente.")



def menu_principal():
    """Exibe o menu principal e gerencia a navegação do usuário."""
    
    database.criar_tabelas()
    database.cadastrar_posicoes_iniciais()

    while True:
        print("\n" + "="*20 + " MENU PRINCIPAL " + "="*20)
        


        print("1. [Gerenciamento de Jogadores]")
        print("2. [Gerenciamento de Contratos]")
        print("3. [Gerenciamento de times]")
        print("4. [Gerenciamento de Dados Gerais]")
        print("\n[Análise e Relatórios]")
        print("5. Acessar Consultas Avançadas")
        
        print("\n[Sistema]")
        print("0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        # CRUD Times
        if opcao == '1': menu_Crud_jogadores()
        elif opcao == '2': menu_crud_contratos()
        elif opcao == '3': menu_crud_times()
        elif opcao == '4': menu_crud_dados_geral()


        # Consultas
        elif opcao == '5': menu_consultas()
        # Sistema
        elif opcao == '0':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu_principal()