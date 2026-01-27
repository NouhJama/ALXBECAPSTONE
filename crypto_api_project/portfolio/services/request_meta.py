import ipaddress

def get_client_ip(request):
    import ipaddress

def get_client_ip(request):
    """
    Try to get the real client IP address in a proxy-friendly way.
    Order of preference:
      1) X-Real-IP (common with Nginx)
      2) X-Forwarded-For (common with proxies/load balancers)
      3) REMOTE_ADDR (direct connection)

    """

    def is_valid_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False
        
    # Check X-Real-IP header
    x_real_ip = request.META.get("HTTP_X_REAL_IP")
    if x_real_ip and is_valid_ip(x_real_ip):
        return x_real_ip
    
    # Check X-Forwarded-For header
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        # X-Forwarded-For can contain multiple IPs, the first one is the client IP
        ip_list = [ip.strip() for ip in x_forwarded_for.split(",")]
        for ip in ip_list:
            if is_valid_ip(ip):
                return ip
    
    # Fallback to REMOTE_ADDR
    remote_addr = request.META.get("REMOTE_ADDR")
    if remote_addr and is_valid_ip(remote_addr):
        return remote_addr
    
    # If all else fails, return a default value
    return "0.0.0.0"