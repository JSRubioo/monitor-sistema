# 🖥️ Monitor de Sistema

Script em Python que faz um diagnóstico rápido da máquina — espaço em
disco, uso de memória e os processos que mais consomem recursos — e gera
um relatório em arquivo `.txt` com data e hora.

## Por que esse projeto?

Em atendimentos de suporte técnico, uma das primeiras coisas que se
verifica quando um usuário reclama de lentidão é: **disco cheio?
memória no limite? algum processo consumindo tudo?** Esse script
automatiza esse primeiro diagnóstico, que normalmente seria feito
manualmente pelo Gerenciador de Tarefas.

## Tecnologias

- Python 3
- [psutil](https://pypi.org/project/psutil/) — coleta de métricas do sistema

## Como rodar

```bash
pip install psutil
python monitor_sistema.py
```

O script imprime o relatório no terminal e também salva um arquivo
`relatorio_AAAAMMDD_HHMMSS.txt` na pasta atual.

## Exemplo de saída

```
=== Relatório de Diagnóstico do Sistema ===
Data/Hora: 23/09/2026 14:32:10
Sistema Operacional: Windows 10

-- Disco --
Total: 476.0 GB | Usado: 210.5 GB | Livre: 265.5 GB (44.2% em uso)

-- Memória --
Total: 16.0 GB | Usado: 9.8 GB (61.3% em uso)

-- Top 5 processos por uso de memória --
PID   4521 | chrome.exe                | 12.4%
PID   1023 | Teams.exe                 | 8.1%
...
```

## Próximos passos (ideias de evolução)

- Enviar o relatório por e-mail automaticamente
- Rodar em agendamento (Windows Task Scheduler / cron) para monitoramento periódico
- Exportar em formato CSV para análise histórica
