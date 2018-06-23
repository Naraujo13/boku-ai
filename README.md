Um motor, servidor e visualizador para jogar Boku feito em Python 3.

Nota: o Jupyter Notebook está deprecado.

## Requerimentos
* Python 3

## Executando

```
./python server.py
```

Use um navegador para acessar o endereço `http://localhost:8080/visualizador.html`.

## API

A API ainda está em desenvolvimento. Estão disponíveis funcionalidades básicas, que são acessadas por http.

* `/jogador`. Retorna o número do jogador de quem é a vez de jogar.
* `/tabuleiro`. Retorna o estado atual do tabuleiro, na forma de lista de listas. Cada lista representa uma coluna. O valor `0` representa um espaço vazio, enquanto `1` representa o primeiro jogador e `2` representa os segundo jogador.
* `/move?player=X&coluna=C&linha=L`. Coloca uma peça do jogador X na coluna C e linha L. Retorna erro se não for a vez do jogoador X, quando o local estiver ocupado ou não existir.
* `/reiniciar`. Reinicia o jogo, limpando o tabuleiro.
* `/ultima_jogada`. Retorna a posição da última jogada realizada (coluna, linha).
* `/movimentos`. Retorna uma lista de posições válidas (coluna,linha) onde o jogador atual pode colocar uma peça (ou remover uma peça do adversário).
* `/num_movimentos`. Retorna o número de movimentos realizados desde o início do jogo.
