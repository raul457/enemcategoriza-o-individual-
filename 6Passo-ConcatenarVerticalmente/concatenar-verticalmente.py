"""Concatena verticalmente as colunas da prova.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from PIL import Image

from config import PASTAS, TOTAL_IMAGENS_ORGANIZADAS
from utilitarios.comum import abrir_rgb, caminho_relativo, listar_pngs, ordenar_colunas

Image.MAX_IMAGE_PIXELS = None


def main() -> None:
    """Concatena na ordem pagina esquerda, pagina direita."""
    entrada = caminho_relativo(PASTAS["colunas"])
    destino = caminho_relativo(PASTAS["concatenada"])
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        destino.unlink()
    arquivos = ordenar_colunas(listar_pngs(entrada))
    if len(arquivos) != TOTAL_IMAGENS_ORGANIZADAS:
        raise RuntimeError(f"Esperadas {TOTAL_IMAGENS_ORGANIZADAS} imagens, encontradas {len(arquivos)}.")
    imagens = [abrir_rgb(p) for p in arquivos]
    largura = max(img.width for img in imagens)
    altura = sum(img.height for img in imagens)
    saida = Image.new("RGB", (largura, altura), "white")
    y = 0
    for arquivo, img in zip(arquivos, imagens):
        saida.paste(img, (0, y))
        print(f"{arquivo.name}: y={y}, tamanho={img.width}x{img.height}")
        y += img.height
        img.close()
    saida.save(destino)
    print(f"Imagem concatenada salva: {destino} ({largura}x{altura}px)")
    saida.close()


if __name__ == "__main__":
    main()
