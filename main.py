
# aqui é so a importacao de todos os métodos que temos no database.py
# signica que vc pode so chaamr o método e passar as variaveis, tipo em java
from database import * 
from consultas import *

def main():
    print("Oi")
    conectar()
    criar_tabelas()
    cadastrarPosicoes()


    cadastrarJogador()


main()




