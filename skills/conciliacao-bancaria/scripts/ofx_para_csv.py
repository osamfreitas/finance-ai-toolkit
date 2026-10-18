#!/usr/bin/env python3
"""Converte um extrato OFX (SGML ou XML) em CSV e imprime um resumo conferido.

Uso:
    python3 ofx_para_csv.py extrato.ofx [saida.csv]

Só usa a biblioteca padrão. O resumo confere:
  - saldo inicial implícito + soma das transações = LEDGERBAL (quando houver)
  - FITIDs duplicados
  - transações com MEMO genérico (PIX/TED/DOC/TRANSF) que precisam de identificação
"""
import csv
import re
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path

MEMO_GENERICO = re.compile(r"^\s*(PIX|TED|DOC|TRANSF\w*|TRANSFERENCIA|TEF)\b[\s\-:]*(ENVIAD\w*|RECEBID\w*)?\s*$", re.I)
ENCODINGS = ("utf-8", "cp1252", "latin-1")


def ler_texto(caminho: Path) -> str:
    dados = caminho.read_bytes()
    for enc in ENCODINGS:
        try:
            return dados.decode(enc)
        except UnicodeDecodeError:
            continue
    return dados.decode("latin-1", errors="replace")


def tag(bloco: str, nome: str) -> str:
    # OFX SGML não fecha tags: <TRNAMT>-10.50 ; XML fecha: <TRNAMT>-10.50</TRNAMT>
    m = re.search(rf"<{nome}>([^<\r\n]*)", bloco, re.I)
    return m.group(1).strip() if m else ""


def valor(txt: str) -> Decimal:
    txt = txt.strip()
    if "," in txt and "." not in txt:
        txt = txt.replace(",", ".")
    return Decimal(txt or "0")


def data(txt: str) -> str:
    d = txt[:8]
    return f"{d[6:8]}/{d[4:6]}/{d[0:4]}" if len(d) == 8 else txt


def brl(v: Decimal) -> str:
    s = f"{abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"-R$ {s}" if v < 0 else f"R$ {s}"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    origem = Path(sys.argv[1])
    destino = Path(sys.argv[2]) if len(sys.argv) > 2 else origem.with_suffix(".csv")
    texto = ler_texto(origem)

    blocos = re.findall(r"<STMTTRN>(.*?)(?=</STMTTRN>|<STMTTRN>|</BANKTRANLIST>)", texto, re.S | re.I)
    linhas = []
    for b in blocos:
        linhas.append({
            "data": data(tag(b, "DTPOSTED")),
            "valor": valor(tag(b, "TRNAMT")),
            "tipo": tag(b, "TRNTYPE"),
            "memo": tag(b, "MEMO") or tag(b, "NAME"),
            "fitid": tag(b, "FITID"),
        })

    with destino.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["data", "valor", "tipo", "memo", "fitid", "precisa_identificar"])
        for l in linhas:
            w.writerow([l["data"], str(l["valor"]).replace(".", ","), l["tipo"], l["memo"], l["fitid"],
                        "SIM" if MEMO_GENERICO.match(l["memo"]) else ""])

    entradas = sum((l["valor"] for l in linhas if l["valor"] > 0), Decimal(0))
    saidas = sum((l["valor"] for l in linhas if l["valor"] < 0), Decimal(0))
    dup = [k for k, n in Counter(l["fitid"] for l in linhas if l["fitid"]).items() if n > 1]
    genericas = [l for l in linhas if MEMO_GENERICO.match(l["memo"])]
    ledger = tag(texto, "BALAMT")

    print(f"Conta: banco {tag(texto, 'BANKID') or '?'} · conta {tag(texto, 'ACCTID') or '?'}")
    print(f"Período: {data(tag(texto, 'DTSTART'))} a {data(tag(texto, 'DTEND'))}")
    print(f"Transações: {len(linhas)}")
    print(f"Entradas:  {brl(entradas)}")
    print(f"Saídas:    {brl(saidas)}")
    print(f"Líquido:   {brl(entradas + saidas)}")
    if ledger:
        saldo_final = valor(ledger)
        print(f"Saldo final (LEDGERBAL): {brl(saldo_final)}")
        print(f"Saldo inicial implícito: {brl(saldo_final - entradas - saidas)}")
    print(f"FITIDs duplicados: {len(dup)}" + (f" -> {', '.join(dup)}" if dup else ""))
    print(f"MEMO genérico (identificar com o cliente): {len(genericas)}")
    print(f"CSV gravado em: {destino}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
