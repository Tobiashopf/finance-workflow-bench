# Bateria de calibração v1 — desenho para revisão

Status: desenho anterior às execuções. Os exemplos abaixo são pontos de conferência, não casos completos nem resultados de modelos. Ainda não existem pacotes executáveis desta bateria.

## Objetivo

Investigar se variantes dos mecanismos financeiros revelam erros que não apareceram nos quatro pilotos. Não presumimos que os novos casos sejam mais difíceis. Um resultado integralmente correto também será publicado. Os casos 001 e 002, seus avaliadores e resultados permanecem preservados.

A bateria terá quatro variantes curtas da família Borrowing Base, com quatro fechamentos semanais cada. Manteremos as regras contratuais explícitas do caso 002: concentração de 25% por cliente sobre o total elegível original; adiantamento de 80%; teto de USD 200 mil; caixa mínimo de USD 50 mil; juros semanais de 0,2%; prioridade da amortização obrigatória; elegibilidade e arredondamentos já definidos. Cada variante terá identidade própria.

## Variantes propostas

| ID planejado | Situação profissional | Erro que queremos detectar | Evidência exigida |
|---|---|---|---|
| bb_rounding_003 | Carteira com centavos e dívida que produz meio centavo de juros | Arredondar garantia para o mais próximo, arredondar só no final ou truncar juros | Limite por cliente, base e juros exatos em centavos |
| bb_customer_004 | Várias faturas elegíveis do mesmo cliente | Aplicar concentração por fatura em vez de por cliente | Reconciliação fatura → cliente → garantia |
| bb_cure_005 | Garantia cai, amortização é integralmente paga, mas falta caixa mínimo | Confundir obrigação quitada com liquidez suficiente ou criar crédito sem limite | Amortização paga, dívida dentro do limite e quebra do mínimo coexistem |
| bb_release_006 | Último snapshot vazio, mas caixa suficiente para quitar toda a dívida | Copiar a conclusão de insolvência do caso 002 ou apagar dívida sem pagamento | Garantia zero, pagamento efetivo da dívida e caixa remanescente positivo |

## Pontos numéricos para revisar

Estes estados são exemplos isolados. Não devem ser concatenados como uma previsão de quatro semanas. A construção dos casos completos deverá gerar trajetórias coerentes e verificar novamente todos os fechamentos.

### 003 — arredondamento em etapas

Recebíveis elegíveis por cliente: A = 100.000,03; B = 80.000,02; C = 60.000,01. Total S = 240.000,06. O teto por cliente é floor(25% × S) = 60.000,01. Reconhecido H = 180.000,03. A base é floor(80% × H) = 144.000,02.

Separadamente, dívida de abertura de 150.002,50 gera juros de 300,005, arredondados half-up para 300,01. Esse estado de dívida deverá ser alcançado por fluxos anteriores válidos ou ser explicitamente definido no contrato do novo caso; não se altera silenciosamente o contrato fixo do caso 002.

### 004 — concentração por cliente

A possui três faturas de 40.000,00; B, C e D possuem uma fatura de 40.000,00 cada. Total elegível = 240.000,00; teto por cliente = 60.000,00. A contribui com 60.000,00, e os demais com 40.000,00 cada. Reconhecido = 180.000,00; limite efetivo = 144.000,00.

O erro de limitar cada fatura separadamente reconheceria 240.000,00 e produziria limite de 192.000,00. Esse resultado deliberadamente incorreto será uma submissão de controle, nunca o gabarito.

### 005 — obrigação quitada, mínimo descumprido

Caixa inicial de 60.000,00, dívida de 150.000,00, entradas de 80.000,00, saídas de 40.000,00 e limite efetivo de 104.000,00. Juros = 300,00; caixa antes do financiamento = 99.700,00. A amortização obrigatória de 46.000,00 é integralmente paga. Sobram 53.700,00; a amortização voluntária é 3.700,00, encerrando com caixa de 50.000,00 e dívida de 100.300,00.

No cenário pareado, somente as entradas caem para 70.000,00. O caixa antes do financiamento fica em 89.700,00. A mesma amortização obrigatória é paga, mas o caixa final fica em 43.700,00 e a dívida em 104.000,00. Não há capacidade para sacar; falta 6.300,00 para o mínimo. A dívida acima do limite e o déficit de caixa são ambos zero. Os dois estados serão usados para conferir a transição de regime.

### 006 — garantia zero sem déficit

Snapshot explicitamente vazio, limite zero, caixa de abertura de 60.000,00, dívida de 150.000,00, entradas de 200.000,00 e saídas de 40.000,00. Após juros de 300,00, o caixa disponível é 219.700,00. A amortização obrigatória de 150.000,00 quita a dívida; caixa final de 69.700,00, sem dívida acima do limite, sem quebra do mínimo e sem déficit.

Snapshot vazio significa ausência de garantia elegível, não ausência automática de caixa. Os recebimentos serão eventos explícitos no arquivo de caixa, não inferidos do desaparecimento das faturas.

## Construção e validação antes das execuções

1. Construir dados sintéticos de quatro semanas por variante, identificadores próprios, tarefa e schema correspondentes. Evitar mudanças não relacionadas à hipótese principal.
2. Gerar a referência e conferir com uma implementação em centavos inteiros, além dos pontos manuais acima. Os dois cálculos continuam sendo desenvolvimento assistido por IA, não auditoria independente.
3. Adaptar o avaliador para selecionar casos apenas por um registro confiável do operador, com hashes fixos. Os avaliadores atuais são específicos dos casos antigos; não devem ser usados diretamente nos novos dados nem aceitar gabaritos indicados pelo candidato.
4. Criar controles incorretos para cada erro-alvo e controles corretos que exercitem ambos os lados dos limites. Verificar invariância dos totais ao reordenar registros e dividir uma fatura elegível em duas do mesmo cliente, preservando os demais atributos e o total. A comparação por registro deverá refletir os novos IDs.
5. Revisar referências, instruções e pacote. Fixar versão e hashes antes de enviar a modelos. O pacote deve excluir gabaritos, este documento, controles e relatórios.

## Protocolo das próximas execuções

- Planejar uma entrega por modelo por variante: quatro variantes × dois modelos = oito execuções. É uma bateria exploratória, sem estimativa de confiabilidade por repetição.
- Uma conversa nova por execução, sem respostas de outros casos. Desativar memória quando possível; registrar explicitamente quando não for possível. Não tratar diretório separado como isolamento comprovado.
- Usar apenas o ZIP da variante e suas instruções internas, verificando o ID antes do envio. Nenhuma instrução adicional de outro caso.
- Permitir ferramentas locais de cálculo e leitura; pedir ausência de navegação. Registrar separadamente o que foi solicitado, observado e apenas declarado pelo modelo.
- Uma tentativa significa uma solução submetida, podendo conter depuração interna. Não fornecer feedback de nota para correção. Falhas de ferramentas e repetições ficam documentadas; não substituir resultados desfavoráveis.
- Registrar o nome exibido do modelo, modo de raciocínio, início/fim quando disponíveis, ferramentas, dicas, memória, conversa nova e intervenções. Desconhecidos ficam nulos.
- Avaliar resultados exatos, status de entrega e erros por mecanismo. Usar revisão textual humana separada. Não comparar velocidade, custo ou ferramentas sem registros equivalentes.

## Como interpretar

Preservar os quatro pilotos como desenvolvimento exploratório. Esta bateria também será de desenvolvimento e não um conjunto secreto de teste. Se ambos os modelos acertarem tudo, relatar ausência de discriminação observada. Qualquer nova hipótese ou mudança após observar respostas pertence a uma nova versão; não se alteram retroativamente critérios ou resultados.

## Revisão solicitada ao responsável

Conferir principalmente: concentração agregada por cliente (004); obrigação integralmente quitada coexistindo com caixa abaixo do mínimo (005); garantia zero coexistindo com solvência (006). A etapa seguinte é implementar os dados completos e os pacotes; nenhuma nova execução externa é necessária agora.
