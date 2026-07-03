"""Organiza as colunas aproveitadas da prova.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from config import PAGINAS_INTEIRAS_REAIS, PASTAS, TOTAL_COLUNAS, TOTAL_IMAGENS_ORGANIZADAS
from utilitarios.comum import caminho_relativo, copiar_arquivo, limpar_pasta, listar_pngs, ordenar_colunas


def main() -> None:
    """Copia colunas e paginas inteiras reais para a pasta colunas."""
    entrada = caminho_relativo(PASTAS["metades_sem_borda"])
    entrada_inteiras = caminho_relativo(PASTAS["sem_bordas"])
    saida = caminho_relativo(PASTAS["colunas"])
    limpar_pasta(saida, ("*.png",))
    arquivos = ordenar_colunas(listar_pngs(entrada))
    if len(arquivos) != TOTAL_COLUNAS:
        raise RuntimeError(f"Esperadas {TOTAL_COLUNAS} imagens de colunas, encontradas {len(arquivos)}.")
    total = 0
    for arquivo in arquivos:
        if any(f"pagina_enem_{pagina:02d}" in arquivo.name.lower() for pagina in PAGINAS_INTEIRAS_REAIS):
            continue
        copiar_arquivo(arquivo, saida / arquivo.name)
        print(f"Copiado: {arquivo.name}")
        total += 1
    for pagina in sorted(PAGINAS_INTEIRAS_REAIS):
        origem = entrada_inteiras / f"pagina_enem_{pagina:02d}.png"
        if not origem.exists():
            raise FileNotFoundError(f"Pagina inteira real ausente: {origem}")
        copiar_arquivo(origem, saida / origem.name)
        print(f"Copiado como pagina inteira real: {origem.name}")
        total += 1
    if total != TOTAL_IMAGENS_ORGANIZADAS:
        raise RuntimeError(f"Esperadas {TOTAL_IMAGENS_ORGANIZADAS} imagens organizadas, obtidas {total}.")
    print(f"Organizacao concluida: {total} imagens.")


if __name__ == "__main__":
    main()
