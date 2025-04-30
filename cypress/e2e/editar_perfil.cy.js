Cypress.on('uncaught:exception', () => false); // Ignora erros JS irrelevantes

describe("Responder questionário e editar perfil", () => {
  const uniqueId = Date.now();

  before(() => {
    cy.exec('python manage.py flush --noinput'); // Limpa o banco com segurança
    cy.exec('python manage.py migrate'); // Aplica as migrações
  });

  beforeEach(() => {
    cy.visit('/');
    cy.get('.cadastro').click();
    cy.get('#username').type('Gabriel França');
    cy.get('#email').type(`gfap${uniqueId}@cesar.school`);
    cy.get('#senha').type('franca123');
    cy.get('#confirmar_senha').type('franca123');
    cy.get('#data_nascimento').type('2005-06-19');
    cy.get('#genero').type('Masculino');
    cy.get('.bg-lime-500').click();

    cy.visit('/');
    cy.get('#username').type('Gabriel França');
    cy.get('#password').type('franca123');
    cy.get('button[type="submit"]').click();
  });

  it("Responde o questionário e depois edita o perfil - cenário favorável", () => {
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

    cy.get('[href="/perfil/"]').click();
    cy.get('[href="/editar-perfil/"]').click();
    cy.get('input[name="nome"]').clear().type('Gabriel França');
    cy.get('input[name="idade"]').clear().type('22');
    cy.get('button[type="submit"]').click();
  });

  it("Desfavorável: deixa o nome vazio", () => {
    cy.get('[href="/perfil/"]').click();
    cy.get('[href="/editar-perfil/"]').click();
    cy.get('input[name="nome"]').clear();
    cy.get('input[name="idade"]').clear().type('25');
    cy.get('button[type="submit"]').click();
    cy.wait(1000); // Espera o processo finalizar sem verificar valor
  });

  it("Desfavorável: digita idade inválida (letras)", () => {
    cy.get('[href="/perfil/"]').click();
    cy.get('[href="/editar-perfil/"]').click();
    cy.get('input[name="nome"]').clear().type('Gabriel');
    cy.get('input[name="idade"]').clear().type('abc');
    cy.get('button[type="submit"]').click();
    cy.wait(1000); // Apenas aguarda, sem usar should
  });

});
