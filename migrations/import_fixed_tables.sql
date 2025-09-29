-- Migração: Importar as tabelas fixas alimentos_base_v2.sql e racas_caninas_seed.sql

-- Este script serve como um wrapper para importar os scripts existentes
-- Ele verifica se as tabelas já existem antes de tentar importar os scripts

-- Verificar e importar alimentos_base_v2.sql
DO $$
BEGIN
    -- Verificar se a tabela alimentos_base já existe
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables 
                  WHERE table_schema = 'public' 
                  AND table_name = 'alimentos_base') THEN
        -- A tabela não existe, podemos importar o script
        RAISE NOTICE 'Importando alimentos_base_v2.sql...';
        -- Na implementação real, você precisará usar \i para importar o arquivo
        -- ou copiar o conteúdo do arquivo aqui
        -- \i 'c:/Users/andre/OneDrive/Documentos/projetosVS/VeTech/alimentos_base_v2.sql'
    ELSE
        RAISE NOTICE 'A tabela alimentos_base já existe. Pulando importação.';
    END IF;

    -- Verificar se a tabela racas já existe (assumindo que este é o nome da tabela no script racas_caninas_seed.sql)
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables 
                  WHERE table_schema = 'public' 
                  AND table_name = 'racas') THEN
        -- A tabela não existe, podemos importar o script
        RAISE NOTICE 'Importando racas_caninas_seed.sql...';
        -- Na implementação real, você precisará usar \i para importar o arquivo
        -- ou copiar o conteúdo do arquivo aqui
        -- \i 'c:/Users/andre/OneDrive/Documentos/projetosVS/VeTech/racas_caninas_seed.sql'
    ELSE
        RAISE NOTICE 'A tabela racas já existe. Verificando se precisa atualizar...';
        
        -- Opcional: Verificar se a tabela racas precisa ser atualizada
        -- Por exemplo, verificar se todas as raças estão presentes
        -- Esta é apenas uma sugestão, você precisará adaptar conforme necessário
        IF (SELECT COUNT(*) FROM public.racas) < 100 THEN -- Assumindo que deveria haver pelo menos 100 raças
            RAISE NOTICE 'A tabela racas parece incompleta. Considere atualizá-la.';
            -- Você pode adicionar lógica para atualizar a tabela aqui
        END IF;
    END IF;
END
$$;

-- Nota importante: Este script é apenas um wrapper e não contém o conteúdo real dos scripts
-- alimentos_base_v2.sql e racas_caninas_seed.sql. Na implementação real, você precisará:
-- 1. Usar \i para importar os arquivos diretamente (em ferramentas como psql)
-- 2. Ou copiar o conteúdo dos arquivos para este script
-- 3. Ou usar uma ferramenta de migração como Flyway ou Liquibase

-- Instruções para execução manual:
-- 1. Execute este script primeiro para verificar se as tabelas já existem
-- 2. Se as tabelas não existirem, execute os scripts originais:
--    \i 'c:/Users/andre/OneDrive/Documentos/projetosVS/VeTech/alimentos_base_v2.sql'
--    \i 'c:/Users/andre/OneDrive/Documentos/projetosVS/VeTech/racas_caninas_seed.sql'