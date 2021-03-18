REPRESENTACAO_INICIO_FITA = '1'
REPRESENTACAO_CELULA_VAZIA = '11'
ESTADO_INICIAL = '1'
REPRESENTACAO_DIRECAO_ESQUERDA = '11'
REPRESENTACAO_DIRECAO_DIREITA = '1'
LIMITE_TAMANHO_FITA = 1000
LIMITE_NUMERO_ITERACOES = 1000

def inicializa_fitas(fita1):
    pos_palavra = fita1.index('000') + len('000')
    fita2 = REPRESENTACAO_INICIO_FITA+'0'+fita1[pos_palavra:]
    fita3 = ESTADO_INICIAL
    return fita2, fita3

def obtem_simbolo_sob_cabecote(pos_cabecote, fita):
    pos_zero = fita.find('0', pos_cabecote)
    if pos_zero == -1:
        return fita[pos_cabecote:]
    return fita[pos_cabecote:pos_zero]
    

def simula_maquina_turing_universal(fita1):
    fita2, fita3 = inicializa_fitas(fita1)
    cabecote_fita2 = len(REPRESENTACAO_INICIO_FITA)+len('0')
    pos_fim_estados_finais = fita1.find('00')
    pos_fim_transicoes = fita1.find('000')
    estados_finais = fita1[:pos_fim_estados_finais].split('0')
    contador = 0
    reconhecido = False
    loop = False
    excedeu_tamanho_fita = False
    while contador < LIMITE_NUMERO_ITERACOES:
        ra = obtem_simbolo_sob_cabecote(cabecote_fita2, fita2)
        re = obtem_simbolo_sob_cabecote(0, fita3)
        # Busca a transição que começa no estado 're' e consome o símbolo 'ra'
        # Limita a busca pelo espaço da fita1 que contêm as transições
        indice = fita1.find('00'+re+'0'+ra+'0', pos_fim_estados_finais, pos_fim_transicoes)
        if indice != -1:
           pos_proximo_simbolo = indice+len('00')+len(re)+len('0')+len(ra)+len('0')
           e_linha = obtem_simbolo_sob_cabecote(pos_proximo_simbolo, fita1)
           pos_proximo_simbolo+=len(e_linha)+len('0')
           a_linha = obtem_simbolo_sob_cabecote(pos_proximo_simbolo, fita1)
           pos_proximo_simbolo+=len(a_linha)+len('0')
           d = obtem_simbolo_sob_cabecote(pos_proximo_simbolo, fita1)
           fita3 = e_linha
           fita2 = fita2.replace(ra, a_linha)
           if d == REPRESENTACAO_DIRECAO_DIREITA:
               # Verifica se o símbolo sobre o cabeçote é o último símbolo diferente de vazio
               indProx = fita2.find('0', cabecote_fita2)
               if indProx == -1:
                   # Se for, adiciona o símbolo vazio na fita e move para ele
                   fita2+='0'+REPRESENTACAO_CELULA_VAZIA
                   # Verifica se a fita2 cresceu para além do seu tamanho máximo
                   if len(fita2) > LIMITE_TAMANHO_FITA:
                       # Entrou em loop
                       excedeu_tamanho_fita = True
                       break
               cabecote_fita2 = fita2.find('0', cabecote_fita2)+1
           elif d == REPRESENTACAO_DIRECAO_ESQUERDA:
               # Move o cabecote para a representação anterior à atual
               # Considera que não se tem transições à esquerda reconhecendo o ínicio da palavra
               # Ou seja, considera que a máquina não possui um erro que a permite acessar posições negativas da fita
               cabecote_fita2 = fita2.rfind('0', 0, cabecote_fita2-2)+1
        else:
            reconhecido = re in estados_finais
            break
        contador+=1
    if reconhecido:
        return 'Palavra reconhecida'
    elif contador == LIMITE_NUMERO_ITERACOES:
        return 'Palavra não reconhecida (loop detectado)'
    elif excedeu_tamanho_fita:
        return 'Palavra não reconhecida (tamanho máximo da fita excedido)'
    else:
        return 'Palavra não reconhecida (parou em um estado não final)'

fita1 = input()
resultado = simula_maquina_turing_universal(fita1)
print(resultado)
