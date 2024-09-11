import os
import time
from PIL import Image, ImageEnhance

# Caminhos das pastas
pasta_entrada = "imagens"  # Pasta onde as imagens originais estão
pasta_saida = "imagens_processadas"  # Pasta onde as imagens processadas serão salvas

# Resolução alvo para o redimensionamento
resolucao_alvo = (800, 600)

# Função para processar uma imagem
def processar_imagem(caminho_imagem, caminho_saida):
    print(f"Processando a imagem: {os.path.basename(caminho_imagem)}")

    # Marca o início do processamento de cada imagem
    inicio_tempo = time.time()

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
    print(f" - Imagem processada salva em: {caminho_saida}")

    # Marca o fim do processamento de cada imagem
    fim_tempo = time.time()
    tempo_total = fim_tempo - inicio_tempo
    print(f" - Tempo para processar a imagem: {tempo_total:.2f} segundos\n")

# Função para processar todas as imagens de uma pasta
def processar_imagens_sequencialmente(pasta_entrada, pasta_saida):
    # Cria a pasta de saída, se não existir
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    # Lista todas as imagens da pasta de entrada
    arquivos_imagem = [f for f in os.listdir(pasta_entrada) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    inicio_tempo_total = time.time()  # Inicia a contagem de tempo total

    # Processa cada imagem
    for arquivo_imagem in arquivos_imagem:
        caminho_entrada = os.path.join(pasta_entrada, arquivo_imagem)
        caminho_saida = os.path.join(pasta_saida, f"processada_{arquivo_imagem}")
        processar_imagem(caminho_entrada, caminho_saida)

    fim_tempo_total = time.time()  # Finaliza a contagem de tempo total

    # Calcula e imprime o tempo total gasto
    tempo_total_execucao = fim_tempo_total - inicio_tempo_total
    minutos, segundos = divmod(tempo_total_execucao, 60)
    print(f"\nTempo total de execução (sequencial): {int(minutos)} minutos e {segundos:.2f} segundos")

# Executa o processamento sequencial
processar_imagens_sequencialmente(pasta_entrada, pasta_saida)
