-- Migração: Adicionar colunas 'objetivo' e 'tipo_alimento_preferencia' na tabela public.preferencias_pet

DO $$
BEGIN
    -- Adicionar coluna 'objetivo' se não existir
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'preferencias_pet' 
                  AND column_name = 'objetivo') THEN
        ALTER TABLE public.preferencias_pet ADD COLUMN objetivo VARCHAR(50);
        COMMENT ON COLUMN public.preferencias_pet.objetivo IS 'Objetivo da dieta (ex: perda de peso, ganho de massa, manutenção)';
    END IF;

    -- Adicionar coluna 'tipo_alimento_preferencia' se não existir
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'preferencias_pet' 
                  AND column_name = 'tipo_alimento_preferencia') THEN
        ALTER TABLE public.preferencias_pet ADD COLUMN tipo_alimento_preferencia VARCHAR(20);
        COMMENT ON COLUMN public.preferencias_pet.tipo_alimento_preferencia IS 'Tipo de alimento preferido (caseiro ou ração)';
    END IF;
END
$$;