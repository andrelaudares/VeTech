-- =============================================================
-- Tabela única de alimentos (caseiros + ração) para cães - CORRIGIDA
-- Ajuste: UNIQUE com expressões substituído por UNIQUE INDEX funcional
-- PostgreSQL >= 12
-- =============================================================

CREATE EXTENSION IF NOT EXISTS citext;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_alimento') THEN
        CREATE TYPE tipo_alimento AS ENUM ('caseiro', 'racao');
    END IF;
END$$;

-- Recriação segura da tabela (se não existir)
CREATE TABLE IF NOT EXISTS alimentos_base (
    alimento_id      BIGSERIAL PRIMARY KEY,
    nome             CITEXT NOT NULL,
    tipo             tipo_alimento NOT NULL,
    especie_destino  CITEXT NOT NULL DEFAULT 'cachorro',
    marca            CITEXT,
    linha            CITEXT,
    subtipo          CITEXT,                    -- 'seca' | 'umida' | NULL
    kcal_por_kg      NUMERIC(8,2),
    kcal_por_100g    NUMERIC(7,2),
    kcal_por_50g     NUMERIC(7,2) GENERATED ALWAYS AS (
                        COALESCE(ROUND(kcal_por_kg * 0.05, 2),
                                 ROUND(kcal_por_100g * 0.50, 2))
                      ) STORED,
    origem_caloria   CITEXT,                    -- 'declarada' | 'estimada' | 'nao_informada'
    fonte            TEXT,
    fonte_url        TEXT,
    observacoes      TEXT,
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Índice único funcional equivalente à antiga constraint
CREATE UNIQUE INDEX IF NOT EXISTS ux_alimentos_base_ident
ON alimentos_base (
  nome,
  tipo,
  COALESCE(marca, ''::citext),
  COALESCE(linha, ''::citext),
  COALESCE(subtipo, ''::citext),
  especie_destino
);

-- (Opcional) Garante que pelo menos uma das kcal foi informada
DO $$
BEGIN
  BEGIN
    ALTER TABLE alimentos_base
      ADD CONSTRAINT kcal_informada_chk
      CHECK (kcal_por_kg IS NOT NULL OR kcal_por_100g IS NOT NULL);
  EXCEPTION WHEN duplicate_object THEN
    -- constraint already exists; ignore
    NULL;
  END;
END $$;
INSERT INTO alimentos_base (nome, tipo, especie_destino, marca, linha, subtipo, kcal_por_kg, kcal_por_100g, origem_caloria, fonte, fonte_url, observacoes) VALUES
  ('Peito de frango cozido (sem pele)', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 157.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/100009715/100g', 'Sem sal/pele; cozido em água.'),
  ('Tilápia cozida', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 128.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/171705/wt1', 'Retirar espinhas.'),
  ('Salmão cozido', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 206.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/171705/wt1', 'Rico em ômega-3; retirar espinhas.'),
  ('Sardinha em lata (em óleo, drenada)', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 208.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/175139/wt1', 'Drenar óleo; atenção a espinhas.'),
  ('Ovo cozido', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 155.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/100133330/wt1', 'Servir bem cozido.'),
  ('Iogurte natural desnatado', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 50.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/2647437/100g', 'Sem açúcar; avaliar tolerância à lactose.'),
  ('Queijo cottage (1% gordura)', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 72.00, 'declarada', 'MyFoodData (USDA)', 'https://foods.fatsecret.com/calories-nutrition/usda/cottage-cheese-%28lowfat-1%25-milkfat%29?portionamount=100.000&portionid=56427', 'Baixo sódio preferível; usar em pequenas porções.'),
  ('Arroz branco cozido', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 130.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/168878/wt1', 'Sem sal/óleo.'),
  ('Arroz integral cozido', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 123.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/169714/wt1', 'Sem sal/óleo.'),
  ('Batata-doce cozida (sem casca)', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 76.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/168484/wt1', 'Baixo IG (cozida).'),
  ('Batata inglesa cozida (sem casca)', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 87.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/173944/wt1', NULL),
  ('Mingau de aveia (cozida em água)', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 71.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/173905/wt1', NULL),
  ('Aveia em flocos (seca)', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 400.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/100102662/wt1', 'Hidratar/cozinhar antes de servir.'),
  ('Quinoa cozida', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 120.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/174732/wt1', NULL),
  ('Cenoura cozida', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 50.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/2710793/100g', 'Picada; boa fonte de fibras e carotenoides.'),
  ('Abóbora cozida', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 20.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/168449/wt1', 'Boa para ajuste de fibra.'),
  ('Abobrinha cozida', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 17.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/173739/wt1', NULL),
  ('Brócolis cozido', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 35.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/174252/wt1', NULL),
  ('Ervilha cozida', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 84.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/174263/wt1', NULL),
  ('Maçã crua (sem sementes)', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 52.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/174736/wt1', 'Remover sementes; servir em cubos.'),
  ('Banana (crua)', 'caseiro', 'ambos', NULL, NULL, NULL, NULL, 89.00, 'declarada', 'MyFoodData (USDA)', 'https://tools.myfooddata.com/nutrition-facts/173944/wt1', 'Porções pequenas por conta dos açúcares.'),
  ('Royal Canin Recovery (lata/paté)', 'racao', 'cachorro', 'Royal Canin', 'Recovery', 'umida', 1146.00, NULL, 'declarada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Umida-Royal-Canin-Recovery-Caes-e-Gatos-3555126/p', 'Energia metabolizável declarada para cães: 1146 Kcal/kg.'),
  ('Royal Canin Mini Light', 'racao', 'cachorro', 'Royal Canin', 'Mini Light', 'seca', 3100.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Royal-Canin-Light-Caes-Adultos-Porte-Pequeno-e-Mini-3510980/p', 'Estimado pela média de rações light secas.'),
  ('Royal Canin Medium Adult', 'racao', 'cachorro', 'Royal Canin', 'Medium Adult', 'seca', 3650.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-royal-canin-medium-adult-3793655/p', 'Estimado para secos adultos.'),
  ('Royal Canin Maxi Adult 5+', 'racao', 'cachorro', 'Royal Canin', 'Maxi Adult 5+', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-royal-canin-maxi-adult-5-mais-caes-3747750/p', 'Estimado para adultos maduros.'),
  ('Royal Canin Satiety Support', 'racao', 'cachorro', 'Royal Canin', 'Satiety Support', 'seca', 3000.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-royal-canin-satiety-caes-adultos-3686646/p', 'Estimado para baixa densidade energética.'),
  ('Royal Canin Hypoallergenic Moderate Calorie', 'racao', 'cachorro', 'Royal Canin', 'Hypoallergenic Moderate Calorie', 'seca', 3400.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Royal-Canin-Caes-Adultos-Veterinary-Hypoallergenic-Moderate-Calorie-3974404/p', 'Estimado.'),
  ('Royal Canin Gastrointestinal High Fibre', 'racao', 'cachorro', 'Royal Canin', 'Gastrointestinal High Fibre', 'seca', 3500.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Royal-Canin-Caes-Gastro-Intestinal-High-Fibre-3970506/p', 'Estimado.'),
  ('Royal Canin Gastrointestinal Moderate Calorie', 'racao', 'cachorro', 'Royal Canin', 'Gastrointestinal Moderate Calorie', 'seca', 3500.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Gastro-Intestinal-Canine-Moderate-Calorie-Royal-Canin-3806617/p', 'Estimado.'),
  ('Pro Plan Puppies Raças Pequenas', 'racao', 'cachorro', 'Purina Pro Plan', 'Puppies Small Breed', 'seca', 4240.00, NULL, 'declarada', 'Purina', 'https://purina.com.br/proplan/caes/puppy/racas-pequenas', 'EM declarada: 4240 kcal/kg.'),
  ('Pro Plan Reduced Calorie Adultos', 'racao', 'cachorro', 'Purina Pro Plan', 'Reduced Calorie', 'seca', 3300.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-purina-pro-plan-reduced-calorie-caes-adultos-calorias-reduzidas-3326429/p', 'Estimado.'),
  ('Pro Plan Adultos 7+ Optiage', 'racao', 'cachorro', 'Purina Pro Plan', 'Adult 7+ Optiage', 'seca', 3500.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-pro-plan-caes-adultos-7-mais-optiage-3961795/p', 'Estimado.'),
  ('GoldeN Formula Adultos Frango e Arroz', 'racao', 'cachorro', 'GoldeN (PremieRpet)', 'Formula Adultos', 'seca', 3797.00, NULL, 'declarada', 'Petlove (Q&A)', 'https://www.petlove.com.br/racao-seca-premier-pet-golden-formula-caes-adultos-frango-e-arroz/pergunta/108777', 'Valor EM informado (pode variar por lote).'),
  ('GoldeN Special Adultos Frango e Carne', 'racao', 'cachorro', 'GoldeN (PremieRpet)', 'Special Adultos', 'seca', 3649.00, NULL, 'declarada', 'Petlove (Q&A)', 'https://www.petlove.com.br/racao-seca-premier-pet-golden-formula-caes-adultos-frango-e-arroz/pergunta/108777', 'Valor EM informado (pode variar por lote).'),
  ('GoldeN Power Training Adultos Frango', 'racao', 'cachorro', 'GoldeN (PremieRpet)', 'Power Training Adultos', 'seca', 4100.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-golden-power-training-adultos-frango-e-arroz-treinamento-e-competicao-3623431/p', 'Estimado.'),
  ('Premier Formula Raças Médias Frango', 'racao', 'cachorro', 'PremieRpet', 'Premier Formula - Raças Médias', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-premier-formula-caes-adultos-racas-medias-sabor-frango-3794589/p', 'Estimado.'),
  ('Premier Formula Raças Pequenas Frango', 'racao', 'cachorro', 'PremieRpet', 'Premier Formula - Raças Pequenas', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-premier-formula-racas-pequenas-caes-adultos-3795267/p', 'Estimado.'),
  ('Premier Formula Raças Grandes e Gigantes Frango', 'racao', 'cachorro', 'PremieRpet', 'Premier Formula - Raças Grandes e Gigantes', 'seca', 3700.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-premier-formula-caes-adultos-racas-grandes-sabor-frango-3299537/p', 'Estimado.'),
  ('GranPlus Menu Adultos Carne e Arroz', 'racao', 'cachorro', 'GranPlus', 'Menu Adultos', 'seca', 3500.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Gran-Plus-Adulto-Carne-e-Arroz-3643068/p', 'Estimado.'),
  ('GranPlus Menu Adultos Mini Carne e Arroz', 'racao', 'cachorro', 'GranPlus', 'Menu Adultos Mini', 'seca', 3500.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Gran-Plus-Caes-Adulto-Mini-Carne-e-Arroz-3903213/p', 'Estimado.'),
  ('Origens Energy Adultos Frango e Cereais', 'racao', 'cachorro', 'Origens', 'Energy Adultos', 'seca', 4000.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-origens-energy-caes-adultos-frango-e-cereais-31138286/p', 'Estimado.'),
  ('Origens Energy Filhotes Frango e Cereais', 'racao', 'cachorro', 'Origens', 'Energy Filhotes', 'seca', 4200.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-origens-energy-caes-filhotes-frango-e-cereais-31138278/p', 'Estimado.'),
  ('Equilíbrio Adultos Porte Mini Frango', 'racao', 'cachorro', 'Equilíbrio', 'Adulto Mini Frango', 'seca', 3700.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-equilibrio-para-caes-adultos-porte-mini-frango-31011537/p', 'Estimado.'),
  ('Equilíbrio Filhotes Porte Médio Frango', 'racao', 'cachorro', 'Equilíbrio', 'Filhote Porte Médio Frango', 'seca', 4000.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-equilibrio-para-caes-filhotes-porte-medio-frango-31011588/p', 'Estimado.'),
  ('Equilíbrio Adultos Porte Grande Carne', 'racao', 'cachorro', 'Equilíbrio', 'Adulto Porte Grande Carne', 'seca', 3650.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-equilibrio-para-caes-adultos-porte-grande-carne-31011723/p', 'Estimado.'),
  ('Equilíbrio Sensíveis Porte Pequeno Cordeiro', 'racao', 'cachorro', 'Equilíbrio', 'Sensíveis Porte Pequeno Cordeiro', 'seca', 3650.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-equilibrio-para-caes-adultos-sensiveis-porte-pequeno-cordeiro-31011456/p', 'Estimado.'),
  ('Equilíbrio Veterinary Obesidade e Diabete', 'racao', 'cachorro', 'Equilíbrio', 'Veterinary Obesidade e Diabete', 'seca', 3100.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-equilibrio-veterinario-caes-obesidade-e-diabete-3681652/p', 'Estimado.'),
  ('Equilíbrio Veterinary Intestinal', 'racao', 'cachorro', 'Equilíbrio', 'Veterinary Intestinal', 'seca', 3500.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Equilibrio-Veterinario-Caes-Intestinal-3681008/p', 'Estimado.'),
  ('Vet Life Obesity & Diabetic (Adultos)', 'racao', 'cachorro', 'Farmina Vet Life', 'Obesity & Diabetic', 'seca', 3000.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Vet-Life-Canine-Obesity-Diabetic-Natural-3799548/p', 'Estimado para baixa EM.'),
  ('Vet Life Obesity & Diabetic Mini', 'racao', 'cachorro', 'Farmina Vet Life', 'Obesity & Diabetic Mini', 'seca', 3000.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Vet-Life-Canine-Obesity-Diabetic-Mini-Natural-3814911/p', 'Estimado.'),
  ('Fórmula Natural Vet Care Obesidade (Médio/Grande)', 'racao', 'cachorro', 'Fórmula Natural', 'Vet Care Obesidade Médio/Grande', 'seca', 3000.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-formula-natural-vet-care-obesidade-caes-medio-e-grande-31003917/p', 'Estimado.'),
  ('Fórmula Natural Vet Care Obesidade (Mini/Pequeno)', 'racao', 'cachorro', 'Fórmula Natural', 'Vet Care Obesidade Mini/Pequeno', 'seca', 3000.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-formula-natural-vet-care-obesidade-caes-mini-e-pequeno-31003852/p', 'Estimado.'),
  ('Fórmula Natural Vet Care Obesidade (úmida)', 'racao', 'cachorro', 'Fórmula Natural', 'Vet Care Obesidade', 'umida', 950.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-umida-formula-natural-vet-care-obesidade-caes-31004808/p', 'Estimado para úmidas light.'),
  ('Quatree Life Adultos Raças Médias e Grandes Frango e Arroz', 'racao', 'cachorro', 'Quatree', 'Life Adultos Médias/Grandes', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-quatree-life-caes-adultos-racas-medias-grandes-31165674/p', 'Estimado.'),
  ('Max Adultos Raças Médias/Grandes Carne e Arroz', 'racao', 'cachorro', 'Max', 'Adultos Médios/Grandes Carne e Arroz', 'seca', 3500.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-max-caes-adultos-racas-medias-e-grandes-carne-e-arroz-31008951/p', 'Estimado.'),
  ('Dog Chow Adultos Médios e Grandes Carne, Frango e Arroz', 'racao', 'cachorro', 'Dog Chow', 'Adultos Médios e Grandes', 'seca', 3400.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Dog-Chow-Adulto-Frango-Arroz-3820849/p', 'Estimado.'),
  ('Dog Chow Adultos Minis e Pequenos Carne, Frango e Arroz', 'racao', 'cachorro', 'Dog Chow', 'Adultos Minis e Pequenos', 'seca', 3450.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/m/dog-chow', 'Estimado.'),
  ('Special Dog Gold Performance Adultos Frango e Carne', 'racao', 'cachorro', 'Special Dog', 'Gold Performance Adultos', 'seca', 3800.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-special-dog-gold-performance-caes-adultos-frango-e-carne-31157558/p', 'Estimado.'),
  ('Special Dog Gold Life Adultos Carne, Frango e Batata-doce', 'racao', 'cachorro', 'Special Dog', 'Gold Life Adultos', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-special-dog-gold-life-caes-adultos-carne-frango-e-batata-doce-31157736/p', 'Estimado.'),
  ('Guabi Natural Adultos Médio Frango e Arroz', 'racao', 'cachorro', 'Guabi Natural', 'Adultos Médio Frango e Arroz', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Guabi-Natural-Caes-Adultos-Medio-Frango-e-Arroz-3909866/p', 'Estimado.'),
  ('Guabi Natural Adultos Grandes Frango e Arroz', 'racao', 'cachorro', 'Guabi Natural', 'Adultos Grandes Frango e Arroz', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Guabi-Natural-Caes-Adultos-Grandes-e-Gigantes-Frango-e-Arroz-3909084/p', 'Estimado.'),
  ('Guabi Natural Obesos Médio e Grande', 'racao', 'cachorro', 'Guabi Natural', 'Obesos Médio e Grande', 'seca', 2900.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Guabi-Natural-Caes-Obesos-Medio-3982660/p', 'Estimado para baixa EM.'),
  ('Farmina N&D Ancestral Grain Selection Adultos Raças Médias (Frango e Cereais)', 'racao', 'cachorro', 'Farmina N&D', 'Ancestral Grain Selection', 'seca', 3800.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Farmina-N-amp-D-Ancestral-Grain-Selection-Caes-Adultos-Racas-Medias-3910864/p', 'Estimado.'),
  ('Farmina N&D Prime Adultos Porte Médio Cordeiro e Blueberry', 'racao', 'cachorro', 'Farmina N&D', 'Prime Adulto Porte Médio', 'seca', 4000.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-farmina-n-d-prime-caes-adultos-porte-medio-cordeiro-e-blueberry-3630659/p', 'Estimado.'),
  ('Farmina N&D Prime Adultos Porte Mini Cordeiro e Blueberry', 'racao', 'cachorro', 'Farmina N&D', 'Prime Adulto Porte Mini', 'seca', 4100.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Farmina-ND-Prime-Caes-Adultos-Mini-Cordeiro-e-Blueberry-3635090/p', 'Estimado.'),
  ('Farmina N&D Ocean Adultos Raças Médias e Grandes Salmão e Melão', 'racao', 'cachorro', 'Farmina N&D', 'Ocean Adulto Médio/Grande', 'seca', 3950.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-farmina-nd-ocean-cachorros-adultos-racas-medias-e-grandes-salmao-e-melao-3447021/p', 'Estimado.'),
  ('Golden Seleção Natural Adultos Frango e Arroz', 'racao', 'cachorro', 'GoldeN (PremieRpet)', 'Seleção Natural Adultos', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-golden-selecao-natural-caes-adultos-frango-e-arroz-3827967/p', 'Estimado.'),
  ('Golden Seleção Natural Adultos Porte Pequeno Frango e Arroz (Mini Bits)', 'racao', 'cachorro', 'GoldeN (PremieRpet)', 'Seleção Natural Adultos Mini', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-golden-selecao-natural-caes-adultos-porte-pequeno-frango-e-arroz-mini-bits-3823813/p', 'Estimado.'),
  ('Golden Fórmula Light Porte Pequeno Frango e Arroz (Mini Bits)', 'racao', 'cachorro', 'GoldeN (PremieRpet)', 'Fórmula Light Raças Pequenas', 'seca', 3100.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Golden-Light-Mini-Bits-3624950/p', 'Estimado para light.'),
  ('Golden Fórmula Raças Pequenas Carne e Arroz (Mini Bits)', 'racao', 'cachorro', 'GoldeN (PremieRpet)', 'Fórmula Raças Pequenas - Carne e Arroz', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-golden-formula-caes-adultos-racas-pequenas-carne-arroz-mini-bits-3811564/p', 'Estimado.'),
  ('Golden Raças Pequenas Frango e Arroz (Mini Bits)', 'racao', 'cachorro', 'GoldeN (PremieRpet)', 'Fórmula Raças Pequenas - Frango e Arroz', 'seca', 3600.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-golden-formula-caes-adultos-racas-pequenas-frango-arroz-mini-bits-3626279/p', 'Estimado.'),
  ('Golden Seleção Natural Filhotes Frango e Arroz', 'racao', 'cachorro', 'GoldeN (PremieRpet)', 'Seleção Natural Filhotes', 'seca', 4100.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Golden-Selecao-Natural-Caes-Filhotes-Frango-e-Arroz-3828009/p', 'Estimado para filhotes.'),
  ('Golden Duii Adultos Salmão e Cordeiro', 'racao', 'cachorro', 'GoldeN (PremieRpet)', 'Duii Adultos', 'seca', 3650.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/Racao-Golden-Duii-Caes-Adultos-Salmao-e-Cordeiro-3919853/p', 'Estimado.'),
  ('Premier Raças Específicas Golden Retriever Adultos', 'racao', 'cachorro', 'PremieRpet', 'Raças Específicas - Golden Retriever Adultos', 'seca', 3650.00, NULL, 'estimada', 'Cobasi', 'https://www.cobasi.com.br/racao-premier-golden-retriever-adultos-3640999/p', 'Estimado.')
ON CONFLICT DO NOTHING;
