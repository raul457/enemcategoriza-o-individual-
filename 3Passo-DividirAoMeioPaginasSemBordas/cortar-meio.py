"""Divide as paginas sem bordas em duas colunas.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from config import PASTAS, TOTAL_PAGINAS_QUESTOES
from utilitarios.comum import abrir_rgb, caminho_relativo, limpar_pasta, listar_pngs


def main() -> None:
    """Corta cada pagina ao meio, preservando a ordem esquerda-direita."""
    entrada = caminho_relativo(PASTAS["sem_bordas"])
    saida = caminho_relativo(PASTAS["metades_com_borda"])
    limpar_pasta(saida, ("*.png",))
    arquivos = listar_pngs(entrada)
    if len(arquivos) != TOTAL_PAGINAS_QUESTOES:
        raise RuntimeError(f"Esperadas {TOTAL_PAGINAS_QUESTOES} paginas, encontradas {len(arquivos)}.")
    for arquivo in arquivos:
        img = abrir_rgb(arquivo)
        meio = img.width // 2
        esquerda = img.crop((0, 0, meio, img.height))
        direita = img.crop((meio, 0, img.width, img.height))
        base = arquivo.stem
        esquerda.save(saida / f"{base}_esquerda.png")
        direita.save(saida / f"{base}_direita.png")
        print(f"{arquivo.name}: esquerda {esquerda.size}, direita {direita.size}")
        img.close()
        esquerda.close()
        direita.close()
    print("Divisao em colunas concluida.")


if __name__ == "__main__":
    main()

