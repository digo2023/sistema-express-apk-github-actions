# SISTEMA EXCLUSIVO - EXPRESS RESTAURANTES - UNIDADE COLORADO

Projeto preparado para gerar um APK Android usando GitHub Actions.

## Como gerar o APK

1. Crie um repositório no GitHub.
2. Envie todos os arquivos deste pacote para o repositório.
3. Abra a aba **Actions**.
4. Escolha **Gerar APK Android**.
5. Clique em **Run workflow**.
6. Ao finalizar, baixe o APK em **Artifacts** com o nome **SISTEMA-EXPRESS-APK**.

## Observação importante

O APK executa o sistema Python dentro de uma tela própria do aplicativo. O sistema mantém banco de dados, backups, relatórios e importações na pasta privada do aplicativo Android.

Para evitar perda de dados, use sempre o menu de backup do sistema.

## Uso no aplicativo

- Digite a opção desejada no campo inferior.
- Toque em **ENVIAR**.
- Use **999** para voltar/cancelar.
- Use **LIMPAR TELA** apenas para limpar a visualização, sem apagar dados.

## Pastas internas do sistema

Dentro do app, o sistema mantém:

- data
- backups
- relatorios/pdf
- relatorios/excel
- importar/analiticos
- importar/ordens_compra
- importar/backups
- importar/outros

