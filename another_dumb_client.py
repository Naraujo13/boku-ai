import urllib.request
import sys
import random
import time
from math import inf
import copy
from functools import lru_cache

# ---------------------------- Server methods ---------------------------------

# Returns a list of positions available on a board
def get_available_moves(board, player, forbidden_move):
    l = []

    for column in range(len(board)):
        for line in range(len(board[column])):
            if board[column][line] == 0:
                if not ((column + 1, line + 1) in forbidden_move):
                    l.append((column + 1, line + 1))
    return l

# Check if a board is in an end-game state. Returns the winning player or None.
def is_final_state(board):
    # test vertical
    for column in range(len(board)):
        s = ""
        for line in range(len(board[column])):
            state = board[column][line]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2

    # test upward diagonals
    diags = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
                (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2
            coords = neighbors(board, column, line)[1]

    # test downward diagonals
    diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    for column_0, line_0 in diags:
        s = ""
        coords = (column_0, line_0)
        while coords != None:
            column = coords[0]
            line = coords[1]
            state = board[column - 1][line - 1]
            s += str(state)
            if "11111" in s:
                return 1
            if "22222" in s:
                return 2
            coords = neighbors(board, column, line)[4]

    return None


# Get a fixed-size list of neighbors: [top, top-right, top-left, down, down-right, down-left].
# None at any of those places where there's no neighbor
def neighbors(board, column, line):
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

# ---------------------------------------------------

# ---------------- Aux Methods ----------------

def get_board():
    return [
        (1,1), (1,2), (1,3), (1,4), (1,5),
        (2,1), (2,2), (2,3), (2,4), (2,5), (2,6),
        (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7),
        (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8),
        (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7), (5,8), (5,9),
        (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7), (6,8), (6,9), (6,10),
        (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (7,8), (7,9),
        (8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8),
        (9,1), (9,2), (9,3), (9,4), (9,5), (9,6), (9,7),
        (10,1), (10,2), (10,3), (10,4), (10,5), (10,6),
        (11,1), (11,2), (11,3), (11,4), (11,5)
    ]

# Função que diz o que tem nas diagonais e seus pontos
def diagonals(board_inicial, ponto_inicial, board):

    # print('Ponto Atual')
    # print(ponto_inicial)
    # Conteúdo das diagonais
    # superior_esquerda = []
    superior_direita = [board[ponto_inicial[0] -1][ponto_inicial[1] - 1]]
    # inferior_esquerda = []
    inferior_direita = [board[ponto_inicial[0] -1][ponto_inicial[1] - 1]]
    # Pontos das diagonais
    # pontos_superior_esquerda = []
    # pontos_superior_direita = []
    # pontos_inferior_esquerda = []
    # pontos_inferior_direita = []

    # valid = True
    # ponto_atual = ponto_inicial
    # # Diagonal superior esquerda
    # while valid:
    #     # Se está no meio do tabuleiro ou na esquerda
    #     if ponto_atual[0] == 6 or ponto_atual[0] < 6:
    #         ponto_atual = (ponto_atual[0] - 1, ponto_atual[1] -1)
    #         if not ponto_atual in board_inicial:
    #             valid = False
    #         else:
    #             superior_esquerda.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
    #             pontos_superior_esquerda.append(ponto_atual)
    #     # Se está na direita do tabuleiro
    #     elif ponto_atual[0] > 6:
    #         ponto_atual = (ponto_atual[0] - 1, ponto_atual[1])
    #         if not ponto_atual in board_inicial:
    #             valid = False
    #         else:
    #             superior_esquerda.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
    #             pontos_superior_esquerda.append(ponto_atual)

    valid = True
    ponto_atual = ponto_inicial
    # Diagonal superior direita
    while valid:
        # Se está no meio do tabuleiro ou na direita
        if ponto_atual[0] == 6 or ponto_atual[0] > 6:
            ponto_atual = (ponto_atual[0] + 1, ponto_atual[1] -1)
            if not ponto_atual in board_inicial:
                valid = False
            else:
                superior_direita.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                # pontos_superior_direita.append(ponto_atual)
        # Se está na esquerda do tabuleiro
        elif ponto_atual[0] < 6:
            ponto_atual = (ponto_atual[0] + 1, ponto_atual[1])
            if not ponto_atual in board_inicial:
                valid = False
            else:
                superior_direita.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                # pontos_superior_direita.append(ponto_atual)

    # valid = True
    # ponto_atual = ponto_inicial
    # # Diagonal inferior esquerda
    # while valid:
    #     # Se está no meio do tabuleiro ou na esquerda
    #     if ponto_atual[0] == 6 or ponto_atual[0] < 6:
    #         ponto_atual = (ponto_atual[0] - 1, ponto_atual[1])
    #         if not ponto_atual in board_inicial:
    #             valid = False
    #         else:
    #             inferior_esquerda.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
    #             pontos_inferior_esquerda.append(ponto_atual)
    #     # Se está na direita do tabuleiro
    #     elif ponto_atual[0] > 6:
    #         ponto_atual = (ponto_atual[0] - 1, ponto_atual[1] + 1)
    #         if not ponto_atual in board_inicial:
    #             valid = False
    #         else:
    #             inferior_esquerda.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
    #             pontos_inferior_esquerda.append(ponto_atual)

    valid = True
    ponto_atual = ponto_inicial
    # Diagonal inferior direita
    while valid:
        # Se está no meio do tabuleiro ou na direita
        if ponto_atual[0] == 6 or ponto_atual[0] > 6:
            ponto_atual = (ponto_atual[0] + 1, ponto_atual[1])
            if not ponto_atual in board_inicial:
                valid = False
            else:
                inferior_direita.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                # pontos_inferior_direita.append(ponto_atual)
        # Se está na esquerda do tabuleiro
        elif ponto_atual[0] < 6:
            ponto_atual = (ponto_atual[0] + 1, ponto_atual[1] + 1)
            if not ponto_atual in board_inicial:
                valid = False
            else:
                inferior_direita.append(board[ponto_atual[0] -1][ponto_atual[1] - 1])
                # pontos_inferior_direita.append(ponto_atual)

    # print('Superior Esquerda: ')
    # print('\t Conteúdo: ' + str(superior_esquerda))
    # print('\t Pontos: ' + str(pontos_superior_esquerda))
    # print('Superior Direita: ')
    # print('\t Conteúdo: ' + str(superior_direita))
    # print('\t Pontos: ' + str(pontos_superior_direita))
    # print('Inferior Esquerda: ')
    # print('\t Conteúdo: ' + str(inferior_esquerda))
    # print('\t Pontos: ' + str(pontos_inferior_esquerda))
    # print('Inferior Direita: ')
    # print('\t Conteúdo: ' + str(inferior_direita))
    # print('\t Pontos: ' + str(pontos_inferior_direita))
    return [
            # superior_esquerda,
           superior_direita,
            #  inferior_esquerda,
           inferior_direita]

def board_to_tuple(board):
  tuples = list()
  for column in board:
    tuples.append(tuple(column))
  return tuple(tuples)

def tuples_to_board(tuples):
  board = list()
  for t in tuples:
    board.append(list(t))
  return board

# ------------- Métodos de tomada de decisão ----------
# num_h = 0
# Função de heurística básica
# @lru_cache(maxsize=131072)
def heuristic(board, player, debug = False):
    board = tuples_to_board(board)

    # global num_h
    # num_h += 1
    # print("Num: " + str(num_h))
    # Score hashes
    player_1 ={
      1: [],
      2: [],
      3: [],
      4: [],
      5: []
    }

    player_2 ={
      1: [],
      2: [],
      3: [],
      4: [],
      5: []
    }


    # ---- Verifica vertical
    for col in range(0, len(board)):
      # ---- Player 1
      # Se a coluna possui alguma peça da sua cor
      if board[col].count(1) > 0:
        # Percorre a coluna
        current = None
        seq_size = 0
        for point in range(0, len(board[col])):
          # Updates previous and current
          previous = current
          current = board[col][point]
          # Ao detectar uma peça do jogador
          if current == 1:
            # Soma um no tamanho da sequência
            seq_size += 1
  	        # Se é o primeiro ponto da sequência, inicializa início
            if previous != 1:
              # Inicializa ponto de início da sequência
              if point - 1 >= 0:
                start = board[col][point - 1]
              else:
                start = 2
          # Ao detectar uma peça que não é do jogador
          else:
            # Define variável end do final da sequencia\
            end = current
            # Salva sequencia se ela existir
            if seq_size > 0:
              # Adiciona no dict de score
              player_1[seq_size].append({
                'start': start,
                'end': end
              })
              # Zera seq_size
              seq_size = 0

      # ---- Player 2
      # Se a coluna possui alguma peça da sua cor
      if board[col].count(2) > 0:
        # Percorre a coluna
        current = None
        seq_size = 0
        for point in range(0, len(board[col])):
          # Updates previous and current
          previous = current
          current = board[col][point]
          # Ao detectar uma peça do jogador
          if current == 2:
            # Soma um no tamanho da sequência
            seq_size += 1
  	        # Se é o primeiro ponto da sequência, inicializa início
            if previous != 2:
              # Inicializa ponto de início da sequência
              if point - 1 >= 0:
                start = board[col][point - 1]
              else:
                start = 1
          # Ao detectar uma peça que não é do jogador
          else:
            # Define variável end do final da sequencia\
            end = current
            # Salva sequencia se ela existir
            if seq_size > 0:
              # Adiciona no dict de score
              player_2[seq_size].append({
                'start': start,
                'end': end
              })
              # Zera seq_size
              seq_size = 0


    # ---- Verifica Upper diags
    upper_diags = [
      (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
      (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)
    ]
    for diag in upper_diags:

      # Pega toda a diagonal superior
      diag_values = diagonals(get_board(), diag, board)[0]

      # ---- Player 1
      # Se a coluna possui alguma peça da sua cor
      if diag_values.count(1) > 0:
        # Percorre a coluna
        current = None
        seq_size = 0
        # Index to keep track of array position
        i = 0
        for point in diag_values:
          # Updates previous and current
          previous = current
          current = point
          # Ao detectar uma peça do jogador
          if current == 1:
            # Soma um no tamanho da sequência
            seq_size += 1
  	        # Se é o primeiro ponto da sequência, inicializa início
            if previous != 1:
              # Inicializa ponto de início da sequência
              if i - 1 >= 0:
                start = previous
              else:
                start = 2
          # Ao detectar uma peça que não é do jogador
          else:
            # Define variável end do final da sequencia\
            end = current
            # Salva sequencia se ela existir
            if seq_size > 0:
              # Adiciona no dict de score
              player_1[seq_size].append({
                'start': start,
                'end': end
              })
              # Zera seq_size
              seq_size = 0
          i += 1
          # Se tem pelo menos uma peça desse jogador na diagonal

      # ---- Player 2
      # Se a coluna possui alguma peça da sua cor
      if diag_values.count(2) > 0:
        # Percorre a coluna
        current = None
        seq_size = 0
        # Index to keep track of array position
        i = 0
        for point in diag_values:
          # Updates previous and current
          previous = current
          current = point
          # Ao detectar uma peça do jogador
          if current == 2:
            # Soma um no tamanho da sequência
            seq_size += 1
  	        # Se é o primeiro ponto da sequência, inicializa início
            if previous != 2:
              # Inicializa ponto de início da sequência
              if i - 1 >= 0:
                start = previous
              else:
                start = 1
          # Ao detectar uma peça que não é do jogador
          else:
            # Define variável end do final da sequencia\
            end = current
            # Salva sequencia se ela existir
            if seq_size > 0:
              # Adiciona no dict de score
              player_2[seq_size].append({
                'start': start,
                'end': end
              })
              # Zera seq_size
              seq_size = 0
          i += 1

    # ---- Verifica Down diags
    down_diags = [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1),
                 (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    for diag in down_diags:

      # Pega toda a diagonal inferior
      diag_values = diagonals(get_board(), diag, board)[1]

      # ---- Player 1
      # Se a coluna possui alguma peça da sua cor
      if diag_values.count(1) > 0:
        # Percorre a coluna
        current = None
        seq_size = 0
        # Index to keep track of array position
        i = 0
        for point in diag_values:
          # Updates previous and current
          previous = current
          current = point
          # Ao detectar uma peça do jogador
          if current == 1:
            # Soma um no tamanho da sequência
            seq_size += 1
  	        # Se é o primeiro ponto da sequência, inicializa início
            if previous != 1:
              # Inicializa ponto de início da sequência
              if i - 1 >= 0:
                start = previous
              else:
                start = 2
          # Ao detectar uma peça que não é do jogador
          else:
            # Define variável end do final da sequencia\
            end = current
            # Salva sequencia se ela existir
            if seq_size > 0:
              # Adiciona no dict de score
              player_1[seq_size].append({
                'start': start,
                'end': end
              })
              # Zera seq_size
              seq_size = 0
          i += 1
          # Se tem pelo menos uma peça desse jogador na diagonal

      # ---- Player 2
      # Se a coluna possui alguma peça da sua cor
      if diag_values.count(2) > 0:
        # Percorre a coluna
        current = None
        seq_size = 0
        # Index to keep track of array position
        i = 0
        for point in diag_values:
          # Updates previous and current
          previous = current
          current = point
          # Ao detectar uma peça do jogador
          if current == 2:
            # Soma um no tamanho da sequência
            seq_size += 1
  	        # Se é o primeiro ponto da sequência, inicializa início
            if previous != 2:
              # Inicializa ponto de início da sequência
              if i - 1 >= 0:
                start = previous
              else:
                start = 1
          # Ao detectar uma peça que não é do jogador
          else:
            # Define variável end do final da sequencia\
            end = current
            # Salva sequencia se ela existir
            if seq_size > 0:
              # Adiciona no dict de score
              player_2[seq_size].append({
                'start': start,
                'end': end
              })
              # Zera seq_size
              seq_size = 0
          i += 1

    # ---- Compute points
    # Sum points for player_1
    player1_score = 0
    if debug:
      print("Player 1")
    for seq_size, sequences in player_1.items():
      for seq in sequences:
        # print(seq)
        start, end = seq['start'], seq['end']
        if start == 0:
          start = 1
        else:
          start = 0
        if end == 0:
          end = 1
        else:
          end = 0
        any_empty_spot = (start + end)
        if any_empty_spot > 0:
          any_empty_spot = 1
        if (start + end) == 2:
          bonus = 2
        else:
          bonus = 1
        score = (any_empty_spot * seq_size) + bonus
        # Caso de 1
        if seq_size == 1 or seq_size == 2:
          score = score % (seq_size + 1)
        # Player 1 venceu
        elif start == 1 and end == 1 and seq_size == 4:
          score = 99999
        # Player 1 venceu
        elif (start == 1 or end == 1) and seq_size == 4 and player == '2':
          score = 99999
        elif start == 1 and end == 1 and seq_size == 3 and player == '1':
          score = 10
        elif start == 1 and end == 1 and seq_size == 3 and player == '2':
          score = 55555
        elif seq_size == 5:
          score = 99999
        player1_score += score
        if debug:
          print("Seq " + str(seq_size) + " - " + str(score))

    # Sum points for player_2
    player2_score = 0
    if debug:
      print("Player 2")
    for seq_size, sequences in player_2.items():
      for seq in sequences:
        start, end = seq['start'], seq['end']
        if start == 0:
          start = 1
        else:
          start = 0
        if end == 0:
          end = 1
        else:
          end = 0
        any_empty_spot = (start + end)
        if any_empty_spot > 0:
          any_empty_spot = 1
        if (start + end) == 2:
          bonus = 2
        else:
          bonus = 1
        score = (any_empty_spot * seq_size) + bonus
        # Caso de 1
        if seq_size == 1 or seq_size == 2:
          score = score % (seq_size + 1)
        # Player 2 venceu
        elif start == 1 and end == 1 and seq_size == 4:
          score = 99999
        # Player 2 venceu
        elif (start == 1 or end == 1) and seq_size == 4 and player == '1':
          score = 99999
        elif start == 1 and end == 1 and seq_size == 3 and player == '2':
          score = 10
        elif start == 1 and end == 1 and seq_size == 3 and player == '1':
          score = 55555
        elif seq_size == 5:
          score = 99999
        player2_score += score
        if debug:
          print("Seq " + str(seq_size) + " - " + str(score))

    if player == '1':
      player2_score *= -1
    else:
      player1_score *= -1

    # print("Score: " + str(player1_score + player2_score) + " | Jogador 1: " + str(player1_score) + " | Jogador 2: " + str(player2_score))
    # print("Jogador 1: " + str(player_1))
    # print("Jogador 2: " + str(player_2))

    return player1_score + player2_score

# Método que faz um minimax com poda alpha beta, e escolhe o próximo movimento
# @lru_cache(maxsize=131072)
def alpha_beta_pruning(board, depth, player, oponent, initial_depth, initial_player, forbidden_move, alpha= -inf, beta = inf):

    board = tuples_to_board(board)
    forbidden_move = list(forbidden_move)

    # Checa se chegou ao objetivo
    final_state = is_final_state(board)
    if final_state is not None:
        if final_state == player:
            return inf, board
        else:
            return -inf, board

    # Encerra quando descer até uma certa profundidade, armazenada em max_depth
    max_depth = 2
    if depth == initial_depth - max_depth:
        h = heuristic(board_to_tuple(board), initial_player)
        return h, board

    # Para o oponente - faz min
    if player == oponent:
        best_mov = None
        value = inf
        for move in get_available_moves(board, player, forbidden_move):
            # print("Move " + str(move))

            # Copies board
            board_cpy = copy.deepcopy(board)\

            # Makes move
            column, line = move
            board_cpy[column-1][line-1] = int(player)

            # Gets next player
            if player == '1':
              next_player = '2'
            else:
              next_player = '1'

            # Gets heuristic of next moves calling recursion
            new_value, _ = alpha_beta_pruning(board_to_tuple(board_cpy), depth-1, next_player, oponent, initial_depth, initial_player, tuple(forbidden_move), alpha, beta)
            # print("Value " + str(value))

            # If new_value is the best, update it and stores move
            if new_value < value or best_mov == None:
              value = new_value
              best_mov = move

            # Updates beta
            beta = min(beta, value)

            # Prunning
            if alpha >= beta:
                # print ("BestVal(" + str(best_val) + ")")
                # print ("Alpha(" + str(alpha) + ") > Beta(" + str(beta) + ") break")
                break
        return value, best_mov
    # Para o jogador principal
    else:
        best_mov = None
        value = -inf
        for move in get_available_moves(board, player, forbidden_move):
            # print("Move " + str(move))

            # Copies board
            board_cpy = copy.deepcopy(board)\

            # Makes move
            column, line = move
            board_cpy[column-1][line-1] = int(player)

            # Gets next player
            if player == '1':
              next_player = '2'
            else:
              next_player = '1'

            # Gets heuristic of next moves calling recursion
            new_value, _ = alpha_beta_pruning(board_to_tuple(board_cpy), depth-1, next_player, oponent, initial_depth, initial_player, tuple(forbidden_move), alpha, beta)
            # print("Value " + str(value))

            # If new_value is the best, update it and stores move
            if new_value > value or best_mov == None:
              value = new_value
              best_mov = move

            # Updates alpha
            alpha = max(alpha, value)

            # Prunning
            if alpha >= beta:
                # print ("BestVal(" + str(best_val) + ")")
                # print ("Alpha(" + str(alpha) + ") > Beta(" + str(beta) + ") break")
                break
        return value, best_mov

# ----------------------------------------------------------------

if len(sys.argv)==1:
    print("Voce deve especificar o numero do jogador (1 ou 2)\n\nExemplo:    ./random_client.py 1")
    quit()

# Alterar se utilizar outro host
host = "http://localhost:8080"

player = int(sys.argv[1])
if player == 1:
    adversary = 2
else:
    adversary = 1

# Reinicia o tabuleiro
resp = urllib.request.urlopen("%s/reiniciar" % host)

done = False
must_remove = False

initial_board = get_board()

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
        time.sleep(1)

        # Pega os movimentos possiveis
        resp = urllib.request.urlopen("%s/movimentos" % host)
        movimentos = eval(resp.read())

        #Pega o tabuleiro completo
        resp = urllib.request.urlopen("%s/tabuleiro" % host)
        board = eval(resp.read()) #lista com 11 listas representando cada fileira na vertical (0 vazio, 1 player 1 e 2 player 2)

        # Pega os movimentos proibidos
        forbidden_move = list(set(initial_board) - set(movimentos))

        # Escolhe um movimento com heurística, a não ser que precise remover, se precisar remove aleatóriamente

        # movimento = random.choice(movimentos)
        # movimento = (10, movimento)

        # print('Status Antes: ' + str(heuristic(board_to_tuple(board), str(player))))
        start_time = time.time()
        if must_remove:
          movimento = random.choice(movimentos)
          movimento = (0, movimento)
          print(movimento)
          must_remove = False
        else:
          if player == 1:
              oponent = 2
          else:
              oponent = 1
          movimento = alpha_beta_pruning(board_to_tuple(board), len(movimentos), str(player), str(oponent), len(movimentos), str(player), tuple(forbidden_move))
          print(movimento)
        end_time = time.time()
        print('Tempo computando movimento: ' + str(end_time - start_time))
        # print("Heuristic stats: " + str(heuristic.cache_info()))
        # print("Minimax stats: " + str(alpha_beta_pruning.cache_info()))

        # Executa o movimento
        resp = urllib.request.urlopen("%s/move?player=%d&coluna=%d&linha=%d" % (host,player,movimento[1][0],movimento[1][1]))
        msg = eval(resp.read())

        # Verifica se deve remover uma peça
        if (msg[0] == 2):
            must_remove = True
        print(msg)

        # Se com o movimento o jogo acabou, o cliente venceu
        if msg[0]==0:
            print("I win")
            done = True
        if msg[0]<0:
            raise Exception(msg[1])
        resp = urllib.request.urlopen("%s/tabuleiro" % host)
        board = eval(resp.read())
        # print('Status Depois: ' + str(heuristic(board_to_tuple(board), str(player), False)))

    # Descansa um pouco para nao inundar o servidor com requisicoes
    time.sleep(1)