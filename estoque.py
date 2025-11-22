from datetime import datetime

produtos = []
movimentacoes = []

'''
 Funcao para cadastro de produtos
 RF1 - Selecionar produtos cadastrados para movimentação
 RF2 - Registrar entrada de produtos
 RF3 - Atualizar automaticamente o estoque na entrada
'''
def cadastro_produtos():
    print('Cadastro de produtos \n')
    
    nome_produto = input('Digite o nome do produto: ')
    qtd = int(input('Digite a quantidade de produtos: '))
    
    produto_base = verifica_nome_produto(nome_produto)
    
    # Neste IF ele verifica se existe existe
    if produto_base:
        
        # Atualiza a quantidade do produto existente na base
        produto_base['quantidade'] += qtd
        
        # Cadastra a movimentacao da atualizacao de estoque do produto
        cadastro_movimentacoes(produto_base, "ENTRADA", produto_base['quantidade'])
        
        print(f'Produto: {produto_base['nome']} com nova quantidade no estoque: {produto_base['quantidade']} \n')
    
    else:
        
        # Cadastra um novo produto na base com id, nome e quantidade 
        produto = {
            "id": len(produtos) + 1,
            "nome": nome_produto.lower(),
            "quantidade": qtd
        }
        
        # Adiciona o produto criado no estoque
        produtos.append(produto)
        
        # Chama funcao para cadastrar movimentacao no estoque
        cadastro_movimentacoes(produto, 'ENTRADA', qtd)
        
        print(f'Produto {nome_produto} cadastrado com sucesso \n')
        

# Verifica existencia de produto na base
def verifica_nome_produto(nome: str):
    # Verifica o nome de cada produto para verificar se existe na base
    for produto in produtos:
        if produto['nome'] == nome.lower():
            return produto
            
    return None


# Funcao para obter lista de produtos
# RNF6 - Precisão no controle de estoque.
def lista_produtos():
    print('Lista de produtos estoque \n')
    
    # Verifica se existe produtos no estoque para serem retornados 
    if not produtos:
        print('Estoque vazio! \n')
    
    # Retorna produtos um por vez
    for p in produtos:
        print(p)
    
    print()
    


# Funcao para registro de saida de produtos
# RF4 - Registrar saída de produtos
# RNF1 - Consistência dos dados de estoque
# RNF3 - Validação obrigatória antes da saída
def registro_saida_produtos():
    print('Registro de saida de produtos \n')
    
    # Listar produtos para verificar o ID
    lista_produtos()
    
    id_produto = int(input('ID do produto para remover: '))
    
    produto = buscar_produto_id(id_produto)
    
    # verificacao se produto existe
    if not produto:
        print(f'Produto id {id_produto} nao encontrado. Passar um id valido \n')
        return
    
    qtd = int(input('Quantidade para ser removida: '))
    
    # Valida se existe quantidade disponivel para realizar a saida de produtos
    if not validacao_quantidade_produto(produto, qtd):
        print(f'Quantidade solicitada indisponivel para realizar a saida dos produtos. \n')
        return
    
    # Atualiza a quantidade disponivel no estoque pelo novo valor
    produto['quantidade'] -= qtd
    
    # Chama funcao para cadastrar a movimentacao de saida de produtos do estoque
    cadastro_movimentacoes(produto, "SAIDA", qtd)
    
    print(f'Produto {produto['nome']} com nova saida do estoque. novo estoque está com {produto['quantidade']} \n')
    
    
# RF6 – Registrar movimentações com data e responsável.     
def lista_movimentacoes():
    print('Todas as movimentacoes do estoque \n')
    
    # Verifica se existe movimentacoes na base
    if not movimentacoes:
        print('Estoque nao teve movimentacoes ainda')
        return

    # Imprime cada movimentacao existente
    for movimentacao in movimentacoes:
        print(movimentacao)


# RF1 - Selecionar produtos cadastrados para movimentação
# RNF4 – Rastreabilidade das movimentações
# RNF5 - Manutenção de histórico das operações
def cadastro_movimentacoes(produto: dict, tipo: str, quantidade: int):
    
    nome_responsavel = input('Nome responsavel: ')
    data_agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cadastro_movimentacao = {
        'produto_id': produto['id'],
        'tipo': tipo,
        'quantidade': quantidade,
        'data_hora': data_agora,
        'responsavel': nome_responsavel
    }
    
    movimentacoes.append(cadastro_movimentacao)
    print(f'Cadastro de movimentacao tipo {tipo} responsavel: {nome_responsavel} \n')


# funcao para validar a quantidade do produto no estoque para realizar o delete da quantidade!
# RF5- Validar quantidade de produtos antes de saída
def validacao_quantidade_produto(produto: dict, qtd_produto: int) -> bool:
    return qtd_produto > 0 and produto['quantidade'] >= qtd_produto

# Buscar produto por ID antes de realizar qualquer coisa
def buscar_produto_id(id_produto: int):
    
    for p in produtos:
        if p['id'] == id_produto:
            return p
        
    return None
    
    

def main():
    while True:
        print('--- Menu Estoque ---')
        print('--- 1 - Cadastro de Produtos ---')
        print('--- 2 - Lista de Produtos Estoque ---')
        print('--- 3 - Registro de Saida de Produtos ---')
        print('--- 4 - Lista Movimentacoes Estoque ---')
        print('--- 0 - Sair do Estoque ---')
        
        opcao = input('Escolha uma opcao: ')

        if opcao == '1':
            cadastro_produtos()
            
        elif opcao == '2':
            lista_produtos()
            
        elif opcao == '3':
            registro_saida_produtos()
        
        elif opcao == '4':
            lista_movimentacoes()
        
        elif opcao == '0':
            print('Saindo do estoque\n')
            break
        
        else:
            print(f'Opcao {opcao} invalida. Passe uma opcao valida!')

if __name__ == "__main__":
    main()