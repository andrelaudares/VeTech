-- Script para limpeza do banco de dados e remoção de tabelas obsoletas

-- IMPORTANTE: Este script deve ser executado SOMENTE após verificar que a migração
-- das tabelas de dietas foi concluída com sucesso e que o sistema está funcionando
-- adequadamente com a nova estrutura.

-- Parte 1: Migração das tabelas de dietas
-- Verificar se a migração foi concluída (dietas_nova deve ter dados)
DO $$
DECLARE
    dieta_rec RECORD;
    opcao_rec RECORD;
    alimento_rec RECORD;
BEGIN
    -- Verificar se a tabela dietas_nova existe
    IF EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name = 'dietas_nova'
    ) THEN
        -- Migrar dados se ainda não foram migrados
        IF (SELECT COUNT(*) FROM public.dietas_nova) = 0 AND 
           EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'dietas') AND
           EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'opcoes_dieta') THEN
            
            RAISE NOTICE 'Iniciando migração de dados para dietas_nova...';
            
            -- Código de migração (similar ao do arquivo unify_dietas_tables.sql)
            -- Para cada dieta existente
            FOR dieta_rec IN SELECT * FROM public.dietas LOOP
                -- Para cada opção de dieta associada a esta dieta
                FOR opcao_rec IN SELECT * FROM public.opcoes_dieta WHERE dieta_id = dieta_rec.id LOOP
                    -- Para cada alimento associado a esta opção de dieta
                    FOR alimento_rec IN SELECT * FROM public.alimentos_dieta WHERE opcao_dieta_id = opcao_rec.id LOOP
                        -- Inserir na nova tabela unificada
                        INSERT INTO public.dietas_nova (
                            animal_id, clinic_id, nome, tipo, objetivo, data_inicio, status,
                            refeicoes_por_dia, calorias_totais_dia, valor_mensal_estimado,
                            quantidade_gramas, horario
                        ) VALUES (
                            dieta_rec.animal_id,
                            dieta_rec.clinic_id,
                            opcao_rec.nome,
                            dieta_rec.tipo,
                            dieta_rec.objetivo,
                            dieta_rec.data_inicio,
                            dieta_rec.status,
                            opcao_rec.refeicoes_por_dia,
                            opcao_rec.calorias_totais_dia,
                            opcao_rec.valor_mensal_estimado,
                            -- Converter quantidade para gramas se necessário
                            (CASE 
                                WHEN alimento_rec.quantidade ~ '^\d+$' THEN alimento_rec.quantidade::INTEGER
                                ELSE 0 -- Valor padrão se não for possível converter
                             END),
                            alimento_rec.horario
                        );
                    END LOOP;
                END LOOP;
            END LOOP;
            
            RAISE NOTICE 'Migração de dados concluída com sucesso!';
        END IF;
        
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
        RAISE EXCEPTION 'A tabela dietas_nova não existe. Execute primeiro o script de migração unify_dietas_tables.sql.';
    END IF;
END
$$;

-- Parte 2: Exclusão de tabelas obsoletas
-- IMPORTANTE: Descomente este bloco SOMENTE após verificar que o sistema está funcionando corretamente
-- com a nova estrutura de tabelas

/*
DO $$
BEGIN
    -- Excluir tabelas antigas de dietas
    DROP TABLE IF EXISTS public.dietas_old;
    DROP TABLE IF EXISTS public.opcoes_dieta_old;
    DROP TABLE IF EXISTS public.alimentos_dieta_old;
    DROP TABLE IF EXISTS public.alimentos_evitar_old;
    
    -- Verificar e excluir outras tabelas potencialmente obsoletas
    -- Estas tabelas foram identificadas como não tendo referências de chave estrangeira
    -- e podem não estar sendo usadas pelo sistema
    
    -- ATENÇÃO: Verifique cada tabela antes de descomentar sua exclusão!
    -- DROP TABLE IF EXISTS public.snacks_entre_refeicoes; -- Verificar se ainda é usada
    -- DROP TABLE IF EXISTS public.dieta_progresso; -- Verificar se ainda é usada
    
    RAISE NOTICE 'Tabelas obsoletas excluídas com sucesso.';
END
$$;
*/

-- Parte 3: Verificação de integridade do banco de dados
-- Este bloco verifica se há tabelas sem referências ou potencialmente não utilizadas

DO $$
DECLARE
    tabela_rec RECORD;
BEGIN
    RAISE NOTICE 'Tabelas sem referências de chave estrangeira (potencialmente não utilizadas):';
    
    FOR tabela_rec IN 
        SELECT t.table_name,
               pg_size_pretty(pg_total_relation_size(quote_ident(t.table_name))) as table_size,
               (SELECT COUNT(*) FROM pg_constraint c WHERE c.confrelid = quote_ident(t.table_name)::regclass) as referenced_by_count
        FROM information_schema.tables t
        WHERE t.table_schema = 'public'
        AND t.table_type = 'BASE TABLE'
        AND (SELECT COUNT(*) FROM pg_constraint c WHERE c.confrelid = quote_ident(t.table_name)::regclass) = 0
        AND t.table_name NOT LIKE '%_old'
        ORDER BY pg_total_relation_size(quote_ident(t.table_name)) DESC
    LOOP
        RAISE NOTICE 'Tabela: %, Tamanho: %, Referências: %', 
                     tabela_rec.table_name, 
                     tabela_rec.table_size, 
                     tabela_rec.referenced_by_count;
    END LOOP;
    
    RAISE NOTICE 'Verifique estas tabelas manualmente para determinar se ainda são necessárias.';
END
$$;