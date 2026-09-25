# SE-AQUÁRIO — Sistema Especialista para Diagnóstico de Problemas em Aquários de Água Doce

Trabalho acadêmico de Sistemas Especialistas. O sistema recebe parâmetros
físico-químicos da água (pH, amônia, nitrito, nitrato, temperatura) e
sintomas observados nos peixes/aquário, e retorna diagnósticos e
recomendações com base em uma base de regras (encadeamento para frente).

## Como executar

```bash
python3 expert_aquario.py          # modo interativo (perguntas no terminal)
python3 expert_aquario.py --demo   # roda 4 casos de teste prontos
```

Requer apenas Python 3 (biblioteca padrão, sem dependências externas).

## Estrutura

- `expert_aquario.py` — base de fatos, base de regras (13 regras),
  motor de inferência e interface de linha de comando.

## Base de conhecimento

Ver a tabela de regras completa no trabalho (PDF) entregue junto com
este repositório.
