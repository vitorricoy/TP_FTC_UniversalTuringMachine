# Constantes usadas no código
REPRESENTACAO_INICIO_FITA = '1'
REPRESENTACAO_CELULA_VAZIA = '11'
ESTADO_INICIAL = '1'
REPRESENTACAO_DIRECAO_ESQUERDA = '11'
REPRESENTACAO_DIRECAO_DIREITA = '1'
LIMITE_TAMANHO_FITA = 1000
LIMITE_NUMERO_ITERACOES = 1000

# Inicializa a fita 2 e 3 com base na fita 1
def inicializa_fitas(fita1):
    pos_palavra = fita1.index('000') + len('000')
    fita2 = REPRESENTACAO_INICIO_FITA+'0'+fita1[pos_palavra:]
    fita3 = ESTADO_INICIAL
    return fita2, fita3

# Obtém o símbolo da máquina M que está sob o cabeçote da fita passada
def obtem_simbolo_sob_cabecote(pos_cabecote, fita):
    pos_zero = fita.find('0', pos_cabecote)
    if pos_zero == -1:
        return fita[pos_cabecote:]
    return fita[pos_cabecote:pos_zero]
    
# Simula a máquina de turing universal
def simula_maquina_turing_universal(fita1):
    # Inicializa as fitas 2 e 3
    fita2, fita3 = inicializa_fitas(fita1)
    # Inicializa o cabeçote da fita 2
    cabecote_fita2 = len(REPRESENTACAO_INICIO_FITA)+len('0')
    # Obtem a posição em que terminam os estados finais na fita 1
    pos_fim_estados_finais = fita1.find('00')
    # Obtem a posição em que terminam as transições na fita 1
    pos_fim_transicoes = fita1.find('000')
    # Cria uma lista com as representações dos estados finais
    estados_finais = fita1[:pos_fim_estados_finais].split('0')
    # Contador para controlar o número de iterações da máquina
    contador = 0
    # Flag para determinar que a palavra foi reconhecida
    reconhecido = False
    # Flag para determinar que a máquina entrou em loop
    loop = False
    # Flag para determinar que algum fita execedeu o tamanho máximo
    excedeu_tamanho_fita = False
    
    # Enquanto não se tiver atingido o limite de iterações
    # Ou seja, enquanto a máquina não estiver em loop
    while contador < LIMITE_NUMERO_ITERACOES:
        # Obtém o próximo símbolo a ser consumido da fita da máquina M
        ra = obtem_simbolo_sob_cabecote(cabecote_fita2, fita2)
        # Obtém o estado atual da máquina M
        re = obtem_simbolo_sob_cabecote(0, fita3)
        # Busca a transição que começa no estado 're' e consome o símbolo 'ra'
        # Limita a busca pelo espaço da fita1 que contêm as transições
        indice = fita1.find('00'+re+'0'+ra+'0', pos_fim_estados_finais, pos_fim_transicoes)
        # Se encontrar tal transição
        if indice != -1:
            # Inicializa ponteiro para o próximo símbolo da palavra que representa a transição
            pos_proximo_simbolo = indice+len('00')+len(re)+len('0')+len(ra)+len('0')
            # Lê o estado de entrada da transição
            e_linha = obtem_simbolo_sob_cabecote(pos_proximo_simbolo, fita1)
            # Move o ponteiro do próximo símbolo
            pos_proximo_simbolo+=len(e_linha)+len('0')
            # Lê o símbolo a ser escrito sob o símbolo 'ra' na fita 2
            a_linha = obtem_simbolo_sob_cabecote(pos_proximo_simbolo, fita1)
            # Move o ponteiro do próximo símbolo
            pos_proximo_simbolo+=len(a_linha)+len('0')
            # Lê a direção que o cabeçote da fita 2 deverá se mover
            d = obtem_simbolo_sob_cabecote(pos_proximo_simbolo, fita1)
            # Salva o estado de entrada como estado atual
            fita3 = e_linha
            # Substitui o símbolo 'ra' da fita 2 pelo 'a_linha'
            fita2 = fita2.replace(ra, a_linha)
            # Se o cabeçote da fita 2 deve se mover para direita
            if d == REPRESENTACAO_DIRECAO_DIREITA:
               # Verifica se o símbolo sobre o cabeçote é o último símbolo diferente de vazio
               indProx = fita2.find('0', cabecote_fita2)
               if indProx == -1:
                   # Se for, adiciona o símbolo vazio na fita e move o cabeçote para ele
                   fita2+='0'+REPRESENTACAO_CELULA_VAZIA
                   # Verifica se a fita2 cresceu para além do seu tamanho máximo
                   if len(fita2) > LIMITE_TAMANHO_FITA:
                       # Fita excedeu o tamanho máximo
                       # Equivalente a ter entrado em loop
                       excedeu_tamanho_fita = True
                       break
               # Salva a nova posição do cabeçote da fita 2
               cabecote_fita2 = fita2.find('0', cabecote_fita2)+1
            elif d == REPRESENTACAO_DIRECAO_ESQUERDA: # Se o cabeçote deve se mover para a esquerda
               # Move o cabecote para a representação anterior à atual
               # Considera que não se tem transições à esquerda reconhecendo o ínicio da palavra
               # Ou seja, considera que a máquina não possui um erro que a permite acessar posições negativas da fita
               cabecote_fita2 = fita2.rfind('0', 0, cabecote_fita2-2)+1
        else:
            # Verifica se a máquina para em um estado final ou não final
            # Caso pare em um estado final a palavra é reconhecida
            # Caso contrário ela não é reconhecida
            reconhecido = re in estados_finais
            break
        # Incrementa o contador de iterações
        contador+=1
    # Retorna o resultad do processamento da palavra
    if reconhecido:
        return 'Palavra reconhecida'
    elif contador == LIMITE_NUMERO_ITERACOES:
        return 'Palavra não reconhecida (loop detectado)'
    elif excedeu_tamanho_fita:
        return 'Palavra não reconhecida (tamanho máximo da fita excedido)'
    else:
        return 'Palavra não reconhecida (parou em um estado não final)'

# Lê o conteúdo da fita 1
# Foi considerado que o alfabeto da fita da máquina de turing universal é {0, 1}
fita1 = input()
# Simula a máquina de turing universal para a representação contida na fita 1
resultado = simula_maquina_turing_universal(fita1)
# Imprime o resultado
print(resultado)
