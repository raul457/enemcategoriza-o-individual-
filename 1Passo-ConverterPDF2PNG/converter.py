"""Converte o PDF do ENEM 2021 em PNG.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from pdf2image import convert_from_path
from PIL import Image

from config import DPI, PASTAS, PDF_CAMINHO, TOTAL_PAGINAS_PDF
from utilitarios.comum import caminho_relativo, limpar_pasta

Image.MAX_IMAGE_PIXELS = None


def main() -> None:
    """Converte todas as paginas do PDF em imagens PNG nomeadas."""
    if not PDF_CAMINHO.exists():
        raise FileNotFoundError(f"PDF nao encontrado: {PDF_CAMINHO}")
    saida = caminho_relativo(PASTAS["convertidas"])
    limpar_pasta(saida, ("*.png",))
    print(f"Convertendo {PDF_CAMINHO.name} em {DPI} DPI...")
    paginas = convert_from_path(str(PDF_CAMINHO), dpi=DPI)
    if len(paginas) != TOTAL_PAGINAS_PDF:
        raise RuntimeError(f"Esperadas {TOTAL_PAGINAS_PDF} paginas, obtidas {len(paginas)}.")
    for indice, imagem in enumerate(paginas, start=1):
        imagem = imagem.convert("RGB")
        destino = saida / f"pagina_enem_{indice:02d}.png"
        imagem.save(destino, "PNG")
        print(f"{destino.name}: {imagem.width}x{imagem.height}px")
        imagem.close()
    print(f"Conversao concluida: {len(paginas)} paginas.")


if __name__ == "__main__":
    main()

