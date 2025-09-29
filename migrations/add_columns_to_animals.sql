-- Migração: Adicionar colunas 'altura' e 'sexo' na tabela public.animals

-- Verificar se as colunas já existem antes de adicioná-las
DO $$
BEGIN
    -- Adicionar coluna 'altura' se não existir
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'animals' 
                  AND column_name = 'altura') THEN
        ALTER TABLE public.animals ADD COLUMN altura NUMERIC;
        COMMENT ON COLUMN public.animals.altura IS 'Altura do animal em centímetros';
    END IF;

    -- Adicionar coluna 'sexo' se não existir
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_schema = 'public' 
                  AND table_name = 'animals' 
                  AND column_name = 'sexo') THEN
        ALTER TABLE public.animals ADD COLUMN sexo VARCHAR(10);
        COMMENT ON COLUMN public.animals.sexo IS 'Sexo do animal (Macho/Fêmea)';
    END IF;
END
$$;