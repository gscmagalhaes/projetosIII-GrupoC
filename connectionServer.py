#implementar conexão com o servidor, envio e recebimento de dados

#função de check do status da conexão
def connectionStatus():
    # necessário implementar check de conexão
    setOn = 1 # simulação de status 'aguardando conexão'

    if setOn == 0: # sistema desconectado
        return 'off'
    elif setOn == 1: # sistema conectado
        return 'on'
    else: #sistema aguardadndo conexão
        return 'wait'

#função de check de status do guincho (retorno soble o acoplamento dos containers)
def getObjectStatus():
    # necessário implementar check de captação de objetos
    holdOn = 2 # simulação de status 'gancho ocupado'

    if holdOn == 0: # gancho livre
        return 'free'
    elif holdOn == 1: # gancho ocupado
        return 'hold'
    else: #ganho tentando coletar objeto
        return 'tring'