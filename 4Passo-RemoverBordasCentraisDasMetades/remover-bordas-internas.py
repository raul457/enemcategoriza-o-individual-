"""Remove a pequena borda central das metades.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from config import PASTAS, REMOVER_BORDA_CENTRAL_PX, TOTAL_COLUNAS
from utilitarios.comum import abrir_rgb, caminho_relativo, limpar_pasta, listar_pngs


def main() -> None:
    """Recorta apenas o lado interno de cada coluna."""
    entrada = caminho_relativo(PASTAS["metades_com_borda"])
    saida = caminho_relativo(PASTAS["metades_sem_borda"])
    limpar_pasta(saida, ("*.png",))
    arquivos = listar_pngs(entrada)
    if len(arquivos) != TOTAL_COLUNAS:
        raise RuntimeError(f"Esperadas {TOTAL_COLUNAS} colunas, encontradas {len(arquivos)}.")
    for arquivo in arquivos:
        img = abrir_rgb(arquivo)
        if "esquerda" in arquivo.name.lower():
            caixa = (0, 0, img.width - REMOVER_BORDA_CENTRAL_PX, img.height)
        elif "direita" in arquivo.name.lower():
            caixa = (REMOVER_BORDA_CENTRAL_PX, 0, img.width, img.height)
        else:
            raise RuntimeError(f"Lado nao identificado: {arquivo.name}")
        recorte = img.crop(caixa)
        recorte.save(saida / arquivo.name)
        print(f"{arquivo.name}: {img.size} -> {recorte.size}")
        img.close()
        recorte.close()
    print("Bordas centrais removidas.")


if __name__ == "__main__":
    main()

