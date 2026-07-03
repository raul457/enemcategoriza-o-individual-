"""Diagnostica as faixas escuras de inicio das questoes.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from PIL import Image, ImageDraw

from config import PASTAS
from utilitarios.faixas import detectar_faixas
from utilitarios.comum import abrir_rgb, caminho_relativo


def main() -> list[int]:
    """Gera imagem de diagnostico com linhas vermelhas nos cortes."""
    origem = caminho_relativo(PASTAS["concatenada"])
    destino = caminho_relativo(PASTAS["diagnostico_faixas"])
    img = abrir_rgb(origem)
    faixas = detectar_faixas(img)
    diag = img.copy()
    draw = ImageDraw.Draw(diag)
    for i, y in enumerate(faixas, start=1):
        draw.line((0, y, diag.width, y), fill=(255, 0, 0), width=4)
        draw.text((8, max(0, y - 22)), f"{i:03d} y={y}", fill=(255, 0, 0))
    diag.save(destino)
    print(f"Faixas detectadas: {len(faixas)}")
    anterior = None
    for i, y in enumerate(faixas, start=1):
        distancia = "-" if anterior is None else str(y - anterior)
        print(f"{i:03d}: y={y} distancia={distancia}")
        anterior = y
    print(f"Diagnostico salvo em {destino}")
    img.close()
    diag.close()
    return faixas


if __name__ == "__main__":
    main()

