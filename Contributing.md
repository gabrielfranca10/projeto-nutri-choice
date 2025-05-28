# 🥗 Guia de Contribuição para o Projeto NutriChoice

Seja bem-vindo(a) à comunidade de desenvolvimento do **NutriChoice**! Agradecemos por seu interesse em contribuir com este projeto, uma plataforma de recomendação nutricional personalizada, desenvolvida com o framework Django. O NutriChoice nasceu como um projeto acadêmico da CESAR School com o objetivo de ajudar pessoas a adotarem hábitos alimentares mais saudáveis com base em seu perfil.

Este guia tem como objetivo orientá-lo sobre como colaborar com o projeto, seja implementando novas funcionalidades, corrigindo bugs ou propondo melhorias. Recomendamos a leitura completa antes de começar, para entender nosso fluxo de trabalho e as boas práticas adotadas pela equipe.

---

## 🚀 Como Você Pode Contribuir?

Você pode ajudar de diversas formas:

- Desenvolvendo novas funcionalidades (ex: histórico de peso, chatbot NutriBot, dicas diárias, etc.)
- Corrigindo erros e bugs detectados no sistema
- Sugerindo melhorias na interface (UI/UX) com Tailwind CSS
- Melhorando a organização do backend
- Criando ou melhorando a documentação

> 💡 Para ideias e tarefas disponíveis, confira a aba **Issues** do repositório.

---

## ⚙️ Preparando Seu Ambiente

1. **Faça um fork do projeto**  
   Crie um fork do repositório [`gabrielfranca10/projeto-nutri-choice`](https://github.com/gabrielfranca10/projeto-nutri-choice) para a sua conta no GitHub.

2. **Clone o fork localmente**  
   ```bash
   git clone https://github.com/seuusuario/projeto-nutri-choice.git
   cd projeto-nutri-choice
   ```

3. **Crie uma nova branch para suas alterações**  
   ```bash
   git checkout -b nome-da-sua-nova-branch
   ```  
   Use nomes descritivos como `fix/correcao-formulario` ou `feature/chatbot-nutribot`.

---

## 🛠️ Configurando o Ambiente de Desenvolvimento

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Aplique as migrações do banco de dados:

   ```bash
   python manage.py migrate
   ```

4. Execute o servidor local:

   ```bash
   python manage.py runserver
   ```

---

## ✅ Regras e Boas Práticas

- ❌ Não utilize Django Forms nem Generic Views (restrição do projeto).
- ✅ Use views baseadas em função (FBVs) e manipulação direta de `request.POST`.
- 🎨 Mantenha o estilo visual consistente (Tailwind CSS, design moderno).
- 🧪 Teste suas alterações antes de abrir um Pull Request.
- 📝 Utilize mensagens de commit claras e explicativas.

---

## 🧪 Testes e Qualidade

1. Certifique-se de ter o Node.js instalado em sua máquina (recomendamos a versão LTS).

2. Instale as dependências do frontend, se aplicável:

   ```bash
   npm ci
   ```

3. Execute os testes com Cypress:

   ```bash
   npx cypress run
   ```

---

## 📄 Submetendo seu Pull Request

1. Commit suas alterações:

   ```bash
   git add .
   git commit -m "feat: adiciona funcionalidade X"
   ```

2. Envie sua branch para seu fork:

   ```bash
   git push origin nome-da-sua-branch-nova
   ```

3. Vá até o seu repositório no GitHub e clique em **"Compare & pull request"**.

4. Preencha o título e a descrição detalhando o que foi feito e por quê.

5. Aguarde a revisão e possíveis comentários da equipe.

---

## 👥 Revisão e Agradecimentos

Seu PR será revisado com atenção e carinho 💚. A revisão poderá incluir:

- Sugestões de melhoria no código
- Solicitação de ajustes para manter a consistência do projeto
- Discussões sobre design ou funcionalidade

Agradecemos desde já pela sua contribuição! Cada colaboração nos aproxima de oferecer uma plataforma mais útil, bonita e funcional para os usuários.

---

## 📬 Contato

Dúvidas, sugestões ou problemas? Entre em contato com o time:

- **Caio Leimig Rodrigues da Silva** (@caioleimig)  
- **Fernando Soares da Silva** (@Fernandosoares10)  
- **Gabriel França de Albuquerque Pernambuco** (@gabrielfranca10) – francagabriel285@gmail.com  
- **Guilherme Baltar**
- **Guilherme Burle Medeiros**
- **Yan Ribeiro Nunes** (@yan791)
