🥗 Guia de Contribuição para o Projeto NutriChoice

Seja bem-vindo(a) à comunidade de desenvolvimento do NutriChoice! Agradecemos por seu interesse em contribuir com este projeto, uma plataforma de recomendação nutricional personalizada, desenvolvida com o framework Django. O NutriChoice nasceu como um projeto acadêmico da CESAR School com o objetivo de ajudar pessoas a adotarem hábitos alimentares mais saudáveis com base em seu perfil.

Este guia tem como objetivo orientá-lo sobre como colaborar com o projeto, seja implementando novas funcionalidades, corrigindo bugs ou propondo melhorias. Recomendamos a leitura completa antes de começar, para entender nosso fluxo de trabalho e as boas práticas adotadas pela equipe.

🚀 Como Você Pode Contribuir?

Você pode ajudar de diversas formas:

Desenvolvendo novas funcionalidades (ex: histórico de peso, chatbot NutriBot, dicas diárias, etc.)

Corrigindo erros e bugs detectados no sistema

Sugerindo melhorias na interface (UI/UX) com Tailwind CSS

Melhorando a organização do backend

Criando ou melhorando a documentação

Para ideias e tarefas disponíveis, confira a aba "Issues" do repositório.

⚙️ Preparando Seu Ambiente

1. Faça um fork do projeto

Crie um fork do repositório gabrielfranca10/projeto-nutri-choice para a sua conta no GitHub.

2. Clone o fork

git clone https://github.com/gabrielfranca10/projeto-nutri-choice.git

3. Crie uma branch para suas alterações

git checkout -b nome da sua nova branch

Use nomes descritivos como fix/correcao-formulario ou feature/chatbot-nutribot.

🛠️ Configurando o Ambiente de Desenvolvimento

Crie e ative um ambiente virtual:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

Instale as dependências:

pip install -r requirements.txt

Aplique as migrações do banco de dados:

python manage.py migrate

Execute o servidor local:

python manage.py runserver
.

✅ Regras e Boas Práticas

Não utilize Django Forms nem Generic Views (restrição do projeto).

Use views baseadas em função (FBVs) e manipulação direta de request.POST.

Mantenha o estilo visual consistente (Tailwind CSS, design moderno).

Teste suas alterações antes de fazer o PR.

Utilize mensagens de commit claras e explicativas.

🧪 Testes e Qualidade

Certifique-se de ter o Node.js instalado em sua máquina (recomendamos a versão LTS).
Instale as dependências do Node.js listadas no package.json (se houver um e for necessário para os testes):

npm ci

Execute os testes Cypress:
npx cypress run

📄 Submetendo seu Pull Request

Commit suas alterações:

git add .
git commit -m "feat: adiciona funcionalidade X"

Envie sua branch para seu fork:

git push origin nome-da-sua-branch-nova

Vá até o seu repositório no GitHub e clique em "Compare & pull request".

Preencha o título e a descrição detalhando o que foi feito e por quê.

Aguarde a revisão e possíveis comentários da equipe.

👥 Revisão e Agradecimentos

Seu PR será revisado com atenção e carinho 💚. A revisão poderá incluir:

Sugestões de melhoria no código

Solicitação de ajustes para manter a consistência do projeto

Discussões sobre design ou funcionalidade

Agradecemos desde já pela sua contribuição! Cada colaboração nos aproxima de oferecer uma plataforma mais útil, bonita e funcional para os usuários.

📬 Contato

Dúvidas, sugestões ou problemas? Entre em contato com o time:

Caio Leimig Rodrigues da Silva(@caioleimig) -
Fernando Soares da Silva (@Fernandosoares10) - 
Gabriel França de Albuquerque Pernambuco (@gabrielfranca10) – francagabriel285@gmail.com
Guilherme Baltar () -
Guilherme Burle Medeiros () -
Yan Ribeiro Nunes (@yan791) - 



