
# bot-discord
#### PT
Bot de musica para o discord que eu desenvolvi com auxilio de inteligência artificical.\
Sinta-se livre para utilizar ou implementá-lo.

#### EN

Music bot for discord that I made with AI assistance.\
Feel free to use or implement it. 





## Como instalar

Versão do python utilizada: 3.10

### Configurando o ambiente virtual
Fonte: https://dev.to/franciscojdsjr/guia-completo-para-usar-o-virtual-environment-venv-no-python-57bo

Como Criar um Ambiente Virtual com o venv
O venv é uma biblioteca Python padrão, disponível nas versões 3.3 e posteriores. Para criar um ambiente virtual, siga os passos abaixo:

#### 1. Abra um Terminal
Abra o terminal ou prompt de comando do seu sistema operacional.

#### 2. Navegue até o Diretório do Projeto
Use o comando cd para navegar até o diretório raiz do seu projeto.

`> cd /caminho/do/seu/projeto`
#### 3. Crie o Ambiente Virtual
Use o comando ``python -m venv nome_do_ambiente`` para criar um ambiente virtual com o nome desejado. Substitua 'nome_do_ambiente' pelo nome que você escolher para o ambiente virtual.

`> python -m venv meu_ambiente_virtual`
#### 4. Ative o Ambiente Virtual
Dependendo do seu sistema operacional, o comando para ativar o ambiente virtual varia:

No Windows:

``> meu_ambiente_virtual\Scripts\activate``

No macOS e Linux:

``$ source meu_ambiente_virtual/bin/activate``

Você verá o nome do ambiente virtual atual no prompt do terminal, indicando que o ambiente foi ativado com sucesso.

### Como Desativar um Ambiente Virtual
Para desativar um ambiente virtual e retornar ao ambiente global do Python, basta digitar:

``> deactivate``

### Como Instalar Pacotes em um Ambiente Virtual
Com o ambiente virtual ativado, você pode instalar pacotes e bibliotecas específicos para o seu projeto sem afetar o ambiente global do Python. Use o comando pip para instalar pacotes:

``> pip install nome_do_pacote``

Por exemplo, para instalar a biblioteca requests em um ambiente virtual:

``> pip install requests``

### Como Usar um Ambiente Virtual em um Projeto Python
Agora que o ambiente virtual está ativado e as bibliotecas necessárias estão instaladas, você pode executar seu projeto Python normalmente. Todas as dependências serão carregadas a partir do ambiente virtual.

### Exemplo bot-discord
Vamos criar um ambiente virtual para o bot

#### Crie um ambiente virtual chamado ".bot":
``> python -m venv .bot``

#### Ative o ambiente virtual:
``> .\bot-discord\Scripts\activate`` # Windows

`$ source bot-discord/Scripts/activate`  # No macOS e Linux

#### Instale as bibliotecas/requisitos
``> pip install -r .\requirements.txt``

#### Iniciando o bot
`> python bot.py`

Lembre-se de sempre ativar o ambiente virtual (`.\bot-discord\Scripts\activate`) antes de rodar o bot.

Você também pode rodar o bot diretamente, utilizando:\
`> <diretório do bot>\.bot\Scripts\python.exe "<diretório do bot>\bot-discord\bot.py"`

**Exemplo:** `> G:\bot_discord\.venv\Scripts\python.exe "G:\bot_discord\bot.py"`


## Documentação

### Identificadores Obrigatórios (`\.env`)
| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `TOKEN` | `string` | TOKEN do seu bot ***Obrigatório**.  |
| `GUILD` | `string` | ID da sua guild/servidor ***Obrigatório**.  |
| `APP_ID` | `string` | APP ID do seu bot ***Obrigatório**.  |

### Comandos ('/')
| Comandos   | Descrição                                    |
| :---------- | :------------------------------------------ |
| `ping`      | `Pong! (retorna a latência em ms)`                      |
| `test`      | `Responde com uma mensagem de teste.` |
| `play`      | `Toca uma música selecionada do YouTube.`   |
| `skip`      | `Pula a música atual que está tocando.`     |
| `queue`     | `Exibe as músicas atualmente na fila.`      |
| `clear`     | `Limpa a fila.`                |
| `stop`      | `Desconecta o bot do canal de voz.`         |
| `help`      | `Exibe a lista de comandos disponíveis.`    |


## Referência

 - [Guia Completo para Usar o Virtual Environment (venv) no Python](https://dev.to/franciscojdsjr/guia-completo-para-usar-o-virtual-environment-venv-no-python-57bo)
