#!/usr/bin/env bash
# Roda os scripts contra os exemplos fictícios e falha se a conferência mudar.
set -euo pipefail
cd "$(dirname "$0")/.."
out=$(python3 skills/conciliacao-bancaria/scripts/ofx_para_csv.py exemplos/extrato-ficticio.ofx "${TMPDIR:-/tmp}/teste.csv")
grep -q "Saldo inicial implícito: R\$ 4.000,00" <<<"$out"
grep -q "MEMO genérico (identificar com o cliente): 2" <<<"$out"
out=$(python3 skills/conferencia-contas-a-pagar/scripts/conferir_relatorio.py exemplos/contas-a-pagar-ficticio.csv \
  --valor Valor --fornecedor Fornecedor --documento Documento --total-informado "13.159,02")
grep -q "TOTAL CONFERIDO: R\$ 13.159,02" <<<"$out"
grep -q "Possíveis duplicidades: 1" <<<"$out"
echo "OK: todos os testes passaram"
