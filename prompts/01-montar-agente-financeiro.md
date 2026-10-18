# Prompt 01 — Montar seu agente financeiro

Cole no Claude Code (ou outro agente com acesso a arquivos e terminal), dentro da pasta onde você guarda o financeiro da empresa.

## Prompt

```
Você vai montar meu ambiente de financeiro com IA nesta pasta.

1. Instale as skills de https://github.com/SEU-USUARIO/finance-ai-toolkit
   (plugin do Claude Code; se não for possível, copie a pasta skills/ para .claude/skills/).
2. Me faça no máximo 8 perguntas para preencher:
   - quais empresas/CNPJs eu cuido (só razão social e regime, sem senhas),
   - quais bancos e como baixo os extratos (OFX ou PDF),
   - qual ERP gera minhas contas a pagar,
   - se emito NFS-e pelo Emissor Nacional.
3. Crie um AGENTS.md nesta pasta com:
   - minhas regras: nunca pagar nada por mim, nunca digitar senha/captcha,
     sempre dizer o que foi conferido, valores em R$ 1.234,56;
   - a estrutura de pastas que você propuser (extratos/, ap/, nfse/, fechamento/).
4. Crie as pastas e um README curto explicando onde colocar cada arquivo.
5. Teste: rode as skills nos exemplos fictícios do toolkit e me mostre o resultado.

No fim, me diga em 5 linhas o que ficou pronto e o que depende de mim.
```
