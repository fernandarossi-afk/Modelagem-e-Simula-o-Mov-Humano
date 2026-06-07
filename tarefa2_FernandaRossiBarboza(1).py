import marimo

__generated_with = "0.23.9"
app = marimo.App(width="medium", auto_download=["html", "ipynb"])


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ###Problema 2: Espectro de Recrutamento de Fuglevand
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt

    # Parâmetros do Problema 2
    n = 120           # Número de unidades motoras
    P1 = 1.0          # Força de pico da unidade 1
    Rp = 100.0        # Razão de força
    Tc1 = 90.0        # Tempo de contração da unidade 1 (ms)
    Tc120 = 30.0      # Tempo de contração da unidade 120 (ms)

    # Vetor de índices das unidades motoras (1 a 120)
    # Usamos arange de 1 a n+1 para bater com a fórmula matemática (i - 1)
    i = np.arange(1, n + 1)

    # Equações 2 e 3: Cálculo de Pi e Tci para cada unidade motora
    P_i = P1 * np.exp(np.log(Rp) * (i - 1) / (n - 1))
    T_ci = Tc1 * np.exp(np.log(Tc120 / Tc1) * (i - 1) / (n - 1))

    # Vetor de tempo de 0 a 300 ms
    # Definimos com uma boa resolução, ex: 1000 pontos
    t = np.linspace(0, 300, 1000)
    return P_i, T_ci, n, np, plt, t


@app.cell
def _(P_i, T_ci, n, np, plt, t):
    import matplotlib.cm as cm
    from matplotlib.colors import Normalize

    # Criando a figura e os eixos
    fig, ax = plt.subplots(figsize=(10, 6))

    # Configurando o mapa de cores (colormap) contínuo
    cmap = cm.viridis 
    # Normalizando as cores para os índices de 1 a 120
    norm = Normalize(vmin=1, vmax=n) 

    # Iterando sobre as 120 unidades motoras para calcular e plotar a curva de cada uma
    for idx in range(n):
        # O índice do Python começa em 0, mas nossas unidades são de 1 a 120
        # Pegamos o P_i e T_ci correspondentes à unidade atual
        Pi_atual = P_i[idx]
        Tci_atual = T_ci[idx]

        # Equação 1: Cálculo da força F_i(t) para o vetor de tempo t
        F_t = (Pi_atual * t / Tci_atual) * np.exp(1 - (t / Tci_atual))

        # Selecionando a cor exata para essa curva baseada no índice (idx + 1)
        cor = cmap(norm(idx + 1))

        # Plotando a curva
        ax.plot(t, F_t, color=cor)

    # Adicionando a barra de cores (colorbar)
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([]) 
    cbar = fig.colorbar(sm, ax=ax)
    cbar.set_label('Índice da Unidade Motora (i)')

    # Ajustes estéticos e rótulos
    ax.set_title('Espectro de Recrutamento de Fuglevand (Abalos Individuais)')
    ax.set_xlabel('Tempo (ms)')
    ax.set_ylabel('Força do Twitch $F_i(t)$')
    ax.grid(True, alpha=0.3)

    # O Marimo renderiza o gráfico automaticamente se deixarmos a figura na última linha
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ###Problema 3: Superfície de Estado do Músculo de Hill
    """)
    return


@app.cell
def _(np, plt):
    # Parâmetros fornecidos no problema
    gamma = 0.45
    Af = 0.25
    Fmax = 1.8

    # Calculando a constante 'c' para a fase excêntrica
    c = (Af * (Fmax - 1)) / (Af + 1)

    # 1. Função Força-Comprimento (FL)
    def calc_FL(l_M):
        return np.exp(-((l_M - 1) / gamma)**2)

    # 2. Função Força-Velocidade (FV)
    def calc_FV(v_M):
        # Criamos um vetor de zeros do mesmo tamanho de v_M para guardar os resultados
        FV = np.zeros_like(v_M)

        # Máscara para a fase concêntrica (v_M <= 0)
        mask_conc = v_M <= 0
        FV[mask_conc] = (1 + v_M[mask_conc]) / (1 - (v_M[mask_conc] / Af))

        # Máscara para a fase excêntrica (v_M > 0)
        mask_exc = v_M > 0
        FV[mask_exc] = (Fmax * v_M[mask_exc] + c) / (v_M[mask_exc] + c)

        return FV

    # Vetores de teste para os gráficos isolados
    # Comprimento de 0.5 a 1.5 e Velocidade de -1.0 a 1.0
    l_M_array = np.linspace(0.5, 1.5, 500)
    v_M_array = np.linspace(-1.0, 1.0, 500)

    # Calculando as forças
    FL_array = calc_FL(l_M_array)
    FV_array = calc_FV(v_M_array)

    # Plotando os gráficos isolados (usando um nome de variável único para a figura)
    fig_isoladas, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Gráfico 1: Força-Comprimento
    ax1.plot(l_M_array, FL_array, color='blue')
    ax1.set_title('Relação Força-Comprimento ($F_L$)')
    ax1.set_xlabel('Comprimento Normalizado $\\tilde{l}^M$')
    ax1.set_ylabel('Força $F_L$')
    ax1.grid(True, alpha=0.3)

    # Gráfico 2: Força-Velocidade
    ax2.plot(v_M_array, FV_array, color='red')
    ax2.set_title('Relação Força-Velocidade ($F_V$)')
    ax2.set_xlabel('Velocidade Normalizada $\\tilde{v}^M$')
    ax2.set_ylabel('Força $F_V$')
    ax2.axvline(0, color='black', linestyle='--', alpha=0.5) # Linha marcando v=0
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    fig_isoladas
    return calc_FL, calc_FV, l_M_array, v_M_array


@app.cell
def _(calc_FL, calc_FV, l_M_array, np, plt, v_M_array):
    # Criando o grid bidimensional numérico usando os arrays da célula anterior
    L_M_grid, V_M_grid = np.meshgrid(l_M_array, v_M_array)

    # Calculando a Força Total (produto das matrizes)
    FL_grid = calc_FL(L_M_grid)
    FV_grid = calc_FV(V_M_grid)
    F_total = FL_grid * FV_grid

    # Criando a figura para a Superfície 3D (aumentei um pouco a largura para dar mais espaço)
    fig_3d = plt.figure(figsize=(10, 8))
    ax_3d = fig_3d.add_subplot(111, projection='3d')

    # Plotando a superfície 3D
    superficie = ax_3d.plot_surface(L_M_grid, V_M_grid, F_total, 
                                    cmap='viridis', 
                                    edgecolor='none', 
                                    alpha=0.9)

    # Adicionando a barra de cores com 'pad' para empurrá-la para a direita
    # Variável renomeada para cbar_3d para evitar conflito no Marimo
    cbar_3d = fig_3d.colorbar(superficie, ax=ax_3d, shrink=0.5, aspect=10, pad=0.10)
    cbar_3d.set_label('Força Total $F_{total}$')

    # Ajustes estéticos e rótulos com 'labelpad' para afastar os textos dos eixos
    ax_3d.set_title('Superfície de Estado do Músculo de Hill ($F_{total}$)', pad=5)
    ax_3d.set_xlabel('Comprimento Normalizado $\\tilde{l}^M$', labelpad=5)
    ax_3d.set_ylabel('Velocidade Normalizada $\\tilde{v}^M$', labelpad=5)
    ax_3d.set_zlabel('Força Total $F_{total}$', labelpad=10)

    # ... (seu código anterior até os ax_3d.set_zlabel) ...

    # 1. Reduzindo o número de marcações no eixo de Velocidade (passos de 0.5)
    ax_3d.set_yticks([-1.0, -0.5, 0.0, 0.5, 1.0])

    # 2. Reduzindo o número de marcações no eixo de Comprimento (opcional, mas recomendado)
    ax_3d.set_xticks([0.6, 0.8, 1.0, 1.2, 1.4])

    # 3. Ajustando o espaçamento (pad) entre os números e as linhas do eixo para todos os eixos
    ax_3d.tick_params(axis='x', pad=3)
    ax_3d.tick_params(axis='y', pad=3)
    ax_3d.tick_params(axis='z', pad=5)

    # Ajuste do ângulo de visualização
    ax_3d.view_init(elev=30, azim=-45)

    # Renderiza a figura
    fig_3d
    return F_total, L_M_grid, V_M_grid


@app.cell
def _(F_total, L_M_grid, V_M_grid, plt):
    # Criando a figura e os eixos para o Gráfico de Contorno
    fig_contour, ax_contour = plt.subplots(figsize=(9, 7))

    # Plotando o contorno preenchido (contourf)
    # O parâmetro 'levels=25' define a quantidade de "degraus" de cores para deixar a transição suave
    contorno = ax_contour.contourf(L_M_grid, V_M_grid, F_total, levels=25, cmap='viridis')

    # Adicionando a barra de cores exclusiva desta célula
    cbar_contour = fig_contour.colorbar(contorno, ax=ax_contour)
    cbar_contour.set_label('Força Total $F_{total}$')

    # Adicionando linhas de referência para facilitar a interpretação
    # Linha vertical no comprimento ótimo (L = 1.0)
    ax_contour.axvline(1.0, color='white', linestyle='--', alpha=0.5) 
    # Linha horizontal na velocidade zero (transição concêntrica/excêntrica)
    ax_contour.axhline(0.0, color='white', linestyle='--', alpha=0.5) 

    # Ajustes estéticos e rótulos
    ax_contour.set_title('Gráfico de Contorno: Superfície de Estado de Hill ($F_{total}$)')
    ax_contour.set_xlabel('Comprimento Normalizado $\\tilde{l}^M$')
    ax_contour.set_ylabel('Velocidade Normalizada $\\tilde{v}^M$')

    # Renderiza a figura
    fig_contour
    return


if __name__ == "__main__":
    app.run()
