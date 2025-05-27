describe('Ingestão de Calorias - NutriChoice', () => {
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

    // Limpa o localStorage de calorias antes de cada teste
    cy.visit('/calorias', {
      onBeforeLoad(win) {
        win.localStorage.clear();
      }
    });
  });

  it('Cenário 1: Exibir total de calorias corretamente (Favorável)', () => {
    // Adiciona refeições
    cy.contains('+250 kcal').click();
    cy.contains('+500 kcal').click();

    // Verifica o total exibido
    cy.get('#progresso-texto')
      .should('contain', '750 kcal de 2500 kcal recomendadas');
    cy.get('#mensagem-nenhum-dado').should('have.class', 'hidden');
  });

  it('Cenário 2: Nenhum alimento registrado (Desfavorável)', () => {
    // Não adiciona nada, só acessa a página
    cy.get('#progresso-texto')
      .should('contain', '0 kcal de 2500 kcal recomendadas');
    cy.get('#mensagem-nenhum-dado')
      .should('not.have.class', 'hidden')
      .and('contain', 'Nenhuma refeição registrada para hoje');
  });

  it('Cenário 3: Atualizar total após nova refeição (Favorável)', () => {
    // Adiciona uma refeição
    cy.contains('+500 kcal').click();
    cy.get('#progresso-texto')
      .should('contain', '500 kcal de 2500 kcal recomendadas');

    // Simula sair e voltar para a página
    cy.visit('/perfil');
    cy.visit('/calorias');

    // Adiciona mais uma refeição
    cy.contains('+1000 kcal').click();

    // O total deve ser atualizado automaticamente
    cy.get('#progresso-texto')
      .should('contain', '1500 kcal de 2500 kcal recomendadas');
  });
});