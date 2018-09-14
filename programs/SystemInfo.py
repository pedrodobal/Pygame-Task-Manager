import platform

def os(): ##Qual Sistema Operacional esta Utilizando##
    return platform.uname().system
def osVersion(): ##Versão do Sistema Operacional##
    return platform.uname().version
def name(): ##Nome do Computador na Rede##
    return platform.uname().node
def arc(): ##Arquitetura da Maquina##
    return platform.uname().machine
def cpu(): ##Modelo do processador##
    return platform.uname().processor