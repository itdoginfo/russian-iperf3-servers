#!/usr/bin/env python3

import yaml
import asyncio
import sys
from datetime import datetime

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

async def test_server(server, semaphore, results_dict):
    """Optimized version of server testing"""
    async with semaphore:
        address = server['address']
        port = server.get('port', 5201)
        server_name = server['Name']

        test_line = f"{server_name}"

        port_open = await check_port_open(address, port)
        
        if not port_open:
            status = "❌ (port closed)"
            print(f"{test_line} {status}")
            results_dict[server_name] = (False, status)
            return False

        for attempt in range(1, RETRY_ATTEMPTS + 1):
            success, error_msg = await run_iperf3(address, port)
            if success:
                if attempt > 1:
                    status = f"✅ (attempt {attempt})"
                else:
                    status = "✅"
                
                print(f"{test_line} {status}")
                results_dict[server_name] = (True, status)
                return True
            elif attempt < RETRY_ATTEMPTS:
                await asyncio.sleep(RETRY_DELAY)

        status = f"❌ ({RETRY_ATTEMPTS} attempts)"
        print(f"{test_line} {status}")
        results_dict[server_name] = (False, status)
        return False

async def test_all_servers(servers, max_concurrent=MAX_CONCURRENT):
    """Asynchronously tests all servers"""
    semaphore = asyncio.Semaphore(max_concurrent)
    results_dict = {}
      
    tasks = [
        asyncio.create_task(test_server(server, semaphore, results_dict))
        for server in servers
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for i, server in enumerate(servers):
        if isinstance(results[i], Exception):
            print(f"Critical error during testing {server['Name']}: {results[i]}")
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
        content += f"| {server['Name']} | {server['City']} | {server['address']} | {server.get('port', 5201)} | {status_emoji} |\n"
    
    current_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    available = sum(1 for s in servers if s.get('status', False))
    total = len(servers)
    
    content += f"\n📅 **Latest test:** {current_time}\n\n"
    content += f"✅ **Available**: {available}/{total} servers\n\n"
    content += f"❌ **Unavailable**: {total - available}/{total} servers\n\n"
    content += f"⏱️ **Execution time**: {duration:.1f} seconds\n\n"

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
