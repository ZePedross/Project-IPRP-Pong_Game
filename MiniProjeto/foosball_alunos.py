#Trabalho realizado por:
#Gonçalo Fernandes Ferreira nº 2022210563
#José Pedro de Pinho Santos nº 2022227876

import turtle as t
import functools
import random
import time

LARGURA_JANELA = 1024
ALTURA_JANELA = 600
DEFAULT_TURTLE_SIZE = 40
DEFAULT_TURTLE_SCALE = 3
RAIO_JOGADOR = DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
RAIO_BOLA = DEFAULT_TURTLE_SIZE / 2
PIXEIS_MOVIMENTO = 90
LADO_MAIOR_AREA = ALTURA_JANELA / 3
LADO_MENOR_AREA = 50
RAIO_MEIO_CAMPO = LADO_MAIOR_AREA / 4
START_POS_BALIZAS = ALTURA_JANELA / 6
BOLA_START_POS = (5, 5)
INTERVALO_DE_DETECAO = 0.5
VELOCIDADE_MAX = 0.6
VEL_MINIMA = 0.2


# Funções responsáveis pelo movimento dos jogadores no ambiente.
# O número de unidades que o jogador se pode movimentar é definida pela constante
# PIXEIS_MOVIMENTO. As funções recebem um dicionário que contém o estado
# do jogo e o jogador que se está a movimentar.

def move_para(nome, x, y):
    nome.up()
    nome.goto(x, y)
    nome.down()


def jogador_cima(estado_jogo, jogador):
    player = estado_jogo[jogador]
    player.seth(90)
    player.fd(PIXEIS_MOVIMENTO)


def jogador_baixo(estado_jogo, jogador):
    player = estado_jogo[jogador]
    player.seth(270)
    player.fd(PIXEIS_MOVIMENTO)


def jogador_direita(estado_jogo, jogador):
    player = estado_jogo[jogador]
    player.seth(0)
    player.fd(PIXEIS_MOVIMENTO)


def jogador_esquerda(estado_jogo, jogador):
    player = estado_jogo[jogador]
    player.seth(180)
    player.fd(PIXEIS_MOVIMENTO)


def desenha_linhas_campo():
    linhas = t.Turtle()
    linhas.color("white")
    linhas.pensize(DEFAULT_TURTLE_SCALE)
    move_para(linhas, 0, -ALTURA_JANELA / 2)
    linhas.seth(90)
    linhas.fd(ALTURA_JANELA)
    linhas.seth(0)
    move_para(linhas, 0, -RAIO_MEIO_CAMPO)
    linhas.circle(RAIO_MEIO_CAMPO)
    move_para(linhas, -LARGURA_JANELA / 2, ALTURA_JANELA / 2)
    for i in range(2):
        linhas.fd(LARGURA_JANELA)
        linhas.right(90)
        linhas.fd(ALTURA_JANELA)
        linhas.right(90)

    for i in range(2):
        if i == 0:
            linhas.seth(0)
            move_para(linhas, -LARGURA_JANELA / 2, -START_POS_BALIZAS)
        else:
            linhas.seth(180)
            move_para(linhas, LARGURA_JANELA / 2, START_POS_BALIZAS)
        for j in range(2):
            linhas.fd(LADO_MENOR_AREA)
            linhas.left(90)
            linhas.fd(LADO_MAIOR_AREA)
            linhas.left(90)
    linhas.hideturtle()


def criar_bola():
    bola = t.Turtle()
    bola.color('black')
    bola.pensize(RAIO_BOLA)
    bola.shape('circle')

    bola.penup()
    bola.goto(BOLA_START_POS)

    x_bola, y_bola = gerarVelocidade(-VEL_MINIMA, VEL_MINIMA)

    estado_bola = {'bola': bola,
                   'direcao x': x_bola,
                   'direcao y': y_bola,
                   'ultima colisao': None,
                   'posição anterior': None}
    return estado_bola


def gerarVelocidade(inf, sup):
    x_bola = 0
    y_bola = 0
    while inf < x_bola < sup and inf < y_bola < sup:
        x_bola = (random.random() * 2 - 1) * VELOCIDADE_MAX
        y_bola = (random.random() * 2 - 1) * VELOCIDADE_MAX
    return x_bola, y_bola


def cria_jogador(x_pos_inicial, y_pos_inicial, cor):
    jogador = t.Turtle()
    jogador.color(cor)
    jogador.pensize(RAIO_JOGADOR)
    jogador.shape('circle')
    move_para(jogador, x_pos_inicial, y_pos_inicial)
    jogador.pu()
    jogador.shapesize(stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE)
    return jogador


def init_state():
    estado_jogo = {}
    estado_jogo['bola'] = None
    estado_jogo['jogador_vermelho'] = None
    estado_jogo['jogador_azul'] = None
    estado_jogo['var'] = {
        'bola': [],
        'jogador_vermelho': [],
        'jogador_azul': [],
    }
    estado_jogo['pontuacao_jogador_vermelho'] = 0
    estado_jogo['pontuacao_jogador_azul'] = 0
    estado_jogo['ultima_colisao'] = 0
    return estado_jogo


def cria_janela():
    # create a window and declare a variable called window and call the screen()
    window = t.Screen()
    window.title("Foosball Game")
    window.bgcolor("green")
    window.setup(width=LARGURA_JANELA, height=ALTURA_JANELA)
    window.tracer(0)
    return window


def cria_quadro_resultados():
    # Code for creating pen for scorecard update
    quadro = t.Turtle()
    quadro.speed(0)
    quadro.color("Blue")
    quadro.penup()
    quadro.hideturtle()
    quadro.goto(0, 260)
    quadro.write("Player A: 0\t\tPlayer B: 0 ", align="center", font=('Monaco', 24, "normal"))
    return quadro


def terminar_jogo(estado_jogo):
    golos_vermelhos = estado_jogo['pontuacao_jogador_vermelho']
    golos_azuis = estado_jogo['pontuacao_jogador_azul']
    header = 'NJogo,JogadorVermelho,JogadorAzul\n'
    fich = 'historico_resultados.csv'
    with open(fich, 'a+') as f:
        f.seek(0)
        linha1 = f.readline()
        contJogos = 1
        if linha1 != header:
            f.write(header)
        else:
            while f.readline():
                contJogos += 1
        informacao_jogo = f"{contJogos},{golos_vermelhos},{golos_azuis}\n"
        f.write(informacao_jogo)
    print("Adeus")
    estado_jogo['janela'].bye()
    '''
     Função responsável por terminar o jogo. Nesta função, deverá atualizar o ficheiro
     ''historico_resultados.csv'' com o número total de jogos até ao momento,
     e o resultado final do jogo. Caso o ficheiro não exista,
     ele deverá ser criado com o seguinte cabeçalho:
     NJogo,JogadorVermelho,JogadorAzul.
    '''


def setup(estado_jogo, jogar):
    janela = cria_janela()
    # Assign keys to play
    janela.listen()
    if jogar:
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_vermelho'), 'w')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_vermelho'), 's')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_vermelho'), 'a')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_vermelho'), 'd')
        janela.onkeypress(functools.partial(jogador_cima, estado_jogo, 'jogador_azul'), 'Up')
        janela.onkeypress(functools.partial(jogador_baixo, estado_jogo, 'jogador_azul'), 'Down')
        janela.onkeypress(functools.partial(jogador_esquerda, estado_jogo, 'jogador_azul'), 'Left')
        janela.onkeypress(functools.partial(jogador_direita, estado_jogo, 'jogador_azul'), 'Right')
        janela.onkeypress(functools.partial(terminar_jogo, estado_jogo), 'Escape')
        quadro = cria_quadro_resultados()
        estado_jogo['quadro'] = quadro
    desenha_linhas_campo()
    bola = criar_bola()
    jogador_vermelho = cria_jogador(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "red")
    jogador_azul = cria_jogador(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "blue")
    estado_jogo['janela'] = janela
    estado_jogo['bola'] = bola
    estado_jogo['jogador_vermelho'] = jogador_vermelho
    estado_jogo['jogador_azul'] = jogador_azul


def update_board(estado_jogo):
    estado_jogo['quadro'].clear()
    estado_jogo['quadro'].write("Player A: {}\t\tPlayer B: {} ".format(estado_jogo['pontuacao_jogador_vermelho'],
                                                                       estado_jogo['pontuacao_jogador_azul']),
                                align="center", font=('Monaco', 24, "normal"))


def movimenta_bola(estado_jogo):
    direcao_x = estado_jogo['bola']['direcao x']
    direcao_y = estado_jogo['bola']['direcao y']

    posicao_anterior_x, posicao_anterior_y = estado_jogo['bola']['bola'].pos()

    nova_posicao_x = posicao_anterior_x + direcao_x
    nova_posicao_y = posicao_anterior_y + direcao_y

    verifica_colisoes_ambiente(estado_jogo)

    estado_jogo['bola']['bola'].goto(nova_posicao_x, nova_posicao_y)

    estado_jogo['bola']['posição anterior'] = (posicao_anterior_x, posicao_anterior_y)
    estado_jogo['bola']['posição'] = (nova_posicao_x, nova_posicao_y)


def verifica_colisoes_ambiente(estado_jogo):
    '''
    Função responsável por verificar se há colisões com os limites do ambiente,
    atualizando a direção da bola. Não se esqueça de considerar que nas laterais,
    fora da zona das balizas, a bola deverá inverter a direção onde atingiu o limite.
    '''

    direcao_x = estado_jogo['bola']['direcao x']
    direcao_y = estado_jogo['bola']['direcao y']
    posicao_anterior_x, posicao_anterior_y = estado_jogo['bola']['bola'].pos()
    nova_posicao_x = posicao_anterior_x + direcao_x
    nova_posicao_y = posicao_anterior_y + direcao_y

    # Verifica se a bola atingiu as bordas da janela
    rangeBal = -START_POS_BALIZAS < nova_posicao_y < START_POS_BALIZAS
    if (
            nova_posicao_x > LARGURA_JANELA / 2 - RAIO_BOLA or nova_posicao_x < -LARGURA_JANELA / 2 + RAIO_BOLA) and not rangeBal:
        estado_jogo['bola']['direcao x'] *= -1
    if nova_posicao_y > ALTURA_JANELA / 2 - RAIO_BOLA or nova_posicao_y < -ALTURA_JANELA / 2 + RAIO_BOLA:
        estado_jogo['bola']['direcao y'] *= -1

    up = ALTURA_JANELA / 2 - RAIO_JOGADOR * 2
    down = -ALTURA_JANELA / 2 + RAIO_JOGADOR * 2

    # jogador vermelho
    player = estado_jogo['jogador_vermelho']
    left = -LARGURA_JANELA / 2 + RAIO_JOGADOR * 2  # verifica a colisão com a linha da baliza
    right = -RAIO_JOGADOR * 2  # Verifica a colisão com o meio campo
    bounds(player, up, down, left, right)  # verifica as colisoes com as laterais do campo

    player = estado_jogo['jogador_azul']
    left = RAIO_JOGADOR * 2  # verifica as colisoes com o meio campo
    right = LARGURA_JANELA / 2 - RAIO_JOGADOR * 2  # verifica a colisão com a linha da baliza
    bounds(player, up, down, left, right)  # verifica as colisoes com as laterais do campo


def bounds(player, up, down, left, right):
    if player.ycor() > up:
        player.sety(up)
    elif player.ycor() < down:
        player.sety(down)
    if player.xcor() < left:
        player.setx(left)
    elif player.xcor() > right:
        player.setx(right)


def verifica_golo_jogador_vermelho(estado_jogo):
    bola = estado_jogo['bola']['bola']
    if bola.xcor() >= LARGURA_JANELA / 2:
        estado_jogo["pontuacao_jogador_vermelho"] += 1
        update_board(estado_jogo)
        reiniciar(estado_jogo)

    '''
    Função responsável por verificar se um determinado jogador marcou golo. 
    Para fazer esta verificação poderá fazer uso das constantes: 
    LADO_MAIOR_AREA e 
    START_POS_BALIZAS. 
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador, 
    criar um ficheiro que permita fazer a análise da jogada pelo VAR, 
    e reiniciar o jogo com a bola ao centro. 
    O ficheiro para o VAR deverá conter todas as informações necessárias 
    para repetir a jogada, usando as informações disponíveis no objeto 
    estado_jogo['var']. O ficheiro deverá ter o nome 

    replay_golo_jv_[TotalGolosJogadorVermelho]_ja_[TotalGolosJogadorAzul].txt 

    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul] 
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho 
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas 
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;

    Em cada linha, os valores de xx e yy das coordenadas são separados por uma 
    ',', e cada coordenada é separada por um ';'.
    '''


def verifica_golo_jogador_azul(estado_jogo):
    bola = estado_jogo['bola']['bola']
    if bola.xcor() <= -LARGURA_JANELA / 2:
        estado_jogo["pontuacao_jogador_azul"] += 1
        update_board(estado_jogo)
        reiniciar(estado_jogo)

    '''
    Função responsável por verificar se um determinado jogador marcou golo. 
    Para fazer esta verificação poderá fazer uso das constantes: 
    LADO_MAIOR_AREA e 
    START_POS_BALIZAS. 
    Note que sempre que há um golo, deverá atualizar a pontuação do jogador, 
    criar um ficheiro que permita fazer a análise da jogada pelo VAR, 
    e reiniciar o jogo com a bola ao centro. 
    O ficheiro para o VAR deverá conter todas as informações necessárias 
    para repetir a jogada, usando as informações disponíveis no objeto 
    estado_jogo['var']. O ficheiro deverá ter o nome 

    replay_golo_jv_[TotalGolosJogadorVermelho]_ja_[TotalGolosJogadorAzul].txt 

    onde [TotalGolosJogadorVermelho], [TotalGolosJogadorAzul] 
    deverão ser substituídos pelo número de golos marcados pelo jogador vermelho 
    e azul, respectivamente. Este ficheiro deverá conter 3 linhas, estruturadas 
    da seguinte forma:
    Linha 1 - coordenadas da bola;
    Linha 2 - coordenadas do jogador vermelho;
    Linha 3 - coordenadas do jogador azul;

    Em cada linha, os valores de xx e yy das coordenadas são separados por uma 
    ',', e cada coordenada é separada por um ';'.
    '''


def reiniciar(estado_jogo):
    update_board(estado_jogo)
    guarda_posicoes_para_var(estado_jogo)
    escreveFichVar(estado_jogo)

    estado_jogo['var']['bola'].clear()
    estado_jogo['var']['jogador_vermelho'].clear()
    estado_jogo['var']['jogador_azul'].clear()

    bola = estado_jogo['bola']['bola']
    bola.goto(BOLA_START_POS)

    x_bola, y_bola = gerarVelocidade(-VEL_MINIMA, VEL_MINIMA)
    estado_jogo['bola']['direcao x'] = x_bola
    estado_jogo['bola']['direcao y'] = y_bola

    jogador_vermelho = estado_jogo["jogador_vermelho"]
    jogador_vermelho.goto(-ALTURA_JANELA / 2 + LADO_MENOR_AREA, 0)

    jogador_azul = estado_jogo["jogador_azul"]
    jogador_azul.goto(ALTURA_JANELA / 2 + LADO_MENOR_AREA, 0)

    guarda_posicoes_para_var(estado_jogo)


def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)


def verifica_toque_jogador_azul(estado_jogo):
    player = estado_jogo["jogador_azul"]
    verifca_toque_jogadores(estado_jogo, player)
    '''
    Função responsável por verificar se o jogador tocou na bola. 
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''


def verifica_toque_jogador_vermelho(estado_jogo):
    player = estado_jogo["jogador_vermelho"]
    verifca_toque_jogadores(estado_jogo, player)
    '''
    Função responsável por verificar se o jogador tocou na bola.
    Sempre que um jogador toca na bola, deverá mudar a direção desta.
    '''


def verifca_toque_jogadores(estado_jogo, player):
    bola = estado_jogo["bola"]["bola"]
    x = estado_jogo['bola']['direcao x']
    y = estado_jogo['bola']['direcao y']

    if player.distance(bola) <= DEFAULT_TURTLE_SIZE and time.time() - estado_jogo[
        'ultima_colisao'] > INTERVALO_DE_DETECAO:
        estado_jogo['ultima_colisao'] = time.time()
        if x < 0:
            while x < VEL_MINIMA:
                x = random.random() * VELOCIDADE_MAX
        else:
            while x > -VEL_MINIMA:
                x = random.random() * -VELOCIDADE_MAX
        if y < 0:
            while y < VEL_MINIMA:
                y = random.random() * VELOCIDADE_MAX
        else:
            while y > -VEL_MINIMA:
                y = random.random() * -VELOCIDADE_MAX
    estado_jogo['bola']['direcao x'] = x
    estado_jogo['bola']['direcao y'] = y


def guarda_posicoes_para_var(estado_jogo):
    estado_jogo['var']['bola'].append(estado_jogo['bola']['bola'].pos())
    estado_jogo['var']['jogador_vermelho'].append(estado_jogo['jogador_vermelho'].pos())
    estado_jogo['var']['jogador_azul'].append(estado_jogo['jogador_azul'].pos())


def escreveLinha(ficheiro, estado_jogo, nome):
    infoPos = estado_jogo['var'][nome]
    linha = ""
    i = 0
    for pos in infoPos:
        stringInfo = f"{pos[0]},{pos[1]}"
        linha += stringInfo
        if i < len(infoPos) - 1:
            linha += ';'
        i += 1
    linha += '\n'
    ficheiro.write(linha)


def escreveFichVar(estado_jogo):
    ficheiro = f"replay_golo_jv_{estado_jogo['pontuacao_jogador_vermelho']}_ja_{estado_jogo['pontuacao_jogador_azul']}.txt"
    with open(ficheiro, 'w') as f:
        escreveLinha(f, estado_jogo, 'bola')
        escreveLinha(f, estado_jogo, 'jogador_vermelho')
        escreveLinha(f, estado_jogo, 'jogador_azul')


def main():
    estado_jogo = init_state()
    setup(estado_jogo, True)
    while True:
        estado_jogo['janela'].update()
        if estado_jogo['bola'] is not None:
            movimenta_bola(estado_jogo)
        verifica_colisoes_ambiente(estado_jogo)
        verifica_golos(estado_jogo)
        if estado_jogo['jogador_vermelho'] is not None:
            verifica_toque_jogador_azul(estado_jogo)
        if estado_jogo['jogador_azul'] is not None:
            verifica_toque_jogador_vermelho(estado_jogo)
        guarda_posicoes_para_var(estado_jogo)


if __name__ == '__main__':
    main()