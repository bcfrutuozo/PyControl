# coding: utf-8
from nfse.rps import Rps
from nfse.response import Response
from nfse.schemas import schemaCreateRps, schemaCancelRps, schemaConsultNfes
from nfse.functions import stringEncode, stringDecode
from requests import post


class TatuiGateway:

    @classmethod
    def sendRps(cls, privateKey, certificate, **kwargs):
        xml = Rps.xmlCreateRps(
            xml=schemaCreateRps,
            privateKeyContent=privateKey,
            certificateContent=certificate,
            **kwargs
        )

        return cls.sendRequest(
            xml=xml,
            privateKey=privateKey,
            certificate=certificate,
            url='http://tatui.jlsoft.com.br/Abrasf/ahrecepcionarloterpssincrono.aspx',
            method="rps",
        )

    @classmethod
    def cancelRps(cls, privateKey, certificate, **kwargs):
        xml = Rps.cancelRps(
            xml=schemaCancelRps,
            privateKeyContent=privateKey,
            certificateContent=certificate,
            **kwargs
        )

        return cls.sendRequest(
            xml=xml,
            privateKey=privateKey,
            certificate=certificate,
            url='http://tatui.jlsoft.com.br/Abrasf/ahcancelarnfse.aspx',
            method="rps",
        )

    @classmethod
    def consultNfes(cls, privateKey, certificate, **kwargs):
        xml = Rps.consultNfes(
            xml=schemaConsultNfes,
            privateKeyContent=privateKey,
            certificateContent=certificate,
            **kwargs
        )

        return cls.sendRequest(
            xml=xml,
            privateKey=privateKey,
            certificate=certificate,
            url='http://tatui.jlsoft.com.br/Abrasf/ahconsultarnfseporrps.aspx',
            method="consult",
        )

    @classmethod
    def clearedResponse(cls, response):
        xmlResponse = response.replace("&lt;", "<")
        xmlResponse = xmlResponse.replace("&gt;", ">")
        return xmlResponse

    @classmethod
    def sendRequest(cls, privateKey, certificate, xml, url, method):
        certPath = "/tmp/cert.crt"
        keyPath = "/tmp/rsaKey.pem"

        headers = {
            "Content-Type": "application/soap+xml; charset=utf-8;",
            "Accept": "application/soap+xml; charset=utf-8;",
            "Cache-Control": "no-cache",
            "Host": "tatui.jlsoft.com.br/",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
        }

        with open(certPath, "w") as tempCert:
            tempCert.write(certificate)
        tempCert.close()

        with open(keyPath, "w") as tempKey:
            tempKey.write(privateKey)
        tempKey.close()

        response = post(
            url=url,
            data=stringEncode(xml),
            headers=headers,
            cert=(certPath, keyPath),
            verify=True
        )

        status = response.status_code
        content = stringDecode(response.content)

        if status != 200:
            return {}, status

        if method == "consult":
            return Response.getTail(cls.clearedResponse(content)), status

        if method == "rps":
            return Response.resultDict(cls.clearedResponse(content)), status

certificateContent = open("./certificate.crt", "rb").read()
privateKeyContent = open("./rsaKey.pem").read()

###Create Nfe:

nota = {
    "CPFCNPJRemetente": "01234567890987",
    "InscricaoPrestador":  "01234567",
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

print(TatuiGateway.sendRps(
    privateKeyContent=privateKeyContent,
    certificateContent=certificateContent,
    **nota
))

###How to delete a Nfe:

nota = {
    "CPFCNPJRemetente": "01234567890123",
    "InscricaoPrestador": "01234567",
    "NumeroNFe": "001"
}

print(TatuiGateway.cancelRps(
    privateKeyContent=privateKeyContent,
    certificateContent=certificateContent,
    **nota
))

###Consult sent Nfes

parameters = {
    "CPFCNPJRemetente": "01234567890123",
    "InscricaoPrestador": "01234567",
    "dtInicio": "2019-09-15",
    "dtFim": "2019-09-18",
}

print(TatuiGateway.consultNfes(
    privateKeyContent=privateKeyContent,
    certificateContent=certificateContent,
    **parameters
))
