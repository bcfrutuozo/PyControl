from decimal import Decimal
from datetime import date
from typing import List

class DeducaoRPS:

    id: int
    deducao_por: str
    tipo_deducao: str
    cpf_cnpj_referencia: str
    numero_nf_referencia: str
    valor_total_referencia: Decimal
    percentual_deduzir: Decimal
    valor_deduzir: Decimal
    id_rps: int



class ItemRPS:

    id: int
    discriminacao_servico: str
    quantidade: Decimal
    valor_unitario: Decimal
    valor_total: Decimal
    tributavel: str
    id_rps: int


class ItensServiceo():

    id: int
    nome: str

class NFSe:

    id: int
    id_lote_rps: int
    assinatura: str
    inscricao_municipal_prestador: str
    razao_social_prestador: str
    tipo_rps: str
    serie_rps: str
    numero_rps: int
    data_emissao_rps: date
    situacao_rps: str
    serie_rps_substituido: str
    numero_nfse_substituida: int
    numero_rps_substituido: int
    data_emissao_nfse_substituido: date
    serie_prestacao: str
    inscricao_municipal_prestador: str
    cpf_cnpj_tomador: str
    razao_social_tomador: str
    doc_tomador_estrangeiro: str
    tipo_logradouro_tomador: str
    logradouro_tomador: str
    numero_endereco_tomador: str
    complemento_endereco_tomador: str
    tipo_bairro_tomador: str
    bairro_tomador: str
    cidade_tomador: str
    cidade_tomador_descricao: str
    cep_tomador: str
    email_tomador: str
    codigo_ativodade: str
    aliquota_atividade: str
    tipo_recolhimento: str
    municipio_prestacao: str
    municipio_prestacao_descricao: str
    operacao: str
    tributacao: str
    valor_pis: Decimal
    valor_cofins: Decimal
    valor_inss: Decimal
    valor_ir: Decimal
    valor_csll: Decimal
    aliquota_pis: Decimal
    aliquota_cofins: Decimal
    aliquota_inss: Decimal
    aliquota_ir: Decimal
    aliquota_csll: Decimal
    descricao_rps: str
    ddd_prestador: str
    telefone_prestador: str
    ddd_tomador: str
    telefone_tomador: str
    motivo_cancelamento: str
    cpf_cnpj_intermediario: str
    matricula_cei: str
    status_processamento: str
    itens_rps: List[ItemRPS] = list()
    deducao_rps: List[DeducaoRPS] = list()