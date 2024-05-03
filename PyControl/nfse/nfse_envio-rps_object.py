from nfse.classes.abrasf_nfsev20 import *


class NFSe_Envio_RPS:

    def __init__(self, CPFCNPJRemetente : str, InscricaoPrestador, SerieRPS, NumeroRPS, TipoRPS, DataEmissao ,StatusRPS, TributacaoRPS,
                 ValorServicos, ValorDeducoes, ValorPIS, ValorIR, ValorCSLL, ValorCOFINS, ValorINSS, CodigoServico, AliquotaServicos,
                 ISSRetido, CPFCNPJTomador, RazaoSocialTomador, Logradouro, NumeroEndereco, ComplementoEndereco, Bairro, Cidade, UF,
                 CEP, EmailTomador, Discriminacao):
        self.CPFCNPJRemetente = CPFCNPJRemetente
        self.InscricaoPrestador = InscricaoPrestador
        self.SerieRPS = SerieRPS
        self.NumeroRPS = NumeroRPS
        self.TipoRPS = TipoRPS
        self.DataEmissao = DataEmissao
        self.StatusRPS = StatusRPS
        self.TributacaoRPS = TributacaoRPS
        self.ValorServicos = ValorServicos
        self.ValorDeducoes = ValorDeducoes
        self.ValorPIS = ValorPIS
        self.ValorIR = ValorIR
        self.ValorCSLL = ValorCSLL
        self.ValorCOFINS = ValorCOFINS
        self.ValorINSS = ValorINSS
        self.CodigoServico = CodigoServico
        self.AliquotaServicos = AliquotaServicos
        self.ISSRetido = ISSRetido
        self.CPFCNPJTomador = CPFCNPJTomador
        self.RazaoSocialTomador = RazaoSocialTomador
        self.Logradouro = Logradouro
        self.NumeroEndereco = NumeroEndereco
        self.ComplementoEndereco = ComplementoEndereco
        self.Bairro = Bairro
        self.Cidade = Cidade
        self.UF = UF
        self.CEP = CEP
        self.EmailTomador = EmailTomador
        self.Discriminacao = Discriminacao

    nota = {
        "CPFCNPJRemetente": "01234567890987",
        "InscricaoPrestador": "01234567",
        "SerieRPS": "TESTE",
        "NumeroRPS": "9117092019",
        "TipoRPS": "RPS",
        "DataEmissao": "2019-07-09",
        "StatusRPS": "N",
        "TributacaoRPS": "T",
        "ValorServicos": "1",
        "ValorDeducoes": "0",
        "ValorPIS": "0",
        "ValorIR": "0",
        "ValorCSLL": "0",
        "ValorCOFINS": "0",
        "ValorINSS": "0",
        "CodigoServico": "05895",
        "AliquotaServicos": "2",
        "ISSRetido": "false",
        "CPFCNPJTomador": "01234567654321",
        "RazaoSocialTomador": "SOME COMPANY NAME",
        "Logradouro": "Rua Um",
        "NumeroEndereco": "123",
        "ComplementoEndereco": "Centro",
        "Bairro": "Vila Unica",
        "Cidade": "3550308",
        "UF": "SP",
        "CEP": "00000000",
        "EmailTomador": "none@none.com",
        "Discriminacao": "Teste de emissao de NFS-e de boletos prestados",
    }