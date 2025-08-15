# Public iPerf3 servers in Russia

List of public iPerf3 servers in Russia, checked daily for availability.

## How it works
- The server list is stored in YAML format in `list.yml`.
- The script automatically tests each iPerf3 server and records the results in the table below.

## Suggest more servers
We need more servers! Please create an issue or PR if you know of others.

## Test script
```
bash <(wget -qO- https://raw.githubusercontent.com/itdoginfo/russian-iperf3-servers/refs/heads/main/speedtest.sh)
```

Fast Mode
```
bash <(wget -qO- https://raw.githubusercontent.com/itdoginfo/russian-iperf3-servers/refs/heads/main/speedtest.sh) -f
```

### Dependencies
- iperf3
- jq
- ping
- awk

### Fallback
For each city, there is a primary and a fallback server. The test first checks the primary server across the port range 5201–5209, only if all ports fail does it fall back to the secondary server. In the results table, this is marked as "City (F)".

## Table of servers