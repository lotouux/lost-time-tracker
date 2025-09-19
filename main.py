# ==== IMPORTANDO LIBS ====

# Lib para interagir com o Windows Management Instrumentation (WMI)
# Coleta informaçõles do SO
import wmi

# Lib para manipulação de dados
# O 'pd" é o padrão para criar e manipular DataFrames
import pandas as pd

# Lib para manipulação de datas e horas
from datetime import datetime, timedelta

# Lib para utilizar modelos de machine learning pré-treinados.
from transformers import pipeline

# Lib para mostrar barras de progresso
from tqdm import tqdm

# ==== CONFIGURAÇÕES ====
# Configuração do classificador de texto usando um modelo pré-treinado
# da Hugging Face para classificação de texto sem necessidade de treinamento adicional.
# O modelo "facebook/bart-large-mnli" é adequado para tarefas de classificação de multiplas categorias.
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Categorias possíveis para classificar os aplicativos
possible_labels = ["Navegador", "Comunicação", "Jogos", "Produtividade", "Entretenimento", "Outros"]

# Nomes de aplicativos para ignorar
ignore_list = [
    "svchost.exe", "RuntimeBroker.exe", "dllhost.exe",
    "SearchIndexer.exe", "conhost.exe", "LockApp.exe",
    "wlanext.exe", "unsecapp.exe", "WmiPrvSE.exe", "lsass.exe",
    "csrss.exe", "smss.exe", "wininit.exe", "winlogon.exe",
    "System Idle Process", "explorer.exe", "py.exe", "python.exe", "pythonw.exe"
]

# ===== FUNÇÕES AUXILIARES ====
def classify_app(app_name):
    """
    Classifica o nome do aplicativo em uma das categorias possíveis usando o classificador de texto.

    Parâmetro: app_name (str): Nome do aplicativo a ser classificado.
    Retorna: str: Categoria com maior score.
    """

    # Executa a classificação Zero-Shot: Modelo tenta classificar o texto em categorias sem ter sido treinado especificamente para elas.
    # 'possible_labels' são as categorias fornecidas.
    result = classifier(app_name, possible_labels)

    # Retorna o rótulo com maior score
    # O pipeline retorna uma lista de rótulos ordenados por score.
    # indice 0 é o rótulo com maior score.
    return result["labels"][0]

# ==== FUNÇÃO PRINCIPAL ====
def run_analyzer_historical():
    """
    Analisa o uso de aplicativos no Windows nos últimos 7 dias.
    Coleta dados de processos, classifica aplicativos, calcula tempo de uso e gera relatórios.
    """
    try:
        # Conecta ao WMI para acessar informações do sistema
        conn = wmi.WMI()
        # Define a data limite para os últimos 7 dias
        data_limite = datetime.now() - timedelta(days=7)
        processos = []

        # --- Coleta dados de processos ---
        # Itera sobre todos os processos e coleta nome, hora de início e duração
        for p in conn.Win32_Process():
            try:
                # Extrai e formata a data de criação do processo
                start_time_str = p.CreationDate.split('.')[0]
                start_time = datetime.strptime(start_time_str, "%Y%m%d%H%M%S")
                # Considera apenas processos iniciados na última semana
                if start_time >= data_limite:
                    # Calcula a duração do processo em horas
                    duration = (datetime.now() - start_time).total_seconds() / 3600  # horas
                    processos.append({
                        "app": p.Name,
                        "start_time": start_time,
                        "duration_hours": duration
                    })
            except Exception:
                # Ocorre quando a data de criação não está disponível
                continue  # ignora processos sem data válida

        # Cria um DF do pandas a partir da lista de processos
        df = pd.DataFrame(processos)

        if df.empty:
            print("Nenhum dado de processo foi encontrado para a última semana.")
            return

        # --- Processamento de dados ---
        # Ignora processados da lista predefinida
        df = df[~df["app"].isin(ignore_list)]

        # Aplica a função de classificação a cada nome de app
        # Adiciona uma nova coluna "category" ao DataFrame
        unique_apps = df["app"].unique()
        app_categories = {}

        # Itera sobre cada app único, mostrando progresso
        for app in tqdm(unique_apps, desc="Classificando aplicativos"):
            app_categories[app] = classify_app(app)

        # Mapeia as categorias de volta ao DataFrame
        df["category"] = df["app"].map(app_categories)

        # --- Análise e Relatórios ---
        # Estima o tempo total de tela desde o primeiro processo registrado
        first_start_time = df['start_time'].min()
        total_screen_time = (datetime.now() - first_start_time).total_seconds() / 3600

        # Agrupa os dados por categoria e app, somando a duração
        # O 'unstack' transforma os apps em colunas
        summary = df.groupby(["category", "app"])["duration_hours"].sum().unstack(level=1).fillna(0)
        # Calcula o tempo total por categoria, ordenando do maior para o menor
        total_time_by_category = df.groupby("category")["duration_hours"].sum().sort_values(ascending=False)

        # --- Relatórios ---
        print("\n--- Relatório de Uso de Tela (Últimos 7 Dias) ---")
        print(f"Tempo Total de Tela (Estimativa): {total_screen_time:.2f} horas")
        print("\nTempo Total de Execução de Processos por Categoria:")
        print(total_time_by_category.round(2))

        # --- Relatório detalhado por categoria e app ---
        # Calcula o total de horas por app dentro de cada categoria
        hours_lost_in_games = total_time_by_category.get("Jogos", 0) + total_time_by_category.get("Navegador", 0)
        # Estima quantos livros de 10 horas poderiam ter sido lidos com o tempo gasto
        books_read = round(hours_lost_in_games / 10, 2)
        print(f"\nVocê poderia ter lido {books_read} livros de 10 horas com o tempo gasto em jogos e navegação.")

    except wmi.x_wmi as e:
        # Exceção específica para erros de WMI
        print(f"Erro ao conectar ao WMI. Verifique se você tem permissão de administrador. Erro: {e}")
    except Exception as e:
        # Exceção geral para outros erros
        print(f"Ocorreu um erro: {e}")


# Executar a análise
run_analyzer_historical()
