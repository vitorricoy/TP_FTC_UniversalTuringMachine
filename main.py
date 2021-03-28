'''
Simulador de uma Máquina de Turing Universal
Lê a entrada de um arquivo 'entrada.txt' e imprime a saída em arquivo 'saida.txt'
'''

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
    # Identifica onde começa a representação da palavra a ser processada na fita 1
    pos_palavra = fita1.index('000') + len('000')
    # Salva na fita 2 a representação do símbolo de ínicio de fita
    # seguido da representação palavra a ser processada
    fita2 = REPRESENTACAO_INICIO_FITA+'0'+fita1[pos_palavra:]
    # Se a palavra a ser processada é vazia
    if len(fita2) == len(REPRESENTACAO_INICIO_FITA+'0'):
        fita2+=REPRESENTACAO_CELULA_VAZIA
    # Salva na fita 3 o estado inicial da máquina M
    fita3 = ESTADO_INICIAL
    return fita2, fita3

# Obtém a representação do símbolo da máquina M que está sob o cabeçote da fita passada
def obtem_simbolo_sob_cabecote(pos_cabecote, fita):
    # Busca um 0, que separa as representações de dois símbolos na fita
    pos_zero = fita.find('0', pos_cabecote)
    # Caso a posição seja -1, essa representação é a última salva na fita
    if pos_zero == -1: 
        return fita[pos_cabecote:]
    # Caso contrário retorna a representação do símbolo sob o cabeçote
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
    # Flag para determinar que alguma fita execedeu o tamanho máximo
    excedeu_tamanho_fita = False
    
    # Enquanto não tiver atingido o limite de iterações
    # Ou seja, enquanto a máquina não estiver em loop
    while contador < LIMITE_NUMERO_ITERACOES:
        # Obtém o próxima representação de um símbolo da máquina M a ser consumido da fita 2
        simbolo = obtem_simbolo_sob_cabecote(cabecote_fita2, fita2)
        # Obtém a representação do estado atual da máquina M
        estado = obtem_simbolo_sob_cabecote(0, fita3)
        # Busca a transição que começa em 'estado' e consome 'simbolo'
        # Limita a busca pelo espaço da fita 1 que contêm as transições
        indice = fita1.find('00'+estado+'0'+simbolo+'0', pos_fim_estados_finais, pos_fim_transicoes)
        # Se encontrar tal transição
        if indice != -1:
            # Inicializa ponteiro para a próxima representação de um elemento da transição
            pos_proximo_simbolo = indice+len('00')+len(estado)+len('0')+len(simbolo)+len('0')
            # Lê o estado de entrada da transição
            novo_estado = obtem_simbolo_sob_cabecote(pos_proximo_simbolo, fita1)
            # Move o ponteiro para a próxima representação de um elemento da transição
            pos_proximo_simbolo+=len(novo_estado)+len('0')
            # Lê a representação do símbolo que deve substituir 'simbolo' na fita 2
            novo_simbolo = obtem_simbolo_sob_cabecote(pos_proximo_simbolo, fita1)
            # Move o ponteiro para a próxima representação de um elemento da transição
            pos_proximo_simbolo+=len(novo_simbolo)+len('0')
            # Lê a direção que o cabeçote da fita 2 deverá se mover
            direcao = obtem_simbolo_sob_cabecote(pos_proximo_simbolo, fita1)
            # Salva o estado de entrada como estado atual
            fita3 = novo_estado
            # Substitui o 'simbolo' lido na fita 2 por 'novo_simbolo'
            fita2_temp = fita2[cabecote_fita2:]
            fita2 = fita2[:cabecote_fita2] + fita2_temp.replace(simbolo, novo_simbolo, 1)
            # Se o cabeçote da fita 2 deve se mover para direita
            if direcao == REPRESENTACAO_DIRECAO_DIREITA:
               # Verifica se o símbolo sobre o cabeçote é a última
               # representação de um símbolo diferente de vazio na fita 2
               indProx = fita2.find('0', cabecote_fita2)
               if indProx == -1:
                   # Se for, adiciona a representação de vazio na fita
                   fita2+='0'+REPRESENTACAO_CELULA_VAZIA
                   # Verifica se a fita2 cresceu para além do seu tamanho máximo
                   if len(fita2) > LIMITE_TAMANHO_FITA:
                       # Fita excedeu o tamanho máximo
                       # Equivalente a ter entrado em loop
                       excedeu_tamanho_fita = True
                       break
               # Move o cabeçote para a representação do próximo símbolo da máquina M na fita 2
               cabecote_fita2 = fita2.find('0', cabecote_fita2)+1
            elif direcao == REPRESENTACAO_DIRECAO_ESQUERDA: # Se o cabeçote deve se mover para a esquerda
               # Move o cabecote para a representação anterior à atual
               # Considera que não se tem transições que movem o cabeçote para a esquerda consumindo o ínicio da palavra
               # Ou seja, considera que a máquina não possui um erro que a permite acessar posições negativas da fita
               cabecote_fita2 = fita2.rfind('0', 0, cabecote_fita2-2)+1
        else:
            # Verifica se a máquina para em um estado final ou não final
            # Caso pare em um estado final a palavra é reconhecida
            # Caso contrário ela não é reconhecida
            reconhecido = estado in estados_finais
            break
        # Incrementa o contador de iterações
        contador+=1
    # Retorna o resultado do processamento da palavra
    if reconhecido:
        return 'Palavra reconhecida'
    elif contador == LIMITE_NUMERO_ITERACOES:
        return 'Palavra não reconhecida (loop detectado)'
    elif excedeu_tamanho_fita:
        return 'Palavra não reconhecida (tamanho máximo da fita excedido)'
    else:
        return 'Palavra não reconhecida (parou em um estado não final)'

# Abre o arquivo de entrada
arquivo = open("entrada.txt", "r")
# Lê o conteúdo da fita 1
# Foi considerado que o alfabeto da fita da máquina de turing universal é {0, 1}
fita1 = arquivo.readline()
# Fecha o arquivo de entrada
arquivo.close()
# Simula a máquina de turing universal para a representação contida na fita 1
resultado = simula_maquina_turing_universal(fita1)
# Imprime o resultado
arquivo = open("saida.txt", "w")
arquivo.write(resultado)
arquivo.close()
