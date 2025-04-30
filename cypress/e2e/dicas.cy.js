describe("Visualizar dicas nutricionais", () => {
    const uniqueId = Date.now();
  
    beforeEach(() => {
      cy.exec('python manage.py flush --noinput');
      cy.exec('python manage.py migrate');
      
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
  
    });

    it("Cenário favorável: Confirmando visualização de dicas nutricionais", () => {
        cy.get('[href="/dicas-nutricionais/"]').click();
        cy.get(':nth-child(1) > button > .text-xl').click();
        cy.get(':nth-child(2) > button > .text-xl').click();
        cy.get(':nth-child(3) > button > .text-xl').click();
        cy.get(':nth-child(4) > button > .text-xl').click();
        cy.get(':nth-child(5) > button > .text-xl').click();
        cy.get('.btn-primary').click();         
    });
      
});
  

  