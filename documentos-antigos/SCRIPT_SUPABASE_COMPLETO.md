# Script Completo para Supabase - Área do Cliente

## 🎯 ESCLARECIMENTOS IMPORTANTES

### **1. Verificação de Acesso**
- ✅ **Via código** (frontend/backend) - NÃO no banco de dados
- ✅ Após login no Supabase, verificar se email está em `clinics` ou `animals`
- ✅ Redirecionar para `/clinic` ou `/client` baseado na verificação

### **2. Triggers de Auditoria**
- ❌ **REMOVIDOS** - Não são necessários para o MVP
- ✅ Controle de último acesso será via aplicação

### **3. RLS (Row Level Security)**
- ❌ **NÃO IMPLEMENTAR** - Conforme sua decisão
- ✅ Segurança via verificação de sessão no código

---

## 📋 SCRIPT COMPLETO PARA EXECUTAR NO SUPABASE

### **PARTE 1: Modificações nas Tabelas Existentes**

```sql
-- ==========================================
-- MODIFICAÇÕES NA TABELA ANIMALS
-- ==========================================

-- Adicionar campos de controle para área do cliente
ALTER TABLE public.animals 
ADD COLUMN IF NOT EXISTS client_active BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS client_activated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
ADD COLUMN IF NOT EXISTS client_last_login TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS gamification_points INTEGER DEFAULT 0;

-- Comentário: 
-- client_active: se o cliente pode acessar a área
-- client_activated_at: quando foi ativado o acesso
-- client_last_login: último acesso (atualizado via código)
-- gamification_points: pontos de gamificação (separado de total_points)
```

```sql
-- ==========================================
-- MODIFICAÇÕES NA TABELA APPOINTMENTS
-- ==========================================

-- Adicionar campos para solicitações de agendamento por clientes
ALTER TABLE public.appointments 
ADD COLUMN IF NOT EXISTS solicitado_por_cliente BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS status_solicitacao VARCHAR(50) DEFAULT 'confirmado',
ADD COLUMN IF NOT EXISTS observacoes_cliente TEXT;

-- Comentário:
-- solicitado_por_cliente: se foi o cliente que solicitou
-- status_solicitacao: 'pendente', 'confirmado', 'rejeitado'
-- observacoes_cliente: observações do cliente na solicitação
```

### **PARTE 2: Novas Tabelas**

```sql
-- ==========================================
-- NOVA TABELA: DIETA_PROGRESSO
-- ==========================================

CREATE TABLE IF NOT EXISTS public.dieta_progresso (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    animal_id UUID NOT NULL REFERENCES public.animals(id) ON DELETE CASCADE,
    dieta_id UUID NOT NULL REFERENCES public.dietas(id) ON DELETE CASCADE,
    opcao_dieta_id UUID REFERENCES public.opcoes_dieta(id) ON DELETE CASCADE,
    data DATE NOT NULL DEFAULT CURRENT_DATE,
    refeicao_completa BOOLEAN DEFAULT false,
    horario_realizado TIME,
    quantidade_consumida VARCHAR(100),
    observacoes_tutor TEXT,
    pontos_ganhos INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Constraint para evitar duplicatas por dia/opção
ALTER TABLE public.dieta_progresso 
ADD CONSTRAINT unique_animal_opcao_data 
UNIQUE(animal_id, opcao_dieta_id, data);

-- Comentário:
-- Tabela para registrar o progresso diário das dietas
-- Cada linha = uma refeição/opção de dieta em um dia específico
```

### **PARTE 3: Melhorias em Tabelas Existentes**

```sql
-- ==========================================
-- MELHORIAS NA TABELA ATIVIDADES_REALIZADAS
-- ==========================================

-- Adicionar campos que podem estar faltando
ALTER TABLE public.atividades_realizadas 
ADD COLUMN IF NOT EXISTS pontos_ganhos INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS horario_inicio TIME,
ADD COLUMN IF NOT EXISTS horario_fim TIME;

-- Comentário:
-- pontos_ganhos: pontos obtidos por essa atividade
-- horario_inicio/fim: controle de horário da atividade
```

### **PARTE 4: Índices para Performance**

```sql
-- ==========================================
-- ÍNDICES PARA OTIMIZAÇÃO
-- ==========================================

-- Índices para dieta_progresso
CREATE INDEX IF NOT EXISTS idx_dieta_progresso_animal_data 
ON public.dieta_progresso(animal_id, data);

CREATE INDEX IF NOT EXISTS idx_dieta_progresso_dieta 
ON public.dieta_progresso(dieta_id);

-- Índices para animals (área do cliente)
CREATE INDEX IF NOT EXISTS idx_animals_client_active 
ON public.animals(client_active) WHERE client_active = true;

CREATE INDEX IF NOT EXISTS idx_animals_email 
ON public.animals(email) WHERE email IS NOT NULL;

-- Índices para appointments (solicitações de cliente)
CREATE INDEX IF NOT EXISTS idx_appointments_solicitado_cliente 
ON public.appointments(solicitado_por_cliente) WHERE solicitado_por_cliente = true;

CREATE INDEX IF NOT EXISTS idx_appointments_animal_date 
ON public.appointments(animal_id, date);

-- Comentário:
-- Índices otimizam consultas frequentes da área do cliente
```

### **PARTE 5: Funções Úteis**

```sql
-- ==========================================
-- FUNÇÃO: VERIFICAR TIPO DE USUÁRIO
-- ==========================================

CREATE OR REPLACE FUNCTION public.check_user_type(user_email TEXT)
RETURNS TEXT AS $$
BEGIN
    -- Verificar se é uma clínica
    IF EXISTS (SELECT 1 FROM public.clinics WHERE email = user_email) THEN
        RETURN 'clinic';
    -- Verificar se é um cliente (animal com acesso ativo)
    ELSIF EXISTS (
        SELECT 1 FROM public.animals 
        WHERE email = user_email 
        AND client_active = true
    ) THEN
        RETURN 'client';
    ELSE
        RETURN 'unknown';
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Comentário:
-- Função para ser chamada via API após login no Supabase
-- Retorna 'clinic', 'client' ou 'unknown'
```

```sql
-- ==========================================
-- FUNÇÃO: OBTER DADOS DO DASHBOARD CLIENTE
-- ==========================================

CREATE OR REPLACE FUNCTION public.get_client_dashboard(animal_email TEXT)
RETURNS TABLE(
    animal_id UUID,
    animal_name VARCHAR,
    species VARCHAR,
    breed VARCHAR,
    age INTEGER,
    weight NUMERIC,
    gamification_points INTEGER,
    total_points INTEGER,
    proxima_consulta DATE,
    dietas_ativas BIGINT,
    atividades_semana BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id,
        a.name,
        a.species,
        a.breed,
        a.age,
        a.weight,
        a.gamification_points,
        a.total_points,
        
        -- Próximo agendamento
        (SELECT date FROM public.appointments 
         WHERE animal_id = a.id AND date >= CURRENT_DATE 
         ORDER BY date, start_time LIMIT 1) as proxima_consulta,
        
        -- Dietas ativas
        (SELECT COUNT(*) FROM public.dietas 
         WHERE animal_id = a.id AND status = 'ativa') as dietas_ativas,
        
        -- Atividades desta semana
        (SELECT COUNT(*) FROM public.atividades_realizadas ar
         JOIN public.planos_atividade pa ON ar.plano_id = pa.id
         WHERE ar.animal_id = a.id 
         AND ar.data >= date_trunc('week', CURRENT_DATE)
         AND ar.realizado = true) as atividades_semana

    FROM public.animals a
    WHERE a.email = animal_email 
    AND a.client_active = true;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Comentário:
-- Função otimizada para carregar dados do dashboard do cliente
```

```sql
-- ==========================================
-- FUNÇÃO: REGISTRAR PROGRESSO DE DIETA
-- ==========================================

CREATE OR REPLACE FUNCTION public.registrar_progresso_dieta(
    p_animal_id UUID,
    p_opcao_dieta_id UUID,
    p_refeicao_completa BOOLEAN DEFAULT false,
    p_observacoes TEXT DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_dieta_id UUID;
    v_pontos INTEGER := 0;
    v_progresso_id UUID;
BEGIN
    -- Buscar dieta_id da opção
    SELECT dieta_id INTO v_dieta_id 
    FROM public.opcoes_dieta 
    WHERE id = p_opcao_dieta_id;
    
    -- Calcular pontos (10 pontos por refeição completa)
    IF p_refeicao_completa THEN
        v_pontos := 10;
    END IF;
    
    -- Inserir ou atualizar progresso
    INSERT INTO public.dieta_progresso (
        animal_id, 
        dieta_id, 
        opcao_dieta_id, 
        data, 
        refeicao_completa, 
        observacoes_tutor, 
        pontos_ganhos
    ) VALUES (
        p_animal_id, 
        v_dieta_id, 
        p_opcao_dieta_id, 
        CURRENT_DATE, 
        p_refeicao_completa, 
        p_observacoes, 
        v_pontos
    )
    ON CONFLICT (animal_id, opcao_dieta_id, data) 
    DO UPDATE SET 
        refeicao_completa = EXCLUDED.refeicao_completa,
        observacoes_tutor = EXCLUDED.observacoes_tutor,
        pontos_ganhos = EXCLUDED.pontos_ganhos,
        updated_at = now()
    RETURNING id INTO v_progresso_id;
    
    -- Atualizar pontos do animal
    UPDATE public.animals 
    SET gamification_points = gamification_points + v_pontos
    WHERE id = p_animal_id;
    
    RETURN v_progresso_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Comentário:
-- Função para registrar progresso de dieta e atualizar pontos automaticamente
```

```sql
-- ==========================================
-- FUNÇÃO: REGISTRAR ATIVIDADE REALIZADA
-- ==========================================

CREATE OR REPLACE FUNCTION public.registrar_atividade_realizada(
    p_animal_id UUID,
    p_plano_id UUID,
    p_duracao_minutos INTEGER,
    p_observacao TEXT DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_pontos INTEGER;
    v_atividade_id UUID;
BEGIN
    -- Calcular pontos (1 ponto por minuto de atividade)
    v_pontos := COALESCE(p_duracao_minutos, 0);
    
    -- Inserir atividade realizada
    INSERT INTO public.atividades_realizadas (
        plano_id,
        animal_id,
        data,
        realizado,
        duracao_realizada_minutos,
        observacao_tutor,
        pontos_ganhos,
        horario_inicio
    ) VALUES (
        p_plano_id,
        p_animal_id,
        CURRENT_DATE,
        true,
        p_duracao_minutos,
        p_observacao,
        v_pontos,
        CURRENT_TIME
    )
    RETURNING id INTO v_atividade_id;
    
    -- Atualizar pontos do animal
    UPDATE public.animals 
    SET gamification_points = gamification_points + v_pontos
    WHERE id = p_animal_id;
    
    RETURN v_atividade_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Comentário:
-- Função para registrar atividade e atualizar pontos automaticamente
```

### **PARTE 6: Views Otimizadas**

```sql
-- ==========================================
-- VIEW: DASHBOARD DO CLIENTE
-- ==========================================

CREATE OR REPLACE VIEW public.view_client_dashboard AS
SELECT 
    a.id as animal_id,
    a.name as animal_name,
    a.species,
    a.breed,
    a.age,
    a.weight,
    a.gamification_points,
    a.total_points,
    a.email,
    
    -- Próximo agendamento
    (SELECT json_build_object(
        'date', date,
        'time', start_time,
        'type', appointment_type,
        'status', status
    ) FROM public.appointments 
     WHERE animal_id = a.id AND date >= CURRENT_DATE 
     ORDER BY date, start_time LIMIT 1) as proximo_agendamento,
    
    -- Estatísticas
    (SELECT COUNT(*) FROM public.dietas 
     WHERE animal_id = a.id AND status = 'ativa') as dietas_ativas,
     
    (SELECT COUNT(*) FROM public.atividades_realizadas ar
     WHERE ar.animal_id = a.id 
     AND ar.data >= date_trunc('week', CURRENT_DATE)
     AND ar.realizado = true) as atividades_semana,
     
    (SELECT COUNT(*) FROM public.dieta_progresso dp
     WHERE dp.animal_id = a.id 
     AND dp.data >= date_trunc('week', CURRENT_DATE)
     AND dp.refeicao_completa = true) as refeicoes_semana

FROM public.animals a
WHERE a.client_active = true;

-- Comentário:
-- View otimizada para carregar dados do dashboard rapidamente
```

---

## 🚀 SCRIPT COMPLETO PARA COPIAR E COLAR

```sql
-- ==========================================
-- SCRIPT COMPLETO - ÁREA DO CLIENTE VETECH
-- Execute este script no SQL Editor do Supabase
-- ==========================================

BEGIN;

-- 1. MODIFICAR TABELA ANIMALS
ALTER TABLE public.animals 
ADD COLUMN IF NOT EXISTS client_active BOOLEAN DEFAULT true,
ADD COLUMN IF NOT EXISTS client_activated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
ADD COLUMN IF NOT EXISTS client_last_login TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS gamification_points INTEGER DEFAULT 0;

-- 2. MODIFICAR TABELA APPOINTMENTS
ALTER TABLE public.appointments 
ADD COLUMN IF NOT EXISTS solicitado_por_cliente BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS status_solicitacao VARCHAR(50) DEFAULT 'confirmado',
ADD COLUMN IF NOT EXISTS observacoes_cliente TEXT;

-- 3. CRIAR TABELA DIETA_PROGRESSO
CREATE TABLE IF NOT EXISTS public.dieta_progresso (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    animal_id UUID NOT NULL REFERENCES public.animals(id) ON DELETE CASCADE,
    dieta_id UUID NOT NULL REFERENCES public.dietas(id) ON DELETE CASCADE,
    opcao_dieta_id UUID REFERENCES public.opcoes_dieta(id) ON DELETE CASCADE,
    data DATE NOT NULL DEFAULT CURRENT_DATE,
    refeicao_completa BOOLEAN DEFAULT false,
    horario_realizado TIME,
    quantidade_consumida VARCHAR(100),
    observacoes_tutor TEXT,
    pontos_ganhos INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 4. CONSTRAINT ÚNICA
ALTER TABLE public.dieta_progresso 
ADD CONSTRAINT unique_animal_opcao_data 
UNIQUE(animal_id, opcao_dieta_id, data);

-- 5. MELHORAR TABELA ATIVIDADES_REALIZADAS
ALTER TABLE public.atividades_realizadas 
ADD COLUMN IF NOT EXISTS pontos_ganhos INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS horario_inicio TIME,
ADD COLUMN IF NOT EXISTS horario_fim TIME;

-- 6. CRIAR ÍNDICES
CREATE INDEX IF NOT EXISTS idx_dieta_progresso_animal_data ON public.dieta_progresso(animal_id, data);
CREATE INDEX IF NOT EXISTS idx_dieta_progresso_dieta ON public.dieta_progresso(dieta_id);
CREATE INDEX IF NOT EXISTS idx_animals_client_active ON public.animals(client_active) WHERE client_active = true;
CREATE INDEX IF NOT EXISTS idx_animals_email ON public.animals(email) WHERE email IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_appointments_solicitado_cliente ON public.appointments(solicitado_por_cliente) WHERE solicitado_por_cliente = true;
CREATE INDEX IF NOT EXISTS idx_appointments_animal_date ON public.appointments(animal_id, date);

-- 7. FUNÇÃO VERIFICAR TIPO DE USUÁRIO
CREATE OR REPLACE FUNCTION public.check_user_type(user_email TEXT)
RETURNS TEXT AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM public.clinics WHERE email = user_email) THEN
        RETURN 'clinic';
    ELSIF EXISTS (SELECT 1 FROM public.animals WHERE email = user_email AND client_active = true) THEN
        RETURN 'client';
    ELSE
        RETURN 'unknown';
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 8. FUNÇÃO DASHBOARD CLIENTE
CREATE OR REPLACE FUNCTION public.get_client_dashboard(animal_email TEXT)
RETURNS TABLE(
    animal_id UUID, animal_name VARCHAR, species VARCHAR, breed VARCHAR, 
    age INTEGER, weight NUMERIC, gamification_points INTEGER, total_points INTEGER,
    proxima_consulta DATE, dietas_ativas BIGINT, atividades_semana BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id, a.name, a.species, a.breed, a.age, a.weight, a.gamification_points, a.total_points,
        (SELECT date FROM public.appointments WHERE animal_id = a.id AND date >= CURRENT_DATE ORDER BY date, start_time LIMIT 1) as proxima_consulta,
        (SELECT COUNT(*) FROM public.dietas WHERE animal_id = a.id AND status = 'ativa') as dietas_ativas,
        (SELECT COUNT(*) FROM public.atividades_realizadas ar JOIN public.planos_atividade pa ON ar.plano_id = pa.id WHERE ar.animal_id = a.id AND ar.data >= date_trunc('week', CURRENT_DATE) AND ar.realizado = true) as atividades_semana
    FROM public.animals a WHERE a.email = animal_email AND a.client_active = true;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 9. FUNÇÃO REGISTRAR PROGRESSO DIETA
CREATE OR REPLACE FUNCTION public.registrar_progresso_dieta(
    p_animal_id UUID, p_opcao_dieta_id UUID, p_refeicao_completa BOOLEAN DEFAULT false, p_observacoes TEXT DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_dieta_id UUID; v_pontos INTEGER := 0; v_progresso_id UUID;
BEGIN
    SELECT dieta_id INTO v_dieta_id FROM public.opcoes_dieta WHERE id = p_opcao_dieta_id;
    IF p_refeicao_completa THEN v_pontos := 10; END IF;
    
    INSERT INTO public.dieta_progresso (animal_id, dieta_id, opcao_dieta_id, data, refeicao_completa, observacoes_tutor, pontos_ganhos) 
    VALUES (p_animal_id, v_dieta_id, p_opcao_dieta_id, CURRENT_DATE, p_refeicao_completa, p_observacoes, v_pontos)
    ON CONFLICT (animal_id, opcao_dieta_id, data) 
    DO UPDATE SET refeicao_completa = EXCLUDED.refeicao_completa, observacoes_tutor = EXCLUDED.observacoes_tutor, pontos_ganhos = EXCLUDED.pontos_ganhos, updated_at = now()
    RETURNING id INTO v_progresso_id;
    
    UPDATE public.animals SET gamification_points = gamification_points + v_pontos WHERE id = p_animal_id;
    RETURN v_progresso_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 10. FUNÇÃO REGISTRAR ATIVIDADE
CREATE OR REPLACE FUNCTION public.registrar_atividade_realizada(
    p_animal_id UUID, p_plano_id UUID, p_duracao_minutos INTEGER, p_observacao TEXT DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_pontos INTEGER; v_atividade_id UUID;
BEGIN
    v_pontos := COALESCE(p_duracao_minutos, 0);
    
    INSERT INTO public.atividades_realizadas (plano_id, animal_id, data, realizado, duracao_realizada_minutos, observacao_tutor, pontos_ganhos, horario_inicio) 
    VALUES (p_plano_id, p_animal_id, CURRENT_DATE, true, p_duracao_minutos, p_observacao, v_pontos, CURRENT_TIME)
    RETURNING id INTO v_atividade_id;
    
    UPDATE public.animals SET gamification_points = gamification_points + v_pontos WHERE id = p_animal_id;
    RETURN v_atividade_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMIT;
```

---

## ✅ CHECKLIST DE EXECUÇÃO

### **Antes de Executar**
- [ ] Fazer backup do banco de dados
- [ ] Testar em ambiente de desenvolvimento primeiro
- [ ] Verificar se todas as tabelas existem

### **Após Executar**
- [ ] Verificar se todas as colunas foram adicionadas
- [ ] Testar as funções criadas
- [ ] Verificar se os índices foram criados
- [ ] Validar que não há erros

### **Teste das Funções**
```sql
-- Testar verificação de tipo de usuário
SELECT public.check_user_type('email@exemplo.com');

-- Testar dashboard (substitua pelo email real)
SELECT * FROM public.get_client_dashboard('email@exemplo.com');
```

---

## 🎯 PRÓXIMOS PASSOS

1. **Execute o script completo** no SQL Editor do Supabase
2. **Teste as funções** com dados reais
3. **Implemente a verificação** no código do frontend/backend
4. **Inicie o desenvolvimento** das sprints

**Status**: ✅ **SCRIPT PRONTO PARA EXECUÇÃO**