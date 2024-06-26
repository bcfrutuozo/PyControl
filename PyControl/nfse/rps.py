from re import search, sub
from nfse.rsa import RSA
from nfse.currency import Currency
from nfse.certificate import Certificate
from nfse.functions import stringDecode
from nfse.serializers.abrasf_ev20 import *


class Rps:

    @classmethod
    def xmlCreateRps(cls, InscricaoPrestador, SerieRPS, NumeroRPS, TipoRPS, DataEmissao, StatusRPS, ValorServicos,
                     ValorDeducoes, CodigoServico, ISSRetido, CPFCNPJTomador, CPFCNPJRemetente, TributacaoRPS, ValorPIS,
                     ValorCOFINS, ValorINSS, ValorIR, ValorCSLL, AliquotaServicos, RazaoSocialTomador, Logradouro,
                     NumeroEndereco, ComplementoEndereco, Bairro, Cidade, UF, CEP, EmailTomador, Discriminacao,
                     privateKeyContent, certificateContent):

        rpsToSign = "{InscricaoPrestador}{SerieRPS}{NumeroRPS}{DataEmissao}{TributacaoRPS}{StatusRPS}" \
                    "{ISSRetido}{ValorServicos}{ValorDeducoes}{CodigoServico}2{RazaoSocialTomador}".format(
            InscricaoPrestador=InscricaoPrestador.zfill(8),
            SerieRPS=SerieRPS.ljust(5).upper(),
            NumeroRPS=NumeroRPS.zfill(12),
            DataEmissao=DataEmissao.replace("-", ""),
            TributacaoRPS=TributacaoRPS.upper(),
            StatusRPS=StatusRPS,
            ISSRetido={"false": "N", "true": "S"}.get(ISSRetido),
            ValorServicos=str(ValorServicos).zfill(15),
            ValorDeducoes=str(ValorDeducoes).zfill(15),
            CodigoServico=CodigoServico.zfill(5),
            RazaoSocialTomador=CPFCNPJTomador.zfill(14),
        )

        rpsSignature = RSA.sign(text=rpsToSign, privateKeyContent=privateKeyContent)

        parameters = {
            "CPFCNPJRemetente": CPFCNPJRemetente,
            "Assinatura": stringDecode(rpsSignature),
            "InscricaoPrestador": InscricaoPrestador,
            "SerieRPS": SerieRPS,
            "NumeroRPS": NumeroRPS,
            "TipoRPS": TipoRPS,
            "DataEmissao": DataEmissao,
            "StatusRPS": StatusRPS,
            "TributacaoRPS": TributacaoRPS,
            "ValorServicos": Currency.formatted(ValorServicos),
            "ValorDeducoes": Currency.formatted(ValorDeducoes),
            "ValorPIS": Currency.formatted(ValorPIS),
            "ValorCOFINS": Currency.formatted(ValorCOFINS),
            "ValorINSS": Currency.formatted(ValorINSS),
            "ValorIR": Currency.formatted(ValorIR),
            "ValorCSLL": Currency.formatted(ValorCSLL),
            "CodigoServico": CodigoServico,
            "AliquotaServicos": Currency.formatted(AliquotaServicos),
            "ISSRetido": ISSRetido,
            "CPFCNPJTomador": CPFCNPJTomador,
            "RazaoSocialTomador": RazaoSocialTomador,
            "Logradouro": Logradouro,
            "NumeroEndereco": NumeroEndereco,
            "ComplementoEndereco": ComplementoEndereco,
            "Bairro": Bairro,
            "Cidade": Cidade,
            "UF": UF,
            "CEP": CEP,
            "EmailTomador": EmailTomador,
            "Discriminacao": Discriminacao,
        }

        xml = cls.signXml(
            xml=xml,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **parameters
        )

        return xml

    @classmethod
    def cancelRps(cls, xml, CPFCNPJRemetente, InscricaoPrestador, NumeroNFe, certificateContent, privateKeyContent):
        cancelToSign = "{InscricaoPrestador}{NumeroNFe}".format(
            InscricaoPrestador=InscricaoPrestador.zfill(8),
            NumeroNFe=NumeroNFe.zfill(12)
        )

        cancelSignature = RSA.sign(text=cancelToSign, privateKeyContent=privateKeyContent)

        parameters = {
            "CPFCNPJRemetente": CPFCNPJRemetente,
            "InscricaoPrestador": InscricaoPrestador,
            "NumeroNFe": NumeroNFe,
            "AssinaturaCancelamento": stringDecode(cancelSignature),
        }

        xml = cls.signXml(
            xml=xml,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **parameters
        )

        return xml

    @classmethod
    def consultNfes(cls, xml, CPFCNPJRemetente, Inscricao, dtInicio, dtFim, certificateContent, privateKeyContent):
        parameters = {
            "CPFCNPJRemetente": CPFCNPJRemetente,
            "Inscricao": Inscricao,
            "dtInicio": dtInicio,
            "dtFim": dtFim,
        }

        xml = cls.signXml(
            xml=xml,
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            **parameters
        )

        return xml

    @classmethod
    def signXml(cls, xml, privateKeyContent, certificateContent, **kwargs):
        xmlWithoutBreakLine = sub("\n*", "", xml)
        xmlWithoutSpaces = sub("\s{2,}", "", xmlWithoutBreakLine)

        p1WithSignature = search("<!\[CDATA\[(.*)\]\]>", xmlWithoutSpaces).group(1)
        p1WithoutSignature = sub("<Signature .*</Signature>", "", p1WithSignature)

        p1 = p1WithoutSignature.format(**kwargs)

        digestValue = stringDecode(RSA.digest(p1))

        namespace = search("<[^> ]+ ?([^>]*)>", p1WithoutSignature).group(1)
        signInfo = search("(<SignedInfo>.*</SignedInfo>)", xmlWithoutSpaces).group(1)
        signInfoWithNamespace = sub("<SignedInfo>", "<SignedInfo xmlns=\"http://www.w3.org/2000/09/xmldsig#\" {namespace}>".format(namespace=namespace), signInfo)
        message = signInfoWithNamespace.format(DigestValue=digestValue)
        signatureValue = stringDecode(RSA.sign(text=message, privateKeyContent=privateKeyContent))

        sigendXml = xmlWithoutSpaces.format(
            DigestValue=digestValue,
            SignatureValue=signatureValue,
            X509Certificate=Certificate.getContent(certificateContent),
            **kwargs
        )

        return sigendXml