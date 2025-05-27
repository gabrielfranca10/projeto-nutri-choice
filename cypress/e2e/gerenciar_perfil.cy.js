describe('Gerenciar Perfil - NutriChoice', () => {
  beforeEach(() => {
    // Limpa o banco e cadastra/loga o usuário
    cy.exec('python manage.py flush --noinput');
    cy.exec('python manage.py migrate');
    cy.visit('/cadastro/');
    cy.get('#nome').type('Usuário Teste');
    cy.get('#username').type('usuario_teste');
    cy.get('#email').type('teste@exemplo.com');
    cy.get('#senha').type('12345');
    cy.get('#confirmar_senha').type('12345');
    cy.get('.btn-cadastrar').click();
    cy.get('.msg-success').should('exist');
    cy.visit('/');
    cy.get('#username').type('usuario_teste');
    cy.get('#password').type('12345');
    cy.get('button[type="submit"]').click();
  });

  it('Cenário 1: Editar informações pessoais (Favorável)', () => {
    cy.get('[href="/editar-perfil/"]').click();

    // Altera nome e idade
    cy.get('input[name="nome"]').clear().type('Novo Nome');
    cy.get('input[name="idade"]').clear().type('28');
    cy.get('form button[type="submit"]').click();

    // Deve redirecionar para o perfil e mostrar mensagem de sucesso
    cy.url().should('include', '/perfil');
  });

  it('Cenário 2: Tentar editar informações sem preencher todos os campos obrigatórios (Desfavorável)', () => {
    cy.get('[href="/editar-perfil/"]').click();

    // Deixa o nome em branco
    cy.get('input[name="nome"]').clear();
    cy.get('input[name="idade"]').clear().type('28');
    cy.get('form button[type="submit"]').click();

    // Deve mostrar mensagem de erro
    cy.contains('O campo nome é obrigatório.').should('exist');

    // Deixa a idade em branco
    cy.get('input[name="nome"]').clear().type('Novo Nome');
    cy.get('input[name="idade"]').clear();
    cy.get('form button[type="submit"]').click();

    cy.contains('O campo idade é obrigatório.').should('exist');

    // Idade inválida
    cy.get('input[name="nome"]').clear().type('Novo Nome');
    cy.get('input[name="idade"]').clear().type('-5');
    cy.get('form button[type="submit"]').click();

    cy.contains('Informe uma idade válida.').should('exist');
  });

  it('Cenário 3: Excluir conta do usuário (Desfavorável)', () => {
    cy.get('.text-red-500').click();

    // Clica em "Sim, Excluir"
    cy.get('form button[type="submit"]').contains('Sim, Excluir').click();

    // Deve redirecionar para login e mostrar mensagem de sucesso
    cy.url().should('include', '/login');
    cy.contains('Sua conta foi excluída com sucesso.').should('exist');
  });
});