-- Script para adicionar chave estrangeira para alimentos_base na tabela dietas (após migração)

-- IMPORTANTE: Este script deve ser executado APÓS o script cleanup_database.sql
-- quando a tabela dietas_nova já tiver sido renomeada para dietas

DO $$
BEGIN
    -- Verificar se a tabela dietas existe (após renomeação de dietas_nova)
    IF EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name = 'dietas'
    ) THEN
        -- Verificar se a chave estrangeira já existe
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.table_constraints
            WHERE constraint_name = 'dietas_alimento_id_fkey'
            AND table_name = 'dietas'
            AND constraint_type = 'FOREIGN KEY'
        ) THEN
            -- Adicionar a chave estrangeira se não existir
            EXECUTE 'ALTER TABLE public.dietas ADD CONSTRAINT dietas_alimento_id_fkey 
                     FOREIGN KEY (alimento_id) REFERENCES public.alimentos_base(alimento_id)';
            
            -- Criar índice para melhorar performance
            EXECUTE 'CREATE INDEX IF NOT EXISTS idx_dietas_alimento_id 
                     ON public.dietas(alimento_id) WHERE alimento_id IS NOT NULL';
            
            RAISE NOTICE 'Chave estrangeira para alimentos_base adicionada com sucesso à tabela dietas.';
        ELSE
            RAISE NOTICE 'A chave estrangeira para alimentos_base já existe na tabela dietas.';
        END IF;
    ELSE
        RAISE EXCEPTION 'A tabela dietas não existe. Execute primeiro o script cleanup_database.sql.';
    END IF;
END
$$;

-- Verificar se a migração de dados incluiu os alimentos_id corretamente
DO $$
DECLARE
    total_dietas INTEGER;
    dietas_com_alimento INTEGER;
BEGIN
    -- Contar total de dietas
    SELECT COUNT(*) INTO total_dietas FROM public.dietas;
    
    -- Contar dietas com alimento_id não nulo
    SELECT COUNT(*) INTO dietas_com_alimento FROM public.dietas WHERE alimento_id IS NOT NULL;
    
    RAISE NOTICE 'Total de dietas: %', total_dietas;
    RAISE NOTICE 'Dietas com alimento_id: %', dietas_com_alimento;
    RAISE NOTICE 'Porcentagem de dietas com alimento_id: %', 
                 CASE WHEN total_dietas > 0 THEN 
                    ROUND((dietas_com_alimento::numeric / total_dietas) * 100, 2) 
                 ELSE 0 END || '%';
    
    -- Alerta se nenhuma dieta tiver alimento_id
    IF dietas_com_alimento = 0 AND total_dietas > 0 THEN
        RAISE WARNING 'ATENÇÃO: Nenhuma dieta possui alimento_id. Pode ser necessário mapear manualmente os alimentos.';
    END IF;
END
$$;