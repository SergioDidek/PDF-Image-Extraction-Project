import os
import zipfile
from pypdf import PdfReader
from pathlib import Path


def extrair_imagens_pypdf2(caminho_pdf, pasta_saida=r"output\images", arquivo_zip=r"output\images.zip"):
    reader = PdfReader(caminho_pdf)
    
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    total_imagens = 0
    arquivos_salvos = []

    for i_pagina, pagina in enumerate(reader.pages, start=1):
        for i_imagem, imagem_file_object in enumerate(pagina.images, start=1):
            ext = os.path.splitext(imagem_file_object.name)[1]
            if not ext:
                ext = ".png"

            nome_arquivo = f"image_{total_imagens}{ext}"
            caminho_completo = os.path.join(pasta_saida, nome_arquivo)

            with open(caminho_completo, "wb") as fp:
                fp.write(imagem_file_object.data)

            arquivos_salvos.append(caminho_completo)
            total_imagens += 1

    caminho_txt = os.path.join(pasta_saida, "report.txt")
    with open(caminho_txt, "w", encoding="utf-8") as f:
        f.write(f"total extracted images: {total_imagens}\n")

    with zipfile.ZipFile(arquivo_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for arquivo in arquivos_salvos:
            zipf.write(arquivo, os.path.basename(arquivo))
        zipf.write(caminho_txt, os.path.basename(caminho_txt))

    print(f"Extração concluída com sucesso! Total de imagens: {total_imagens}")
    print(f"Arquivo ZIP gerado em: {arquivo_zip}")

for pdf in Path('input').glob("*.pdf"):
    extrair_imagens_pypdf2(pdf)