# Finance AI Toolkit

**IA no financeiro brasileiro, no modo conferido.**

Skills, scripts e prompts de copiar e colar para quem cuida de contas, conciliação e notas fiscais e quer que um agente de IA (Claude Code, Codex ou similar) faça o trabalho braçal sem errar o total.

Nasceu no dia a dia de um family office com cerca de 30 empresas. Tudo aqui foi limpo de dados reais.

> O agente faz. Você confere. Nenhum número sai sem a frase "o que foi conferido".

---

## 00 · Por onde começar

| Sua situação | Caminho | O que você ganha |
|---|---|---|
| Quero montar meu ambiente | [Prompt 01](prompts/01-montar-agente-financeiro.md) | Skills instaladas, pastas organizadas, regras do agente |
| Tenho extratos para conciliar | Skill [`conciliacao-bancaria`](skills/conciliacao-bancaria/SKILL.md) | Transações classificadas D/C, quadro de conciliação, pendências |
| Vou pagar a semana | Skill [`conferencia-contas-a-pagar`](skills/conferencia-contas-a-pagar/SKILL.md) | Total conferido, duplicidades apontadas |
| Preciso emitir NFS-e | Skill [`nfse-emissor-nacional`](skills/nfse-emissor-nacional/SKILL.md) | Wizard preenchido até a revisão, PDF conferido, envio ao tomador |
| Fechar o mês | [Prompt 02](prompts/02-fechamento-mensal.md) | Conciliação + contas a pagar cruzados em um relatório |

## 01 · Instalar

**Claude Code (plugin):**

```bash
claude plugin marketplace add osamfreitas/finance-ai-toolkit
```

```bash
claude plugin install finance-ai-toolkit@finance-ai-toolkit
```

**Manual (qualquer agente):** copie a pasta `skills/` para `.claude/skills/` do seu projeto, ou aponte o agente para o `SKILL.md` que precisar.

## 02 · O que tem dentro

```
finance-ai-toolkit/
├── skills/
│   ├── conciliacao-bancaria/       OFX/PDF → classificação D/C → conciliação
│   │   └── scripts/ofx_para_csv.py
│   ├── conferencia-contas-a-pagar/ Relatório do ERP → total conferido + duplicidades
│   │   └── scripts/conferir_relatorio.py
│   └── nfse-emissor-nacional/      Emissor Nacional pelo navegador, com humano no captcha
├── prompts/                        Prompts prontos para colar
├── exemplos/                       Dados 100% fictícios para testar
└── scripts/testar.sh               Garante que as conferências não quebram
```

Os scripts usam **só a biblioteca padrão do Python** (`Decimal`, nada de float em dinheiro). Rodam em qualquer Mac, Windows ou Linux sem instalar nada.

## 03 · Teste em 30 segundos

```bash
python3 skills/conferencia-contas-a-pagar/scripts/conferir_relatorio.py exemplos/contas-a-pagar-ficticio.csv --valor Valor --fornecedor Fornecedor --documento Documento --total-informado "13.159,02"
```

```
Linhas de total/subtotal removidas: 1 (linhas 7)
TOTAL CONFERIDO: R$ 13.159,02
Total informado pelo ERP: R$ 13.159,02 -> BATE
Possíveis duplicidades: 1
  - ENERGIA SA | NF 1001 | R$ 1.234,56 -> linhas 2, 5
```

Repare: **o total bate com o ERP e mesmo assim tem uma conta lançada em dobro.** É por isso que conferir só o total não basta.

## 04 · Princípios

1. **Agente executa, humano decide.** Senha, captcha, clique de emitir e pagamento são sempre do humano.
2. **Conferência de ponta a ponta.** Totais batendo, sem duplicidade, identidade contábil fechando — e dito por escrito.
3. **Nunca adivinhar.** `PIX ENVIADO` sem descrição vira pergunta ao cliente, não lançamento chutado.
4. **Base normativa citada.** NBC TG 1000, NBC TG 03, legislação da NFS-e nacional.
5. **Dados reais nunca entram no repositório.** O `.gitignore` bloqueia OFX, PDF e planilhas.

## 05 · Roadmap

- [ ] Conciliação de cartão de crédito (fatura × lançamentos)
- [ ] Cobrança: régua de lembretes com conferência de pagamento antes de cobrar
- [ ] DRE gerencial a partir do plano de contas
- [ ] Leitura de boletos/DARF/DAS em PDF → programação de pagamentos
- [ ] Versão em inglês

Contribuições são bem-vindas: abra uma issue contando a dor do seu financeiro.

## Aviso

Ferramenta de apoio. Não substitui contador habilitado nem gera escrituração oficial. Revise tudo antes de usar.

---

MIT · feito por Samuel Freitas — administrador, contábil e MBA em Data Science & IA (USP/Esalq).
