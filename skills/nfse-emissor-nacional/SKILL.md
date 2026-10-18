---
name: nfse-emissor-nacional
description: Prepara e preenche NFS-e no Emissor Nacional (nfse.gov.br) pelo navegador, do levantamento do pedido até o envio do PDF ao tomador. Use quando o usuário pedir "emite a nota", "NFS-e", "nota de serviço", "nota de comissão" ou "RPS" e a empresa emitir pelo Emissor Nacional.
---

# NFS-e no Emissor Nacional

Funciona com um agente que controla o navegador (Claude in Chrome, navegador do app ou similar). O agente faz o trabalho braçal; o humano faz só o que é dele.

## O que é SEMPRE do humano
- Senha do portal e qualquer captcha (hCaptcha do download do DANFSe).
- Clique final em **Emitir NFS-e** — o agente para na tela de revisão e mostra o resumo.
- Escolha de arquivo em janela do sistema operacional.

## 0. Configuração da empresa (preencher uma vez em `empresa.md`, ao lado desta skill)

```markdown
- Prestador: <RAZÃO SOCIAL> — CNPJ <00.000.000/0000-00>
- Regime: <Simples Nacional / Lucro Presumido> · Município: <cidade/UF>
- Código de tributação nacional: <xx.xx.xx> · NBS: <000000000>
- Alíquota aproximada de tributos (Lei 12.741): <x,xx%>
- Texto-padrão da descrição: <modelo com {TOMADOR}, {REF}, {VALOR}, {CONDICAO}>
- Dados de pagamento a citar no e-mail: <PIX/banco>
```

Nunca grave senha nesse arquivo.

## 1. Levantar o pedido
1. Ache o pedido (e-mail, planilha ou mensagem): tomador, CNPJ, e-mail do contato, referência (RPS/pedido), valor.
2. CNPJ ausente: buscar razão social + CNPJ em fonte pública e mostrar ao humano antes de usar.
3. **Antes de emitir, confira em "NFS-e Emitidas" se a nota já não existe.** Duplicar nota é o erro mais caro desse fluxo.

## 2. Login
Abra `https://www.nfse.gov.br/EmissorNacional/Login`, preencha o CNPJ, deixe o cursor na senha e diga: "Digite a senha e não troque de aba". Depois vá direto para `/EmissorNacional/DPS/Pessoas`.

## 3. Wizard (dicas técnicas validadas)
- O site usa jQuery + Chosen: selects mudam com `$(sel).val(x).trigger('chosen:updated').trigger('change')`; radios com `label.click()`.
- Screenshots desse portal costumam vir atrasados: **confie no DOM** para conferir o que foi preenchido.
- **Pessoas:** data de competência, regime, tomador (CNPJ, nome, e-mail), CEP + `keyup/focusout` para autopreencher endereço, número.
- **Serviço:** município de prestação, código de tributação nacional (digitar e escolher), NBS, descrição pelo texto-padrão.
- **Valores:** valor do serviço (o campo recebe centavos digitados: `143850` → 1.438,50), retenção de ISS, dedução, tributos aproximados.
- **Revisão:** pare. Mostre ao humano tomador, CNPJ, código, valor e descrição. Só siga com o OK.

## 4. Depois de emitida
1. Leia a chave de acesso na tela de sucesso. O número da nota está nos dígitos 24 a 36 da chave.
2. "Baixar DANFSe" abre captcha → humano resolve.
3. Renomeie: `NFSe_<numero>_<Tomador>_<ref>.pdf` e confira o PDF (`pdftotext`) contra o pedido: CNPJ, valor, descrição.

## 5. Enviar ao tomador
Responda/encaminhe a thread original do pedido com o PDF anexo. Corpo curto: número da nota, referência, valor, data de emissão, dados de pagamento, pedido de confirmação. Confira destinatários e anexo antes de enviar e registre o envio.

## Checklist de conferência (dizer ao final)
- [ ] Nota não existia antes
- [ ] CNPJ do tomador conferido em fonte pública
- [ ] Valor da nota = valor do pedido
- [ ] PDF conferido por texto
- [ ] E-mail enviado com anexo, para o contato certo
