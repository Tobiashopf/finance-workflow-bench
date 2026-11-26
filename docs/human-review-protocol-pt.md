# Protocolo de revisão humana das explicações

**Versão:** 1.0  
**Escopo:** Cash Forecast 001, Borrowing Base 002 e Calibration v1 (casos 003–006)  
**Natureza:** procedimento operacional do projeto; não constitui auditoria externa nem certificação profissional.

## 1. Objetivo e separação de decisões

O Finance Workflow Bench mantém três decisões separadas:

1. **Validação numérica:** executada pelo grader determinístico contra a referência protegida.
2. **Conformidade da entrega:** presença, formato, codificação e limite de tamanho dos artefatos.
3. **Revisão humana da explicação:** julgamento fundamentado da qualidade e fidelidade da análise escrita.

A aprovação final exige que as condições numéricas e de entrega sejam satisfeitas e que os quatro critérios da revisão humana sejam aprovados. Uma explicação convincente nunca compensa um erro numérico. Uma nota numérica de 100, por si só, nunca significa aprovação final.

## 2. Papéis e independência

- **Operador:** preserva a submissão original, executa o grader, gera o template de revisão e mantém os arquivos de evidência.
- **Revisor humano:** lê a explicação, compara suas afirmações com a tarefa, os dados de entrada e os resultados financeiros; decide cada critério e escreve a justificativa.
- **Assistente de IA:** pode produzir uma triagem preliminar separada. Não pode preencher o formulário oficial, escolher vereditos em nome do revisor, nem transformar uma recomendação de IA em aprovação humana.

Na versão atual, um revisor humano identificado pode concluir a revisão. Quando houver um segundo revisor disponível, recomenda-se revisão independente de todos os casos reprovados e de uma amostra de pelo menos 25% dos aprovados. Divergências devem ser registradas e resolvidas antes de publicar uma conclusão agregada. A ausência de segundo revisor deve ser declarada, não ocultada.

O revisor não deve usar a própria resposta do modelo, um parecer de IA ou o nome do provedor como evidência de correção. Sempre que possível, faça a primeira leitura sem consultar a identidade do modelo e sem ver a revisão preliminar de IA.

## 3. Elegibilidade antes da revisão

1. Confirme o identificador do caso e a versão do grader.
2. Preserve `forecast.json` e `analysis.md` exatamente como recebidos. Não corrija, formate, resuma ou regrave os artefatos.
3. Execute o grader e guarde o relatório original.
4. Se a entrega estiver `invalid_submission` ou `incomplete_submission`, registre a causa. Não emita aprovação final. A explicação pode ser analisada para diagnóstico, mas não deve receber `passed`.
5. Se houver falha numérica, registre-a como `numerical_fail`. A revisão explicativa pode ser feita para fins diagnósticos, mas não pode alterar esse estado.
6. Somente uma entrega válida e dentro do limite de palavras é elegível a uma aprovação final.

Para Calibration v1, duas das oito submissões históricas excederam o limite de 800 palavras. Elas permanecem `incomplete_submission`; não devem ser encurtadas retroativamente nem submetidas à revisão como se fossem entregas conformes. As outras seis submissões, com aprovação numérica e texto dentro do limite, estão elegíveis à revisão humana.

## 4. Procedimento de revisão

1. Abra a tarefa e as instruções exatas fornecidas ao modelo.
2. Leia `analysis.md` integralmente antes de consultar o parecer preliminar de IA.
3. Verifique as afirmações materiais contra os arquivos de entrada e o relatório numérico. Consulte a referência protegida para confirmar a interpretação financeira; não envie a referência ao modelo nem a incorpore ao pacote do agente.
4. Julgue cada um dos quatro critérios abaixo separadamente.
5. Para cada critério, selecione somente `pass` ou `fail` e escreva uma justificativa específica. A justificativa deve apontar a afirmação, cálculo, data, registro, regra contratual ou omissão que sustenta o veredito.
6. Se um tópico não for aplicável ao caso, a explicação deve tratá-lo de modo coerente com a tarefa; não use a ausência de ocorrência como motivo automático para reprovar.
7. Não use `pass` por impressão geral, fluência, extensão ou aparência profissional. Não invente fatos para preencher lacunas.
8. Gere o relatório final com o arquivo de revisão externo e confirme `overall_passed`.

## 5. Rubrica

Os identificadores são comuns aos casos, mas o conteúdo financeiro é específico de cada família.

### `correct_summary`

- **Cash Forecast 001:** a conclusão deve concordar com o menor caixa de fechamento e sua semana, todas as semanas abaixo do buffer e com déficit não financiado, pico de dívida e primeira semana em que ocorre, além dos totais de saques, amortizações e juros. Deve distinguir violação do caixa mínimo de déficit não financiado.
- **Borrowing Base 002 e Calibration 003–006:** deve concordar com o colateral elegível, concentração, borrowing base, limite efetivo, caixa, dívida, curas obrigatórias, curas não pagas, excesso de limite e déficits. Não confunda recebíveis/colateral com recebimentos de caixa, nem redução de limite com baixa automática da dívida.

### `supported_drivers`

Os fatores materiais devem ser rastreáveis aos arquivos de entrada, datas, IDs de registros, faturas ou clientes e valores corretos. No Cash Forecast, a explicação deve citar pelo menos três drivers materiais e explicar sua relevância financeira. Em Borrowing Base e calibrações, deve sustentar mudanças relevantes de elegibilidade, concentração, borrowing base e financiamento com os snapshots e identificadores aplicáveis. Não aceite registros inexistentes nem causalidade sem suporte.

### `complete_exceptions`

- **Cash Forecast 001:** trate corretamente duplicidades exatas, pagamentos parciais, transferências internas, exclusões e eventos fora do horizonte, quando presentes.
- **Borrowing Base 002 e Calibration 003–006:** trate faturas disputadas, partes relacionadas, atraso superior ao limite contratual, saldos zerados, deduções por concentração e snapshots vazios. Respeite a precedência de motivos de exclusão e não deduplique uma fatura entre datas diferentes.
- Em qualquer família, não invente exceções nem reprove automaticamente um tópico que não ocorre no caso; avalie se a explicação o tratou de forma coerente com os dados e instruções.

### `assumptions_and_limitations`

- **Cash Forecast 001:** diferencie premissas fornecidas de conclusões, respeite a convenção de juros e arredondamento, a política semanal obrigatória e o escopo semanal determinístico. Reconheça que caixa negativo é um déficit projetado diagnóstico, não um cheque especial autorizado.
- **Borrowing Base 002 e Calibration 003–006:** aplique as regras contratuais de elegibilidade, concentração, advance rate, arredondamento, cura obrigatória e prioridade sobre o buffer mínimo. Diferencie fatos, premissas e inferências; reconheça que colateral não é caixa e que um limite menor não extingue automaticamente a dívida.
- Em todos os casos, não substitua as regras sintéticas por convenções externas nem apresente o cenário como previsão de comportamento real.

## 6. Regras de decisão

- Cada critério requer um veredito e uma justificativa não vazia.
- Os quatro critérios devem ser `pass` para a revisão explicativa ser aprovada.
- Um único `fail` resulta em `explanation_fail`, desde que a entrega numérica seja aprovada.
- Se a nota numérica falhar, a revisão humana não pode produzir `passed`.
- O status final do grader é a fonte de verdade operacional. Não substitua o resultado por uma média subjetiva.

## 7. Integridade, hashes e armazenamento

O template oficial deve ser copiado do campo `human_review_template` do relatório gerado para aquela submissão. Não reutilize um template de outro caso ou execução.

O arquivo de revisão deve:
- ficar fora da pasta da submissão;
- manter `grader_version`, `forecast_sha256` e `analysis_sha256` exatamente como gerados;
- conter o nome real do revisor;
- preencher os quatro critérios com `pass`/`fail` e justificativas escritas;
- ser preservado junto ao relatório final, sem sobrescrever o relatório numérico original.

Qualquer alteração nos artefatos exige nova execução do grader e nova revisão. A localização externa e os hashes vinculam a revisão aos arquivos, mas **não autenticam a identidade do revisor**. A identidade e a autorização são responsabilidade do operador. Não coloque segredos ou dados pessoais desnecessários nos registros.

## 8. Comandos operacionais

Exemplo para Borrowing Base 002:

```sh
python scripts/grade_borrowing_base.py path/to/submission --report reports/bb-run.json
```

Exemplo para Calibration v1:

```sh
python scripts/grade_calibration.py bb_cure_005 path/to/submission --report reports/cure-run.json
```

Copie o objeto `human_review_template` do relatório para um arquivo externo, complete os campos de revisão e execute novamente:

```sh
python scripts/grade_calibration.py bb_cure_005 path/to/submission --review path/to/operator-review.json --report reports/cure-reviewed.json
```

Use sempre um caminho de relatório novo. O código de saída zero significa que a avaliação foi executada; a aprovação deve ser confirmada por `overall_passed: true`.

## 9. Evidências e comunicação

Para cada revisão formal, preserve:
- identificador do caso e da execução;
- versão do grader e hashes dos dois artefatos;
- relatório numérico original;
- arquivo de revisão humana preenchido;
- relatório final com `overall_passed`;
- identidade do revisor e, em nota operacional separada, data da revisão e eventuais divergências.

Os registros `ai-explanation-review.json` são pareceres preliminares assistidos por IA. Eles devem continuar separados dos arquivos oficiais de revisão humana.

Ao publicar resultados, diferencie explicitamente: aprovado numericamente, elegível à revisão humana, revisão humana aprovada/reprovada e entrega incompleta. Não descreva submissões pendentes como totalmente aprovadas.

## 10. Estado inicial da Calibration v1

Na data da formalização deste protocolo:
- 8 submissões recebidas;
- 8/8 com todos os checks numéricos aprovados;
- 6 explicações dentro do limite e elegíveis à revisão humana;
- 2 explicações acima de 800 palavras, classificadas como incompletas;
- 0 aprovações humanas formais registradas por este protocolo.

Os pareceres de IA existentes não alteram essa contagem.
