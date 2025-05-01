describe("Responder Questionario", () => {
  beforeEach(() => {
    cy.exec('python manage.py migrate');
    cy.visit('/');
    cy.get('.cadastro').click();
    cy.get('#username').type('Gabriel França');
    cy.get('#email').type('gfap@cesar.school');
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

  it("Caso favorável para responder questionário", () => {
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

  it("Caso desfavorável preencher o questionário com informações inconsistentes", () => {
    cy.get('[href="/questionario/"]').click();
  
  // Seleciona objetivo
    cy.get('select[name="objetivo"]').select('Ganhar massa muscular');
  
  // Declara restrição vegetariana
    cy.get('input[name="restricoes"]').type('vegetariano');
  
  // Afirma gostar de carne
    cy.get('textarea[name="preferencia"]').type('Gosto de carne vermelha e frango');
  
  // Número de refeições e sono
    cy.get('input[name="refeicoes_por_dia"]').type('5');
    cy.get('input[name="sono"]').type('8');
  
  // Frequência de atividade física
    cy.get('select[name="atividade_fisica"]').select('5 ou mais vezes por semana');
  
  // Diz que consome carne (inconsistência com restrição "vegetariano")
    cy.get('input[name="come_carne"][value="sim"]').check();
  
  // Gosta de legumes, usa suplementos
    cy.get('input[name="gosta_de_legumes"][value="sim"]').check();
    cy.get('input[name="usa_suplementos"][value="nao"]').check();
  
  // Estresse
    cy.get('select[name="estresse"]').select('Moderado');
  
    cy.get('button[type="submit"]').click();

    cy.get('#mensagem-erro').should('not.exist');
    cy.url().should('not.include', 'error'); 
  });


  it("Caso desfavorável para abandonar o questionário antes de finalizar", () => {
    cy.get('[href="/questionario/"]').click()
    cy.get('select[name="objetivo"]').select('Perder peso')
    cy.go('back')
    cy.get('[href="/questionario/"]').click()
    cy.get('select[name="objetivo"]').should('have.value', '')
  });

});
    
    // Implemente aqui se necessário
