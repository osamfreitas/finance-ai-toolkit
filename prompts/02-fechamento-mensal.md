# Prompt 02 — Fechamento do mês em uma conversa

Pré-requisito: Prompt 01 rodado, extratos OFX do mês em `extratos/AAAA-MM/` e relatório do ERP em `ap/AAAA-MM/`.

## Prompt

```
Faça o fechamento financeiro de <MÊS/ANO> usando as skills do finance-ai-toolkit.

1. Para cada extrato em extratos/<AAAA-MM>/: rode a skill conciliacao-bancaria.
   Saldo contábil de cada conta: <informar ou "pedir para mim">.
2. Rode a skill conferencia-contas-a-pagar no relatório de ap/<AAAA-MM>/.
3. Cruze: todo pagamento do extrato deve ter título no contas a pagar e vice-versa.
   Liste o que sobrou dos dois lados.
4. Gere fechamento/<AAAA-MM>.md com:
   - quadro de conciliação por conta,
   - pendências com o cliente (PIX/TED sem identificação), já como perguntas,
   - pagamentos sem título e títulos sem pagamento,
   - resumo do que foi conferido.

Não exclua nem corrija nada sozinho: só aponte.
```
