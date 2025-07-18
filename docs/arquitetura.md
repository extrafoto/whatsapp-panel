
## Arquitetura do Sistema

### Visão Geral
O sistema será composto por um frontend (painel web), um backend (API) e integrações com serviços externos (Z-API, Google Sheets, n8n).

### Frontend
- **Tecnologia:** React
- **Funcionalidades:**
    - Visualização de contatos e conversas.
    - Envio de mensagens manuais.
    - Controle do status do bot (ON/OFF).
    - Sincronização em tempo real com o backend.

### Backend
- **Tecnologia:** Flask (Python)
- **Funcionalidades:**
    - API REST para o frontend.
    - Integração com Z-API para envio de mensagens.
    - Integração com Google Sheets para leitura/escrita do status do bot.
    - Integração opcional com n8n para gerenciamento de status.

### Banco de Dados
- **Principal:** Google Sheets (para status dos contatos).
- **Cache/Local:** O backend poderá usar um banco de dados local (como SQLite) para armazenar temporariamente o histórico de conversas, a fim de otimizar a performance.

### Integrações
- **Z-API:** Para envio de mensagens via WhatsApp.
- **Google Sheets API:** Para ler e atualizar o status do bot por contato.
- **n8n (opcional):** Como um intermediário para atualizar o status no Google Sheets, caso a API do Google Sheets apresente alguma limitação ou para simplificar o fluxo.




### APIs Necessárias
- **Z-API:**
    - Endpoint para envio de mensagens: `POST /send-message` (ou similar).
    - Parâmetros: `phone_number`, `message_text`.
- **Google Sheets API:**
    - Endpoint para leitura de dados: `GET /spreadsheets/{spreadsheetId}/values/{range}`.
    - Endpoint para escrita de dados: `PUT /spreadsheets/{spreadsheetId}/values/{range}`.
    - Autenticação: OAuth 2.0.
- **n8n (se utilizado):**
    - Endpoint customizado no n8n para receber requisições de atualização de status do bot.

### Modelo de Dados (Simplificado)

#### Contato
- `id`: Identificador único do contato.
- `phone_number`: Número de telefone do contato (chave primária).
- `name`: Nome do contato.
- `status`: Status do atendimento (`bot` ou `humano`).
- `last_message_timestamp`: Timestamp da última mensagem trocada.

#### Mensagem
- `id`: Identificador único da mensagem.
- `contact_id`: ID do contato associado.
- `direction`: Direção da mensagem (`received` ou `sent`).
- `text`: Conteúdo da mensagem.
- `timestamp`: Timestamp da mensagem.





### Segurança e Autenticação

Para garantir a segurança do painel, serão implementadas as seguintes medidas:

- **Autenticação de Usuários:** O acesso ao painel será restrito a operadores autenticados. Será utilizado um sistema de autenticação baseado em tokens (JWT - JSON Web Tokens) para proteger as rotas do backend. O processo de login envolverá o envio de credenciais (usuário/senha) para o backend, que, após validação, retornará um token JWT. Este token deverá ser incluído em todas as requisições subsequentes ao backend.

- **Autorização:** Além da autenticação, poderá ser implementado um sistema de autorização para controlar o que cada operador pode fazer no painel (ex: alguns operadores podem apenas visualizar, outros podem enviar mensagens e alterar o status do bot).

- **Comunicação Segura (HTTPS):** Todas as comunicações entre o frontend e o backend, e entre o backend e as APIs externas (Z-API, Google Sheets, n8n), deverão ser realizadas via HTTPS para garantir a criptografia dos dados em trânsito.

- **Validação de Entrada:** Todas as entradas de dados do usuário (ex: mensagens, alterações de status) serão validadas no backend para prevenir ataques como injeção de código ou dados maliciosos.

- **Gerenciamento de Credenciais:** As chaves de API e outras credenciais sensíveis serão armazenadas de forma segura no ambiente do servidor, utilizando variáveis de ambiente ou um sistema de gerenciamento de segredos, e nunca diretamente no código-fonte.

- **Limitação de Taxa (Rate Limiting):** Para prevenir ataques de força bruta ou uso excessivo da API, será implementada limitação de taxa nos endpoints do backend.

- **Logs e Monitoramento:** Serão configurados logs de acesso e erros para monitorar o uso do sistema e identificar possíveis atividades suspeitas.



