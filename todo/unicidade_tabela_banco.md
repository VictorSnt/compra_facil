### Regras de Negócio para Unicidade nas Tabelas

1. *Unicidade na Tabela items_compra:*
   - *Descrição:* Na tabela items_compra, a combinação dos campos quotation_id e iddetalhe deve ser única.
   - *Regra:*
     - A combinação de quotation_id e iddetalhe deve ser única na tabela items_compra.

2. *Unicidade na Tabela quotation_submit:*
   - *Descrição:* Na tabela quotation_submit, a combinação dos campos user_id e quotation_id deve ser única.
   - *Regra:*
     - A combinação de user_id e quotation_id deve ser única na tabela quotation_submit.