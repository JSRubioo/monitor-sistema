"""
Monitor de Sistema
Script de diagnóstico rápido que verifica espaço em disco, uso de memória
e os processos que mais consomem recursos no momento, gerando um relatório
em arquivo de texto com data e hora — útil como primeiro passo de
diagnóstico em atendimentos de suporte técnico.

Requisitos:
    pip install psutil

Uso:
    python monitor_sistema.py
"""
import shutil
import platform
import datetime
import psutil


def get_disk_info():
    total, used, free = shutil.disk_usage("/")
    return {
        "total_gb": round(total / (1024 ** 3), 2),
        "usado_gb": round(used / (1024 ** 3), 2),
        "livre_gb": round(free / (1024 ** 3), 2),
        "uso_percentual": round((used / total) * 100, 1),
    }


def get_memory_info():
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024 ** 3), 2),
        "usado_gb": round(mem.used / (1024 ** 3), 2),
        "uso_percentual": mem.percent,
    }


def get_top_processes(n=5):
    processos = []
    for proc in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            processos.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    processos.sort(key=lambda p: p["memory_percent"] or 0, reverse=True)
    return processos[:n]


def gerar_relatorio():
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    disco = get_disk_info()
    memoria = get_memory_info()
    top_procs = get_top_processes()

    linhas = []
    linhas.append("=== Relatório de Diagnóstico do Sistema ===")
    linhas.append(f"Data/Hora: {agora}")
    linhas.append(f"Sistema Operacional: {platform.system()} {platform.release()}")
    linhas.append("")
    linhas.append("-- Disco --")
    linhas.append(
        f"Total: {disco['total_gb']} GB | Usado: {disco['usado_gb']} GB | "
        f"Livre: {disco['livre_gb']} GB ({disco['uso_percentual']}% em uso)"
    )
    if disco["uso_percentual"] > 90:
        linhas.append("⚠ ALERTA: espaço em disco crítico (acima de 90%)")
    linhas.append("")
    linhas.append("-- Memória --")
    linhas.append(
        f"Total: {memoria['total_gb']} GB | Usado: {memoria['usado_gb']} GB "
        f"({memoria['uso_percentual']}% em uso)"
    )
    if memoria["uso_percentual"] > 90:
        linhas.append("⚠ ALERTA: uso de memória crítico (acima de 90%)")
    linhas.append("")
    linhas.append("-- Top 5 processos por uso de memória --")
    for p in top_procs:
        nome = p["name"] or "desconhecido"
        pct = p["memory_percent"] or 0
        linhas.append(f"PID {p['pid']:>6} | {nome:<25} | {pct:.1f}%")

    relatorio = "\n".join(linhas)
    print(relatorio)

    nome_arquivo = f"relatorio_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(relatorio)
    print(f"\nRelatório salvo em: {nome_arquivo}")


if __name__ == "__main__":
    gerar_relatorio()
