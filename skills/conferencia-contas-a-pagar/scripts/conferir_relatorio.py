#!/usr/bin/env python3
"""Confere um relatório de contas a pagar/receber exportado do ERP em CSV.

Uso:
    python3 conferir_relatorio.py relatorio.csv --valor "Valor" --fornecedor "Fornecedor" \
        [--documento "Documento"] [--vencimento "Vencimento"] [--total-informado 12345,67]

O que faz:
  1. Remove linhas de total/subtotal (sem fornecedor, ou com "total" no texto).
  2. Soma os valores em Decimal (sem erro de ponto flutuante).
  3. Aponta duplicidades (mesmo fornecedor + documento + valor, ou fornecedor + valor + vencimento).
  4. Compara com o total que o ERP informou, se você passar --total-informado.
Só usa a biblioteca padrão. Aceita ; ou , como separador e valores 1.234,56 ou 1234.56.
"""
import argparse
import csv
import io
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path


def ler_csv(caminho: Path):
    bruto = caminho.read_bytes()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            texto = bruto.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    dialeto = csv.Sniffer().sniff(texto[:4096], delimiters=";,\t")
    return list(csv.DictReader(io.StringIO(texto), dialect=dialeto))


def para_decimal(txt: str):
    t = (txt or "").strip().replace("R$", "").replace(" ", "")
    if not t:
        return None
    negativo = t.startswith("(") and t.endswith(")")
    t = t.strip("()")
    if "," in t:
        t = t.replace(".", "").replace(",", ".")
    try:
        v = Decimal(t)
    except InvalidOperation:
        return None
    return -v if negativo else v


def brl(v: Decimal) -> str:
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"-R$ {s}" if v < 0 else f"R$ {s}"


def eh_total(linha: dict, col_fornecedor: str) -> bool:
    if not (linha.get(col_fornecedor) or "").strip():
        return True
    return any("total" in (v or "").lower() for v in linha.values())


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("arquivo")
    p.add_argument("--valor", required=True)
    p.add_argument("--fornecedor", required=True)
    p.add_argument("--documento")
    p.add_argument("--vencimento")
    p.add_argument("--total-informado")
    a = p.parse_args()

    linhas = ler_csv(Path(a.arquivo))
    validas, removidas, sem_valor = [], [], []
    for n, l in enumerate(linhas, start=2):
        if eh_total(l, a.fornecedor):
            removidas.append((n, l))
            continue
        v = para_decimal(l.get(a.valor, ""))
        if v is None:
            sem_valor.append(n)
            continue
        validas.append((n, l, v))

    total = sum((v for _, _, v in validas), Decimal(0))

    grupos = defaultdict(list)
    for n, l, v in validas:
        chave_meio = (l.get(a.documento) or "").strip() if a.documento else (l.get(a.vencimento) or "").strip() if a.vencimento else ""
        grupos[((l.get(a.fornecedor) or "").strip().upper(), chave_meio, v)].append(n)
    duplicados = {k: ns for k, ns in grupos.items() if len(ns) > 1}

    por_fornecedor = defaultdict(Decimal)
    for _, l, v in validas:
        por_fornecedor[(l.get(a.fornecedor) or "").strip()] += v

    print(f"Linhas lidas: {len(linhas)}")
    print(f"Linhas de total/subtotal removidas: {len(removidas)}" + (f" (linhas {', '.join(str(n) for n, _ in removidas)})" if removidas else ""))
    if sem_valor:
        print(f"ATENÇÃO: linhas sem valor legível: {', '.join(map(str, sem_valor))}")
    print(f"Títulos válidos: {len(validas)}")
    print(f"TOTAL CONFERIDO: {brl(total)}")
    if a.total_informado:
        informado = para_decimal(a.total_informado)
        dif = total - informado
        status = "BATE" if dif == 0 else f"DIFERENÇA DE {brl(dif)}"
        print(f"Total informado pelo ERP: {brl(informado)} -> {status}")
    print(f"Possíveis duplicidades: {len(duplicados)}")
    for (forn, meio, v), ns in duplicados.items():
        print(f"  - {forn} | {meio or '-'} | {brl(v)} -> linhas {', '.join(map(str, ns))}")
    print("Top 5 fornecedores:")
    for forn, v in sorted(por_fornecedor.items(), key=lambda x: -abs(x[1]))[:5]:
        print(f"  {brl(v):>16}  {forn}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
