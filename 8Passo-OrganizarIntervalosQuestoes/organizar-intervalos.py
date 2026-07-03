"""Organiza partes por intervalos de questoes.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from config import PASTAS
from utilitarios.comum import caminho_relativo, copiar_arquivo, limpar_pasta, listar_pngs

INTERVALOS = {
    "1-5-ingles": (1, 5, 5),
    "1-5-espanhol": (6, 10, 5),
    "6-45": (11, 50, 40),
    "46-90": (51, 95, 45),
}


def main() -> None:
    """Distribui automaticamente parte_001 a parte_095."""
    entrada = caminho_relativo(PASTAS["questoes_colunas"])
    partes = {p.name: p for p in listar_pngs(entrada)}
    base_saida = caminho_relativo(PASTAS["passo8"])
    for nome in INTERVALOS:
        limpar_pasta(base_saida / nome, ("*.png",))
    for pasta, (ini, fim, esperado) in INTERVALOS.items():
        destino_pasta = base_saida / pasta
        total = 0
        for numero in range(ini, fim + 1):
            nome = f"parte_{numero:03d}.png"
            if nome not in partes:
                raise FileNotFoundError(f"Arquivo ausente: {nome}")
            copiar_arquivo(partes[nome], destino_pasta / nome)
            total += 1
        if total != esperado:
            raise RuntimeError(f"{pasta}: esperado {esperado}, copiado {total}.")
        print(f"{pasta}: {total} arquivos")
    print("Intervalos organizados.")


if __name__ == "__main__":
    main()

