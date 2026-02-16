import psutil


def net_status(check_ports: bool = True, check_connections: bool = True) -> dict:
    """
    Inspects the system's network posture.

    Args:
        check_ports (bool): Whether to check for listening ports.
        check_connections (bool): Whether to check for established connections.

    Returns:
        dict: A dictionary containing network status information.
    """
    results = {"ports": [], "connections": []}

    if not check_ports and not check_connections:
        results["info"] = "No checks requested."
        return results

    try:
        if check_ports:
            # net_connections can also be used to find listening ports
            # status=psutil.CONN_LISTEN
            listeners = [
                conn
                for conn in psutil.net_connections(kind="inet")
                if conn.status == psutil.CONN_LISTEN
            ]
            for conn in listeners:
                results["ports"].append(
                    {
                        "fd": conn.fd,
                        "family": conn.family.name,
                        "type": conn.type.name,
                        "local_address": f"{conn.laddr.ip}:{conn.laddr.port}",
                        "status": conn.status,
                        "pid": conn.pid,
                    }
                )

        if check_connections:
            # Established connections
            conns = [
                conn
                for conn in psutil.net_connections(kind="inet")
                if conn.status == psutil.CONN_ESTABLISHED
            ]
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
                    }
                )
    except psutil.AccessDenied:
        results["error"] = (
            "Access denied to retrieve network information. Try running with higher privileges."
        )
    except Exception as e:
        results["error"] = str(e)

    return results
