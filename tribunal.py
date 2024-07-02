import face_recognition as reconhecedor
import colored
import random
import simpy
import json

ARQUIVO_DE_CONFIGURACAO = "configuracao.json"

CICLOS_DE_DETECCAO_DE_ADVOGADOS_E_REUS = 40
CICLOS_DE_DETECCAO_DE_REUS = 40
CICLOS_DE_LIBERACAO_DE_REUS = 60
CICLOS_DE_DETECCAO_DE_RESERVA_DE_SALAS = 30
CICLOS_DE_DETECCAO_DE_LIBERACAO_DE_SALAS = 40
CICLOS_DE_DETECCAO_DE_ENTRADA = 30
CICLOS_DE_DETECCAO_DE_SAIDA = 40

PROBABILIDADE_DE_LIBERACAO_REU = 30
PROBABILIDADE_DE_JULGAMENTO = 40
PROBABILIDADE_DE_LIBERACAO_DE_TRIBUNAL = 30
PROBABILIDADE_DE_ENTRADA = 30
PROBABILIDADE_DE_SAIDA = 20

TOTAL_DE_SALAS_DE_TRIBUNAL = 5


FOTOS_DOS_PARTICIPANTES = [
    "imgs/participantes/participantes1.png",
    "imgs/participantes/participantes2.png",
    "imgs/participantes/participantes3.png",
    "imgs/participantes/participantes4.png",
    "imgs/participantes/participantes5.png",
    "imgs/participantes/participantes6.png",
    "imgs/participantes/participantes7.png",
    "imgs/participantes/participantes8.png"
]


def preparar():
    preparado, ambiente = False, simpy.Environment()

    configuracao = None
    try:
        with open(ARQUIVO_DE_CONFIGURACAO, "r") as arquivo:
            configuracao = json.load(arquivo)

            arquivo.close()

        preparado = True
    except Exception as e:
        print(f"ocorreu um erro carregando a configuração: " + str(e))

    return preparado, ambiente, configuracao


def reconhecer_participantes(ambiente, configuracao, advogados_promotores_reconhecidos, reus_reconhecidos):
    while True:
        imprimir(f"reconhecendo participantes em {ambiente.now}", "yellow")

        participantes = simular_participacao()
        ocorreu_reconhecimento, advogados_promotores = reconhecer_advogados_promotores_entre_participantes(
            participantes, configuracao)
        if ocorreu_reconhecimento:
            for advogado_promotor in advogados_promotores:
                if not advogado_promotor_trabalhando(advogado_promotor, advogados_promotores_reconhecidos):
                    imprimir(
                        f"Trabalhos iniciados com o advogado/promotor {advogado_promotor['nome']}", 'yellow')

                    advogado_promotor["em_tribunal"] = False
                    advogado_promotor["em_sala_de_provas"] = False
                    advogados_promotores_reconhecidos[advogado_promotor['codigo']
                                                      ] = advogado_promotor

        reconhecimento_reu, reus = reconhecer_reus_entre_participantes(
            participantes, configuracao)
        if reconhecimento_reu:
            for reu in reus:
                if not reu_em_julgamento(reu, reus_reconhecidos):
                    imprimir(
                        f"Réu {reu['nome']} está em julgamento", 'yellow')

                    reu["em_julgamento"] = True
                    reus_reconhecidos[reu['codigo']] = reu

        yield ambiente.timeout(CICLOS_DE_DETECCAO_DE_ADVOGADOS_E_REUS)


def simular_participacao():
    foto = random.choice(FOTOS_DOS_PARTICIPANTES)
    print(f"foto capturada: {foto}")

    participantes = {
        "foto": foto,
        "participantes": []
    }

    return participantes


def reconhecer_advogados_promotores_entre_participantes(participantes, configuracao):
    ocorreu_reconhecimento, advogados_promotores = False, []

    foto = participantes['foto']
    foto = reconhecedor.load_image_file(foto)
    caracteristicas_dos_participantes = reconhecedor.face_encodings(foto)

    for advogado_promotor in configuracao['advogadosPromotores']:
        fotos = advogado_promotor['fotos']
        total_de_reconhecimentos = 0

        for foto in fotos:
            foto = reconhecedor.load_image_file(foto)
            caracteristicas = reconhecedor.face_encodings(foto)[0]

            reconhecimentos = reconhecedor.compare_faces(
                caracteristicas_dos_participantes, caracteristicas)
            if True in reconhecimentos:
                total_de_reconhecimentos += 1

        if total_de_reconhecimentos/len(fotos) >= 0.7:
            advogados_promotores.append(advogado_promotor)
            ocorreu_reconhecimento = True

    return ocorreu_reconhecimento, advogados_promotores


def reconhecer_reus_entre_participantes(participantes, configuracao):
    reconhecimento_reu, reus = False, []

    foto = participantes['foto']
    foto = reconhecedor.load_image_file(foto)
    caracteristicas_dos_participantes = reconhecedor.face_encodings(foto)

    for reu in configuracao['reus']:
        fotos = reu['fotos']
        total_de_reconhecimentos = 0

        for foto in fotos:
            foto = reconhecedor.load_image_file(foto)
            caracteristicas = reconhecedor.face_encodings(foto)[0]

            reconhecimentos = reconhecedor.compare_faces(
                caracteristicas_dos_participantes, caracteristicas)
            if True in reconhecimentos:
                total_de_reconhecimentos += 1

        if total_de_reconhecimentos/len(fotos) >= 0.7:
            reus.append(reu)
            reconhecimento_reu = True

    return reconhecimento_reu, reus


def advogado_promotor_trabalhando(advogado_promotor, advogados_promotores_reconhecidos):
    return advogado_promotor["codigo"] in advogados_promotores_reconhecidos


def reu_em_julgamento(reu, reus_reconhecidos):
    return reu["codigo"] in reus_reconhecidos


def liberar_reus(ambiente, reus_reconhecidos):
    while True:
        imprimir(f"Liberando reus em {ambiente.now} do julgamento", "blue")

        for codigo, reu in list(reus_reconhecidos.items()):
            liberar = (random.randint(1, 100) <=
                       PROBABILIDADE_DE_LIBERACAO_REU) and reu["em_julgamento"]
            if liberar:
                reus_reconhecidos.pop(codigo)

                imprimir(
                    f"Liberando o reu {reu['nome']} com código {codigo}", "blue")

        yield ambiente.timeout(CICLOS_DE_LIBERACAO_DE_REUS)


def reservar_tribunal(ambiente, advogados_promotores_reconhecidos):
    while True:
        imprimir(f"Reservando tribunal em {ambiente.now}", "red")

        if contar_advogados_promotores_em_tribunal(advogados_promotores_reconhecidos) < TOTAL_DE_SALAS_DE_TRIBUNAL:
            for codigo, advogado_promotor in list(advogados_promotores_reconhecidos.items()):
                julgamento = (random.randint(
                    1, 100) <= PROBABILIDADE_DE_JULGAMENTO) and not advogado_promotor["em_tribunal"] and not advogado_promotor["em_sala_de_provas"]
                if julgamento:
                    advogado_promotor["em_tribunal"] = True

                    imprimir(
                        f"O/A {advogado_promotor['nome']} com código {codigo} está no tribunal", "red")
        else:
            imprimir("Capacidade máxima de Tribunais atingida", "red")

        yield ambiente.timeout(CICLOS_DE_DETECCAO_DE_RESERVA_DE_SALAS)


def contar_advogados_promotores_em_tribunal(advogados_promotores_reconhecidos):
    contagem = 0

    for advogado_promotor in advogados_promotores_reconhecidos.values():
        if advogado_promotor["em_tribunal"]:
            contagem += 1

    return contagem


def liberar_tribunal(ambiente, advogados_promotores_reconhecidos):
    while True:
        imprimir(f"Liberando tribunal em {ambiente.now}", "green")

        for codigo, advogado_promotor in list(advogados_promotores_reconhecidos.items()):
            liberar = (random.randint(
                1, 100) <= PROBABILIDADE_DE_LIBERACAO_DE_TRIBUNAL) and advogado_promotor["em_tribunal"]
            if liberar:
                advogado_promotor["em_tribunal"] = False

                imprimir(
                    f"O/A {advogado_promotor['nome']} com código {codigo} liberado do tribunal", "green")

        yield ambiente.timeout(CICLOS_DE_DETECCAO_DE_LIBERACAO_DE_SALAS)


def liberar_entrada_sala_de_provas(ambiente, advogados_promotores_reconhecidos):
    advogados_promotores_em_sala = []

    while True:
        imprimir(
            f"Liberando entrada na sala de provas em {ambiente.now}", "green")

        for codigo, advogado_promotor in advogados_promotores_reconhecidos.items():
            if advogado_promotor["em_sala_de_provas"]:
                if random.randint(1, 100) <= PROBABILIDADE_DE_SAIDA:
                    advogado_promotor["em_sala_de_provas"] = False
                    advogados_promotores_em_sala.remove(codigo)
                    print(
                        f"O/A {advogado_promotor['nome']} com código {codigo} saiu da sala de provas")

        if len(advogados_promotores_em_sala) < 1 and random.randint(1, 100) <= PROBABILIDADE_DE_ENTRADA:
            for codigo, advogado_promotor in advogados_promotores_reconhecidos.items():
                if not advogado_promotor["em_sala_de_provas"] and not advogado_promotor["em_tribunal"]:
                    advogado_promotor["em_sala_de_provas"] = True
                    advogados_promotores_em_sala.append(codigo)
                    imprimir(
                        f"O/A {advogado_promotor['nome']} com código {codigo} entrou na sala de provas", "green")
                    break

        yield ambiente.timeout(CICLOS_DE_DETECCAO_DE_SAIDA)


def imprimir(mensagem, cor):
    print(colored.fg('black'), colored.bg(
        cor), mensagem, colored.attr('reset'))


if __name__ == "__main__":
    preparado, ambiente, configuracao = preparar()

    if preparado:
        advogados_promotores_reconhecidos = {}
        reus_reconhecidos = {}

        ambiente.process(reconhecer_participantes(
            ambiente, configuracao, advogados_promotores_reconhecidos, reus_reconhecidos))
        ambiente.process(liberar_reus(ambiente, reus_reconhecidos))
        ambiente.process(reservar_tribunal(
            ambiente, advogados_promotores_reconhecidos))
        ambiente.process(liberar_tribunal(
            ambiente, advogados_promotores_reconhecidos))
        ambiente.process(liberar_entrada_sala_de_provas(
            ambiente, advogados_promotores_reconhecidos))

        ambiente.run(until=4000)
