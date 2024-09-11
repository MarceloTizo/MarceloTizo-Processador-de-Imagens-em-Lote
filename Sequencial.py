import os
import time
from PIL import Image, ImageEnhance

input_folder = "imagens" 
output_folder = "imagens_processadas" 

target_resolution = (800, 600)

# Função para processar uma imagem
def process_image(image_path, output_path):
    print(f"Processando a imagem: {os.path.basename(image_path)}")

    # Marca o início do processamento de cada imagem
    start_time = time.time()

    # Abre a imagem
    img = Image.open(image_path)
    print(f" - Dimensão original: {img.size}")

    # Redimensiona a imagem
    img_resized = img.resize(target_resolution)
    print(f" - Redimensionada para: {target_resolution}")

    # Aplica o primeiro filtro - preto e branco
    img_bw = img_resized.convert('L')
    print(" - Filtro preto e branco aplicado")

    # Aplica o segundo filtro - aumento de contraste
    enhancer = ImageEnhance.Contrast(img_bw)
    img_contrast = enhancer.enhance(2)  # Aumenta o contraste em 2 vezes
    print(" - Filtro de aumento de contraste aplicado")

    # Salva a imagem processada
    img_contrast.save(output_path)
    print(f" - Imagem processada salva em: {output_path}")

    # Marca o fim do processamento de cada imagem
    end_time = time.time()
    total_time = end_time - start_time
    print(f" - Tempo para processar a imagem: {total_time:.2f} segundos\n")

# Função para processar todas as imagens de uma pasta
def process_images_sequentially(input_folder, output_folder):
    # Cria a pasta de saída, se não existir
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Lista todas as imagens da pasta de entrada
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    start_time = time.time()  # Inicia a contagem de tempo

    # Processa cada imagem
    for image_file in image_files:
        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, f"processed_{image_file}")
        process_image(input_path, output_path)

    end_time = time.time()  # Finaliza a contagem de tempo

    # Calcula e imprime o tempo total gasto
    total_time = end_time - start_time
    minutes, seconds = divmod(total_time, 60)
    print(f"\nTempo total de execução (sequencial): {int(minutes)} minutos e {seconds:.2f} segundos")

# Executa o processamento sequencial
process_images_sequentially(input_folder, output_folder)
