"""Divide a imagem concatenada em partes de questoes.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
import runpy
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from config import FAIXA_ALTURA_MIN_QUESTAO, PASTAS, TOTAL_IMAGENS_FINAIS
from utilitarios.comum import abrir_rgb, caminho_relativo, limpar_pasta
from utilitarios.faixas import detectar_faixas


def main() -> None:
    """Usa as faixas como inicio das questoes e salva parte_001 a parte_095."""
    origem = caminho_relativo(PASTAS["concatenada"])
    saida = caminho_relativo(PASTAS["questoes_colunas"])
    limpar_pasta(saida, ("*.png",))
    img = abrir_rgb(origem)
    faixas = detectar_faixas(img)
    if len(faixas) != TOTAL_IMAGENS_FINAIS:
        runpy.run_path(str(caminho_relativo(PASTAS["passo7"]) / "diagnosticar-faixas.py"), run_name="__main__")
        raise RuntimeError(
            f"Esperadas {TOTAL_IMAGENS_FINAIS} faixas/questoes, encontradas {len(faixas)}. "
            "Ajuste config.py e rode diagnosticar-faixas.py."
        )
    cortes = faixas + [img.height]
    for i, (inicio, fim) in enumerate(zip(cortes, cortes[1:]), start=1):
        if fim - inicio < FAIXA_ALTURA_MIN_QUESTAO:
            raise RuntimeError(f"Parte {i:03d} muito pequena: {fim - inicio}px.")
        parte = img.crop((0, inicio, img.width, fim))
        destino = saida / f"parte_{i:03d}.png"
        parte.save(destino)
        print(f"{destino.name}: y={inicio}-{fim}, {parte.width}x{parte.height}px")
        parte.close()
    img.close()
    print(f"Divisao concluida: {TOTAL_IMAGENS_FINAIS} partes.")


if __name__ == "__main__":
    main()
