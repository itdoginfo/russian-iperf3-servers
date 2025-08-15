#!/bin/bash

# Network Speed Test Script from https://github.com/itdoginfo/russian-iperf3-servers

# Configuration variables
IPERF_TIMEOUT=15
IPERF_TEST_DURATION=10
PARALLEL_STREAMS=8
FALLBACK_STREAMS=8
INTER_TEST_DELAY=1
MAX_JSON_LENGTH=50

# Port range for iperf3 servers
IPERF_PORT_RANGE=(5201 5202 5203 5204 5205 5206 5207 5208 5209)

# Runtime flags
DEBUG=false
RESULTS=()

# Server configurations
declare -A SERVERS=(
    ["Moscow"]="spd-rudp.hostkey.ru"
    ["Saint Petersburg"]="st.spb.ertelecom.ru"
    ["Nizhny Novgorod"]="st.nn.ertelecom.ru"
    ["Chelyabinsk"]="st.chel.ertelecom.ru"
    ["Tyumen"]="st.tmn.ertelecom.ru"
)

declare -A FALLBACK_SERVERS=(
    ["Moscow"]="st.tver.ertelecom.ru"
    ["Saint Petersburg"]="st.yar.ertelecom.ru"
    ["Nizhny Novgorod"]="speed-nn.vtt.net"
    ["Chelyabinsk"]="st.mgn.ertelecom.ru"
    ["Tyumen"]="st.krsk.ertelecom.ru"
)

declare -A FALLBACK_CITIES=(
    ["Moscow"]="Tver"
    ["Saint Petersburg"]="Yaroslavl"
    ["Nizhny Novgorod"]="Nizhny Novgorod"
    ["Chelyabinsk"]="Magnitogorsk"
    ["Tyumen"]="Krasnoyarsk"
)

# Test order
CITY_ORDER=("Moscow" "Saint Petersburg" "Nizhny Novgorod" "Chelyabinsk" "Tyumen")

# Functions
find_available_port() {
    local host="$1"
    
    log_debug "Scanning ports for $host"
    
    for port in "${IPERF_PORT_RANGE[@]}"; do
        log_debug "Trying port $port on $host"
        
        local test_result
        test_result=$(timeout "$IPERF_TIMEOUT" iperf3 -c "$host" -p "$port" -t 1 2>&1 || echo "")
        
        if [[ "$test_result" == *"receiver"* && "$test_result" != *"error"* ]]; then
            log_debug "Found working port $port on $host"
            echo "$port"
            return 0
        fi
    done
    
    log_debug "No working ports found on $host"
    return 1
}

log_debug() {
    if [[ "$DEBUG" == true ]]; then
        if [[ -n "${SPINNER_PID:-}" ]]; then
            echo -e "\n\e[37m[DEBUG] $1\e[0m" >&2
        else
            echo -e "\e[37m[DEBUG] $1\e[0m" >&2
        fi
    fi
}

start_spinner() {
    local message="$1"
    echo -n "$message"
    (
        local chars=("⠇" "⠏" "⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧")
        local i=0
        while true; do
            printf "\r$message %s" "${chars[$i]}"
            i=$(( (i + 1) % ${#chars[@]} ))
            sleep 0.15
        done
    ) &
    SPINNER_PID=$!
}

stop_spinner() {
    local result="$1"
    [[ -n "${SPINNER_PID:-}" ]] && kill "$SPINNER_PID" 2>/dev/null
    printf "\r\033[K"
    
    if [[ "$DEBUG" == true ]]; then
        echo "$result"
    fi
    
    unset SPINNER_PID
}

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

OPTIONS:
    -d, --debug     Enable debug output
    -f, --fast      Fast mode (shorter test duration)
    -h, --help      Show this help message

EXAMPLES:
    $0              Run standard speed test
    $0 -f           Run fast speed test
    $0 -d           Run with debug output
EOF
}

test_iperf_server() {
    local host="$1"
    local port="$2"
    local streams="$3"
    
    log_debug "Testing iperf3 server $host:$port with $streams streams"
    
    local result
    result=$(timeout "$IPERF_TIMEOUT" iperf3 -c "$host" -p "$port" -P "$streams" -t "$IPERF_TEST_DURATION" -J 2>/dev/null || echo "")
    
    # Check if we got valid JSON with receiver data
    if [[ -n "$result" && "$result" == *'"receiver"'* && "${#result}" -gt "$MAX_JSON_LENGTH" ]]; then
        echo "$result"
        return 0
    else
        return 1
    fi  
}

parse_speed() {
    local json="$1"
    local direction="$2"
    
    if [[ "$direction" == "sender" ]]; then
        echo "$json" | jq -r ".end.sum_sent.bits_per_second // 0" | awk '{printf "%.1f", $1/1000000}'
    else
        echo "$json" | jq -r ".end.sum_received.bits_per_second // 0" | awk '{printf "%.1f", $1/1000000}'
    fi
}

get_ping() {
    local host="$1"
    ping -c 5 -W 2 "$host" 2>/dev/null | grep -oP 'rtt min/avg/max/mdev = [0-9.]+/\K[0-9]+' || echo "N/A"
}

process_test_result() {
    local result="$1"
    local city="$2"
    local host="$3"
    local port="$4"
    local is_fallback="${5:-false}"
    
    local download upload ping_result
    download=$(parse_speed "$result" "receiver")
    upload=$(parse_speed "$result" "sender")
    ping_result=$(get_ping "$host")
    
    if [[ "$download" != "0.0" ]] || [[ "$upload" != "0.0" ]]; then
        local display_city="$city"
        [[ "$is_fallback" == "true" ]] && display_city="$city (F)"
        
        stop_spinner "Testing $city ($host:$port)... ✓"
        RESULTS+=("$(printf "%-18s %-15s %-15s %-10s" "$display_city" "${download} Mbps" "${upload} Mbps" "${ping_result} ms")")
        return 0
    fi
    return 1
}

test_server() {
    local city="$1"
    local host="$2"
    local fallback_host="$3"
    
    local fallback_city="${FALLBACK_CITIES[$city]}"
    
    start_spinner "Testing $city ($host)..."
    
    # Test primary server
    local port
    if port=$(find_available_port "$host"); then
        local result
        # Try with full streams
        if result=$(test_iperf_server "$host" "$port" "$PARALLEL_STREAMS"); then
            if process_test_result "$result" "$city" "$host" "$port"; then
                return 0
            fi
        fi
        
        # Retry with fewer streams
        log_debug "Retrying with $FALLBACK_STREAMS stream"
        if result=$(test_iperf_server "$host" "$port" "$FALLBACK_STREAMS"); then
            if process_test_result "$result" "$city" "$host" "$port"; then
                return 0
            fi
        fi
    fi
    
    # Test fallback server
    log_debug "Primary server failed, trying fallback $fallback_host"
    
    local fallback_port
    if fallback_port=$(find_available_port "$fallback_host"); then
        local result
        # Try fallback with full streams
        if result=$(test_iperf_server "$fallback_host" "$fallback_port" "$PARALLEL_STREAMS"); then
            if process_test_result "$result" "$fallback_city" "$fallback_host" "$fallback_port" "true"; then
                return 0
            fi
        fi
        
        # Retry fallback with fewer streams
        log_debug "Retrying fallback with $FALLBACK_STREAMS stream"
        if result=$(test_iperf_server "$fallback_host" "$fallback_port" "$FALLBACK_STREAMS"); then
            if process_test_result "$result" "$fallback_city" "$fallback_host" "$fallback_port" "true"; then
                return 0
            fi
        fi
    fi
    
    stop_spinner "Testing $city ($host)... ✗"
    RESULTS+=("$(printf "%-18s %-15s %-15s %-10s" "$city" "\e[31m-\e[0m" "\e[31m-\e[0m" "N/A")")
    return 1
}

run_tests() {
    log_debug "Starting network speed tests"
    
    for city in "${CITY_ORDER[@]}"; do
        local server="${SERVERS[$city]}"
        local fallback="${FALLBACK_SERVERS[$city]}"
        
        test_server "$city" "$server" "$fallback"
        
        # Add delay between tests to prevent server overload
        [[ ${#CITY_ORDER[@]} -gt 1 ]] && sleep "$INTER_TEST_DELAY"
    done
}

print_results() {
    echo
    printf '🤝 \033[1;32m%s\033[0m \033[0;34m%s\033[0m\n' "From the community, for the community:" "https://github.com/itdoginfo/russian-iperf3-servers"
    echo
    printf "%-18s %-15s %-15s %-10s\n" "Server" "Download" "Upload" "Ping"
    printf "%-18s %-15s %-15s %-10s\n" "------" "--------" "------" "----"
    
    for result in "${RESULTS[@]}"; do
        echo -e "$result"
    done
}

cleanup() {
    [[ -n "${SPINNER_PID:-}" ]] && kill "$SPINNER_PID" 2>/dev/null
    exit 0
}

main() {
    local start_time=$(date +%s)
    
    # Set up signal handlers
    trap cleanup SIGINT SIGTERM
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            -d|--debug)
                DEBUG=true
                echo "Debug mode enabled"
                shift
                ;;
            -f|--fast)
                IPERF_TEST_DURATION=1
                IPERF_TIMEOUT=5
                echo "Fast mode enabled"
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1" >&2
                show_usage >&2
                exit 1
                ;;
        esac
    done
    
    # Check dependencies
    for cmd in iperf3 jq awk ping; do
        if ! command -v "$cmd" &> /dev/null; then
            echo "Error: Required command '$cmd' not found. Please install it and rerun the script." >&2
            exit 1
        fi
    done
    
    run_tests
    print_results
    
    local end_time=$(date +%s)
    local execution_time=$((end_time - start_time))
    echo
    printf "\033[0;36mExecution time: %d seconds\033[0m\n" "$execution_time"
}

main "$@"