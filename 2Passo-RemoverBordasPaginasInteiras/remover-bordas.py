"""Remove bordas externas das paginas de questoes.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from config import (
    LINHA_AGRUPAMENTO_DISTANCIA,
    LINHA_ESCURA_MAX_RGB,
    LINHA_HORIZONTAL_ALTURA_MIN,
    LINHA_HORIZONTAL_PROP_MIN,
    MARGEM_CORTE_INFERIOR,
    MARGEM_CORTE_SUPERIOR,
    MARGEM_LATERAL_EXTRA,
    MARGEM_LATERAL_PADRAO,
    PAGINAS_QUESTOES,
    PASTAS,
)
from utilitarios.comum import abrir_rgb, caminho_relativo, limpar_pasta, listar_pngs, numero_pagina


def linhas_horizontais(img):
    """Detecta grupos de linhas horizontais escuras e longas."""
    largura, altura = img.size
    pix = img.load()
    candidatas = []
    for y in range(0, altura):
        escuros = 0
        for x in range(80, largura - 80, 3):
            r, g, b = pix[x, y]
            if max(r, g, b) <= LINHA_ESCURA_MAX_RGB:
                escuros += 1
        proporcao = escuros / max(1, ((largura - 160 + 2) // 3))
        if proporcao >= LINHA_HORIZONTAL_PROP_MIN:
            candidatas.append(y)
    grupos = []
    for y in candidatas:
        if not grupos or y - grupos[-1][-1] > LINHA_AGRUPAMENTO_DISTANCIA:
            grupos.append([y])
        else:
            grupos[-1].append(y)
    return [(g[0], g[-1]) for g in grupos if len(g) >= LINHA_HORIZONTAL_ALTURA_MIN]


def caixa_util(img):
    """Calcula a caixa de recorte conservadora da area util."""
    largura, altura = img.size
    grupos = linhas_horizontais(img)
    superiores = [g for g in grupos if g[0] < altura * 0.25]
    inferiores = [g for g in grupos if g[0] > altura * 0.82]
    topo = (superiores[-1][1] if superiores else 349) + MARGEM_CORTE_SUPERIOR
    base = (inferiores[-1][0] if inferiores else altura - 180) + MARGEM_CORTE_INFERIOR
    topo = max(0, min(topo, altura - 100))
    base = max(topo + 100, min(base, altura))
    esquerda = MARGEM_LATERAL_PADRAO - MARGEM_LATERAL_EXTRA
    direita = largura - MARGEM_LATERAL_PADRAO + MARGEM_LATERAL_EXTRA
    return (max(0, esquerda), topo, min(largura, direita), base)


def main() -> None:
    """Processa somente as paginas aproveitadas da prova."""
    entrada = caminho_relativo(PASTAS["convertidas"])
    saida = caminho_relativo(PASTAS["sem_bordas"])
    limpar_pasta(saida, ("*.png",))
    arquivos = [p for p in listar_pngs(entrada) if numero_pagina(p) in PAGINAS_QUESTOES]
    if len(arquivos) != len(PAGINAS_QUESTOES):
        raise RuntimeError(f"Esperadas {len(PAGINAS_QUESTOES)} paginas de questoes, encontradas {len(arquivos)}.")
    for arquivo in arquivos:
        img = abrir_rgb(arquivo)
        caixa = caixa_util(img)
        recorte = img.crop(caixa)
        destino = saida / arquivo.name
        recorte.save(destino)
        print(f"{arquivo.name}: caixa {caixa} -> {recorte.width}x{recorte.height}px")
        img.close()
        recorte.close()
    print(f"Bordas externas removidas: {len(arquivos)} paginas.")


if __name__ == "__main__":
    main()
