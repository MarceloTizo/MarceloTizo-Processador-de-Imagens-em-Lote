import os
import time
import threading
from queue import Queue
from PIL import Image, ImageEnhance

# Caminhos das pastas
pasta_entrada = "imagens"  # Pasta onde as imagens originais estão
pasta_saida = "imagens_processadas_concorrente"  # Pasta onde as imagens processadas serão salvas

# Resolução alvo para o redimensionamento
resolucao_alvo = (800, 600)

# Função para processar uma imagem
def processar_imagem(caminho_imagem, caminho_saida):
    print(f"Processando a imagem: {os.path.basename(caminho_imagem)}")

    # Abre a imagem
    img = Image.open(caminho_imagem)
    print(f" - Dimensão original: {img.size}")

    # Redimensiona a imagem
    img_redimensionada = img.resize(resolucao_alvo)
    print(f" - Redimensionada para: {resolucao_alvo}")

    # Aplica o primeiro filtro - preto e branco
    img_pb = img_redimensionada.convert('L')
    print(" - Filtro preto e branco aplicado")

    # Aplica o segundo filtro - aumento de contraste
    aprimorador = ImageEnhance.Contrast(img_pb)
    img_contraste = aprimorador.enhance(2)  # Aumenta o contraste em 2 vezes
    print(" - Filtro de aumento de contraste aplicado")

    # Salva a imagem processada
    img_contraste.save(caminho_saida)
    print(f" - Imagem processada salva em: {caminho_saida}\n")

# Função para processar imagens com threads
def processar_imagens_com_threads(pasta_entrada, pasta_saida, num_threads):
    # Cria a pasta de saída, se não existir
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Lista todas as imagens da pasta de entrada
    arquivos_imagem = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    # Fila para armazenar as imagens a serem processadas
    fila_imagens = Queue()

    # Coloca todas as imagens na fila
    for arquivo_imagem in arquivos_imagem:
        caminho_entrada = os.path.join(pasta_entrada, arquivo_imagem)
        caminho_saida = os.path.join(pasta_saida, f"processada_{arquivo_imagem}")
        fila_imagens.put((caminho_entrada, caminho_saida))

    # Função executada por cada thread
    def worker():
        while not fila_imagens.empty():
            caminho_imagem, caminho_saida = fila_imagens.get()
            processar_imagem(caminho_imagem, caminho_saida)
            fila_imagens.task_done()

    # Cria e inicia as threads
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    # Espera todas as threads terminarem
    fila_imagens.join()

    # Aguarda todas as threads finalizarem
    for t in threads:
        t.join()

# Função principal para testar com diferentes números de threads
def testar_threads(pasta_entrada, pasta_saida, num_threads):
    print(f"\nIniciando o processamento com {num_threads} threads...")

    # Inicia a contagem de tempo
    inicio_tempo = time.time()

    # Processa as imagens com o número de threads especificado
    processar_imagens_com_threads(pasta_entrada, pasta_saida, num_threads)

    # Calcula o tempo total
    fim_tempo = time.time()
    tempo_total = fim_tempo - inicio_tempo
    minutos, segundos = divmod(tempo_total, 60)

    print(f"\nTempo total de execução com {num_threads} threads: {int(minutos)} minutos e {segundos:.2f} segundos\n")

# Executa o processamento com diferentes números de threads
for num_threads in [2, 4, 8]:
    testar_threads(pasta_entrada, pasta_saida, num_threads)
