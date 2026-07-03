"""Valida as imagens finais produzidas.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from PIL import Image

from config import ALTURA_MINIMA_IMAGEM_FINAL, PASTAS, PERCENTUAL_BRANCO_MAXIMO, TOTAL_IMAGENS_FINAIS
from utilitarios.comum import caminho_relativo, chave_questao_final, listar_pngs, nomes_esperados, sha256_arquivo

Image.MAX_IMAGE_PIXELS = None


def percentual_branco(img: Image.Image) -> float:
    """Calcula percentual aproximado de pixels brancos."""
    amostra = img.resize((max(1, img.width // 8), max(1, img.height // 8)))
    pix = amostra.load()
    total = amostra.width * amostra.height
    brancos = 0
    for y in range(amostra.height):
        for x in range(amostra.width):
            r, g, b = pix[x, y][:3]
            if min(r, g, b) >= 246:
                brancos += 1
    return brancos * 100 / total


def main() -> None:
    """Gera CSV e valida quantidade, nomes, hashes e dimensoes."""
    pasta = caminho_relativo(PASTAS["finalizadas"])
    relatorio = caminho_relativo(PASTAS["relatorio"])
    relatorio.parent.mkdir(parents=True, exist_ok=True)
    arquivos = sorted(listar_pngs(pasta), key=chave_questao_final)
    esperados = nomes_esperados()
    nomes = [p.name for p in arquivos]
    inesperados = sorted(set(nomes) - set(esperados))
    faltantes = sorted(set(esperados) - set(nomes))
    hashes = {}
    corrompidos = 0
    linhas = []
    for arquivo in arquivos:
        status = "OK"
        obs = []
        try:
            with Image.open(arquivo) as img:
                img.verify()
            with Image.open(arquivo) as img:
                img = img.convert("RGB")
                largura, altura = img.size
                branco = percentual_branco(img)
        except Exception as exc:
            corrompidos += 1
            largura = altura = 0
            branco = 100.0
            status = "ERRO"
            obs.append(f"corrompido: {exc}")
        if largura <= 0 or altura <= 0:
            status = "ERRO"
            obs.append("dimensao zero")
        if altura < ALTURA_MINIMA_IMAGEM_FINAL:
            status = "ERRO"
            obs.append("imagem excessivamente pequena")
        if branco > PERCENTUAL_BRANCO_MAXIMO:
            status = "ERRO"
            obs.append("quase totalmente branca")
        h = sha256_arquivo(arquivo)
        if h in hashes:
            status = "ERRO"
            obs.append(f"duplicado de {hashes[h]}")
        hashes[h] = arquivo.name
        linhas.append([arquivo.name, largura, altura, arquivo.stat().st_size, f"{branco:.2f}", h, status, "; ".join(obs)])
    with relatorio.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["nome", "largura", "altura", "tamanho_bytes", "percentual_branco", "sha256", "status", "observacoes"])
        writer.writerows(linhas)
    erros = [l for l in linhas if l[6] != "OK"]
    ordem_ok = nomes == esperados
    if len(arquivos) == TOTAL_IMAGENS_FINAIS and not faltantes and not inesperados and not erros and ordem_ok:
        print("VALIDACAO CONCLUIDA")
        print("95 imagens encontradas")
        print("95 nomes corretos")
        print("0 arquivos corrompidos")
        print("0 arquivos inesperados")
    else:
        raise RuntimeError(
            f"Validacao falhou: total={len(arquivos)}, faltantes={faltantes}, "
            f"inesperados={inesperados}, erros={len(erros)}, ordem_ok={ordem_ok}, corrompidos={corrompidos}"
        )


if __name__ == "__main__":
    main()

