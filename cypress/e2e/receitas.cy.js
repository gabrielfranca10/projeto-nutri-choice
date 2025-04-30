describe("Visualizar receitas culinárias", () => {
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
  
    it("Cenário Favorável: Buscar receita e exibir ingredientes e modo de preparo", () => {
      cy.get('[href="/perfil/"]').click();
      cy.get('[href="/receitas/"]').click();
      cy.get(':nth-child(1) > button > .text-xl').click();
      cy.get('.space-y-4 > :nth-child(2)').click();
      cy.get('.space-y-4 > :nth-child(3)').click();
      cy.get(':nth-child(4) > button > .text-xl').click();
      cy.get(':nth-child(5) > button > .text-xl').click();
      cy.get('.space-y-4 > :nth-child(6)').click();
      cy.get(':nth-child(7) > button > .text-xl').click();
      cy.get(':nth-child(8) > button > .text-xl').click();
      cy.get('.btn-primary').click();
    });
  
  });
  