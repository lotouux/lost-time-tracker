import wmi
import pandas as pd
from datetime import datetime, timedelta

# Nomes de aplicativos para ignorar
ignore_list = [
    "svchost.exe", "RuntimeBroker.exe", "dllhost.exe",
    "SearchIndexer.exe", "conhost.exe", "LockApp.exe",
    "wlanext.exe", "unsecapp.exe", "WmiPrvSE.exe", "lsass.exe",
    "csrss.exe", "smss.exe", "wininit.exe", "winlogon.exe",
    "System Idle Process", "explorer.exe", "py.exe", "python.exe", "pythonw.exe"
]

# Mapeamento de categorias de apps
categories = {
    "chrome.exe": "Navegador",
    "msedge.exe": "Navegador",
    "Discord.exe": "Comunicação",
    "WhatsApp.exe": "Comunicação",
    "steam.exe": "Jogos",
    "steamwebhelper.exe": "Jogos",
    "pycharm64.exe": "Produtividade",
    "powershell.exe": "Produtividade",
    "idea64.exe": "Produtividade",
    "code.exe": "Produtividade",
    "Spotify.exe": "Entretenimento",
    "vlc.exe": "Entretenimento",
    "Netflix.exe": "Entretenimento"
}


# --- Analisador de Dados Históricos ---
def run_analyzer_historical():
    try:
        # Conectar ao WMI
        conn = wmi.WMI()

        # Definir período: últimos 7 dias
        data_limite = datetime.now() - timedelta(days=7)

        # Lista para armazenar dados coletados
        processos = []

        # Obter todos os processos criados na última semana
        # Nota: WMI não armazena a hora de término. Para os processos que estão ativos, a duração
        # é calculada até o momento da execução do script. Para os que foram encerrados,
        # a duração exata não é conhecida, por isso esta abordagem é uma estimativa.
        for p in conn.Win32_Process():
            try:
                start_time_str = p.CreationDate.split('.')[0]
                start_time = datetime.strptime(start_time_str, "%Y%m%d%H%M%S")

                if start_time >= data_limite:
                    # Para simplificar e manter a lógica do seu código, a duração é calculada
                    # do início até agora. Isso é uma estimativa para o propósito do projeto.
                    duration = (datetime.now() - start_time).total_seconds() / 3600  # horas

                    processos.append({
                        "app": p.Name,
                        "start_time": start_time,
                        "duration_hours": duration
                    })
            except Exception as e:
                # Ignora erros em processos do sistema que não têm data de criação
                continue

        df = pd.DataFrame(processos)

        if df.empty:
            print("Nenhum dado de processo foi encontrado para a última semana.")
            return

        # Limpar a lista de processos irrelevantes
        df = df[~df["app"].isin(ignore_list)]

        # Aplicar as categorias
        df["category"] = df["app"].map(categories).fillna("Outros")

        # Calcula o tempo total de tela de forma mais realista.
        # Ele encontra a hora de início do primeiro processo da semana e calcula a duração
        # até agora. Isso é uma estimativa mais fiel do tempo de uso do computador.
        first_start_time = df['start_time'].min()
        total_screen_time = (datetime.now() - first_start_time).total_seconds() / 3600

        # Agrupar por aplicativo e categoria para o relatório final
        summary = df.groupby(["category", "app"])["duration_hours"].sum().unstack(level=1).fillna(0)

        total_time_by_category = df.groupby("category")["duration_hours"].sum().sort_values(ascending=False)

        print("\n--- Relatório de Uso de Tela (Últimos 7 Dias) ---")
        print(f"Tempo Total de Tela (Estimativa): {total_screen_time:.2f} horas")
        print("\nTempo Total de Execução de Processos por Categoria:")
        print(total_time_by_category.round(2))

        # Exemplo de "tempo perdido" (lógica de conversão)
        hours_lost_in_games = total_time_by_category.get("Jogos", 0) + total_time_by_category.get("Navegador", 0)
        books_read = round(hours_lost_in_games / 10, 2)
        print(
            f"\nVocê poderia ter lido {books_read} livros de 10 horas de duração com o tempo gasto em jogos e navegação.")

    except wmi.x_wmi as e:
        print(f"Erro ao conectar ao WMI. Verifique se você tem permissão de administrador. Erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


# Executar a análise
run_analyzer_historical()
