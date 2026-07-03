"""Verifica o ambiente necessario ao projeto.

Autor da adaptacao: Raul
Baseado no fluxo desenvolvido por Alexandre Nassar de Peder.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ))

from config import PDF_CAMINHO


def verificar() -> None:
    """Executa as verificacoes de ambiente."""
    print(f"Python: {sys.version.split()[0]}")
    if sys.version_info < (3, 9):
        raise RuntimeError("Use Python 3.9 ou superior.")

    for pacote, modulo in (("Pillow", "PIL"), ("pdf2image", "pdf2image")):
        if not importlib.util.find_spec(modulo):
            raise RuntimeError(f"Pacote ausente: {pacote}. Execute pip install -r requirements.txt")
        print(f"OK: {pacote} instalado")

    if not PDF_CAMINHO.exists():
        raise FileNotFoundError(f"PDF nao encontrado em {PDF_CAMINHO}")
    print(f"OK: PDF encontrado ({PDF_CAMINHO.name})")

    for exe in ("pdfinfo", "pdftoppm"):
        caminho = shutil.which(exe)
        if not caminho:
            raise RuntimeError(f"Poppler nao encontrado: {exe} nao esta no PATH.")
        print(f"OK: {exe} em {caminho}")

    subprocess.run(["pdfinfo", str(PDF_CAMINHO)], check=True, capture_output=True, text=True)
    teste = RAIZ / "0Passo-ComecePorAqui" / "_teste_permissao"
    teste.mkdir(exist_ok=True)
    (teste / "ok.txt").write_text("ok", encoding="utf-8")
    (teste / "ok.txt").unlink()
    teste.rmdir()
    print("OK: permissao de criacao e remocao de pastas")
    print("AMBIENTE VALIDADO")


if __name__ == "__main__":
    verificar()

