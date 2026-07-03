"""Remove excessos brancos inferiores das questoes.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from config import BRANCO_TOLERANCIA, MARGEM_SEGURANCA_INFERIOR, MARGEM_SEGURANCA_LATERAL, PASTAS, TOTAL_IMAGENS_FINAIS
from utilitarios.comum import abrir_rgb, caminho_relativo, chave_questao_final, limpar_pasta, listar_pngs


def bbox_nao_branco(img):
    """Encontra o bounding box de pixels que nao sao quase brancos."""
    pix = img.load()
    largura, altura = img.size
    min_x, min_y, max_x, max_y = largura, altura, 0, 0
    achou = False
    for y in range(altura):
        for x in range(largura):
            r, g, b = pix[x, y]
            if min(r, g, b) < BRANCO_TOLERANCIA:
                achou = True
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    if not achou:
        return None
    return (min_x, min_y, max_x + 1, max_y + 1)


def main() -> None:
    """Recorta apenas a sobra externa branca, mantendo margem de seguranca."""
    entrada = caminho_relativo(PASTAS["questoes"])
    saida = caminho_relativo(PASTAS["finalizadas"])
    limpar_pasta(saida, ("*.png",))
    arquivos = sorted(listar_pngs(entrada), key=chave_questao_final)
    if len(arquivos) != TOTAL_IMAGENS_FINAIS:
        raise RuntimeError(f"Esperadas {TOTAL_IMAGENS_FINAIS} imagens, encontradas {len(arquivos)}.")
    for arquivo in arquivos:
        img = abrir_rgb(arquivo)
        bbox = bbox_nao_branco(img)
        if bbox is None:
            raise RuntimeError(f"Imagem quase totalmente branca: {arquivo.name}")
        esquerda = max(0, bbox[0] - MARGEM_SEGURANCA_LATERAL)
        topo = 0
        direita = min(img.width, bbox[2] + MARGEM_SEGURANCA_LATERAL)
        base = min(img.height, bbox[3] + MARGEM_SEGURANCA_INFERIOR)
        recorte = img.crop((esquerda, topo, direita, base))
        recorte.save(saida / arquivo.name)
        print(f"{arquivo.name}: {img.size} -> {recorte.size}")
        img.close()
        recorte.close()
    print("Excessos inferiores removidos.")


if __name__ == "__main__":
    main()

