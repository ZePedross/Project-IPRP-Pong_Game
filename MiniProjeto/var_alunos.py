import foosball_alunos


def carrega(f):
    posicoes = []
    linha = f.readline().split(';')
    for i in linha:
        pos = i.split(',')
        tpl = (float(pos[0]), float(pos[1]))
        posicoes.append(tpl)
    return posicoes


def le_replay(nome_ficheiro):
    pos_var = {}

    with open(nome_ficheiro, 'r') as f:
        pos_var['bola'] = carrega(f)
        pos_var['jogador_vermelho'] = carrega(f)
        pos_var['jogador_azul'] = carrega(f)
    '''
    Função que recebe o nome de um ficheiro contendo um replay, e que deverá
    retornar um dicionário com as seguintes chaves:
    bola - lista contendo tuplos com as coordenadas xx e yy da bola
    jogador_vermelho - lista contendo tuplos com as coordenadas xx e yy da do jogador\_vermelho
    jogador_azul - lista contendo tuplos com as coordenadas xx e yy da do jogador\_azul
    '''
    return pos_var


def main():
    estado_jogo = foosball_alunos.init_state()
    foosball_alunos.setup(estado_jogo, False)
    replay = le_replay('replay_golo_jv_0_ja_1.txt')
    for i in range(len(replay['bola'])):
        estado_jogo['janela'].update()
        estado_jogo['jogador_vermelho'].setpos(replay['jogador_vermelho'][i])
        estado_jogo['jogador_azul'].setpos(replay['jogador_azul'][i])
        estado_jogo['bola']['bola'].setpos(replay['bola'][i])
    estado_jogo['janela'].exitonclick()


if __name__ == '__main__':
    main()