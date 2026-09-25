"""
SE-AQUÁRIO — Sistema Especialista para Diagnóstico de Problemas em
Aquários de Água Doce.

Minimundo: um aquarista informa parâmetros físico-químicos da água
(pH, amônia, nitrito, nitrato, temperatura) e sintomas observados nos
peixes e no aquário (comportamento, sinais físicos, aspecto da água).
O motor de inferência (encadeamento para frente / forward chaining)
percorre a base de regras e retorna o(s) diagnóstico(s) e a(s)
recomendação(ões) correspondentes.

Autor: Trabalho acadêmico — Sistemas Especialistas
"""

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any


# ---------------------------------------------------------------------------
# 1. BASE DE FATOS
# ---------------------------------------------------------------------------
@dataclass
class BaseDeFatos:
    """Representa os fatos coletados sobre um aquário em um dado momento."""
    ph: float = 7.0
    amonia_ppm: float = 0.0
    nitrito_ppm: float = 0.0
    nitrato_ppm: float = 0.0
    temperatura_c: float = 25.0
    horas_luz_dia: float = 8.0

    letargico: bool = False
    natacao_erratica: bool = False
    boquejando_superficie: bool = False
    esfregando_em_objetos: bool = False
    isolamento: bool = False

    manchas_brancas_sal: bool = False
    fungo_algodao: bool = False
    barbatanas_corroidas: bool = False
    inchaco_abdominal: bool = False
    olhos_saltados: bool = False
    hemorragias: bool = False

    agua_turva_esbranquicada: bool = False
    alga_verde_excessiva: bool = False
    cianobacteria: bool = False
    espuma_superficie: bool = False


@dataclass
class Regra:
    """Uma regra de produção SE (condição) ENTÃO (diagnóstico/ação)."""
    identificador: str
    descricao: str
    condicao: Callable[[BaseDeFatos], bool]
    diagnostico: str
    recomendacao: str
    prioridade: int = 0  # regras mais críticas (ex.: amônia) têm prioridade maior


@dataclass
class Resultado:
    regra: str
    diagnostico: str
    recomendacao: str


# ---------------------------------------------------------------------------
# 2. BASE DE CONHECIMENTO (BASE DE REGRAS)
# ---------------------------------------------------------------------------
def construir_base_de_regras() -> List[Regra]:
    regras: List[Regra] = []

    regras.append(Regra(
        "R01", "Pico de amônia",
        lambda f: f.amonia_ppm > 0.25,
        "Pico de amônia (ciclo do nitrogênio não estabelecido ou "
        "sobrecarga de matéria orgânica).",
        "Realizar troca parcial de água (25%-50%) imediatamente; "
        "reduzir a quantidade de ração; adicionar bactérias "
        "nitrificantes comerciais; verificar superlotação e filtragem.",
        prioridade=10,
    ))

    regras.append(Regra(
        "R02", "Pico de nitrito",
        lambda f: f.nitrito_ppm > 0 and f.amonia_ppm <= 0.25,
        "Síndrome do aquário novo / pico de nitrito.",
        "Trocar 25% da água a cada 1-2 dias até o nitrito zerar; "
        "não limpar o filtro biológico; monitorar diariamente.",
        prioridade=9,
    ))

    regras.append(Regra(
        "R03", "Nitrato elevado",
        lambda f: f.nitrato_ppm > 40,
        "Acúmulo de nitrato por manutenção insuficiente.",
        "Aumentar a frequência de trocas parciais de água; sifonar o "
        "substrato; revisar a densidade de peixes e a alimentação.",
        prioridade=5,
    ))

    regras.append(Regra(
        "R04", "Ictioftiríase (Ich)",
        lambda f: f.manchas_brancas_sal and f.esfregando_em_objetos,
        "Ictioftiríase (Ich) — infecção parasitária por protozoário.",
        "Elevar a temperatura gradualmente para 28-29°C; aplicar sal "
        "para aquário na dosagem indicada; usar medicamento "
        "antiparasitário específico; manter aeração extra.",
        prioridade=8,
    ))

    regras.append(Regra(
        "R05", "Hidropisia (Dropsy)",
        lambda f: f.inchaco_abdominal,
        "Hidropisia (Dropsy) — provável infecção bacteriana/renal.",
        "Isolar o peixe em quarentena; revisar imediatamente a "
        "qualidade da água; tratamento antibacteriano especializado; "
        "prognóstico reservado em casos avançados.",
        prioridade=9,
    ))

    regras.append(Regra(
        "R06", "Pop-eye (exoftalmia)",
        lambda f: f.olhos_saltados,
        "Pop-eye — provável infecção bacteriana ou má qualidade da água.",
        "Verificar amônia/nitrito imediatamente; isolar o peixe "
        "afetado; tratamento antibacteriano se houver outros sinais "
        "de infecção.",
        prioridade=7,
    ))

    regras.append(Regra(
        "R07", "Podridão de barbatanas (Fin rot)",
        lambda f: f.barbatanas_corroidas,
        "Podridão de barbatanas (Fin rot) — infecção bacteriana "
        "secundária à má qualidade da água.",
        "Melhorar a qualidade da água com trocas parciais; tratamento "
        "antibacteriano tópico; remover pontas de barbatanas mortas "
        "não é necessário.",
        prioridade=6,
    ))

    regras.append(Regra(
        "R08", "Infecção fúngica",
        lambda f: f.fungo_algodao,
        "Infecção fúngica (aspecto de algodão branco).",
        "Isolar o peixe afetado; aplicar tratamento antifúngico; "
        "verificar e corrigir a qualidade da água.",
        prioridade=6,
    ))

    regras.append(Regra(
        "R09", "Baixo oxigênio dissolvido",
        lambda f: f.boquejando_superficie,
        "Baixo teor de oxigênio dissolvido na água.",
        "Aumentar a aeração/agitação da superfície; verificar se a "
        "temperatura está muito alta; realizar troca parcial de água; "
        "reduzir a densidade de peixes se necessário.",
        prioridade=8,
    ))

    regras.append(Regra(
        "R10", "Surto de cianobactérias",
        lambda f: f.cianobacteria,
        "Surto de cianobactérias (\"alga\" azul-esverdeada).",
        "Escurecer o aquário por 3-4 dias; sifonar o substrato; "
        "melhorar a circulação e a oxigenação; reduzir fosfato e "
        "nitrato na água.",
        prioridade=5,
    ))

    regras.append(Regra(
        "R11", "Excesso de algas verdes",
        lambda f: f.alga_verde_excessiva and f.horas_luz_dia > 8,
        "Proliferação de algas verdes por excesso de luz/nutrientes.",
        "Reduzir o fotoperíodo para 6-8 horas diárias; controlar "
        "nitrato e fosfato; inserir plantas de crescimento rápido "
        "para competir por nutrientes.",
        prioridade=3,
    ))

    regras.append(Regra(
        "R12", "Bloom bacteriano (água turva)",
        lambda f: f.agua_turva_esbranquicada and f.amonia_ppm <= 0.25,
        "Bloom bacteriano — comum em aquários recém-montados.",
        "Aguardar o processo natural de maturação (poucos dias); "
        "reduzir a alimentação; evitar trocas excessivas de água "
        "durante o período.",
        prioridade=2,
    ))

    regras.append(Regra(
        "R13", "pH fora da faixa recomendada",
        lambda f: (f.ph < 6.5 or f.ph > 7.8) and f.letargico,
        "Estresse por pH fora da faixa ideal para a maioria das "
        "espécies de água doce comunitárias.",
        "Ajustar o pH gradualmente (nunca de forma brusca); verificar "
        "compatibilidade do pH com as espécies cadastradas; usar "
        "substratos/produtos tamponantes adequados.",
        prioridade=4,
    ))

    return regras


# ---------------------------------------------------------------------------
# 3. MOTOR DE INFERÊNCIA
# ---------------------------------------------------------------------------
class MotorDeInferencia:
    """Motor de encadeamento para frente (forward chaining).

    Percorre todas as regras da base de conhecimento, avalia a condição
    de cada uma contra a base de fatos e retorna todos os diagnósticos
    cujas condições foram satisfeitas, ordenados por prioridade
    (regras mais críticas primeiro).
    """

    def __init__(self, regras: List[Regra]):
        self.regras = regras

    def diagnosticar(self, fatos: BaseDeFatos) -> List[Resultado]:
        disparadas = [r for r in self.regras if r.condicao(fatos)]
        disparadas.sort(key=lambda r: r.prioridade, reverse=True)
        return [Resultado(r.identificador, r.diagnostico, r.recomendacao)
                for r in disparadas]


# ---------------------------------------------------------------------------
# 4. INTERFACE (CLI simples) — camada de apresentação
# ---------------------------------------------------------------------------
def pergunta_float(msg: str, padrao: float) -> float:
    entrada = input(f"{msg} [{padrao}]: ").strip()
    return float(entrada.replace(",", ".")) if entrada else padrao


def pergunta_bool(msg: str) -> bool:
    entrada = input(f"{msg} (s/n) [n]: ").strip().lower()
    return entrada == "s"


def coletar_fatos_interativo() -> BaseDeFatos:
    print("\n--- Parâmetros da água ---")
    ph = pergunta_float("pH", 7.0)
    amonia = pergunta_float("Amônia (ppm)", 0.0)
    nitrito = pergunta_float("Nitrito (ppm)", 0.0)
    nitrato = pergunta_float("Nitrato (ppm)", 10.0)
    temperatura = pergunta_float("Temperatura (°C)", 25.0)
    horas_luz = pergunta_float("Horas de luz por dia", 8.0)

    print("\n--- Sintomas observados (responda s/n) ---")
    fatos = BaseDeFatos(
        ph=ph, amonia_ppm=amonia, nitrito_ppm=nitrito,
        nitrato_ppm=nitrato, temperatura_c=temperatura,
        horas_luz_dia=horas_luz,
        letargico=pergunta_bool("Peixe letárgico/parado"),
        natacao_erratica=pergunta_bool("Natação errática"),
        boquejando_superficie=pergunta_bool("Boquejando na superfície"),
        esfregando_em_objetos=pergunta_bool("Esfregando-se em objetos"),
        isolamento=pergunta_bool("Isolamento do cardume"),
        manchas_brancas_sal=pergunta_bool("Manchas brancas tipo sal"),
        fungo_algodao=pergunta_bool("Fungo/algodão branco"),
        barbatanas_corroidas=pergunta_bool("Barbatanas corroídas"),
        inchaco_abdominal=pergunta_bool("Inchaço abdominal"),
        olhos_saltados=pergunta_bool("Olhos saltados"),
        hemorragias=pergunta_bool("Hemorragias/manchas vermelhas"),
        agua_turva_esbranquicada=pergunta_bool("Água turva/esbranquiçada"),
        alga_verde_excessiva=pergunta_bool("Excesso de algas verdes"),
        cianobacteria=pergunta_bool("Presença de cianobactérias"),
        espuma_superficie=pergunta_bool("Espuma na superfície"),
    )
    return fatos


def exibir_resultados(resultados: List[Resultado]) -> None:
    print("\n================ RESULTADO DO DIAGNÓSTICO ================")
    if not resultados:
        print("Nenhuma regra foi disparada.")
        print("Diagnóstico: parâmetros dentro da normalidade ou situação "
              "não coberta pela base de conhecimento.")
        print("Recomendação: continue o monitoramento de rotina; em caso "
              "de dúvida, consulte um especialista humano (aquarista "
              "experiente ou médico-veterinário especializado em peixes).")
    else:
        for i, r in enumerate(resultados, start=1):
            print(f"\n[{r.regra}] Diagnóstico {i}: {r.diagnostico}")
            print(f"  Recomendação: {r.recomendacao}")
    print("============================================================\n")


def main() -> None:
    print("###########################################################")
    print("#     SE-AQUÁRIO — Sistema Especialista em Aquarismo       #")
    print("###########################################################")

    regras = construir_base_de_regras()
    motor = MotorDeInferencia(regras)

    while True:
        fatos = coletar_fatos_interativo()
        resultados = motor.diagnosticar(fatos)
        exibir_resultados(resultados)

        if not pergunta_bool("\nDeseja realizar nova consulta"):
            print("Encerrando o SE-AQUÁRIO. Até logo!")
            break


# ---------------------------------------------------------------------------
# 5. EXEMPLOS DE USO PROGRAMÁTICO / TESTES DE DEMONSTRAÇÃO
# ---------------------------------------------------------------------------
def exemplos_de_teste() -> None:
    regras = construir_base_de_regras()
    motor = MotorDeInferencia(regras)

    casos = {
        "Caso 1 - Pico de amônia": BaseDeFatos(amonia_ppm=1.0),
        "Caso 2 - Ich": BaseDeFatos(manchas_brancas_sal=True,
                                     esfregando_em_objetos=True),
        "Caso 3 - Hidropisia": BaseDeFatos(inchaco_abdominal=True),
        "Caso 4 - Aquário saudável": BaseDeFatos(),
    }

    for nome, fatos in casos.items():
        print(f"\n### {nome} ###")
        exibir_resultados(motor.diagnosticar(fatos))


if __name__ == "__main__":
    import sys
    if "--demo" in sys.argv:
        exemplos_de_teste()
    else:
        main()
