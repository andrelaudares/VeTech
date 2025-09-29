-- Script para excluir tabelas antigas de dietas após migração bem-sucedida

-- IMPORTANTE: Execute este script SOMENTE após verificar que todos os dados foram migrados corretamente
-- para a tabela dietas_nova e que o sistema está funcionando adequadamente com a nova estrutura.

-- Verificar se a migração foi concluída (dietas_nova deve ter dados)
DO $$
BEGIN
    -- Verificar se a tabela dietas_nova existe e tem dados
    IF EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name = 'dietas_nova'
    ) AND (
        SELECT COUNT(*) FROM public.dietas_nova
    ) > 0 THEN
        -- Renomear tabelas antigas para _old antes de excluir (backup de segurança)
        EXECUTE 'ALTER TABLE IF EXISTS public.dietas RENAME TO dietas_old';
        EXECUTE 'ALTER TABLE IF EXISTS public.opcoes_dieta RENAME TO opcoes_dieta_old';
        EXECUTE 'ALTER TABLE IF EXISTS public.alimentos_dieta RENAME TO alimentos_dieta_old';
        EXECUTE 'ALTER TABLE IF EXISTS public.alimentos_evitar RENAME TO alimentos_evitar_old';
        
        -- Renomear dietas_nova para dietas
        EXECUTE 'ALTER TABLE public.dietas_nova RENAME TO dietas';
        
        -- Atualizar o nome do trigger para refletir o novo nome da tabela
        EXECUTE 'ALTER TRIGGER update_dietas_nova_modtime ON public.dietas RENAME TO update_dietas_modtime';
        
        RAISE NOTICE 'Tabelas antigas renomeadas com sucesso e dietas_nova renomeada para dietas.';
    ELSE
        RAISE EXCEPTION 'A migração não foi concluída ou a tabela dietas_nova não contém dados. Operação cancelada.';
    END IF;
END
$$;

-- Após verificar que tudo está funcionando corretamente com as tabelas renomeadas,
-- execute o seguinte bloco para excluir permanentemente as tabelas antigas

/*
DO $$
BEGIN
    -- Excluir tabelas antigas
    DROP TABLE IF EXISTS public.dietas_old;
    DROP TABLE IF EXISTS public.opcoes_dieta_old;
    DROP TABLE IF EXISTS public.alimentos_dieta_old;
    DROP TABLE IF EXISTS public.alimentos_evitar_old;
    
    RAISE NOTICE 'Tabelas antigas excluídas com sucesso.';
END
$$;
*/