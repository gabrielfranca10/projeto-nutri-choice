describe('Registro de Ingestão de Água - NutriChoice', () => {
  beforeEach(() => {
    // Limpa o banco e cadastra/loga o usuário
    cy.exec('python manage.py flush --noinput');
    cy.exec('python manage.py migrate');
    cy.visit('/cadastro/');
    cy.get('#nome').type('Luis Guilherme');
    cy.get('#username').type('luisin');
    cy.get('#email').type('luisgx10@gmail.com');
    cy.get('#senha').type('12345');
    cy.get('#confirmar_senha').type('12345');
    cy.get('.btn-cadastrar').click();
    cy.get('.msg-success').should('exist');
    cy.visit('/');
    cy.get('#username').type('luisin');
    cy.get('#password').type('12345');
    cy.get('button[type="submit"]').click();
    // Limpa o localStorage antes de cada teste
    cy.visit('/agua/', {
      onBeforeLoad(win) {
        win.localStorage.clear();
      }
    });
  });

  it('Cenário 1: Registro bem-sucedido da ingestão de água (Favorável)', () => {
    cy.get('#quantidade').type('300');
    cy.get('form#water-form button[type="submit"]').click();

    cy.get('#message')
      .should('be.visible')
      .and('contain', 'Registro salvo com sucesso');
    cy.get('#history .registro-quantidade')
      .should('contain', '300 ml');
  });

  it('Cenário 2: Tentativa de registrar um valor inválido (Desfavorável)', () => {
  // Valor em branco
    cy.get('#quantidade').clear();
    cy.get('form#water-form button[type="submit"]').click();

  // Valor negativo
    cy.get('#quantidade').clear().type('-100');
    cy.get('form#water-form button[type="submit"]').click();

  // Valor não numérico
    cy.get('#quantidade').clear().type('abc');
    cy.get('form#water-form button[type="submit"]').click();
  });

  it('Cenário 3: Editar um registro de água já salvo (Favorável)', () => {
    // Adiciona um registro
    cy.get('#quantidade').type('200');
    cy.get('form#water-form button[type="submit"]').click();
    cy.get('#history .registro-quantidade').should('contain', '200 ml');

    // Stub do prompt ANTES de clicar em editar
    cy.window().then((win) => {
      cy.stub(win, 'prompt').returns('350');
    });

    // Clica em "Editar" do primeiro registro (apenas uma vez, pois o stub já está ativo)
    cy.get('#history .btn-editar').first().click();

    // Verifica mensagem de sucesso e histórico atualizado
    cy.get('#message')
      .should('be.visible')
      .and('contain', 'Registro atualizado com sucesso');
    cy.get('#history .registro-quantidade').should('contain', '350 ml');
  });
});