from pyxb import BIND
from lxml import *
from nfse.classes import *
from importlib import import_module
from __future__ import print_function


class SerializacaoBetha():

    def __init__(self):
        pass

    def gerar(self, nfse):
        """Retorna string de um XML gerado a partir do
        XML Schema (XSD). Binding gerado pelo modulo PyXB."""

        servico = TcDadosServico()
        valores_servico = TcValoresDeclaracaoServico()
        valores_servico.valor_servicos = nfse.servico.valor_servico

        servico.iss_retido = nfse.servico.iss_retido
        servico.item_lista_servico = nfse.servico.item_lista
        servico.discriminacao = nfse.servico.discriminacao
        servico.codigo_municipio = nfse.servico.codigo_municipio
        servico.exigibilidade_iss = nfse.servico.exigibilidade
        servico.municipio_incidencia = nfse.servico.municipio_incidencia
        servico.valores = valores_servico

        # Prestador
        id_prestador = TcIdentificacaoPrestador()
        id_prestador.cpf_cnpj = nfse.emitente.cnpj
        id_prestador.inscricao_municipal = nfse.emitente.inscricao_municipal

        # Cliente
        id_tomador = TcIdentificacaoTomador()
        id_tomador.cpf_cnpj = nfse.cliente.numero_documento
        if nfse.cliente.inscricao_municipal:
            id_tomador.inscricao_municipal = nfse.cliente.inscricao_municipal

        endereco_tomador = TcEndereco()
        endereco_tomador.endereco = nfse.cliente.endereco_logradouro
        endereco_tomador.numero = nfse.cliente.endereco_numero
        endereco_tomador.bairro = nfse.cliente.endereco_bairro
        endereco_tomador.codigo_municipio = nfse.cliente.endereco_cod_municipio
        endereco_tomador.uf = nfse.cliente.endereco_uf
        endereco_tomador.codigo_pais = nfse.cliente.endereco_pais
        endereco_tomador.cep = nfse.cliente.endereco_cep

        tomador = TcDadosTomador()
        tomador.identificacao_tomador = id_tomador
        tomador.razao_social= nfse.cliente.razao_social
        tomador.endereco = endereco_tomador

        id_rps = TcIdentificacaoRps()
        id_rps.numero = nfse.identificador
        id_rps.serie = nfse.serie
        id_rps.tipo = nfse.tipo

        rps = TcInfRps()
        rps.identificacao_rps = id_rps
        rps.data_emissao = nfse.data_emissao.strftime("%Y-%m-%d")
        rps.Status = 1

        inf_declaracao_servico = TcInfDeclaracaoPrestacaoServico()
        inf_declaracao_servico.competencia = nfse.data_emissao.strftime("%Y-%m-%d")
        inf_declaracao_servico.servico = servico
        inf_declaracao_servico.prestador = id_prestador
        inf_declaracao_servico.tomador = tomador
        inf_declaracao_servico.optante_simples_nacional = nfse.simples
        inf_declaracao_servico.incentivo_fiscal = nfse.incentivo
        inf_declaracao_servico.id = nfse.identificador
        inf_declaracao_servico.rps = rps

        declaracao_servico = TcDeclaracaoPrestacaoServico()
        declaracao_servico.InfDeclaracaoPrestacaoServico = inf_declaracao_servico

        gnfse = GerarNfseEnvio()
        gnfse.Rps = declaracao_servico

        return gnfse.toxml(element_name="GerarNfseEnvio")

    def consultar_rps(self, nfse):
        """Retorna string de um XML gerado a partir do
        XML Schema (XSD). Binding gerado pelo modulo PyXB."""

        # Rps
        id_rps = TcIdentificacaoRps()
        id_rps.numero = nfse.identificador
        id_rps.serie = nfse.serie
        id_rps.tipo = nfse.tipo

        # Prestador
        id_prestador = TcIdentificacaoPrestador()
        id_prestador.cpf_cnpj = nfse.emitente.cnpj
        id_prestador.inscricao_municipal = nfse.emitente.inscricao_municipal

        consulta = ConsultarNfseRpsEnvio()
        consulta.identificacao_rps = id_rps
        consulta.prestador = id_prestador

        consulta = (
            consulta.toxml(element_name="ConsultarNfseRpsEnvio")
            .replace("ns1:", "")
            .replace(":ns1", "")
            .replace('<?xml version="1.0" ?>', "")
        )

        return consulta

    def cancelar(self, nfse):
        """Retorna string de um XML gerado a partir do
        XML Schema (XSD). Binding gerado pelo modulo PyXB."""

        # id nfse
        id_nfse = TcIdentificacaoNfse()
        id_nfse.numero = nfse.identificador
        id_nfse.cpf_cnpj = nfse.emitente.cnpj
        id_nfse.inscricao_municipal = nfse.emitente.inscricao_municipal
        id_nfse.codigo_municipio = nfse.emitente.endereco_cod_municipio

        # Info Pedido de cancelamento
        info_pedido = TcInfPedidoCancelamento()
        info_pedido.id = "1"
        info_pedido.identificacao_nfse = id_nfse
        # pedido.CodigoCancelamento =

        # Pedido
        pedido = TcPedidoCancelamento()
        pedido.inf_pedido_cancelamento = info_pedido

        # Cancelamento
        cancelar = CancelarNfseEnvio()
        cancelar.pedido = pedido

        return cancelar.toxml(element_name="CancelarNfseEnvio")

    def serializar_lote_sincrono(self, nfse):
        """Retorna string de um XML gerado a partir do
        XML Schema (XSD). Binding gerado pelo modulo PyXB."""

        servico = TcDadosServico()
        valores_servico = TcValoresDeclaracaoServico()
        valores_servico.valor_servicos = nfse.servico.valor_servico

        servico.iss_retido = nfse.servico.iss_retido
        servico.item_lista_servico = nfse.servico.item_lista
        servico.discriminacao = nfse.servico.discriminacao
        servico.codigo_municipio = nfse.servico.codigo_municipio
        servico.exigibilidade_iss = nfse.servico.exigibilidade
        servico.municipio_incidencia = nfse.servico.municipio_incidencia
        servico.valores = valores_servico

        # Prestador
        id_prestador = TcIdentificacaoPrestador()
        id_prestador.cpf_cnpj = nfse.emitente.cnpj
        id_prestador.inscricao_municipal = nfse.emitente.inscricao_municipal

        # Cliente
        id_tomador = TcIdentificacaoTomador()
        id_tomador.cpf_cnpj = nfse.cliente.numero_documento
        if nfse.cliente.inscricao_municipal:
            id_tomador.inscricao_municipal = nfse.cliente.inscricao_municipal

        endereco_tomador = TcEndereco()
        endereco_tomador.endereco = nfse.cliente.endereco_logradouro
        endereco_tomador.numero = nfse.cliente.endereco_numero
        endereco_tomador.bairro = nfse.cliente.endereco_bairro
        endereco_tomador.codigo_municipio = nfse.cliente.endereco_cod_municipio
        endereco_tomador.uf = nfse.cliente.endereco_uf
        endereco_tomador.codigo_pais = nfse.cliente.endereco_pais
        endereco_tomador.cep = nfse.cliente.endereco_cep

        tomador = TcDadosTomador()
        tomador.identificacao_tomador = id_tomador
        tomador.razao_social = nfse.cliente.razao_social
        tomador.endereco = endereco_tomador

        id_rps = TcIdentificacaoRps()
        id_rps.numero = nfse.identificador
        id_rps.serie = nfse.serie
        id_rps.tipo = nfse.tipo

        rps = TcInfRps()
        rps.identificacao_rps = id_rps
        rps.data_emissao = nfse.data_emissao.strftime("%Y-%m-%d")
        rps.status = 1

        inf_declaracao_servico = TcInfDeclaracaoPrestacaoServico()
        inf_declaracao_servico.competencia = nfse.data_emissao.strftime("%Y-%m-%d")
        inf_declaracao_servico.servico = servico
        inf_declaracao_servico.prestador = id_prestador
        inf_declaracao_servico.tomador = tomador
        inf_declaracao_servico.optante_simples_nacional = nfse.simples
        inf_declaracao_servico.incentivo_fiscal = nfse.incentivo
        #inf_declaracao_servico.identificador = nfse.identificador
        inf_declaracao_servico.rps = rps

        declaracao_servico = TcDeclaracaoPrestacaoServico()
        declaracao_servico.inf_declaracao_prestacao_servico = inf_declaracao_servico

        lote = TcLoteRps()
        lote.numero_lote = 1
        lote.id = 1
        lote.cpf_cnpj = nfse.emitente.cnpj
        lote.inscricao_municipal = nfse.emitente.inscricao_municipal
        lote.quantidade_rps = 1
        if nfse.autorizador.upper() == "BETHA":
            lote.versao = "2.02"
        lote.lista_rps = BIND(declaracao_servico)

        gnfse = EnviarLoteRpsSincronoEnvio()
        gnfse.lote_rpsl = lote

        return gnfse.toxml(element_name="EnviarLoteRpsSincronoEnvio")