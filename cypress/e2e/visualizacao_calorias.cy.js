describe('Ingestão de Calorias - NutriChoice', () => {
  beforeEach(() => {
    // Limpa o banco e cadastra/loga o usuário
    cy.exec('python manage.py flush --noinput');
    cy.exec('python manage.py migrate');
    cy.visit('/cadastro/');
    cy.get('#nome').type('Lil Gabi');
    cy.get('#username').type('lilgabi22');
    cy.get('#email').type('france@gmail.com');
    cy.get('#senha').type('12345');
    cy.get('#confirmar_senha').type('12345');
    cy.get('.btn-cadastrar').click();
    cy.get('.msg-success').should('exist');
    cy.visit('/');
    cy.get('#username').type('lilgabi22');
    cy.get('#password').type('12345');
    cy.get('button[type="submit"]').click();
  });

  it('Cenário 1: Exibir total de calorias corretamente (Favorável)', () => {
    cy.get('[href="/app/calorias/"]').click();
    // Adiciona refeições
    cy.contains('+250 kcal').click();
    cy.contains('+500 kcal').click();

    // Verifica o total exibido
    cy.get('#progresso-texto')
      .should('contain', '750 kcal de 2500 kcal recomendadas');
    cy.get('#mensagem-nenhum-dado').should('have.class', 'hidden');
  });

  it('Cenário 2: Nenhum alimento registrado (Desfavorável)', () => {
    cy.get('[href="/app/calorias/"]').click();
    // Não adiciona nada, só acessa a página
    cy.get('#progresso-texto')
      .should('contain', '0 kcal de 2500 kcal recomendadas');
    cy.get('#mensagem-nenhum-dado')
      .should('not.have.class', 'hidden')
      .and('contain', 'Nenhuma refeição registrada para hoje');
  });

  it('Cenário 3: Atualizar total após nova refeição (Favorável)', () => {
    cy.get('[href="/app/calorias/"]').click();
    // Adiciona uma refeição
    cy.contains('+500 kcal').click();
    cy.get('#progresso-texto')
      .should('contain', '500 kcal de 2500 kcal recomendadas');

    // Adiciona mais uma refeição
    cy.contains('+1000 kcal').click();

    // O total deve ser atualizado automaticamente
    cy.get('#progresso-texto')
      .should('contain', '1500 kcal de 2500 kcal recomendadas');
  });
});
