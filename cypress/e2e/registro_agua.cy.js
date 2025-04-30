describe("Registro diário de Água", () => {
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
  
    it("Cenário Favorável: Confirmação de ingestão de água", () => {
        cy.get('[href="/agua/"]').click();
        cy.get('.bg-blue-400').click();
        cy.get('.bg-blue-500').click();
        cy.get('.bg-blue-600').click();
        cy.get('.bg-blue-600').click();
        cy.get('.bg-blue-600').click();
        cy.get('.bg-blue-600').click();
        cy.get('.inline-block').click();
    });

    it("Cenário Desfavorável: Tentativa de finalizar sem registrar ingestão de água", () => {
        cy.get('[href="/agua/"]').click();

        cy.get('.inline-block').click();

    });

    it("Cenário Desfavorável: Registro parcial de ingestão de água e abandono", () => {
        cy.get('[href="/agua/"]').click();
        cy.get('.bg-blue-400').click();
        cy.get('.bg-blue-500').click();    
        cy.visit('/perfil/');
        cy.get('[href="/agua/"]').click();
      });
  
  });
  