# 🤖 SunSec CTFTime Bot

<img src="https://github.com/user-attachments/assets/d589b30d-a3c1-4074-95ea-6ad3a4ca58b4" width="300px" />

Um bot para Discord que avisa automaticamente sobre novos CTFs listados no [CTFTime](https://ctftime.org). Ele também disponibiliza um comando `/prox_ctf` para listar os próximos eventos!

---

## ⚙️ Requisitos

- Python 3.8+
- Um bot criado no [Discord Developer Portal](https://discord.com/developers/applications)

---

## 🚀 Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/sunsec-rn/ctftime-discord-bot.git
cd ctftime-discord-bot
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` baseado no exemplo abaixo:

```bash
cp .env.example .env
```

Edite o `.env` com os valores corretos:

```env
DISCORD_TOKEN=seu_token_do_bot
CHANNEL_ID=123456789012345678
ROLE_ID=123456789012345678
```

> 💡 Dica: ative o “Modo de desenvolvedor” no Discord para copiar os IDs de canais e cargos.

---

### 5. Execute o bot

```bash
python server.py
```

---

## 💬 Comandos disponíveis

- `/prox_ctf` — Lista os próximos eventos do CTFTime.

---

## 📌 Sobre

Esse bot foi criado por membros da [SunSec RN](https://sunsec.net) com muito amor, café e algumas flags 🏴‍☠️🤖

Sinta-se à vontade para contribuir, abrir issues ou sugerir melhorias!
