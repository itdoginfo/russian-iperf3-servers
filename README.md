# Public iPerf3 servers in Russia

List of public iPerf3 servers in Russia, checked daily for availability.

## How it works
- The server list is stored in YAML format in `list.yml`.
- The script automatically tests each iPerf3 server and records the results in the table below.

## Suggest more servers
We need more servers! Please create an issue or PR if you know of others.

## Test script
```
bash <(wget -qO- https://github.com/itdoginfo/russian-iperf3-servers/raw/main/speedtest.sh)
```

Fast Mode
```
bash <(wget -qO- https://github.com/itdoginfo/russian-iperf3-servers/raw/main/speedtest.sh) -f
```

### Dependencies
- iperf3
- jq
- ping
- awk

### Fallback
For each city, there is a primary and a fallback server. The test first checks the primary server across the port range 5201–5209, only if all ports fail does it fall back to the secondary server. In the results table, this is marked as "City (F)".

## Table of servers

| Name | City | Address | Port | Status |
|------|------|---------|------|--------|
| Ertelecom Barnaul | Barnaul | st.barnaul.ertelecom.ru | 5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Yekaterinburg | Yekaterinburg | st.ekat.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Izhevsk | Izhevsk | st.izhevsk.ertelecom.ru | 5201<br>5202<br>5204<br>5205<br>5206<br>5207<br>5208 | ✅ |
| Ertelecom Irkutsk | Irkutsk | st.irkutsk.ertelecom.ru | 5201<br>5202<br>5203<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Kazan | Kazan | st.kzn.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Kirov | Kirov | st.kirov.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Krasnoyarsk | Krasnoyarsk | st.krsk.ertelecom.ru | 5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208 | ✅ |
| Ertelecom Kurgan | Kurgan | st.kurgan.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Kursk | Kursk | st.kursk.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Magnitogorsk | Magnitogorsk | st.mgn.ertelecom.ru | 5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Naberezhnye Chelny | Naberezhnye Chelny | st.chelny.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Omsk | Omsk | st.omsk.ertelecom.ru | 5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208 | ✅ |
| Ertelecom Penza | Penza | st.penza.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Perm | Perm | st.perm.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Rostov-on-Don | Rostov-on-Don | st.rostov.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Ryazan | Ryazan | st.ryazan.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Samara | Samara | st.samara.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Saint Petersburg | Saint Petersburg | st.spb.ertelecom.ru | 5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Saratov | Saratov | st.saratov.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Tver | Tver | st.tver.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Tomsk | Tomsk | st.tomsk.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Tula | Tula | st.tula.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Tyumen | Tyumen | st.tmn.ertelecom.ru | 5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208 | ✅ |
| Ertelecom Ulyanovsk | Ulyanovsk | st.ulsk.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Ufa | Ufa | st.ufa.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208 | ✅ |
| Ertelecom Cheboksary | Cheboksary | st.cheb.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Chelyabinsk | Chelyabinsk | st.chel.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Yaroslavl | Yaroslavl | st.yar.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Lipetsk | Lipetsk | st.lipetsk.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Bryansk | Bryansk | st.bryansk.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Volgograd | Volgograd | st.volgograd.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Voronezh | Voronezh | st.voronezh.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Nizhny Novgorod | Nizhny Novgorod | st.nn.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |
| Ertelecom Yoshkar-Ola | Yoshkar-Ola | st.yola.ertelecom.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208 | ✅ |
| TTK Volgograd | Volgograd | speed-vgd.vtt.net | 5201 | ✅ |
| TTK Nizhny Novgorod | Nizhny Novgorod | speed-nn.vtt.net | 5201 | ✅ |
| TTK Saratov | Saratov | speed.vtt.net | 5201 | ✅ |
| TTK Saransk | Saransk | speed-sar.vtt.net | 5201 | ✅ |
| Beeline Voronezh | Voronezh | voronezh-speedtest.corbina.net | 5201 | ✅ |
| Beeline Astrakhan | Astrakhan | astrakhan1.speedtest.corbina.net | 5201 | ✅ |
| Hostkey Moscow | Moscow | spd-rudp.hostkey.ru | 5201<br>5202<br>5203<br>5204<br>5205<br>5206<br>5207<br>5208<br>5209 | ✅ |

📅 **Latest test:** 08.09.2025 07:42:19 (MSK, UTC+3)

✅ **Available**: 41/41 servers

❌ **Unavailable**: 0/41 servers

⏱️ **Execution time**: 148.5 seconds

