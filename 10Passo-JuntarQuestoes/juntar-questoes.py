"""Reune as questoes renomeadas em uma unica pasta.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from config import PASTAS, TOTAL_IMAGENS_FINAIS
from utilitarios.comum import caminho_relativo, chave_questao_final, copiar_arquivo, limpar_pasta, listar_pngs, nomes_esperados


def main() -> None:
    """Copia as 95 imagens finais renomeadas para questoes."""
    entrada = caminho_relativo(PASTAS["passo9"])
    saida = caminho_relativo(PASTAS["questoes"])
    limpar_pasta(saida, ("*.png",))
    arquivos = sorted(listar_pngs(entrada), key=chave_questao_final)
    esperados = nomes_esperados()
    if [p.name for p in arquivos] != esperados:
        faltantes = set(esperados) - {p.name for p in arquivos}
        extras = {p.name for p in arquivos} - set(esperados)
        raise RuntimeError(f"Nomes invalidos. Faltantes={sorted(faltantes)} Extras={sorted(extras)}")
    if len(arquivos) != TOTAL_IMAGENS_FINAIS:
        raise RuntimeError(f"Esperadas {TOTAL_IMAGENS_FINAIS}, encontradas {len(arquivos)}.")
    for arquivo in arquivos:
        copiar_arquivo(arquivo, saida / arquivo.name)
        print(f"Reunido: {arquivo.name}")
    print("Questoes reunidas.")


if __name__ == "__main__":
    main()

