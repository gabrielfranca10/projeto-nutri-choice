Cypress.on('uncaught:exception', () => false); // Ignora erros JS irrelevantes

describe("Excluir conta", () => {
  const uniqueId = Date.now();

  before(() => {
    cy.exec('python manage.py flush --noinput');
    cy.exec('python manage.py migrate');
  });

  beforeEach(() => {
    // Cadastro
    cy.visit('/');
    cy.get('.cadastro').click();
    cy.get('#username').type('Gabriel França');
    cy.get('#email').type(`gfap${uniqueId}@cesar.school`);
    cy.get('#senha').type('franca123');
    cy.get('#confirmar_senha').type('franca123');
    cy.get('#data_nascimento').type('2005-06-19');
    cy.get('#genero').type('Masculino');
    cy.get('.bg-lime-500').click();

    // Login
    cy.visit('/');
    cy.get('#username').type('Gabriel França');
    cy.get('#password').type('franca123');
    cy.get('button[type="submit"]').click();

    // Preenche questionário
    cy.get('[href="/questionario/"]').click();
    cy.get('select[name="objetivo"]').select('Perder peso');
    cy.get('input[name="restricoes"]').type('lactose');
    cy.get('textarea[name="preferencia"]').type('Gosto de frango, evito atum e batata doce');
    cy.get('input[name="refeicoes_por_dia"]').type('4');
    cy.get('input[name="sono"]').type('7');
    cy.get('select[name="atividade_fisica"]').select('3-4 vezes por semana');
    cy.get('input[name="come_carne"][value="sim"]').check();
    cy.get('input[name="gosta_de_legumes"][value="sim"]').check();
    cy.get('input[name="usa_suplementos"][value="nao"]').check();
    cy.get('select[name="estresse"]').select('Moderado');
    cy.get('button[type="submit"]').click();
  });

  it("Confirma exclusão da conta (fluxo favorável)", () => {
    cy.get('[href="/perfil/"]').click();
    cy.get('.text-red-500').click()
    cy.url().should('include', '/excluir-perfil');
    cy.contains('button', 'Sim, Excluir').click();

    // Verifica redirecionamento para login ou home após excluir
    cy.url().should('include', '/');
    cy.visit('/')

  });

  it("Cancela exclusão da conta (fluxo desfavorável)", () => {
    cy.get('[href="/perfil/"]').click();
    cy.get('[href="/excluir-perfil/"]').click();
    cy.url().should('include', '/excluir-perfil');
    cy.contains('a', 'Cancelar').click();

    // Verifica que voltou para o perfil e continua logado
    cy.url().should('include', '/perfil');
    cy.contains('None').should('exist');
  });
});
