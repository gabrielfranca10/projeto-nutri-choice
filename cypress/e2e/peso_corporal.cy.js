describe('Registro de Peso - NutriChoice', () => {
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

  it('Cenário 1: Adicionar novo peso com sucesso (Favorável)', () => {
    cy.get('[href="/registrar-peso/"]', { timeout: 10000 }).should('be.visible').click();
    // Preenche mês e peso
    cy.get('#mes-peso').type('2024-06');
    cy.get('#peso-atual').type('70.5');
    cy.get('form#form-peso button[type="submit"]').click();

    // Verifica mensagem de sucesso
    cy.get('#peso-salvo')
      .should('contain', '✅ Peso de 70.5kg salvo para o mês de 2024-06.');
  });

  it('Cenário 2: Inserir peso com data repetida (Desfavorável)', () => {
    cy.get('[href="/registrar-peso/"]', { timeout: 10000 }).should('be.visible').click();
    // Registra um peso para o mês
    cy.get('#mes-peso').type('2024-06');
    cy.get('#peso-atual').type('70.5');
    cy.get('form#form-peso button[type="submit"]').click();
    cy.get('#peso-salvo').should('contain', '70.5kg salvo');

    // Tenta registrar outro peso para o mesmo mês
    cy.get('#mes-peso').clear().type('2024-06');
    cy.get('#peso-atual').clear().type('72.0');

    // Stub do confirm para simular o usuário clicando em "Cancelar"
    cy.window().then((win) => {
      cy.stub(win, 'confirm').returns(false);
    });
    cy.get('form#form-peso button[type="submit"]').click();
    cy.get('#peso-salvo').should('contain', '❌ Registro não alterado.');

    // Stub do confirm para simular o usuário clicando em "OK"
    cy.window().then((win) => {
      win.confirm.restore && win.confirm.restore(); // Remove o stub anterior, se existir
      cy.stub(win, 'confirm').returns(true);
    });
    cy.get('form#form-peso button[type="submit"]').click();
    cy.get('#peso-salvo').should('contain', '✅ Peso de 72.0kg salvo para o mês de 2024-06.');
  });

  it('Cenário 3: Inserir valor inválido de peso (Desfavorável)', () => {
    cy.get('[href="/registrar-peso/"]', { timeout: 10000 }).should('be.visible').click();
    // Peso negativo
    cy.get('#mes-peso').type('2024-07');
    cy.get('#peso-atual').type('-10');
    cy.get('form#form-peso button[type="submit"]').click();
    cy.get('#peso-salvo').should('contain', '❌ Por favor, insira um valor válido de peso');

    // Peso zero
    cy.get('#peso-atual').clear().type('0');
    cy.get('form#form-peso button[type="submit"]').click();
    cy.get('#peso-salvo').should('contain', '❌ Por favor, insira um valor válido de peso');

    // Peso não numérico
    cy.get('#peso-atual').clear().type('abc');
    cy.get('form#form-peso button[type="submit"]').click();
    cy.get('#peso-salvo').should('contain', '❌ Por favor, insira um valor válido de peso');
  });
});
