-- Migração: Unificar as tabelas de dieta (dietas, opcoes_dieta, alimentos_dieta, alimentos_evitar) em uma única tabela public.dietas

-- Criar nova tabela unificada de dietas
CREATE TABLE IF NOT EXISTS public.dietas_nova (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    animal_id UUID NOT NULL REFERENCES public.animals(id) ON DELETE CASCADE,
    clinic_id UUID NOT NULL REFERENCES public.clinics(id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL, -- Tipo da dieta (ex: caseira, ração, mista)
    objetivo VARCHAR(50) NOT NULL, -- Objetivo da dieta (ex: perda de peso, ganho de massa, manutenção)
    data_inicio DATE NOT NULL,
    data_fim DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'ativa', -- ativa, inativa, concluída
    refeicoes_por_dia INTEGER NOT NULL,
    calorias_totais_dia INTEGER,
    valor_mensal_estimado NUMERIC,
    alimento_id BIGINT REFERENCES public.alimentos_base(alimento_id), -- FK para tabela de alimentos base
    quantidade_gramas INTEGER, -- Quantidade em gramas do alimento
    horario VARCHAR(20), -- Horário da refeição
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Criar índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_dietas_nova_animal_id ON public.dietas_nova(animal_id);
CREATE INDEX IF NOT EXISTS idx_dietas_nova_clinic_id ON public.dietas_nova(clinic_id);
CREATE INDEX IF NOT EXISTS idx_dietas_nova_alimento_id ON public.dietas_nova(alimento_id) WHERE alimento_id IS NOT NULL;

-- Migrar dados das tabelas antigas para a nova tabela
-- Este é um exemplo simplificado. Na implementação real, você precisará ajustar
-- conforme a estrutura exata dos seus dados e garantir que todos os dados importantes sejam migrados.
DO $$
DECLARE
    dieta_rec RECORD;
    opcao_rec RECORD;
    alimento_rec RECORD;
BEGIN
    -- Verificar se as tabelas antigas existem antes de tentar migrar
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'dietas') AND
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'opcoes_dieta') AND
       EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'alimentos_dieta') THEN
        
        -- Para cada dieta existente
        FOR dieta_rec IN SELECT * FROM public.dietas LOOP
            -- Para cada opção de dieta associada a esta dieta
            FOR opcao_rec IN SELECT * FROM public.opcoes_dieta WHERE dieta_id = dieta_rec.id LOOP
                -- Para cada alimento associado a esta opção de dieta
                FOR alimento_rec IN SELECT * FROM public.alimentos_dieta WHERE opcao_dieta_id = opcao_rec.id LOOP
                    -- Inserir na nova tabela unificada
                    -- Nota: alimento_id será NULL aqui pois precisamos mapear os alimentos antigos para os novos
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
    END IF;
END
$$;

-- Após migração bem-sucedida, você pode renomear as tabelas
-- IMPORTANTE: Estas operações devem ser executadas apenas após verificar que a migração foi bem-sucedida
-- e fazer backup das tabelas antigas

-- Comentado para segurança - descomente após verificar a migração
/*
ALTER TABLE public.dietas RENAME TO dietas_old;
ALTER TABLE public.opcoes_dieta RENAME TO opcoes_dieta_old;
ALTER TABLE public.alimentos_dieta RENAME TO alimentos_dieta_old;
ALTER TABLE public.alimentos_evitar RENAME TO alimentos_evitar_old;

ALTER TABLE public.dietas_nova RENAME TO dietas;
*/

-- Trigger para atualizar o campo updated_at automaticamente
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_dietas_nova_modtime
BEFORE UPDATE ON public.dietas_nova
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();