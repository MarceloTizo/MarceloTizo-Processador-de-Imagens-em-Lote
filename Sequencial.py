import os
import time
from PIL import Image, ImageEnhance

pasta_entrada = "imagens"  
pasta_saida = "imagens_processadas" 

resolucao_alvo = (800, 600)

def processar_imagem(caminho_imagem, caminho_saida):
    print(f"Processando a imagem: {os.path.basename(caminho_imagem)}")

    inicio_tempo = time.time()

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
    print(f" - Imagem processada salva em: {caminho_saida}")

    fim_tempo = time.time()
    tempo_total = fim_tempo - inicio_tempo
    print(f" - Tempo para processar a imagem: {tempo_total:.2f} segundos\n")

def processar_imagens_sequencialmente(pasta_entrada, pasta_saida):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    arquivos_imagem = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    inicio_tempo_total = time.time() 

    # Processa cada imagem
    for arquivo_imagem in arquivos_imagem:
        caminho_entrada = os.path.join(pasta_entrada, arquivo_imagem)
        caminho_saida = os.path.join(pasta_saida, f"processada_{arquivo_imagem}")
        processar_imagem(caminho_entrada, caminho_saida)

    fim_tempo_total = time.time()  

    tempo_total_execucao = fim_tempo_total - inicio_tempo_total
    minutos, segundos = divmod(tempo_total_execucao, 60)
    print(f"\nTempo total de execução (sequencial): {int(minutos)} minutos e {segundos:.2f} segundos")

processar_imagens_sequencialmente(pasta_entrada, pasta_saida)
