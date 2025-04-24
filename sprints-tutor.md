# Backlog e Planejamento de Sprints — Rotas da Área do Tutor

Este documento apresenta o backlog de requisitos focado nas rotas (endpoints) da área do tutor (animal owner) e o planejamento de sprints.

---

## 📋 Backlog de Requisitos (User Stories)

| ID    | User Story                                                                                       | Critérios de Aceitação                                                                                      | Rota API                                                        |
|-------|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------|
| US-A1 | Como tutor, quero me registrar na plataforma para acessar minha área.                           | Retornar token JWT e perfil do tutor após cadastro.                                                          | `POST /api/v1/tutor/register`                                   |
| US-A2 | Como tutor, quero fazer login para acessar funcionalidades.                                       | Retornar token JWT válido.                                                                                   | `POST /api/v1/tutor/login`                                      |
| US-A3 | Como tutor, quero fazer logout para encerrar minha sessão.                                       | Token inválido após logout.                                                                                  | `POST /api/v1/tutor/logout`                                     |
| US-A4 | Como tutor, quero visualizar e editar meu perfil.                                                | `GET` retorna dados corretos; `PUT` atualiza e retorna perfil.                                               | `GET/PUT /api/v1/tutor/profile`                                |
| US-A5 | Como tutor, quero listar meus pets associados.                                                    | Retorna lista de pets com informações básicas.                                                               | `GET /api/v1/tutor/pets`                                        |
| US-A6 | Como tutor, quero ver detalhes de um pet específico.                                             | Retorna ficha completa do pet, incluindo histórico.                                                          | `GET /api/v1/tutor/pets/:petId`                                 |
| US-A7 | Como tutor, quero visualizar as opções de dieta sugeridas pela clínica.                          | Retorna até 3 opções com detalhes (porção, calorias, preço).                                                 | `GET /api/v1/tutor/pets/:petId/diets/options`                  |
| US-A8 | Como tutor, quero selecionar uma das opções de dieta.                                             | Seleção persiste no servidor e metas são atualizadas.                                                        | `POST /api/v1/tutor/pets/:petId/diets/select`                  |
| US-A9 | Como tutor, quero visualizar os alimentos proibidos para meu pet.                                | Retorna lista de alimentos a evitar.                                                                         | `GET /api/v1/tutor/pets/:petId/avoid-foods`                     |
| US-A10| Como tutor, quero visualizar os snacks recomendados entre refeições.                             | Retorna lista com frequência e quantidades.                                                                  | `GET /api/v1/tutor/pets/:petId/snacks`                          |
| US-A11| Como tutor, quero registrar no app quando alimento meu pet.                                       | Registro gravado com data, refeição e calorias estimadas.                                                    | `POST /api/v1/tutor/pets/:petId/feeding-records`                |
| US-A12| Como tutor, quero registrar o peso do pet.                                                        | Registro de peso salvo com data.                                                                             | `POST /api/v1/tutor/pets/:petId/weight-records`                |
| US-A13| Como tutor, quero visualizar meu plano de atividades físicas.                                     | Retorna plano com tipos, frequência e orientações.                                                           | `GET /api/v1/tutor/pets/:petId/activity-plans`                 |
| US-A14| Como tutor, quero marcar uma atividade como realizada.                                            | Cria registro de conclusão com duração e data.                                                               | `POST /api/v1/tutor/activity-plans/:planId/records`             |
| US-A15| Como tutor, quero visualizar minhas metas de gamificação.                                         | Retorna metas ativas (alimentação, atividade, geral).                                                       | `GET /api/v1/tutor/gamification/goals`                          |
| US-A16| Como tutor, quero consultar minha pontuação acumulada.                                           | Retorna pontos totais e níveis.                                                                              | `GET /api/v1/tutor/pets/:petId/gamification/score`             |
| US-A17| Como tutor, quero ver o catálogo de recompensas disponíveis.                                     | Retorna lista de recompensas com pontos necessários.                                                         | `GET /api/v1/tutor/gamification/rewards`                       |
| US-A18| Como tutor, quero resgatar uma recompensa.                                                       | Cria registro de resgate e decrementa pontos.                                                               | `POST /api/v1/tutor/gamification/rewards/:rewardId/redeem`     |
| US-A19| Como tutor, quero consultar o ranking dos tutores.                                               | Retorna lista ordenada por pontuação.                                                                        | `GET /api/v1/tutor/leaderboard`                                |
| US-A20| Como tutor, quero receber notificações e lembretes.                                              | `GET` retorna notificações não lidas; `PUT` marca como lida.                                                 | `GET/PUT /api/v1/tutor/notifications`                          |
| US-A21| Como tutor, quero atualizar preferências alimentares do pet.                                      | `GET` retorna preferências; `PUT` atualiza dados de likes/dislikes.                                          | `GET/PUT /api/v1/tutor/pets/:petId/preferences`                |

---

## 🚀 Planejamento de Sprints
Assumindo sprints de 2 semanas:

### Sprint 1 — Autenticação e Perfil
**Período:** Dias 1–14
- US-A1: Cadastro do tutor
- US-A2: Login do tutor
- US-A3: Logout do tutor
- US-A4: Visualização/edição de perfil

### Sprint 2 — Visão Geral de Pets
**Período:** Dias 15–28
- US-A5: Listagem de pets
- US-A6: Detalhes do pet
- US-A21: CRUD preferências alimentares

### Sprint 3 — Nutrição Interativa
**Período:** Dias 29–42
- US-A7: Visualizar opções de dieta
- US-A8: Selecionar dieta
- US-A9: Ver alimentos proibidos
- US-A10: Ver snacks recomendados
- US-A11: Registrar alimentação
- US-A12: Registrar peso do pet

### Sprint 4 — Atividades Físicas
**Período:** Dias 43–56
- US-A13: Visualizar plano de atividades
- US-A14: Marcar atividade realizada

### Sprint 5 — Gamificação e Recompensas
**Período:** Dias 57–70
- US-A15: Visualizar metas de gamificação
- US-A16: Consultar pontuação acumulada
- US-A17: Ver catálogo de recompensas
- US-A18: Resgatar recompensa
- US-A19: Consultar ranking
- US-A20: Notificações e lembretes

---

**Observações:**
- Adaptar estimativas de esforço conforme capacidade da equipe.
- Incluir testes de integração e documentação das rotas (Swagger/OpenAPI).
- Realizar retrospectivas e refinamentos ao final de cada sprint.

Boa codificação! 🚀

