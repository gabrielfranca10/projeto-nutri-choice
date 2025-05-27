describe("Questionário Nutricional - Cenários do Usuário", () => {
  beforeEach(() => {
    // Limpa o banco e cadastra um novo usuário
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

  it("Cenário 1: Preencher o questionário corretamente (Favorável)", () => {
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

    // Verifica mensagem de sucesso e botão de voltar ao perfil
    cy.get('.bg-green-500').should('exist');
    cy.contains('Voltar ao Perfil').should('exist');
    cy.get('a').contains('Voltar ao Perfil').click();
    cy.url().should('include', '/perfil/');
  });

  it("Cenário 2: Deixar o questionário incompleto (Desvaforável)", () => {
    cy.get('[href="/questionario/"]').click();

    // Preenche apenas alguns campos
    cy.get('select[name="objetivo"]').select('perder');
    cy.get('input[name="restricoes"]').type('lactose');
    // Não preenche o resto

    cy.get('button[type="submit"]').click();

    // Deve aparecer mensagem de erro/alerta
    cy.get('.error-message, .bg-red-500').should('exist');
  });

  it("Cenário 3: Abandonar o questionário antes de finalizar (Desfavorável)", () => {
    cy.get('[href="/questionario/"]').click();
    cy.get('select[name="objetivo"]').select('perder');
    cy.get('input[name="restricoes"]').type('lactose');
    // Sai da página antes de enviar
    cy.visit('/perfil/');

    // Volta para o questionário
    cy.get('[href="/questionario/"]').click();

    // Os campos devem estar vazios (não salvos)
    cy.get('select[name="objetivo"]').should('have.value', '');
    cy.get('input[name="restricoes"]').should('have.value', '');
  });
});