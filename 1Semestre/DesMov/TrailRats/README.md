# TrailRats - Aplicativo de Trilhas

TrailRats é um aplicativo desenvolvido com **React Native** e **Python (Flask)** que permite aos usuários:

* Cadastrar e explorar trilhas com informações detalhadas.
* Adicionar fotos às trilhas.
* Visualizar um feed de trilhas com imagens de capa.
* Acessar detalhes completos da trilha e do autor.

> Este projeto foi feito para fins educacionais, com foco em desenvolvimento fullstack mobile + backend.

---

## 🚀 Tecnologias Utilizadas

### Frontend:

* React Native com Expo
* AsyncStorage (para persistência de sessão)
* React Navigation

### Backend:

* Flask
* MySQL
* JWT para autenticação
* Upload de imagens com `werkzeug`

---

## 📂 Estrutura do Projeto

```
TrailRats/
├── backend/
│   ├── app.py
│   ├── db.py
│   ├── routes/
│   │   ├── login.py
│   │   ├── trail.py
│   │   ├── upload_image.py
│   │   ├── feed.py
│   │   └── trail_details.py
│   └── uploads/         # Pasta com imagens salvas
├── frontend/
│   ├── screens/
│   │   ├── LoginScreen.tsx
│   │   ├── TrailFormScreen1.tsx
│   │   ├── AdicionarFotosScreen.tsx
│   │   ├── FeedScreen.tsx
│   │   └── TrailDetailsScreen.tsx
│   └── assets/
│       └── images/
├── .env
└── README.md
```

---

## 📅 Configuração do Ambiente

### 1. Crie o arquivo `.env` na raiz do backend:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=trailrats_db
SECRET_KEY=sua_chave_ultra_secreta
```

### 2. Instale as dependências do backend:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Crie as tabelas do banco de dados MySQL (usando MySQL Workbench ou similar):

```sql
CREATE DATABASE trailrats_db;
USE trailrats_db;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE trails (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  nome VARCHAR(255),
  dificuldade INT,
  perigo INT,
  distancia VARCHAR(50),
  tempo VARCHAR(50),
  assistencia BOOLEAN,
  precisa_guia BOOLEAN,
  idosos BOOLEAN,
  criancas BOOLEAN,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE images (
  id INT AUTO_INCREMENT PRIMARY KEY,
  trail_id INT NOT NULL,
  image_url TEXT NOT NULL,
  data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (trail_id) REFERENCES trails(id) ON DELETE CASCADE
);
```

---

## 🚀 Como Rodar Localmente

### Backend (Flask)

```bash
cd backend
python app.py
```

### Frontend (React Native)

```bash
cd frontend
npx expo start
```

Certifique-se de ajustar o IP no `API_URL` para o IP local da sua máquina na rede (ex: `192.168.X.X`).

---

## 🧵 Funcionalidades

* [x] Login com criptografia de senha
* [x] Cadastro de trilhas
* [x] Upload de múltiplas imagens por trilha (armazenadas em pastas por ID)
* [x] Visualização de feed com imagens de capa e detalhes
* [x] Expansão da trilha para ver detalhes e galeria

---

## 📊 Melhorias Futuras

* [ ] Edição de perfil
* [ ] Curtidas ou comentários em trilhas
* [ ] Geolocalização e mapa de trilha
* [ ] Upload para nuvem (ex: S3) ao invés de armazenamento local

---

## 🌟 Agradecimentos

- [Marjorie Ap. Cortez Daenecke](https://github.com/MarjorieDaenecke) – pela colaboração e apoio durante o desenvolvimento do projeto.

---

**Licença**: Livre para fins educacionais e pessoais.
