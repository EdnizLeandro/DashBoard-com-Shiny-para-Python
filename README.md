# Dashboard Estatístico Interativo com Shiny for Python
Dashboard interativo em Python para análise descritiva, testes de hipóteses, intervalos de confiança e regressão linear simples.

## Sobre o Projeto

Este projeto consiste no desenvolvimento de um dashboard estatístico interativo utilizando Python e Shiny for Python.

A aplicação permite ao usuário carregar arquivos CSV diretamente do computador e realizar análises estatísticas de forma dinâmica, incluindo:

- Análise descritiva de variáveis quantitativas;
- Teste de hipóteses para média com variância conhecida;
- Construção de intervalos de confiança;
- Regressão linear simples;
- Visualização gráfica dos resultados.

O projeto foi desenvolvido com foco educacional e acadêmico (UFRPE) para aplicação dos principais conceitos de Estatística e Ciência de Dados.

---

## Funcionalidades

### 1. Análise Descritiva

O usuário pode:

- Selecionar um arquivo CSV local;
- Escolher uma variável quantitativa;
- Visualizar:
  - Histograma;
  - Boxplot;
  - Estatísticas descritivas.

Estatísticas apresentadas:

- Média;
- Mediana;
- Desvio-padrão;
- Tamanho da amostra;
- Valor mínimo;
- Valor máximo.

---

### 2. Teste de Hipóteses para Média

Permite realizar testes para média populacional assumindo variância conhecida.

Parâmetros configuráveis:

- Variância populacional;
- Valor hipotético da média (μ₀);
- Nível de significância (α);
- Tipo de teste:
  - Bilateral;
  - Unilateral à direita;
  - Unilateral à esquerda.

Resultados:

- Estatística Z;
- Valor crítico;
- Decisão do teste.

Além disso, o dashboard apresenta uma visualização gráfica da curva normal e das regiões críticas.

---

### 3. Intervalo de Confiança

Construção automática de intervalos de confiança para a média populacional.

O usuário define:

- Nível de confiança.

Resultados:

- Limite inferior;
- Limite superior;
- Nível de confiança utilizado.

Também é exibida uma representação visual do intervalo de confiança.

---

### 4. Regressão Linear Simples

Permite selecionar:

- Variável explicativa (X);
- Variável resposta (Y).

Resultados:

- Coeficiente de correlação (R);
- Coeficiente de determinação (R²);
- Equação da reta ajustada.

Visualizações:

- Gráfico de dispersão;
- Linha de regressão ajustada.

---

## Tecnologias Utilizadas

- Python
- Shiny for Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SciPy

---

## Instalação

### Clonar o repositório

```bash
git clone https://github.com/seu-usuario/dashboard-estatistico.git
```

Entrar na pasta:

```bash
cd dashboard-estatistico
```

---

### Criar ambiente virtual (opcional)

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

---

### Instalar dependências

```bash
pip install -r requirements.txt
```

---

## Executando a Aplicação

Inicie o servidor Shiny:

```bash
shiny run app.py
```

ou

```bash
shiny run --reload app.py
```

Acesse:

```text
http://127.0.0.1:8000
```

ou

```text
http://localhost:8000
```

---

## Datasets de Exemplo

### Iris Dataset

https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv

### Penguins Dataset

https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv

### Tips Dataset

https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv

---

## Exemplo de Aplicação

O dashboard pode ser utilizado para:

- Exploração de dados;
- Análises estatísticas básicas;
- Estudos acadêmicos;
- Demonstração de conceitos de inferência estatística;
- Visualização de relações entre variáveis.

---

## Possíveis Melhorias Futuras

- Testes t para média;
- ANOVA;
- Regressão múltipla;
- Exportação de relatórios PDF;
- Exportação de gráficos;
- Dashboard responsivo para dispositivos móveis;
- Integração com bancos de dados.

---

## Autor

Projeto desenvolvido como atividade acadêmica (UFRPE - ESTATÍSTICA APLICADA A ANÁLISE DE DADOS) utilizando Python e Shiny for Python.

---

## Licença

Este projeto possui finalidade educacional e acadêmica.
