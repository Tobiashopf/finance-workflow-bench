# Primeira rodada manual — instruções para Tobias

## O que está pronto

O pacote `packages/cash_forecast_001-v0.2/agent-package.zip` contém somente oito arquivos: tarefa, esquema de resposta, instruções e os cinco arquivos de dados. Não contém solução, código do avaliador, testes, relatórios ou exemplos de respostas.

A rodada `runs/manual-pilot-001` está preparada, mas nenhum modelo foi executado. Não há integração de API nem cobrança por execução feita pelo projeto. A sua assinatura e os limites do serviço continuam sujeitos às condições do serviço que você usa.

Esta é uma avaliação exploratória de um caso público. Ela não é uma comparação controlada entre modelos nem uma estimativa geral de competência financeira.

## 1. Abra uma conversa nova no chat que você já assina

Não use esta conversa de construção: ela contém a solução. Use uma conversa sem anexos ou mensagens anteriores sobre este projeto. Não coloque o repositório inteiro à disposição do modelo.

Anote o nome do serviço e o nome exato do modelo mostrado na interface. Se uma versão técnica não estiver disponível, registraremos essa informação como desconhecida. Não deduza a versão pelo estilo da resposta.

## 2. Envie apenas o pacote do agente

Anexe `agent-package.zip`. Se o serviço não aceitar ZIP, extraia esse pacote e anexe somente os oito arquivos extraídos, preservando os nomes. Não anexe o README do repositório, arquivos `reference`, relatórios ou exemplos.

Se o serviço não conseguir ler os arquivos necessários, registre a limitação e pare essa tentativa. Não cole números da solução para ajudá-lo.

## 3. Copie as instruções iniciais

Copie integralmente o conteúdo de `prompts/agent_instructions.md` como a primeira mensagem. Esse mesmo texto está dentro do ZIP.

O modelo deverá ler `task.md`, usar os dados e devolver `forecast.json` e `analysis.md`. Ele pode usar uma ferramenta de cálculo/Python, caso o chat ofereça isso. Não peça busca na internet. Se houver controle visível de navegação, mantenha-a desativada para esta tentativa e registre a configuração observada.

## 4. Deixe o modelo concluir uma tentativa

Não forneça dicas, correções, respostas esperadas ou notas do avaliador durante a tentativa. Não selecione a melhor entre várias respostas regeneradas. Se você quiser tentar novamente, isso será registrado como outra rodada.

Registre as ferramentas realmente utilizadas, conforme o que a interface mostrar, e eventuais problemas. Se puder, anote o início e o fim. Horários e duração desconhecidos permanecem desconhecidos; não precisamos estimá-los.

Se o modelo pedir esclarecimentos, registre a pergunta. Para manter esta primeira tentativa sem intervenção, não complete regras com a solução; registre a tentativa como incompleta ou interrompida. Isso não impede criar depois um protocolo distinto com esclarecimentos, desde que seja identificado separadamente.

## 5. Baixe os resultados sem corrigir

Guarde os dois arquivos com os nomes originais. Se o modelo retornar somente blocos de código, salve exatamente o conteúdo indicado para cada arquivo, sem alterar números, texto ou estrutura, e informe que houve transferência manual.

Se possível, guarde também o histórico dessa tentativa em texto (`transcript.txt`), incluindo sua mensagem inicial, respostas e ferramentas visíveis. Não inclua conversas pessoais ou dados de outras tarefas. Se o histórico não estiver disponível, registraremos a ausência.

Uma resposta ausente ou inválida é um resultado útil. Não conserte o arquivo antes de trazê-lo para a avaliação.

## 6. Volte a esta conversa

Anexe os arquivos produzidos ou indique onde foram salvos. Diga também:

- Serviço e modelo utilizados, conforme a interface.
- Se o modelo usou Python/análise de dados, navegação ou outras ferramentas.
- Se foi uma única tentativa em conversa nova, sem dicas adicionais.
- Se houve erro, interrupção ou necessidade de copiar os blocos manualmente.

Eu registrarei os metadados, preservarei uma cópia exata dos arquivos, executarei o avaliador e apresentarei os erros encontrados. Você não precisa editar JSON de configuração nem executar comandos.

## Como serão registrados custo e limites

Tokenização e custo por mensagem costumam não estar disponíveis no uso manual. Registraremos campos desconhecidos como `null`, não como zero. A mensalidade não será convertida artificialmente em custo desta execução. Configurações e ferramentas serão informações relatadas pelo operador, não telemetria verificada automaticamente.

## Limite de isolamento desta rodada

O pacote foi verificado para não incluir respostas. Isso separa os materiais enviados, mas não audita o ambiente interno do provedor, memórias, treinamento prévio ou acesso real à rede. Não foram encontrados executáveis Docker ou Podman no PATH deste computador durante a preparação; não foi instalado software nem executado código gerado por modelo localmente.

## Depois da primeira tentativa

Separaremos os resultados numéricos da revisão da explicação. Em seguida, poderemos repetir o mesmo protocolo com outro modelo ou ampliar os casos. Uma comparação só será apresentada com as diferenças de ferramentas, contexto, intervenções e condições explicitadas.
