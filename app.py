

# DASHBOARD ESTATÍSTICO SHINY FOR PYTHON
from shiny import App, ui, render, reactive, req
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, linregress

# ESTILO
sns.set_style("whitegrid")
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.titlecolor": "#1f4e79",
    "axes.labelcolor": "#374151",
    "axes.edgecolor": "#d1d5db",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": "#6b7280",
    "ytick.color": "#6b7280",
    "grid.color": "#e5e7eb",
    "grid.linestyle": "--",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "legend.frameon": False,
})

# PALETA
COR_PRIMARIA = "#2563eb"
COR_SECUNDARIA = "#7c3aed"
COR_DESTAQUE = "#ef4444"
COR_SUCESSO = "#10b981"

# INTERFACE
app_ui = ui.page_fluid(
    # CSS
    ui.tags.style("""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        *{ box-sizing:border-box; }
        body{
            background: linear-gradient(135deg, #eef2ff 0%, #f8fafc 50%, #f0f9ff 100%);
            background-attachment: fixed;
            font-family:'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color:#1f2937;
            min-height:100vh;
        }
        h1{
            background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align:center;
            margin: 32px 0 36px 0;
            font-weight: 800;
            font-size: 2.4rem;
            letter-spacing: -0.02em;
        }
        h3{
            color:#1e293b;
            font-weight:700;
            font-size: 1.15rem;
            margin: 0 0 16px 0;
            padding-bottom: 10px;
            border-bottom: 2px solid #f1f5f9;
            position: relative;
        }
        h3::before{
            content:"";
            position:absolute;
            bottom:-2px;
            left:0;
            width:48px;
            height:2px;
            background: linear-gradient(90deg, #2563eb, #7c3aed);
            border-radius: 2px;
        }
        h4{
            color:#475569;
            font-weight:600;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin: 4px 0 12px 0;
        }
        .card{
            background:#ffffff;
            padding:24px 28px;
            border-radius:16px;
            margin-bottom:20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 8px 24px rgba(15, 23, 42, 0.06);
            border: 1px solid rgba(226, 232, 240, 0.8);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .card:hover{
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.04), 0 16px 32px rgba(15, 23, 42, 0.08);
        }

        /* SIDEBAR */
        .bslib-sidebar-layout > .sidebar,
        aside.sidebar{
            background: #f8fafc !important;
            border-right: 1px solid #e2e8f0 !important;
            box-shadow: 2px 0 12px rgba(15,23,42,0.04);
            padding: 16px !important;
        }

        /* CARDS DA SIDEBAR */
        .sidebar-card{
            background: #ffffff;
            border-radius: 14px;
            margin-bottom: 16px;
            border: 1px solid rgba(226, 232, 240, 0.9);
            box-shadow: 0 2px 8px rgba(15,23,42,0.04);
            overflow: hidden;
        }
        .sidebar-card-header{
            background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
            color: #ffffff;
            font-weight: 700;
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 12px 16px;
        }
        .sidebar-card-body{ padding: 8px 0; }

        /* ACCORDION */
        .accordion{ --bs-accordion-border-color: transparent; }
        .accordion-item{
            background: transparent !important;
            border: none !important;
            border-bottom: 1px solid #f1f5f9 !important;
        }
        .accordion-item:last-child{ border-bottom: none !important; }
        .accordion-button{
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            color: #1e293b !important;
            background: transparent !important;
            padding: 12px 16px !important;
            box-shadow: none !important;
        }
        .accordion-button:not(.collapsed){
            background: rgba(37, 99, 235, 0.06) !important;
            color: #2563eb !important;
        }
        .accordion-button:focus{
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15) !important;
        }
        .accordion-button::after{
            background-size: 1rem;
            transition: transform 0.2s ease;
        }
        .accordion-body{
            padding: 12px 16px 18px 16px !important;
        }

        /* INPUTS */
        .form-control, .form-select{
            border-radius: 8px !important;
            border: 1px solid #e2e8f0 !important;
            font-size: 0.875rem !important;
            transition: all 0.15s ease;
        }
        .form-control:focus, .form-select:focus{
            border-color: #2563eb !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
        }
        label, .control-label{
            font-weight:500;
            color:#475569;
            font-size: 0.825rem;
            margin-bottom: 6px;
        }

        /* TABS */
        .nav-tabs{
            border-bottom: 2px solid #e2e8f0;
            gap: 4px;
            padding: 0 8px;
        }
        .nav-tabs .nav-link{
            border:none !important;
            color:#64748b;
            font-weight:600;
            font-size: 0.9rem;
            padding: 12px 20px;
            border-radius: 10px 10px 0 0 !important;
            transition: all 0.15s ease;
            margin-bottom: -2px;
        }
        .nav-tabs .nav-link:hover{
            color:#2563eb;
            background: rgba(37, 99, 235, 0.05);
        }
        .nav-tabs .nav-link.active{
            color:#2563eb !important;
            background: transparent !important;
            border-bottom: 2px solid #2563eb !important;
        }

        /* SLIDERS */
        .irs--shiny .irs-bar{
            background: linear-gradient(90deg, #2563eb, #7c3aed) !important;
            border-color: transparent !important;
        }
        .irs--shiny .irs-handle{
            border-color: #2563eb !important;
            background: #ffffff !important;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3) !important;
        }
        .irs--shiny .irs-single,
        .irs--shiny .irs-from,
        .irs--shiny .irs-to{
            background: #2563eb !important;
            border-radius: 6px !important;
        }

        /* RADIO */
        .form-check-input:checked{
            background-color: #2563eb !important;
            border-color: #2563eb !important;
        }

        /* OUTPUT TEXT */
        pre{
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
            border: 1px solid #e2e8f0 !important;
            border-left: 4px solid #2563eb !important;
            border-radius: 10px !important;
            padding: 18px 22px !important;
            font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
            font-size: 0.875rem !important;
            color: #1e293b !important;
            line-height: 1.7 !important;
        }

        /* FILE INPUT */
        .btn-default, .btn-file{
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
            color:white !important;
            border:none !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            padding: 8px 16px !important;
            transition: all 0.15s ease;
        }
        .btn-default:hover, .btn-file:hover{
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }
    """),

    ui.h1("Dashboard Estatístico Interativo"),

    ui.layout_sidebar(
        # SIDEBAR
        ui.sidebar(
            # CARD 1 — DADOS
            ui.div(
                {"class": "sidebar-card"},
                ui.div({"class": "sidebar-card-header"}, "📁 Dados"),
                ui.div(
                    {"class": "sidebar-card-body"},
                    ui.accordion(
                        ui.accordion_panel(
                            "Upload CSV",
                            ui.input_file("arquivo", "Escolha um arquivo CSV", accept=[".csv"]),
                            value="p_upload",
                        ),
                        ui.accordion_panel(
                            "Variável Quantitativa",
                            ui.input_select("variavel", None, choices=["Carregue um CSV"]),
                            value="p_variavel",
                        ),
                        id="acc_dados",
                        open=["p_upload", "p_variavel"],
                        multiple=True,
                    ),
                ),
            ),

            # CARD 2 — TESTE DE HIPÓTESES
            ui.div(
                {"class": "sidebar-card"},
                ui.div({"class": "sidebar-card-header"}, "🧪 Teste de Hipóteses"),
                ui.div(
                    {"class": "sidebar-card-body"},
                    ui.accordion(
                        ui.accordion_panel(
                            "Variância Populacional",
                            ui.input_numeric("variancia", None, value=1, min=0.0001),
                            value="p_var",
                        ),
                        ui.accordion_panel(
                            "Tipo de Teste",
                            ui.input_radio_buttons(
                                "tipo",
                                None,
                                choices={
                                    "bilateral": "Bilateral",
                                    "direita": "Unilateral à Direita",
                                    "esquerda": "Unilateral à Esquerda",
                                },
                                selected="bilateral",
                            ),
                            value="p_tipo",
                        ),
                        ui.accordion_panel(
                            "Valor de μ0",
                            ui.input_slider("mu0", None, min=-100, max=100, value=0, step=0.5),
                            value="p_mu0",
                        ),
                        ui.accordion_panel(
                            "Nível de Significância",
                            ui.input_slider("alpha", None, min=0.01, max=0.10, value=0.05, step=0.01),
                            value="p_alpha",
                        ),
                        id="acc_teste",
                        open=["p_tipo"],
                        multiple=True,
                    ),
                ),
            ),

            # CARD 3 — INTERVALO DE CONFIANÇA
            ui.div(
                {"class": "sidebar-card"},
                ui.div({"class": "sidebar-card-header"}, "📊 Intervalo de Confiança"),
                ui.div(
                    {"class": "sidebar-card-body"},
                    ui.accordion(
                        ui.accordion_panel(
                            "Nível de Confiança",
                            ui.input_slider("confianca", None, min=0.80, max=0.99, value=0.95, step=0.01),
                            value="p_conf",
                        ),
                        id="acc_ic",
                        open=["p_conf"],
                        multiple=True,
                    ),
                ),
            ),

            # CARD 4 — REGRESSÃO LINEAR
            ui.div(
                {"class": "sidebar-card"},
                ui.div({"class": "sidebar-card-header"}, "📈 Regressão Linear"),
                ui.div(
                    {"class": "sidebar-card-body"},
                    ui.accordion(
                        ui.accordion_panel(
                            "Variável X",
                            ui.input_select("x", None, choices=["Carregue um CSV"]),
                            value="p_x",
                        ),
                        ui.accordion_panel(
                            "Variável Y",
                            ui.input_select("y", None, choices=["Carregue um CSV"]),
                            value="p_y",
                        ),
                        id="acc_reg",
                        open=[],
                        multiple=True,
                    ),
                ),
            ),
        ),

        # CONTEÚDO PRINCIPAL
        ui.navset_tab(
            # ANÁLISE DESCRITIVA
            ui.nav_panel(
                "Análise Descritiva",
                ui.div({"class": "card"}, ui.h3("Histograma"), ui.output_plot("histograma")),
                ui.div({"class": "card"}, ui.h3("Boxplot Estatístico"), ui.output_plot("boxplot")),
                ui.div({"class": "card"}, ui.h3("Estatísticas Descritivas"), ui.output_text_verbatim("estatisticas")),
            ),

            # TESTE DE HIPÓTESES
            ui.nav_panel(
                "Teste de Hipóteses",
                ui.div({"class": "card"}, ui.h3("Curva Normal do Teste"), ui.output_plot("grafico_teste")),
                ui.div({"class": "card"}, ui.output_text_verbatim("teste")),
            ),

            # INTERVALO DE CONFIANÇA
            ui.nav_panel(
                "Intervalo de Confiança",
                ui.div({"class": "card"}, ui.output_plot("grafico_ic")),
                ui.div({"class": "card"}, ui.output_text_verbatim("ic")),
            ),

            # REGRESSÃO
            ui.nav_panel(
                "Regressão Linear",
                ui.div({"class": "card"}, ui.output_plot("regressao")),
                ui.div({"class": "card"}, ui.output_text_verbatim("resultado_reg")),
            ),
        ),
    ),
)

# SERVER
def server(input, output, session):

    # DATAFRAME REATIVO
    df_reactive = reactive.value(None)

    # CARREGAR CSV
    @reactive.effect
    @reactive.event(input.arquivo)
    def carregar_csv():
        arquivo = input.arquivo()
        req(arquivo)
        caminho = arquivo[0]["datapath"]
        df = pd.read_csv(caminho)
        df_reactive.set(df)
        cols = df.select_dtypes(include=np.number).columns.tolist()

        req(len(cols) > 0)

        ui.update_select("variavel", choices=cols, selected=cols[0], session=session)
        ui.update_select("x", choices=cols, selected=cols[0], session=session)
        ui.update_select("y", choices=cols, selected=cols[1] if len(cols) > 1 else cols[0], session=session)

    # HISTOGRAMA
    @output
    @render.plot
    @reactive.event(input.variavel)
    def histograma():
        df = df_reactive.get()
        req(df is not None)
        var = input.variavel()

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(
            df[var].dropna(),
            bins=20,
            kde=True,
            color=COR_PRIMARIA,
            edgecolor="white",
            alpha=0.85,
            ax=ax,
        )
        ax.set_title(f"Histograma — {var}", pad=15)
        ax.set_xlabel(var)
        ax.set_ylabel("Frequência")
        fig.tight_layout()
        return fig

    # BOXPLOT ESTATÍSTICO
    @output
    @render.plot
    @reactive.event(input.variavel, input.mu0, input.tipo, input.alpha, input.variancia)
    def boxplot():
        df = df_reactive.get()
        req(df is not None)

        var = input.variavel()
        s = df[var].dropna()
        media = s.mean()
        mu0 = input.mu0()
        tipo = input.tipo()
        alpha = input.alpha()
        sigma = np.sqrt(input.variancia())
        n = len(s)

        z = (media - mu0) / (sigma / np.sqrt(n))

        if tipo == "bilateral":
            cor = "#7c3aed"
            z_critico = norm.ppf(1 - alpha / 2)
            decisao = "Rejeitar H0" if abs(z) > z_critico else "Não rejeitar H0"
        elif tipo == "direita":
            cor = "#10b981"
            z_critico = norm.ppf(1 - alpha)
            decisao = "Rejeitar H0" if z > z_critico else "Não rejeitar H0"
        else:
            cor = "#f59e0b"
            z_critico = norm.ppf(alpha)
            decisao = "Rejeitar H0" if z < z_critico else "Não rejeitar H0"

        fig, ax = plt.subplots(figsize=(10, 3.2))
        sns.boxplot(x=s, color=cor, ax=ax, linewidth=1.5, fliersize=4)
        for patch in ax.artists if hasattr(ax, "artists") else []:
            patch.set_alpha(0.75)

        ax.axvline(media, color=COR_PRIMARIA, linestyle="--", linewidth=2.5,
                   label=f"Média = {media:.2f}")
        ax.axvline(mu0, color=COR_DESTAQUE, linestyle="-", linewidth=2.5,
                   label=f"μ0 = {mu0}")

        ax.set_title(f"{var}  |  {tipo.upper()}  |  {decisao}", pad=12)
        ax.legend(loc="upper right")
        fig.tight_layout()
        return fig

    # ESTATÍSTICAS
    @output
    @render.text
    @reactive.event(input.variavel)
    def estatisticas():
        df = df_reactive.get()
        req(df is not None)
        var = input.variavel()
        s = df[var].dropna()

        return f"""
Variável analisada: {var}

Média: {s.mean():.4f}
Mediana: {s.median():.4f}
Desvio-padrão: {s.std():.4f}
Tamanho da amostra: {len(s)}
Valor mínimo: {s.min():.4f}
Valor máximo: {s.max():.4f}
"""

    # GRÁFICO TESTE DE HIPÓTESES
    @output
    @render.plot
    @reactive.event(input.variavel, input.variancia, input.mu0, input.alpha, input.tipo)
    def grafico_teste():
        df = df_reactive.get()
        req(df is not None)

        var = input.variavel()
        s = df[var].dropna()
        media = s.mean()
        n = len(s)
        sigma = np.sqrt(input.variancia())
        mu0 = input.mu0()
        alpha = input.alpha()
        tipo = input.tipo()

        z = (media - mu0) / (sigma / np.sqrt(n))
        x = np.linspace(-4, 4, 1000)
        y = norm.pdf(x)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, color=COR_PRIMARIA, linewidth=2.2)
        ax.fill_between(x, y, color=COR_PRIMARIA, alpha=0.08)

        if tipo == "bilateral":
            z_critico = norm.ppf(1 - alpha / 2)
            ax.fill_between(x, y, where=(x <= -z_critico), color=COR_DESTAQUE, alpha=0.55)
            ax.fill_between(x, y, where=(x >= z_critico), color=COR_DESTAQUE, alpha=0.55)
        elif tipo == "direita":
            z_critico = norm.ppf(1 - alpha)
            ax.fill_between(x, y, where=(x >= z_critico), color=COR_DESTAQUE, alpha=0.55)
        else:
            z_critico = norm.ppf(alpha)
            ax.fill_between(x, y, where=(x <= z_critico), color=COR_DESTAQUE, alpha=0.55)

        ax.axvline(z, color=COR_SUCESSO, linestyle="--", linewidth=2.5,
                   label=f"Z calculado = {z:.2f}")

        ax.set_title("Curva Normal do Teste de Hipóteses", pad=15)
        ax.set_xlabel("Z")
        ax.set_ylabel("Densidade")
        ax.legend()
        fig.tight_layout()
        return fig

    # TESTE
    @output
    @render.text
    @reactive.event(input.variavel, input.variancia, input.mu0, input.alpha, input.tipo)
    def teste():
        df = df_reactive.get()
        req(df is not None)

        var = input.variavel()
        s = df[var].dropna()
        media = s.mean()
        n = len(s)
        sigma = np.sqrt(input.variancia())
        mu0 = input.mu0()
        alpha = input.alpha()
        tipo = input.tipo()

        z = (media - mu0) / (sigma / np.sqrt(n))

        if tipo == "bilateral":
            z_critico = norm.ppf(1 - alpha / 2)
            decisao = "Rejeitar H0" if abs(z) > z_critico else "Não rejeitar H0"
        elif tipo == "direita":
            z_critico = norm.ppf(1 - alpha)
            decisao = "Rejeitar H0" if z > z_critico else "Não rejeitar H0"
        else:
            z_critico = norm.ppf(alpha)
            decisao = "Rejeitar H0" if z < z_critico else "Não rejeitar H0"

        return f"""
Teste de Hipóteses para Média

H0: μ = {mu0}

Estatística Z: {z:.4f}
Valor crítico: {z_critico:.4f}
Nível de significância: {alpha:.2%}

Decisão:
{decisao}
"""

    # GRÁFICO IC
    @output
    @render.plot
    @reactive.event(input.variavel, input.confianca)
    def grafico_ic():
        df = df_reactive.get()
        req(df is not None)

        var = input.variavel()
        s = df[var].dropna()
        media = s.mean()
        desvio = s.std()
        n = len(s)
        conf = input.confianca()
        alpha = 1 - conf

        z = norm.ppf(1 - alpha / 2)
        erro = z * (desvio / np.sqrt(n))
        inferior = media - erro
        superior = media + erro

        fig, ax = plt.subplots(figsize=(8, 2.4))
        ax.errorbar(media, 0, xerr=erro, fmt='o',
                    color=COR_PRIMARIA, ecolor=COR_SECUNDARIA,
                    elinewidth=3, capsize=12, capthick=2, markersize=12)
        ax.axvline(media, color=COR_DESTAQUE, linestyle="--", linewidth=2)
        ax.set_title(f"IC {conf:.0%}: [{inferior:.2f}, {superior:.2f}]", pad=12)
        ax.set_yticks([])
        fig.tight_layout()
        return fig

    # IC TEXTO
    @output
    @render.text
    @reactive.event(input.variavel, input.confianca)
    def ic():
        df = df_reactive.get()
        req(df is not None)

        var = input.variavel()
        s = df[var].dropna()
        media = s.mean()
        desvio = s.std()
        n = len(s)
        conf = input.confianca()
        alpha = 1 - conf

        z = norm.ppf(1 - alpha / 2)
        erro = z * (desvio / np.sqrt(n))
        inferior = media - erro
        superior = media + erro

        return f"""
Intervalo de Confiança para Média

Nível de confiança: {conf:.2%}
Limite inferior: {inferior:.4f}
Limite superior: {superior:.4f}
"""

    # REGRESSÃO
    @output
    @render.plot
    @reactive.event(input.x, input.y)
    def regressao():
        df = df_reactive.get()
        req(df is not None)

        x = input.x()
        y = input.y()
        dados_reg = df[[x, y]].dropna()

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.regplot(
            x=dados_reg[x],
            y=dados_reg[y],
            scatter_kws={"color": COR_PRIMARIA, "alpha": 0.6, "s": 50, "edgecolor": "white"},
            line_kws={"color": COR_DESTAQUE, "linewidth": 2.5},
            ax=ax,
        )
        ax.set_title(f"Regressão Linear: {y} vs {x}", pad=15)
        fig.tight_layout()
        return fig

    # RESULTADOS REGRESSÃO
    @output
    @render.text
    @reactive.event(input.x, input.y)
    def resultado_reg():
        df = df_reactive.get()
        req(df is not None)

        x = input.x()
        y = input.y()
        dados_reg = df[[x, y]].dropna()

        resultado = linregress(dados_reg[x], dados_reg[y])

        return f"""
Resultados da Regressão Linear

Variável resposta (y): {y}
Variável explicativa (x): {x}

Coeficiente de Correlação (R): {resultado.rvalue:.4f}
Coeficiente de Determinação (R²): {resultado.rvalue**2:.4f}

Equação da reta ajustada:
y = {resultado.slope:.4f}x + {resultado.intercept:.4f}
"""

# APP
app = App(app_ui, server)