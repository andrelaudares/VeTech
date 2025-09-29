# Limpeza do Banco de Dados VeTech

## Visão Geral

Este documento descreve o processo de limpeza do banco de dados do sistema VeTech, focando na migração das tabelas de dietas e na identificação e remoção de tabelas obsoletas.

## Tabelas Obsoletas Identificadas

As seguintes tabelas foram identificadas como parte do antigo sistema de dietas e serão substituídas pela nova estrutura unificada:

1. **dietas** - Tabela principal de dietas (7 registros)
2. **opcoes_dieta** - Opções de dieta associadas a cada dieta (5 registros)
3. **alimentos_dieta** - Alimentos associados a cada opção de dieta (0 registros)
4. **alimentos_evitar** - Alimentos a serem evitados em dietas específicas (4 registros)

Estas tabelas serão substituídas pela nova tabela unificada **dietas_nova**, que posteriormente será renomeada para **dietas**.

## Tabelas Sem Referências

As seguintes tabelas foram identificadas como não tendo referências de chave estrangeira, o que pode indicar que não estão sendo utilizadas pelo sistema ou que são tabelas de suporte sem relações diretas:

1. **racas** (104 kB)
2. **appointments** (96 kB)
3. **gamificacao_pontuacoes** (64 kB)
4. **preferencias_pet** (48 kB)
5. **alimentos_evitar** (48 kB)
6. **gamificacao_recompensas_atribuidas** (40 kB)
7. **dietas_nova** (40 kB)
8. **dieta_progresso** (40 kB)
9. **consultations** (32 kB)
10. **snacks_entre_refeicoes** (24 kB)
11. **messages** (16 kB)
12. **alimentos_dieta** (16 kB)

É importante verificar cada uma dessas tabelas individualmente para determinar se ainda são necessárias para o funcionamento do sistema antes de considerar sua remoção.

## Scripts de Limpeza

Foram criados três scripts para auxiliar no processo de limpeza do banco de dados:

1. **drop_old_dietas_tables.sql** - Script específico para a migração e remoção das tabelas antigas de dietas.
2. **cleanup_database.sql** - Script mais abrangente que inclui a migração das tabelas de dietas e também identifica outras tabelas potencialmente obsoletas.
3. **add_alimento_base_fk_to_dietas.sql** - Script para garantir que a chave estrangeira para a tabela alimentos_base esteja corretamente configurada na tabela dietas após a migração.

## Processo de Migração e Limpeza

O processo de limpeza deve seguir estas etapas:

1. **Backup do Banco de Dados** - Sempre faça um backup completo do banco de dados antes de executar qualquer script de migração ou limpeza.

2. **Migração de Dados** - Execute o script `unify_dietas_tables.sql` para criar a nova tabela unificada e migrar os dados das tabelas antigas.

3. **Verificação da Migração** - Verifique se os dados foram migrados corretamente para a nova tabela `dietas_nova`.

4. **Renomeação de Tabelas** - Execute a primeira parte do script `cleanup_database.sql` para renomear as tabelas antigas com sufixo `_old` e renomear `dietas_nova` para `dietas`.

5. **Verificação da Chave Estrangeira** - Execute o script `add_alimento_base_fk_to_dietas.sql` para garantir que a chave estrangeira para a tabela alimentos_base esteja corretamente configurada.

6. **Teste do Sistema** - Teste o sistema com a nova estrutura de tabelas para garantir que tudo está funcionando corretamente.

7. **Remoção de Tabelas Obsoletas** - Após confirmar que o sistema está funcionando corretamente, descomente e execute a segunda parte do script `cleanup_database.sql` para remover permanentemente as tabelas obsoletas.

## Considerações Importantes

- **Nunca** execute scripts de exclusão sem antes verificar se a migração foi bem-sucedida e que o sistema está funcionando corretamente com a nova estrutura.

- Mantenha backups do banco de dados antes e depois de cada etapa do processo de migração e limpeza.

- Algumas tabelas sem referências podem ainda ser utilizadas pelo sistema através de consultas diretas. Verifique o código da aplicação antes de remover qualquer tabela.

- As tabelas relacionadas à gamificação (`gamificacao_pontuacoes`, `gamificacao_recompensas_atribuidas`, etc.) podem ser parte de um módulo em desenvolvimento e não devem ser removidas sem verificação adicional.

- A chave estrangeira para `alimentos_base` na tabela `dietas` é importante para a funcionalidade do sistema. O script `add_alimento_base_fk_to_dietas.sql` verifica e adiciona essa chave estrangeira se necessário, além de verificar se os dados foram migrados corretamente com os valores de `alimento_id`.

## Próximos Passos

1. Executar o script de migração e verificar os dados na nova tabela.
2. Atualizar o código da aplicação para utilizar a nova estrutura de tabelas.
3. Após testes completos, remover as tabelas obsoletas.
4. Documentar a nova estrutura do banco de dados para referência futura.