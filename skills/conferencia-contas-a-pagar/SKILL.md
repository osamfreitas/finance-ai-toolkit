---
name: conferencia-contas-a-pagar
description: Confere relatórios de contas a pagar ou a receber exportados do ERP (CSV/XLS) antes de qualquer pagamento ou fechamento - remove linhas de total, soma com precisão, acha duplicidades e compara com o total do sistema. Use quando o usuário mandar relatório do ERP, planilha de títulos, "programação de pagamentos", "contas a pagar da semana" ou pedir "confere esse total".
---

# Conferência de contas a pagar / a receber

Relatório de ERP é a origem de quase todo pagamento em dobro. Esta skill existe para que nenhum total seja entregue sem conferência de ponta a ponta.

## Armadilhas reais que ela pega
1. **Linha de total sem fornecedor** no fim (ou subtotais por dia). Somar a coluna inteira dobra o valor.
2. **Duplicidade**: mesmo fornecedor + documento + valor lançado duas vezes. Note que o total do relatório *bate* com o do ERP mesmo assim — conferir só o total não basta.
3. Valores em texto (`1.234,56`, `(500,00)`, `R$ 89,90`) somados como float e arredondados errado.
4. Vencimentos fora do período pedido misturados no relatório.

## Passo a passo
1. Se vier `.xls`/`.xlsx`, exporte para CSV (planilha → Salvar como CSV, ou `soffice --headless --convert-to csv`). Identifique os nomes exatos das colunas de fornecedor, documento, vencimento e valor.
2. Rode:
   ```bash
   python3 scripts/conferir_relatorio.py relatorio.csv \
     --valor "Valor" --fornecedor "Fornecedor" \
     --documento "Documento" --total-informado "13.159,02"
   ```
3. Leia a saída e trate cada alerta:
   - Linhas removidas: confirme que eram mesmo totais.
   - Duplicidades: liste para o humano decidir; **não exclua sozinho**.
   - Diferença contra o total do ERP: investigue antes de seguir.
4. Filtre o período/vencimento pedido, se for o caso, e reconfira.

## Entrega
- Tabela final dos títulos (fornecedor, documento, vencimento, valor), ordenada por vencimento.
- **Total conferido** em R$ e a frase do que foi verificado, por exemplo:
  "54 linhas lidas, 3 de subtotal removidas, 51 títulos, total R$ 87.412,30 = total do ERP; 1 possível duplicidade (ENERGIA SA NF 1001, linhas 2 e 5)."
- Pendências em lista numerada.

## Regras
- Nunca executar pagamento. Preparar a lista (linha digitável, PIX, valor, vencimento) e o humano paga.
- Boleto sem PIX: avisar que é boleto comum.
- Depois que o humano disser que pagou, procurar o comprovante antes de dar baixa.
