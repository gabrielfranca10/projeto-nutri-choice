describe('Dicas Diárias de Alimentação Saudável - História do Usuário', () => {
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

  it('Cenário 1: Receber dicas diárias corretamente (Favorável)', () => {
    cy.get('[href="/dicas-nutricionais/"]').click();
    cy.get('#btn-activate').click();
  });

    it('Cenário 2: Não receber dicas por falha na configuração (Desfavorável)', () => {
    // Acessa a página de dicas nutricionais
    cy.get('[href="/dicas-nutricionais/"]').click();

  // Garante que as dicas estão desativadas (se necessário)
    cy.get('#btn-deactivate').then($btn => {
      if ($btn.is(':visible')) {
        cy.wrap($btn).click();
      }
    });

  // Simula erro na ativação das dicas diárias
    cy.window().then((win) => {
    win.simulateActivationError = () => true;
    });

  // Tenta ativar as dicas diárias
    cy.get('#btn-activate').should('be.visible').click();

  // Verifica que a mensagem de erro aparece
    cy.get('#error-message')
    .should('be.visible')
    .and('contain', 'Erro ao ativar notificações');

  // Verifica que não há dica diária ativa
    cy.get('#daily-tip-container').should('contain', 'Notificações de dicas diárias desativadas.');
    cy.get('#btn-know').should('not.be.visible');
    });

  it('Cenário 3: Receber dicas repetidas constantemente (Desfavorável)', () => {
    cy.get('[href="/dicas-nutricionais/"]').click();
    cy.get('#btn-activate').should('be.visible').click();
  });
});