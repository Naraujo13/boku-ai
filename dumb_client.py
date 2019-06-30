import urllib.request
import sys
import random
import time
from heapq import heappush, heappop

# Get a fixed-size list of neighbors: [top, top-right, top-left, down, down-right, down-left].
# None at any of those places where there's no neighbor
def neighbors(column, line, board):
  l = []

  if line > 1:
      l.append((column, line - 1))  # up
  else:
      l.append(None)

  if (column < 6 or line > 1) and (column < len(board)):
      if column >= 6:
          l.append((column + 1, line - 1))  # upper right
      else:
          l.append((column + 1, line))  # upper right
  else:
      l.append(None)

  if (column > 6 or line > 1) and (column > 1):
      if column > 6:
          l.append((column - 1, line))  # upper left
      else:
          l.append((column - 1, line - 1))  # upper left
  else:
      l.append(None)

  if line < len(board[column - 1]):
      l.append((column, line + 1))  # down
  else:
      l.append(None)

  if (column < 6 or line < len(board[column - 1])) and column < len(board):
      if column < 6:
          l.append((column + 1, line + 1))  # down right
      else:
          l.append((column + 1, line))  # down right
  else:
      l.append(None)

  if (column > 6 or line < len(board[column - 1])) and column > 1:
      if column > 6:
          l.append((column - 1, line + 1))  # down left
      else:
          l.append((column - 1, line))  # down left
  else:
      l.append(None)

  return l

def pick_move(tabuleiro, movimentos):

  # Fila de Prioridade com movimentos ordenados por peso
  evaluated_moves = []

  # Para cada movimento possivel
  for move in movimentos:
    # Pega coordenadas do movimento
    move_x, move_y = move[0], move[1]

    # Cria variável para o score do movimento
    score = 0

    # Busca lista de vizinhos
    neighbors_list = neighbors(move_x, move_y, tabuleiro)

    # Para cada vizinho
    for neighbor in neighbors_list:
      if neighbor != None:
        # Pega a posição do tabuleiro do vizinho
        neighbor_x, neighbor_y = neighbor[0], neighbor[1]
        pos = tabuleiro[neighbor_x][neighbor_y]
        # Se é do mesmo jogador
        if (pos == player):
          score += 2
        # Se é em branco
        elif (pos == 0):
          score += 1
          # TODO: add more logic here to see sequences of whitespaces
        # Se é do outro jogador
        else:
          # TODO: REVIEW THIS LOGIC
          score -= 1
    item = (score, move)
    heappush(evaluated_moves, item)

  move = heappop(evaluated_moves)
  return move


if len(sys.argv)==1:
    print("Voce deve especificar o numero do jogador (1 ou 2)\n\nExemplo:    ./random_client.py 1")
    quit()

# Alterar se utilizar outro host
host = "http://localhost:8080"

player = int(sys.argv[1])

# Reinicia o tabuleiro
resp = urllib.request.urlopen("%s/reiniciar" % host)

done = False
while not done:
    # Pergunta quem eh o jogador
    resp = urllib.request.urlopen("%s/jogador" % host)
    player_turn = int(resp.read())

    # Se jogador == 0, o jogo acabou e o cliente perdeu
    if player_turn==0:
        print("I lose.")
        done = True

    # Se for a vez do jogador
    if player_turn==player:
        # Pega o tabuleiro atual
        resp = urllib.request.urlopen("%s/tabuleiro" % host)
        tabuleiro = eval(resp.read())

        # Pega os movimentos possiveis
        resp = urllib.request.urlopen("%s/movimentos" % host)
        movimentos = eval(resp.read())

        # Escolhe um movimento aleatoriamente
        # movimento = random.choice(movimentos)
        movimento = pick_move(tabuleiro, movimentos)

        # Executa o movimento
        resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[0],movimento[1]))
        msg = eval(resp.read())

        # Se com o movimento o jogo acabou, o cliente venceu
        if msg[0]==0:
            print("I win")
            done = True
        if msg[0]<0:
            raise Exception(msg[1])

    # Descansa um pouco para nao inundar o servidor com requisicoes
    time.sleep(1)

# def direction(move, neighbor, board):
#   column, line = move[0], move[1]
#   # UP
#   if line > 1 and (column, line - 1) == (neighbor):  # up
#     return 'up'
#   # UPPER RIGHT
#   elif (column < 6) and (column + 1, line - 1) == neighbor:
#     return 'upper_right'
#   elif (line > 1 and column >= 6) and (column + 1, line - 1) == neighbor:  # upper right
#     return 'upper_right'
#   # UPPER LEFT
#   elif (column > 6) and (column - 1, line) == neighbor:
#     return 'upper_left'
#   elif (column > 1) and (column <= 6) and (column - 1, line - 1) == neighbor
#     return 'upper_left'
#   # DOWN
#   elif (column, line + 1) == neighbor:
#     return 'down'
#   # DOWN RIGHT
#   elif column < 6 and (column + 1, line + 1) == neighbor:
#     return 'down_right'
#   elif column <= 6  and line < len(board[column - 1]) and (column + 1, line) == neighbor:
#     return 'down_right'
#   # DOWN LEFT
#   elif column > 6 and (column - 1, line + 1) == neighbor:
#     return 'down_left'
#   elif column <= 6 and line < len(board[column - 1]) and (column - 1, line) == neighbor:
#     return 'down_left'
#   else:
#     return None




