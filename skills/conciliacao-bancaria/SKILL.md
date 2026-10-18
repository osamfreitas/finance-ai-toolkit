---
name: conciliacao-bancaria
description: Lê extratos bancários (OFX ou PDF) e relatórios de caixa, classifica cada transação com lançamento contábil D/C, concilia o saldo do extrato com o saldo contábil e entrega diagnóstico com divergências e pendências. Use quando o usuário enviar extrato, OFX, relatório de caixa ou falar em "conciliação bancária", "classificar transações", "saldo não bate", "PIX/TED sem identificação", "tarifa bancária" ou "aplicação financeira".
---

# Conciliação bancária

**Base normativa:** NBC TG 1000 (R1) Seções 7 e 11 · NBC TG 03 (R3) Demonstração dos Fluxos de Caixa.

Você atua como assistente de conciliação **sob supervisão de profissional contábil habilitado**. Analisa e sinaliza; quem concilia definitivamente é o humano.

## 1. Extrair (sempre começar pelo script quando for OFX)

```bash
python3 scripts/ofx_para_csv.py extrato.ofx saida.csv
```

O script gera o CSV e já confere: entradas, saídas, saldo final (LEDGERBAL), saldo inicial implícito, FITIDs duplicados e MEMOs genéricos. Use os números dele; não refaça soma "de cabeça".

Para PDF: extraia o texto (`pdftotext -layout`) e monte a mesma tabela (data, valor, memo). Confira: saldo anterior + créditos − débitos = saldo final impresso no extrato. Se não bater, pare e mostre a diferença antes de classificar.

## 2. Classificar

### Entradas
| Natureza | Débito | Crédito |
|---|---|---|
| Recebimento de cliente | Banco | Clientes |
| Resgate de aplicação | Banco | Aplicações Financeiras |
| Rendimento de aplicação | Banco | Receitas Financeiras |
| Aporte de capital | Banco | Capital Social / AFAC |
| Empréstimo recebido | Banco | Empréstimos a Pagar |

### Saídas
| Natureza | Débito | Crédito |
|---|---|---|
| Pagamento a fornecedor | Fornecedores | Banco |
| Salários | Salários a Pagar | Banco |
| INSS / FGTS / IRRF / DAS | Obrigação a Recolher | Banco |
| Tarifa bancária | Despesas Bancárias | Banco |
| Aplicação financeira | Aplicações Financeiras | Banco |
| Retirada de sócio / lucros | Lucros a Distribuir | Banco |
| IOF | Despesas Financeiras (IOF) | Banco |

**Regras firmes**
- MEMO genérico (`PIX ENVIADO`, `TED RECEBIDA`, `TRANSFERENCIA`) = **não identificado**. Nunca adivinhe a natureza: liste para o cliente informar.
- Aplicação com liquidez em até 90 dias pode ser equivalente de caixa (NBC TG 1000, 7.2) — sinalize, não reclassifique sozinho.
- Caixa físico nunca pode ficar negativo: saldo negativo = erro de lançamento.
- Transferência entre contas da mesma empresa: lançar nas duas pontas e conferir que se anulam.

## 3. Conciliar

```
Saldo do extrato em DD/MM/AAAA            R$ X
(+) Depósitos em trânsito                 R$ X
(−) Pagamentos em trânsito                R$ X
(=) Saldo ajustado do extrato             R$ X

Saldo contábil (razão)                    R$ X
(+/−) Ajustes identificados               R$ X
(=) Saldo contábil ajustado               R$ X

Diferença                                 R$ X   ← tem que ser zero
```

Sem saldo contábil informado: faça só a classificação e avise que a conciliação ficou pendente.

## 4. Entregar

1. Identificação: banco, conta, período.
2. Tabela de transações classificadas (data, valor, memo, D, C, status).
3. Bloco **Pendências com o cliente** (não identificadas), já redigido como pergunta.
4. Quadro de conciliação.
5. Resumo: totais, divergências, alertas — e **o que foi conferido** (ex.: "soma das 48 transações = variação do saldo; 0 FITIDs duplicados").

Valores sempre no padrão brasileiro: R$ 1.234,56. Nunca omita transação.
