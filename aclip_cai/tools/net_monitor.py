import psutil
import socket


def net_status(
    check_ports: bool = True, 
    check_connections: bool = True,
    check_interfaces: bool = True,  # NEW
    check_routing: bool = True,      # NEW
    target_host: str = None         # Compatibility arg
) -> dict:
    """
    Inspects the system's network posture.
    Hardened with Interface & Routing Awareness (V2).

    Args:
        check_ports: Check listening ports
        check_connections: Check active connections
        check_interfaces: Check NIC status (UP/DOWN, IP)
        check_routing: Check default route
        target_host: Optional host to ping (not fully implemented in this minimal ver, but arg exists)
    """
    
    results = {}

    try:
        if check_ports:
            # net_connections can also be used to find listening ports
            listeners = [
                conn
                for conn in psutil.net_connections(kind="inet")
                if conn.status == psutil.CONN_LISTEN
            ]
            results["ports"] = []
            for conn in listeners:
                results["ports"].append(
                    {
                        "fd": conn.fd,
                        "family": conn.family.name,
                        "type": conn.type.name,
                        "local_address": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "status": conn.status,
                        "pid": conn.pid,
                        "process_name": _get_proc_name(conn.pid),
                    }
                )

        if check_connections:
            # Established connections
            conns = [
                conn
                for conn in psutil.net_connections(kind="inet")
                if conn.status == psutil.CONN_ESTABLISHED
            ]
            results["connections"] = []
            for conn in conns:
                results["connections"].append(
                    {
                        "fd": conn.fd,
                        "family": conn.family.name,
                        "type": conn.type.name,
                        "local_address": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "remote_address": (
                            f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                        ),
                        "status": conn.status,
                        "pid": conn.pid,
                        "process_name": _get_proc_name(conn.pid),
                    }
                )
    except psutil.AccessDenied:
        results["error"] = "Access denied to retrieve network information. Try running with higher privileges."
    except Exception as e:
        results["error"] = str(e)

    # NEW: Interface Logic
    if check_interfaces:
        results["interfaces"] = {}
        try:
            addrs = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            
            for iface, addr_list in addrs.items():
                is_up = stats[iface].isup if iface in stats else "Unknown"
                speed = stats[iface].speed if iface in stats else 0
                
                ipv4 = [a.address for a in addr_list if a.family == socket.AF_INET]
                ipv6 = [a.address for a in addr_list if a.family == socket.AF_INET6]
                
                results["interfaces"][iface] = {
                    "status": "UP" if is_up else "DOWN",
                    "speed_mbps": speed,
                    "ipv4": ipv4,
                    "ipv6": ipv6
                }
        except Exception as e:
            results["interfaces_error"] = str(e)

    # NEW: Basic Routing (Gateway)
    if check_routing:
        results["routing"] = {}
        try:
            # Simple hack to find the interface used for internet
            # Does not ping, just checks kernel routing table preference
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0)
            try:
                s.connect(('8.8.8.8', 1)) 
                local_ip = s.getsockname()[0]
                results["routing"]["default_route_interface_ip"] = local_ip
            except Exception:
                results["routing"]["error"] = "No route to internet (8.8.8.8)"
            finally:
                s.close()
        except Exception as e:
            results["routing"]["error"] = f"Routing check failed: {e}"

    if not results:
        results["info"] = "No checks requested or all failed."

    return results


def _get_proc_name(pid: int) -> str:
    """Helper to resolve PID to process name safely."""
    if not pid:
        return "N/A"
    try:
        return psutil.Process(pid).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return "Unknown"
