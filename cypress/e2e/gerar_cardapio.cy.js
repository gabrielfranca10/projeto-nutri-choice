describe("Cardápio Personalizado - NutriChoice", () => {
  const uniqueId = Date.now();

  beforeEach(() => {
    cy.exec('python manage.py flush --noinput');
    cy.exec('python manage.py migrate');

    // Cadastro
    cy.visit('/cadastro/');
    cy.get('#nome').type('Gabriel França');
    cy.get('#username').type('gabriel_franca');
    cy.get('#email').type(`gfap${uniqueId}@cesar.school`);
    cy.get('#senha').type('franca123');
    cy.get('#confirmar_senha').type('franca123');
    cy.get('.btn-cadastrar').click();
    cy.get('.msg-success').should('exist');

    // Login
    cy.visit('/');
    cy.get('#username').type('gabriel_franca');
    cy.get('#password').type('franca123');
    cy.get('button[type="submit"]').click();

    // Preenche questionário
    cy.get('[href="/questionario/"]').click();
    cy.get('select[name="objetivo"]').select('perder');
    cy.get('input[name="restricoes"]').type('lactose');
    cy.get('textarea[name="preferencia"]').type('Gosto de frango, evito atum e batata doce');
    cy.get('input[name="refeicoes_por_dia"]').clear().type('4');
    cy.get('input[name="sono"]').clear().type('7');
    cy.get('select[name="atividade_fisica"]').select('3-4x');
    cy.get('select[name="come_carne"]').select('sim');
    cy.get('select[name="gosta_de_legumes"]').select('sim');
    cy.get('select[name="usa_suplementos"]').select('nao');
    cy.get('select[name="estresse"]').select('medio');
    cy.get('button[type="submit"]').click();
    cy.get('.bg-green-500').should('exist');
  });

  it("Cenário 1: Receber um cardápio adequado ao meu perfil", () => {
    cy.get('.p-4 > .bg-white').click();
    cy.get('[href="/cardapio/"]').click();
    cy.contains('Seu Cardápio Personalizado').should('exist');
    cy.get('.main-box').within(() => {
    });
  });

  it("Cenário 2: Atualizar o cardápio após mudanças no perfil", () => {
    cy.get('.p-4 > .bg-white').click();
    cy.get('[href="/questionario/"]').click();
    cy.get('select[name="objetivo"]').select('ganhar');
    cy.get('input[name="restricoes"]').clear().type('glúten');
    cy.get('textarea[name="preferencia"]').clear().type('Gosto de peixe, evito carne vermelha');
    cy.get('input[name="refeicoes_por_dia"]').clear().type('5');
    cy.get('input[name="sono"]').clear().type('8');
    cy.get('select[name="atividade_fisica"]').select('5+');
    cy.get('select[name="come_carne"]').select('nao');
    cy.get('select[name="gosta_de_legumes"]').select('sim');
    cy.get('select[name="usa_suplementos"]').select('sim');
    cy.get('select[name="estresse"]').select('baixo');
    cy.get('button[type="submit"]').click();
    cy.get('.bg-green-500').should('exist');

    cy.get('.p-4 > .bg-white').click();
    cy.get('[href="/cardapio/"]').click();

    // Verifica aviso de cardápio atualizado e as novas informações
    cy.get('.main-box').within(() => {
      cy.contains('Seu cardápio foi atualizado').should('exist');
      cy.contains('glúten').should('exist');
    });
  });

  it("Cenário 3: Receber um cardápio desatualizado", () => {
    cy.get('.p-4 > .bg-white').click();
    cy.get('[href="/cardapio/"]').click();

    cy.get('.main-box').within(() => {
    });
  });
});