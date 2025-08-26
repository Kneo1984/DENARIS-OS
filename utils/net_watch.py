# ===============================================
# NetWatch  Netzwerküberwachung für DENARIS OS
# ===============================================
import threading, time, logging, psutil

class NetWatch:
    def __init__(self, config=None, alert_callback=None):
        self.cfg = config or {}
        self.cb = alert_callback
        self.running = False
        self.known = set()
        self.log = logging.getLogger("denaris.net_watch")
        self.interval = int(self.cfg.get("interval", 5))
        self.suspicious_ports = set(self.cfg.get("suspicious_ports", []))
        self.ignore_loopback = bool(self.cfg.get("ignore_local_loopback", True))
        self.only_alert_suspicious = bool(self.cfg.get("only_alert_suspicious", False))
        self.whitelist_ips = set(self.cfg.get("whitelist_ips", []))

    def _is_loopback(self, ip):
        return ip.startswith("127.") or ip == "::1"

    def _is_whitelisted(self, ip):
        return ip in self.whitelist_ips

    def _scan(self):
        current = set()
        for c in psutil.net_connections(kind="inet"):
            if not (c.laddr and c.raddr): 
                continue
            if c.status != psutil.CONN_ESTABLISHED:
                continue
            src_ip, src_port = c.laddr
            dst_ip, dst_port = c.raddr
            entry = (src_ip, src_port, dst_ip, dst_port)
            current.add(entry)
            if entry not in self.known:
                if self.ignore_loopback and (self._is_loopback(src_ip) or self._is_loopback(dst_ip)):
                    continue
                if self._is_whitelisted(dst_ip) or self._is_whitelisted(src_ip):
                    continue
                if self.only_alert_suspicious and (dst_port not in self.suspicious_ports and src_port not in self.suspicious_ports):
                    continue
                msg = f"Neue Verbindung: {src_ip}:{src_port}  {dst_ip}:{dst_port}"
                self.log.info(msg)
                if self.cb:
                    try: self.cb(msg)
                    except Exception: pass
        self.known = current

    def _loop(self):
        self.log.info("NetWatch gestartet (Intervall %ss)", self.interval)
        while self.running:
            try: self._scan()
            except Exception as e: self.log.exception("Scan-Fehler: %s", e)
            time.sleep(self.interval)

    def start(self):
        if self.running: return
        self.running = True
        t = threading.Thread(target=self._loop, daemon=True)
        t.start()

    def stop(self):
        self.running = False
        self.log.info("NetWatch gestoppt.")

def start_monitor_in_background(config=None, alert_callback=None):
    nw = NetWatch(config=config, alert_callback=alert_callback)
    nw.start()
    return nw
