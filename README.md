# 🚀 Chat Backend API — Guia de Fluxo de Autenticação e Mensagens

Este documento descreve o fluxo sequencial correto para a utilização dos endpoints do sistema de Chat. Como a API utiliza segurança baseada em **JWT (JSON Web Tokens)** via cabeçalhos `Bearer`, as requisições possuem uma ordem lógica obrigatória que vai desde a identificação do usuário até o envio efetivo de uma mensagem.

---

## 🗺️ Visão Geral do Fluxo de Uso

Para enviar uma mensagem com sucesso no sistema, um cliente (ou analista de QA) deve seguir obrigatoriamente a sequência abaixo:

[ Passo 1: /auth/login ]
│
▼ (Gera o Access Token)
[ Passo 2: /chats ]
│
▼ (Obtém o chat_id desejado)
[ Passo 3: /messages ] (Envia a mensagem vinculando Token + chat_id)

---

## 🛠️ Detalhamento dos Endpoints

### 🔐 Passo 1: Autenticação (`POST /auth/login`)
Antes de interagir com qualquer recurso, o usuário precisa se identificar para receber o seu passaporte de acesso (Token).

* **URL:** `http://localhost:8000/auth/login`
* **Método:** `POST`
* **Corpo da Requisição (JSON):**
```json
{
    "email": "usuario@teste.com",
    "password": "sua_senha_segura"
}

Resposta de Sucesso (200 OK):

{
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "user_id": "3cad9271-bf1a-4d74-9844-3d969bc7491d",
    "name": "Nome do Usuário"
}

⚠️ Atenção QA/Desenvolvedor: Copie o valor contido em "access_token" (sem as aspas). Você precisará dele nos próximos passos.

💬 Passo 2: Identificar a Conversa (GET ou POST /chats)
Para enviar uma mensagem, você precisa dizer ao banco de dados em qual sala ou com quem você está conversando. Para isso, precisamos listar os chats existentes para capturar o identificador único (chat_id).

URL: http://localhost:8000/chats/

Método: GET (ou POST para criar um novo)

Autenticação Obrigatória: Aba Authorization do Postman → Tipo: Bearer Token → Cole o token obtido no Passo 1.

Resposta de Sucesso (200 OK):

[
    {
        "id": "5041e5e1-dd51-4af8-8b88-7d66855d0e0d",
        "name": "Grupo de Desenvolvimento",
        "created_at": "2026-06-05T12:00:00Z"
    }
]

⚠️ Atenção QA/Desenvolvedor: Copie o valor do campo "id". Esse é o UUID exato do chat que receberá a mensagem. Atenção à quantidade de caracteres (formato padrão UUID4 de 36 caracteres).

✉️ Passo 3: Enviar a Mensagem (POST /messages)
Agora que você possui a sua credencial ativa e o identificador do chat de destino, você pode publicar o texto.

URL: http://localhost:8000/messages/

Método: POST

Autenticação Obrigatória: Aba Authorization do Postman → Tipo: Bearer Token → Cole o mesmo token obtido no Passo 1.

Corpo da Requisição (JSON):

{
    "chat_id": "5041e5e1-dd51-4af8-8b88-7d66855d0e0d",
    "content": "Olá! Esta é a minha primeira mensagem enviada de forma segura através da API."
}

Resposta de Sucesso (201 Created):

{
    "id": "8f3b14d2-7c39-44bb-ba52-ea1c324869fa",
    "chat_id": "5041e5e1-dd51-4af8-8b88-7d66855d0e0d",
    "sender_id": "3cad9271-bf1a-4d74-9844-3d969bc7491d",
    "content": "Olá! Esta é a minha primeira mensagem enviada de forma segura através da API.",
    "created_at": "2026-06-05T12:05:22.184Z"
}

💡 Nota de Arquitetura: O campo sender_id (quem envia) não é enviado no JSON da mensagem. O backend o extrai de forma blindada decodificando o Token JWT injetado no cabeçalho de autorização.

🛑 Tratamento de Erros Comuns para QA
Ao testar as rotas, fique atento às respostas de validação do FastAPI:

1. 401 Unauthorized (Token Inválido ou Expirado)
Causa: O token colado na aba Authorization está mal copiado, pertence a outra assinatura de chave, ou a sessão expirou (padrão de 7 dias).

Solução: Repita o Passo 1, gere um token atualizado e substitua-o no cabeçalho da requisição do Postman.

2. 422 Unprocessable Entity (uuid_parsing)
Causa: O chat_id enviado no corpo da mensagem possui algum erro de digitação ou tamanho incorreto.

Exemplo de Erro: invalid group length in group 0: expected 8, found 9.

Solução: Garanta que copiou o UUID exatamente como retornado pelo banco (sem caracteres extras, espaços vazios ou omissão de letras).

3. 404 Not Found (Chat não existente)
Causa: O ID do chat está semanticamente correto como formato UUID, mas não existe nenhuma linha correspondente na tabela de chats do banco de dados.

Solução: Valide se o chat não foi deletado ou crie um novo através do endpoint correspondente antes de enviar mensagens para ele.


Passo 2: Testar no Postman (Fluxo do QA) 🧪
Agora você tem o par perfeito: uma rota para enviar e uma para ler. Vamos testar a leitura:

Garanta que o seu servidor recarregou sem erros.

No Postman, crie uma nova requisição do tipo GET.

A URL será: http://localhost:8000/messages/COLOQUE-O-UUID-DO-CHAT-AQUI

Vá na aba Authorization, mude o tipo para Bearer Token e cole o seu token de login atualizado.

Clique em Send.

O que deve acontecer:
A API vai te retornar uma lista ([]) contendo todas as mensagens que você já salvou para esse chat no banco de dados, ordenadas bonitinho pelo tempo:

[
    {
        "id": "8f3b14d2-7c39-44bb-ba52-ea1c324869fa",
        "chat_id": "5041e5e1-dd51-4af8-8b88-7d66855d0e0d",
        "sender_id": "3cad9271-bf1a-4d74-9844-3d969bc7491d",
        "content": "Olá! Esta é a minha primeira mensagem enviada de forma segura através da API.",
        "created_at": "2026-06-05T12:05:22.184000"
    }
]

