# EPG automático (GitHub Actions + GitHub Pages)

Gera um guia XMLTV a partir do [iptv-org/epg](https://github.com/iptv-org/epg) e publica no GitHub Pages,
atualizando sozinho **a cada 24–32 horas**.

## Instalação (5 minutos)
1. Crie um repositório no GitHub e envie estes ficheiros (mantenha a pasta `.github`).
2. **Settings → Pages → Build and deployment → Source: "GitHub Actions"**.
3. **Actions → Update EPG → Run workflow** para a primeira geração (pode demorar de minutos a horas, conforme o nº de canais).
4. No app de IPTV, use como fonte de EPG:
   - `https://SEU_USUARIO.github.io/NOME_DO_REPO/guide.xml.gz`  (ou `guide.xml`)

## Escolher os canais
Edite `config/channels.txt` com os ficheiros `*.channels.xml` que quer (um por linha).
Veja os disponíveis em https://github.com/iptv-org/epg/tree/master/sites.
Para canais próprios, crie ficheiros em `custom/` no mesmo formato:
```xml
<channels>
  <channel site="meo.pt" site_id="SIC" lang="pt" xmltv_id="SIC.pt@HD">SIC</channel>
</channels>
```
O `xmltv_id` tem de bater com o `tvg-id` da sua lista M3U.

## Como funciona o intervalo de 24–32h
O GitHub não agenda "a cada 28h". Por isso o workflow acorda a cada 8h e só gera um guia novo
se o publicado tiver **24h ou mais** (lê `last_update.txt`). Resultado: atualização entre 24h e ~32h.
Ajuste em `update-epg.yml`: `MIN_HOURS`, `DAYS` (dias de programação), `MAX_CONNECTIONS`.

## Proteções
- Se o guia novo tiver menos de `MIN_PROGRAMMES` programas, **não publica** e mantém o anterior.
- Execuções não se sobrepõem (`concurrency`).

## Avisos
- Em repositórios **públicos**, o GitHub **desativa os agendamentos após 60 dias sem atividade**.
  Se parar de atualizar, faça um commit ou reative em Actions.
- O guia fica **público**. Não coloque aqui playlists M3U com credenciais ou links privados.
- Sites de origem podem mudar ou bloquear; se um scraper falhar, os canais dele ficam sem programação.
  Use poucos `MAX_CONNECTIONS` e só os canais de que precisa.
- Respeite os termos de uso dos sites de origem.
