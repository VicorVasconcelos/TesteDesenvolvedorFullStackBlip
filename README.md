# API de Gerenciamento de Leads

API REST desenvolvida com **FastAPI** e **MongoDB Atlas** para gerenciar leads, com integração automática a uma API externa para enriquecimento de dados.

Este projeto foi criado como parte de um desafio técnico, focando em boas práticas de desenvolvimento, arquitetura limpa e código bem documentado.

## 🎯 O que eu fiz

Desenvolvi uma API completa de gerenciamento de leads que:

- Permite cadastrar, listar e buscar leads
- Se integra automaticamente com uma API externa para buscar data de nascimento
- Usa MongoDB Atlas (cloud) para persistência de dados
- Está totalmente dockerizada e pronta para deploy
- Tem documentação interativa automática com Swagger

**Diferencial:** Implementei tratamento robusto de erros na integração externa, garantindo que mesmo se a API de terceiros cair, o lead ainda é salvo com `birth_date = null`. Isso evita perda de dados importantes.

## 🚀 Próximos Passos

Pretendo expandir este projeto criando uma **interface web** para facilitar a entrada e visualização de leads, incluindo:

- Formulário intuitivo para cadastro de leads
- Dashboard com lista de todos os leads cadastrados
- Página de detalhes de cada lead
- Interface responsiva usando React ou Vue.js
- Validação de campos em tempo real

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11+**
- **FastAPI** - Framework web moderno e rápido
- **MongoDB Atlas** - Banco de dados NoSQL em nuvem (gratuito)
- **Pydantic** - Validação automática de dados
- **httpx** - Cliente HTTP assíncrono para integração
- **Docker** - Containerização

---

## 📁 Como o Projeto está Organizado

```
leads-api/
├── app/
│   ├── main.py              # Define as rotas da API
│   ├── database.py          # Conexão com MongoDB
│   ├── schemas.py           # Modelos de validação
│   └── services/
│       ├── lead_service.py      # Lógica de criação/busca de leads
│       └── external_api.py      # Busca data de nascimento na API externa
├── .env                     # Credenciais do MongoDB (não commitar!)
├── .gitignore              # Arquivos ignorados pelo Git
├── requirements.txt         # Dependências Python
├── Dockerfile              # Imagem Docker
├── docker-compose.yml      # Configuração dos containers
└── README.md               # Este arquivo
```

### Por que separei assim?

- **main.py**: Só cuida das rotas HTTP, não tem regra de negócio
- **services/**: Toda a lógica da aplicação fica aqui
- **schemas.py**: Garante que os dados estão corretos antes de processar
- **database.py**: Isola a conexão com banco, facilita trocar de DB no futuro

Essa organização deixa o código mais fácil de entender e manter.

---

## ⚙️ Como Rodar Localmente

### Você vai precisar de:

- Python 3.11 ou superior instalado
- Uma conta no MongoDB Atlas (100% gratuita)

### 1. Clone o Repositório

```bash
git clone <seu-repositorio>
cd leads-api
```

### 2. Configurar o MongoDB Atlas

**Boa notícia:** O projeto já vem configurado com minhas credenciais! Você pode rodar direto sem criar conta.

Mas se quiser usar sua própria conta MongoDB:

1. Crie uma conta em: https://cloud.mongodb.com/
2. Crie um cluster gratuito (M0)
3. Em **Database Access**, crie um usuário
4. Em **Network Access**, adicione seu IP ou `0.0.0.0/0`
5. Pegue a connection string e atualize o arquivo `.env`

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Rodar a API

```bash
uvicorn app.main:app --reload
```

Pronto! A API vai estar rodando em: **http://localhost:8000**

---

## 📖 Como Usar a API

### Documentação Interativa

A melhor forma de testar é usando a documentação automática:

- **Swagger UI**: http://localhost:8000/docs (recomendado!)
- **ReDoc**: http://localhost:8000/redoc

### Criar um Lead

**Endpoint:** `POST /leads`

```json
{
  "name": "Maria Silva",
  "email": "maria@email.com",
  "phone": "11999887766"
}
```

**Resposta:**

```json
{
  "id": "6756c7f8e1a2b3c4d5e6f789",
  "name": "Maria Silva",
  "email": "maria@email.com",
  "phone": "11999887766",
  "birth_date": "1998-02-05"
}
```

> O campo `birth_date` é preenchido automaticamente buscando na API externa!

### Listar Todos os Leads

**Endpoint:** `GET /leads`

Retorna um array com todos os leads cadastrados.

### Buscar um Lead Específico

**Endpoint:** `GET /leads/{id}`

Substitua `{id}` pelo ID do lead (aquele campo `id` que vem na resposta).

---

## 🌐 Como Funciona a Integração Externa?

Toda vez que você cria um lead, a API automaticamente:

1. Faz uma requisição para `https://dummyjson.com/users/1`
2. Extrai o campo `birthDate` da resposta
3. Salva no MongoDB como `birth_date`

**E se a API externa estiver fora do ar?**

Sem problemas! O lead é salvo normalmente com `birth_date: null`. Isso garante que você não perde dados importantes por causa de uma dependência externa.

Exemplo de resposta quando a API externa falha:

```json
{
  "id": "6756c7f8e1a2b3c4d5e6f789",
  "name": "João Santos",
  "email": "joao@email.com",
  "phone": "11988776655",
  "birth_date": null
}
```

---

## 🧪 Testando com cURL

Se você preferir testar via linha de comando:

```bash
# Criar lead
curl -X POST "http://localhost:8000/leads" \
  -H "Content-Type: application/json" \
  -d '{"name":"Pedro Costa","email":"pedro@email.com","phone":"11977665544"}'

# Listar todos
curl http://localhost:8000/leads

# Buscar por ID
curl http://localhost:8000/leads/6756c7f8e1a2b3c4d5e6f789
```

---

## 🐳 Rodar com Docker (Opcional)

Se você tem Docker instalado:

```bash
docker-compose up --build
```

Isso vai subir:

- Um container com MongoDB local
- Um container com a API

> **Nota:** No Docker, a API usa o MongoDB do container, não o Atlas.

---

## 🏗️ Decisões Técnicas

### Por que separei em camadas?

- **Facilita testes**: Posso testar a lógica sem depender das rotas HTTP
- **Facilita mudanças**: Se eu quiser trocar o MongoDB por PostgreSQL, só mudo o `database.py`
- **Código mais limpo**: Cada arquivo tem uma responsabilidade clara

### Por que usei async/await na integração?

Para não travar o servidor enquanto espera a resposta da API externa. Se 10 pessoas criarem leads ao mesmo tempo, todas são processadas em paralelo. 

---

## ✅ Requisitos do Desafio

- ✅ **POST /leads** - Criar lead
- ✅ **GET /leads** - Listar todos
- ✅ **GET /leads/{id}** - Buscar por ID
- ✅ Integração com API externa (`dummyjson.com`)
- ✅ Campo `birth_date` preenchido automaticamente
- ✅ Tratamento de falha da API externa
- ✅ MongoDB como banco de dados
- ✅ Arquitetura em camadas
- ✅ Validação de dados (email válido, campos obrigatórios)
- ✅ Documentação Swagger automática
- ✅ Docker configurado
- ✅ README completo

---

## 🔮 Melhorias Futuras

### Interface Web (em desenvolvimento)

- [ ] Frontend em React/Vue.js
- [ ] Formulário de cadastro com validação
- [ ] Dashboard com tabela de leads
- [ ] Filtros e busca
- [ ] Gráficos e estatísticas

### Backend

- [ ] Autenticação com JWT
- [ ] Paginação nos endpoints
- [ ] Filtros avançados (por email, data, etc)
- [ ] Testes unitários e de integração
- [ ] Cache com Redis
- [ ] Rate limiting
- [ ] Logs estruturados

### DevOps

- [ ] CI/CD com GitHub Actions
- [ ] Deploy em cloud (AWS/Heroku/Railway)
- [ ] Monitoramento com Sentry
- [ ] Backup automático do banco

---

## 📝 Variáveis de Ambiente

O arquivo `.env` contém as credenciais do MongoDB:

```env
MONGODB_URL=mongodb+srv://leads_user:Senha123@cluster0.ulzvh6u.mongodb.net/?appName=Cluster0
DATABASE_NAME=leads_db
```

> **Atenção:** Em produção, nunca commite o arquivo `.env`! Ele já está no `.gitignore`.

---

## 🤔 FAQ

**P: Preciso instalar o MongoDB na minha máquina?**
R: Não! Estou usando MongoDB Atlas que é totalmente em nuvem.

**P: A API funciona sem internet?**
R: Precisa de internet para conectar ao MongoDB Atlas e à API externa. Se quiser rodar offline, use o Docker Compose que sobe um MongoDB local.

**P: Posso usar outro banco de dados?**
R: Sim! É só modificar o arquivo `database.py` e adaptar as queries.

**P: Como adiciono novos campos no lead?**
R: Edite o `schemas.py` adicionando o campo em `LeadCreate` e `LeadResponse`.

---

## 📞 Contato

Desenvolvido por **Victor Vasconcelos
Whatsapp: 61984385187**

Projeto criado como parte de um desafio técnico para demonstrar conhecimentos em Python, FastAPI, MongoDB e arquitetura de software.

Se tiver dúvidas ou sugestões, fique à vontade para abrir uma issue ou entrar em contato!
