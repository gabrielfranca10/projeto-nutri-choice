describe("Visualizar receitas culinárias", () => {
  const uniqueId = Date.now();

  beforeEach(() => {
    cy.exec('python manage.py flush --noinput');
    cy.exec('python manage.py migrate');
    cy.visit('/cadastro/');
    cy.get('#nome').type('Guilherme Burle');
    cy.get('#username').type('guibu10');
    cy.get('#email').type('burle@gmail.com');
    cy.get('#senha').type('12345');
    cy.get('#confirmar_senha').type('12345');
    cy.get('.btn-cadastrar').click();
    cy.get('.msg-success').should('exist');
    cy.visit('/');
    cy.get('#username').type('guibu10');
    cy.get('#password').type('12345');
    cy.get('button[type="submit"]').click();
  });

  it("Cenário 1: Buscar receita e exibir ingredientes e modo de preparo (Favorável)", () => {
    // Dado que o usuário deseja visualizar a receita do chef;
    cy.get('[href="/receitas/"]').click();

    // Quando ele acessar a aba de Receitas Culinária e procurar por uma receita;
    cy.get('#search-recipe').type('Panqueca de Banana');
    cy.get('#btn-search').click();

    // Então o sistema exibirá os ingredientes e modo de preparo.
    cy.get('.recipe-title')
      .should('be.visible')
      .and('contain', 'Panqueca de Banana');
    cy.get('.recipe-ingredients')
      .should('be.visible')
      .and('not.be.empty');
    cy.get('.recipe-preparation')
      .should('be.visible')
      .and('not.be.empty');
  });

  it("Cenário 2: Buscar receita inexistente ou erro de digitação (Desfavorável)", () => {
    // Dado que o usuário acessa a aba de Receitas Culinárias e digita uma receita inexistente ou com erro de digitação;
    cy.get('[href="/receitas/"]').click();
    cy.get('#search-recipe').type('Cuscuz com Ovo');
    cy.get('#btn-search').click();

    // Então o sistema informará que a receita não foi encontrada
    cy.get('.msg-not-found')
      .should('be.visible')
      .and('contain', 'Receita não encontrada');

    // e sugerirá receitas semelhantes (se houver) ou recomendará ao usuário tentar novamente com outro nome.
    cy.get('.suggested-recipes').then($el => {
      if ($el.children().length > 0) {
        cy.get('.suggested-recipes').should('be.visible');
      } else {
        cy.get('.suggested-recipes').should('contain', 'tente novamente com outro nome');
      }
    });
  });

  it("Cenário 3: Campo de busca deixado em branco (Desfavorável)", () => {
    // Dado que o usuário acessa a aba de Receitas Culinárias;
    cy.get('[href="/receitas/"]').click();

    // Quando ele tenta realizar a busca sem digitar nada no campo de pesquisa;
    cy.get('#search-recipe').clear();
    cy.get('#btn-search').click();

    // Então o sistema exibirá uma mensagem de aviso solicitando que o usuário informe o nome de uma receita antes de prosseguir com a busca.
    cy.get('.msg-warning')
      .should('be.visible')
      .and('contain', 'digite o nome de uma receita antes de buscar');
  });
});