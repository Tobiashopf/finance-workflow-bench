# Caso 004 — concentração por cliente

| Identificação informada | Nota numérica | Verificações | Palavras | Estado |
|---|---:|---:|---:|---|
| GPT-6 Astra | 100/100 | 140/140 | 636 | explanation_review_pending |
| Claude, configurado claude-opus-5-5; modelo efetivo incerto | 100/100 | 140/140 | 751 | explanation_review_pending |

Ambos os arquivos JSON satisfazem o esquema e acertam todas as verificações. Ambas as explicações ficam dentro do limite de 800 palavras. A revisão preliminar por IA recomenda aprovação dos quatro critérios de conteúdo financeiro, mas a aprovação humana permanece pendente e `overall_passed=false` em ambas as avaliações.

## Mecanismos resolvidos

- A-1, A-2 e A-3 foram agregadas por cliente antes da concentração. Na semana 1, A tem 120.000,00 elegíveis e apenas 60.000,00 reconhecidos.
- Na semana 2, D-1 tem saldo zero e é excluída; D continua no controle por cliente, com valores zero e o teto compartilhado. O total elegível permanece 240.000,00, mas a concentração adicional em B reduz o limite de 144.000,00 para 128.000,00.
- As amortizações obrigatórias de 6.000,00 e 16.000,00 são pagas integralmente, deixando faltas para o caixa mínimo de 6.300,00 e 32.588,00. Não há déficit de caixa nem dívida acima do limite nos fechamentos.
- A semana 3 permite amortização voluntária de 17.156,00; a semana 4 exige saque de 40.221,69. As mudanças da carteira não são tratadas como fluxos de caixa.

## Identidade e condições da execução

O registro fornecido para o Claude declara configuração `claude-opus-5-5`, mas ressalva que o modelo efetivamente responsável pela resposta pode ser outro. Este resultado pertence à entrega recebida sob essa configuração, sem atribuição verificada a uma versão específica.

O mesmo registro informa shell com Python 3 (decimal, csv, json, jsonschema), editor de arquivos, nenhuma falha ou intervenção adicional, uma tentativa de cálculo e uma submissão final. São informações fornecidas pelo usuário, não um histórico de ferramentas observado pelo avaliador.

Para o GPT, foi informado o nome GPT-6 Astra; ferramentas, tentativas e modo de raciocínio não foram detalhados nesta entrega. Conversa nova, memória e navegação não foram reconfirmadas para esta rodada; as condições relatadas no caso 003 não foram automaticamente transferidas.

## Preservação e comparação

Os arquivos `forecast (3).json` e `analysis (3).md` foram registrados em `runs/cal-v1-bb_customer_004-A`; `forecast4.json` e `analysis4.md`, em `runs/cal-v1-bb_customer_004-B`. O conteúdo foi preservado byte a byte. Os arquivos de Downloads reutilizados não sobrescreveram as submissões arquivadas do caso 003.

Cada pasta contém `grade.json`, `execution.json`, o parecer preliminar por IA e os dois entregáveis. O plano agora registra quatro execuções avaliadas e quatro ainda não iniciadas.

Neste caso não foi observada diferença de correção numérica ou de cumprimento do limite textual. A entrega do Claude com 802 palavras no caso 003 permanece registrada como incompleta; o resultado válido do caso 004 não substitui nem corrige aquela entrega. Estes resultados não estabelecem ranking geral, especialmente diante da identidade efetiva incerta do segundo modelo.

## Próximo passo

Executar `bb_cure_005` nos dois serviços, em conversas novas, usando exclusivamente o pacote e as instruções dessa variante. Registrar a configuração exibida e qualquer incerteza sobre a identidade efetiva. Preservar a primeira entrega, sem dicas específicas baseadas nas notas anteriores.
