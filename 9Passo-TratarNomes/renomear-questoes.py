"""Renomeia as partes para os nomes finais das questoes.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from utilitarios.comum import caminho_relativo, copiar_arquivo, limpar_pasta
from config import PASTAS, TOTAL_IMAGENS_FINAIS


def mapa_nomes() -> list[tuple[str, str]]:
    """Gera o mapeamento parte_XXX -> questao."""
    pares = []
    for i in range(1, 6):
        pares.append((f"parte_{i:03d}.png", f"questao-{i}-ingles.png"))
    for i in range(1, 6):
        pares.append((f"parte_{i+5:03d}.png", f"questao-{i}-espanhol.png"))
    parte = 11
    for questao in range(6, 91):
        pares.append((f"parte_{parte:03d}.png", f"questao-{questao}.png"))
        parte += 1
    return pares


def main() -> None:
    """Copia imagens renomeadas para a pasta do passo 9."""
    entrada = caminho_relativo(PASTAS["questoes_colunas"])
    saida = caminho_relativo(PASTAS["passo9"])
    limpar_pasta(saida, ("questao-*.png",))
    pares = mapa_nomes()
    if len(pares) != TOTAL_IMAGENS_FINAIS:
        raise RuntimeError("Mapeamento interno invalido.")
    print("Previa do mapeamento:")
    for origem_nome, destino_nome in pares:
        print(f"{origem_nome} -> {destino_nome}")
    for origem_nome, destino_nome in pares:
        origem = entrada / origem_nome
        destino = saida / destino_nome
        if not origem.exists():
            raise FileNotFoundError(f"Origem ausente: {origem}")
        if destino.exists():
            raise FileExistsError(f"Destino ja existe: {destino}")
        copiar_arquivo(origem, destino)
    print("Questoes renomeadas.")


if __name__ == "__main__":
    main()

