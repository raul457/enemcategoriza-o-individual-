"""Gera uma folha de contato visual com as 95 questoes.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from PIL import Image, ImageDraw, ImageFont

from config import PASTAS, TOTAL_IMAGENS_FINAIS
from utilitarios.comum import caminho_relativo, chave_questao_final, listar_pngs


def main() -> None:
    """Monta miniaturas acompanhadas dos nomes dos arquivos."""
    entrada = caminho_relativo(PASTAS["finalizadas"])
    destino = caminho_relativo(PASTAS["contato_visual"])
    arquivos = sorted(listar_pngs(entrada), key=chave_questao_final)
    if len(arquivos) != TOTAL_IMAGENS_FINAIS:
        raise RuntimeError(f"Esperadas {TOTAL_IMAGENS_FINAIS}, encontradas {len(arquivos)}.")
    colunas = 5
    largura_celula = 300
    altura_celula = 420
    linhas = (len(arquivos) + colunas - 1) // colunas
    folha = Image.new("RGB", (colunas * largura_celula, linhas * altura_celula), "white")
    draw = ImageDraw.Draw(folha)
    fonte = ImageFont.load_default()
    for i, arquivo in enumerate(arquivos):
        with Image.open(arquivo) as img:
            img = img.convert("RGB")
            img.thumbnail((largura_celula - 20, altura_celula - 48))
            x = (i % colunas) * largura_celula + 10
            y = (i // colunas) * altura_celula + 28
            draw.text((x, y - 20), arquivo.name, fill=(0, 0, 0), font=fonte)
            folha.paste(img, (x, y))
            draw.rectangle((x - 1, y - 1, x + img.width + 1, y + img.height + 1), outline=(160, 160, 160))
    folha.save(destino)
    print(f"Contato visual salvo em {destino}")
    folha.close()


if __name__ == "__main__":
    main()

