# Sistema de Gestão Nutricional para Clínicas Veterinárias

## ?? Descrição Geral

Sistema para clínicas veterinárias que oferece:

- Cadastro de pets e informações clínicas.
- Avaliação nutricional personalizada feita pela clínica.
- Definição de dietas e orientações alimentares específicas.
- Controle de alimentos proibidos.
- Recomendação de snacks e alimentos entre refeições.
- Registro de preferências e restrições alimentares.
- Painel gamificado para o tutor acompanhar metas e progresso.

---

## ?? Estrutura de Banco de Dados

### `dietas`

| Campo            | Tipo    | Descrição                                       |
| ---------------- | ------- | ----------------------------------------------- |
| id               | UUID    | Identificador único da dieta                    |
| pet\_id          | UUID    | Relacionamento com `pets`                       |
| clinica\_id      | UUID    | Relacionamento com `clinicas`                   |
| tipo             | VARCHAR | `caseira` ou `ração`                            |
| objetivo         | VARCHAR | Ex: "Emagrecimento", "Doença Renal", "Nutrição" |
| peso\_atual\_pet | FLOAT   | Peso atual no momento do planejamento           |
| idade\_pet       | INTEGER | Idade atual                                     |
| raca\_pet        | VARCHAR | Raça                                            |
| tamanho\_pet     | VARCHAR | Porte/tamanho (`pequeno`, `médio`, `grande`)    |
| observacoes      | TEXT    | Observações clínicas                            |
| data\_inicio     | DATE    | Data de início da dieta                         |
| data\_fim        | DATE    | Data de fim (se houver)                         |
| status           | VARCHAR | `ativa`, `finalizada`, `aguardando_aprovacao`   |

### `opcoes_dieta`

| Campo                   | Tipo    | Descrição                                 |
| ----------------------- | ------- | ----------------------------------------- |
| id                      | UUID    | Identificador da opção                    |
| dieta\_id               | UUID    | Relacionamento com `dietas`               |
| nome                    | VARCHAR | Nome da opção (ex: "Ração Premium Light") |
| valor\_mensal\_estimado | FLOAT   | Preço médio mensal                        |
| calorias\_totais\_dia   | INTEGER | Calorias totais recomendadas por dia      |
| porcao\_refeicao        | VARCHAR | Ex: "200g ou 2 scoops por refeição"       |
| refeicoes\_por\_dia     | INTEGER | Número de refeições                       |
| indicacao               | TEXT    | Porque essa dieta é recomendada           |

### `alimentos_dieta`

| Campo            | Tipo    | Descrição                         |
| ---------------- | ------- | --------------------------------- |
| id               | UUID    | Identificador                     |
| opcao\_dieta\_id | UUID    | Relacionamento com `opcoes_dieta` |
| nome             | VARCHAR | Nome do alimento                  |
| tipo             | VARCHAR | `ração`, `caseira`, `complemento` |
| quantidade       | VARCHAR | Ex: "200g", "2 scoops"            |
| calorias         | INTEGER | Calorias estimadas                |
| horario          | VARCHAR | Ex: "Café", "Almoço", "Jantar"    |

### `alimentos_evitar`

| Campo   | Tipo    | Descrição                             |
| ------- | ------- | ------------------------------------- |
| id      | UUID    | Identificador                         |
| pet\_id | UUID    | Relacionamento com `pets`             |
| nome    | VARCHAR | Nome do alimento                      |
| motivo  | TEXT    | Ex: "Alergia", "Alto teor de gordura" |

### `snacks_entre_refeicoes`

| Campo               | Tipo    | Descrição                 |
| ------------------- | ------- | ------------------------- |
| id                  | UUID    | Identificador             |
| pet\_id             | UUID    | Relacionamento com `pets` |
| nome                | VARCHAR | Nome do snack ou alimento |
| frequencia\_semanal | INTEGER | Quantas vezes por semana  |
| quantidade          | VARCHAR | Ex: "1 bifinho", "50g"    |
| observacoes         | TEXT    | Ex: "Dar após caminhadas" |

### `preferencias_pet`

| Campo          | Tipo | Descrição                                |
| -------------- | ---- | ---------------------------------------- |
| id             | UUID | Identificador                            |
| pet\_id        | UUID | Relacionamento com `pets`                |
| gosta\_de      | TEXT | Ex: "Carne, Bifinho de frango, Mexerica" |
| nao\_gosta\_de | TEXT | Ex: "Ração de peixe, Cenoura"            |


#### `atividades`
- id
- nome
- tipo (caminhada, corrida, natação, brincadeira)
- calorias_estimadas_por_minuto

#### `planos_atividade`
- id
- id_pet
- id_clinica
- atividade_id
- frequencia_semanal
- duracao_minutos
- data_inicio

#### `atividades_realizadas`
- id
- plano_id
- data
- realizado (boolean)

#### `gamificacao_metas`
- id
- descricao
- tipo (alimentacao / atividade)
- quantidade
- unidade (vezes, minutos, refeicoes)
- periodo (semanal / mensal)

#### `gamificacao_pontuacoes`
- id
- id_pet
- id_meta
- pontos_obtidos
- data

#### `gamificacao_recompensas`
- id
- nome
- pontos_necessarios
- tipo (desconto, brinde, certificado)

###

---

## ?? Fluxo de dieta e alimentação

1. Clínica acessa o painel e seleciona o pet.
2. Avalia peso, idade, condição clínica, objetivo e preferências.
3. Define `dietas` e cadastra até 3 `opcoes_dieta`.
4. Preenche os `alimentos_dieta` de cada opção.
5. Registra `alimentos_evitar` para aquele pet.
6. Cadastra `snacks_entre_refeicoes` personalizados.
7. Tutor visualiza no app:
   - As 3 opções com valores, porções e recomendações.
   - Lista de alimentos proibidos.
   - Snacks liberados e frequência.
8. Tutor escolhe a dieta ? App atualiza metas e gamificação.

---

# Fluxo de Atividades Físicas

1. **Clínica acessa o painel e seleciona o pet.**
2. **Avalia peso, idade, condição clínica e nível de energia.**
3. **Define plano de atividades personalizado:**
   - Tipo de atividade (caminhada, corrida, natação, brincadeira)
   - Frequência semanal (ex: 3x por semana)
   - Duração por sessão (ex: 20 minutos)
   - Intensidade (leve, moderada, intensa)
4. **Registra preferências ou restrições do pet.**
5. **Tutor visualiza no app:**
   - Plano semanal de atividades.
   - Orientações da clínica.
   - Calorias estimadas por atividade.
6. **Tutor marca as atividades como “Realizadas”.**
7. **Veterinário acompanha o histórico e ajusta o plano conforme evolução.**
8. **App atualiza o progresso nas metas de atividade física.**

---

# Fluxo de Gamificação

1. **Criação de Metas pela Clínica:**
   - Exemplo:
     - Cumprir 5 caminhadas de 20 minutos na semana.
     - Completar as refeições recomendadas durante 7 dias.
     - Evitar alimentos proibidos no período.
     - Realizar brincadeiras interativas 3x por semana.
2. **Tutor realiza ações:**
   - Marca atividades físicas.
   - Registra refeições feitas.
   - Indica snacks e petiscos dados.
3. **Sistema calcula o progresso:**
   - Percentual de conclusão por meta.
   - Pontos acumulados.
4. **Desbloqueio de recompensas:**
   - Pontuação extra.
   - Descontos na clínica.
   - Brindes (kits pet, produtos, brinquedos)
   - Certificados digitais (Pet saudável do mês)
5. **Tutor consulta ranking e histórico:**
   - Ranking entre tutores (opcional)
   - Progresso pessoal e recompensas conquistadas.
6. **Veterinário acompanha desempenho e adapta metas.

