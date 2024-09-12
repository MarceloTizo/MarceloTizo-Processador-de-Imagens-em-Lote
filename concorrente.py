import os
import time
import threading
from queue import Queue
from PIL import Image, ImageEnhance

pasta_entrada = "imagens"  
pasta_saida = "imagens_processadas_concorrente"  

resolucao_alvo = (800, 600)

def processar_imagem(caminho_imagem, caminho_saida):
    print(f"Processando a imagem: {os.path.basename(caminho_imagem)}")

    img = Image.open(caminho_imagem)
    print(f" - Dimensão original: {img.size}")

    img_redimensionada = img.resize(resolucao_alvo)
    print(f" - Redimensionada para: {resolucao_alvo}")

    img_pb = img_redimensionada.convert('L')
    print(" - Filtro preto e branco aplicado")

    aprimorador = ImageEnhance.Contrast(img_pb)
    img_contraste = aprimorador.enhance(2) 
    print(" - Filtro de aumento de contraste aplicado")

    img_contraste.save(caminho_saida)
    print(f" - Imagem processada salva em: {caminho_saida}\n")

def processar_imagens_com_threads(pasta_entrada, pasta_saida, num_threads):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    arquivos_imagem = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    fila_imagens = Queue()

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

    fila_imagens.join()

    for t in threads:
        t.join()

def testar_threads(pasta_entrada, pasta_saida, num_threads):
    print(f"\nIniciando o processamento com {num_threads} threads...")

    inicio_tempo = time.time()

    processar_imagens_com_threads(pasta_entrada, pasta_saida, num_threads)

    fim_tempo = time.time()
    tempo_total = fim_tempo - inicio_tempo
    minutos, segundos = divmod(tempo_total, 60)

    print(f"\nTempo total de execução com {num_threads} threads: {int(minutos)} minutos e {segundos:.2f} segundos\n")

for num_threads in [2, 4, 8]:
    testar_threads(pasta_entrada, pasta_saida, num_threads)
