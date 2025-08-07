#!/usr/bin/env python3

import yaml
import asyncio
import sys
from datetime import datetime, timezone, timedelta

PORT_CHECK_TIMEOUT = 3
IPERF3_TIMEOUT = 8
IPERF3_TEST_DURATION = 3
MAX_CONCURRENT = 15
RETRY_ATTEMPTS = 3
RETRY_DELAY = 2

async def load_servers_from_yaml(file_path='list.yml'):
    """Loads the list of servers from a YAML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            servers = yaml.safe_load(f)
        return servers
    except FileNotFoundError:
        print(f"Error: file {file_path} not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error reading YAML file: {e}")
        sys.exit(1)

async def check_port_open(address, port, timeout=PORT_CHECK_TIMEOUT):
    """Asynchronously checks if the port is open on the server"""
    try:
        future = asyncio.open_connection(address, port)
        reader, writer = await asyncio.wait_for(future, timeout=timeout)
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False
    except Exception:
        return False

async def run_iperf3(address, port, timeout=IPERF3_TIMEOUT):
    """Simplified version of running iperf3"""
    try:
        process = await asyncio.create_subprocess_exec(
            'iperf3', '-c', address, '-p', str(port), '-t', str(IPERF3_TEST_DURATION),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=timeout
        )
        
        if process.returncode == 0 and stdout:
            return True, "Test passed"
        
        return False, stderr.decode('utf-8', errors='ignore') if stderr else "Test error"
        
    except asyncio.TimeoutError:
        if 'process' in locals():
            try:
                process.terminate()
                await asyncio.wait_for(process.wait(), timeout=2)
            except:
                process.kill()
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def parse_ports(port_field):
    if isinstance(port_field, int):
        return [port_field]
    
    if not isinstance(port_field, str):
        return [5201]
    
    s = port_field.strip()
    if '-' in s:
        start, end = map(int, s.split('-', 1))
        return list(range(min(start, end), max(start, end) + 1))
    
    if ',' in s:
        return [int(x.strip()) for x in s.split(',') if x.strip()]
    
    return [int(s)] if s else [5201]

async def test_server(server, semaphore):
    async with semaphore:
        address = server['address']
        ports = parse_ports(server.get('port', 5201))
        server_name = server['Name']

        passed_ports = []
        failed_ports = []

        open_ports = []
        for port in ports:
            if await check_port_open(address, port):
                open_ports.append(port)

        if not open_ports:
            print(f"{server_name} ❌ (all ports closed)")
            server.update({'passed_ports': [], 'failed_ports': ports})
            return False

        for port in open_ports:
            success = False
            last_error = None

            for attempt in range(1, RETRY_ATTEMPTS + 1):
                success, error_msg = await run_iperf3(address, port)
                if success:
                    print(f"{server_name} ✅ (port {port})" + 
                          (f", attempt {attempt}" if attempt > 1 else ""))
                    passed_ports.append(port)
                    break
                else:
                    last_error = error_msg
                    if attempt < RETRY_ATTEMPTS:
                        print(f"{server_name} ❌ attempt {attempt} on port {port}: {error_msg}")
                        await asyncio.sleep(RETRY_DELAY)

            if not success:
                failed_ports.append(port)
                if attempt == RETRY_ATTEMPTS:
                    print(f"{server_name} ❌ port {port} failed: {last_error}")

        server.update({
            'passed_ports': passed_ports,
            'failed_ports': failed_ports + [p for p in ports if p not in open_ports]
        })

        return bool(passed_ports)

async def test_all_servers(servers, max_concurrent=MAX_CONCURRENT):
    """Asynchronously tests all servers"""
    semaphore = asyncio.Semaphore(max_concurrent)
      
    tasks = [
        asyncio.create_task(test_server(server, semaphore))
        for server in servers
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, server in enumerate(servers):
        if isinstance(results[i], Exception):
            server['status'] = False
        else:
            server['status'] = results[i]
    
    return servers

def load_readme_header(file_path='readme-header.md'):
    """Loads the header content for README.md from a separate file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: {file_path} not found, using default header")
        return "## Table of servers\n"
    except Exception as e:
        print(f"Warning: Error reading {file_path}: {e}")
        return "## Table of servers\n"

def generate_readme(servers, duration):
    """Generates README.md with results table"""
    content = load_readme_header()
    
    if not content.endswith('\n\n'):
        content += '\n\n'
    
    content += "| Name | City | Address | Port | Status |\n"
    content += "|------|------|---------|------|--------|\n"
    
    for server in servers:
        status_emoji = '✅' if server.get('status', False) else '❌'
        passed_ports = server.get('passed_ports', [])
        port_display = "<br>".join(map(str, passed_ports)) if passed_ports else "-"
        content += (f"| {server['Name']} | {server['City']} | "
                   f"{server['address']} | {port_display} | {status_emoji} |\n")
    
    available = sum(1 for s in servers if s.get('status', False))
    total = len(servers)
    current_time = datetime.now(timezone(timedelta(hours=3))).strftime("%d.%m.%Y %H:%M:%S")
    
    content += (f"\n📅 **Latest test:** {current_time} (MSK, UTC+3)\n\n"
               f"✅ **Available**: {available}/{total} servers\n\n"
               f"❌ **Unavailable**: {total - available}/{total} servers\n\n"
               f"⏱️ **Execution time**: {duration:.1f} seconds\n\n")

    try:
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n📄 README.md created successfully!")
        print(f"✅ Available: {available}/{total} servers")
        print(f"❌ Unavailable: {total - available}/{total} servers")
        print(f"⏱️ Execution time: {duration:.1f} seconds")
    except Exception as e:
        print(f"Error creating README.md: {e}")

async def main():
    """Main asynchronous function"""
    servers = await load_servers_from_yaml('list.yml')
    print(f"⚡ Starting iPerf3 testing on \033[1m{len(servers)}\033[0m servers\n")

    start_time = datetime.now()
    
    servers = await test_all_servers(servers)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    generate_readme(servers, duration)

if __name__ == '__main__':
    asyncio.run(main())
