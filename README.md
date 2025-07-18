# Painel de Atendimento WhatsApp Integrado

Este projeto consiste em um painel web para gerenciamento de atendimento via WhatsApp, integrando automação (bots) com atendimento humano. Ele permite que operadores visualizem conversas, respondam manualmente aos clientes e controlem dinamicamente quando o atendimento deve ser automatizado ou manual para cada contato específico.

## Funcionalidades

- **Visualização de Conversas:** Listagem de contatos, histórico de mensagens trocadas (recebidas e enviadas), com atualização em tempo real.
- **Campo de Resposta Manual:** Operadores podem digitar e enviar mensagens manualmente para o cliente.
- **Controle ON/OFF do Bot por Contato:** Botão/switch para ligar ou desligar o atendimento automático (bot) para cada número.
- **Sincronização com Google Sheets:** O status do bot é sincronizado com uma planilha Google Sheets.
- **Integrações:** Z-API para envio de mensagens, Google Sheets para controle de status, e n8n para automação de bots.

## Arquitetura do Sistema

O projeto é dividido em duas partes principais:

- **Backend (Flask - Python):** Responsável pela lógica de negócio, gerenciamento de contatos e mensagens, e integração com APIs externas (Z-API, Google Sheets).
- **Frontend (React - JavaScript):** Interface de usuário intuitiva, similar ao WhatsApp Web, para operadores de atendimento.

## Instalação e Configuração

Para configurar e rodar o projeto localmente, siga os passos abaixo:

### Pré-requisitos

- Python 3.8 ou superior
- Node.js 16.x ou superior (com pnpm)
- Git
- Conta Z-API ativa com instância configurada
- Conta Google com acesso ao Google Sheets API
- Planilha Google Sheets configurada com a coluna 'status' (padrão 'ON')
- Instância n8n configurada com o workflow fornecido (opcional)

### 1. Backend (whatsapp-panel-backend)

```bash
# Navegue até o diretório do backend
cd whatsapp-panel-backend

# Crie e ative um ambiente virtual Python
python3 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Crie o arquivo .env na raiz do diretório whatsapp-panel-backend
# Substitua os valores pelos seus dados reais
```

**.env (exemplo)**

```env
# Configurações Flask
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui_gerada_aleatoriamente

# Configurações Z-API
ZAPI_INSTANCE_ID=SUA_ZAPI_INSTANCE_ID
ZAPI_TOKEN=SEU_ZAPI_TOKEN
ZAPI_CLIENT_TOKEN=SEU_ZAPI_CLIENT_TOKEN
ZAPI_BASE_URL=https://api.z-api.io

# Configurações Google Sheets
GOOGLE_SHEETS_ID=SEU_GOOGLE_SHEETS_ID
GOOGLE_SHEETS_RANGE=Sheet1!A:H
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json

# Configurações n8n (opcional)
N8N_WEBHOOK_URL=https://sua-instancia-n8n.com/webhook/ce01af9e-c388-4ace-a75f-7e1fb0b2062b

# Configurações Banco de Dados
DATABASE_URL=sqlite:///app.db
```

```bash
# Inicialize o banco de dados (isso criará o arquivo app.db)
python src/main.py
```

### 2. Frontend (whatsapp-panel-frontend)

```bash
# Navegue até o diretório do frontend
cd ../whatsapp-panel-frontend

# Instale as dependências
pnpm install

# Crie o arquivo .env.local na raiz do diretório whatsapp-panel-frontend
# Substitua os valores pelos seus dados reais
```

**.env.local (exemplo)**

```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_TITLE=Painel de Atendimento WhatsApp
```

### 3. Rodando o Projeto

**Inicie o Backend:**

No diretório `whatsapp-panel-backend`:

```bash
source venv/bin/activate
python src/main.py
```

**Inicie o Frontend:**

No diretório `whatsapp-panel-frontend`:

```bash
pnpm run dev
```

Após iniciar ambos os servidores, acesse o painel no seu navegador: `http://localhost:5173`

## Uso

1. **Visualização de Contatos:** A lista de contatos será exibida no lado esquerdo do painel.
2. **Seleção de Conversa:** Clique em um contato para ver o histórico de mensagens.
3. **Envio de Mensagens:** Digite sua mensagem no campo inferior e pressione Enter ou clique no botão de envio.
4. **Controle ON/OFF do Bot:** Use o switch ao lado de cada contato ou no cabeçalho da conversa para alternar o status do bot.

## Contribuição

Sinta-se à vontade para contribuir com o projeto. Para isso, siga os passos:

1. Faça um fork do repositório.
2. Crie uma nova branch para sua feature (`git checkout -b feature/sua-feature`).
3. Faça suas alterações e commit (`git commit -m 'feat: sua nova feature'`).
4. Envie para o repositório remoto (`git push origin feature/sua-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

