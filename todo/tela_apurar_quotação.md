### Regras de Negócio para a Tela de Compra

1. *Tabela de Produtos da Cotação:*
   - *Descrição:* Exibir uma tabela com todos os produtos associados à cotação a ser comprada.
   - *Fields:*
     - *Descrição:* Exibe a descrição do produto.
     - *Quantidade Cotada (qtcotada):* Exibe a quantidade de produto cotada.
     - *Botão de Escolher Fornecedor:* Permite selecionar um fornecedor para o produto, apartir dos dados de process_quotations apenas do produto filtrado
     - *Fornecedor Escolhido:* Exibe o fornecedor escolhido ou null se nenhum fornecedor tiver sido selecionado. Esta informação deve ser consultada na tabela compras utilizando o quotation_id.

2. *Botão de Visão Geral:*
   - *Descrição:* Abre um modal que exibe uma visão geral dos processos de cotação.
   - *Modal:*
     - *Tabela de Processos de Cotação (process_quotations):*
       - Exibe todos os processos de cotação associados ao pedido atual.
     - *Botão de Compra:*
       - Permite lançar o pedido para o fornecedor selecionado.
       - Ao clicar, o pedido é registrado no sistema e a tabela principal de produtos é atualizada para refletir o fornecedor escolhido nos itens correspondentes.

### Fluxo de Interação

1. *Exibição Inicial:*
   - A tabela de produtos é carregada com os campos descrição, qtcotada, botão de escolher fornecedor, e fornecedor escolhido.
   - Para cada produto, o campo fornecedor escolhido é consultado na tabela compras utilizando o quotation_id.

2. *Seleção de Fornecedor:*
   - O usuário clica no botão de escolher fornecedor para selecionar um fornecedor para um produto específico.
   - O sistema atualiza o campo fornecedor escolhido com a escolha do usuário.

3. *Visão Geral:*
   - O usuário clica no botão de visão geral para abrir o modal.
   - O modal exibe a tabela com o process_quotations e a opção de criar_pedido.

4. *criar_pedido:*
   - No modal, o usuário clica no botão de compra para registrar o pedido com o fornecedor selecionado.
   - O sistema registra o pedido no banco de dados.
   - Após o registro, a tabela principal é atualizada para refletir o fornecedor escolhido nos itens correspondentes.