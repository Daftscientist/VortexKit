class terminalEffects:
    FINE = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class App:
    def __init__(self, host=None, port=None, secretKey=None):
        if not host and not port:
            print(terminalEffects.FAIL + '[-] No host and port were spesified.' + terminalEffects.ENDC)
            exit()
        if not host:
            print(terminalEffects.FAIL + '[-] No host was spesified.' + terminalEffects.ENDC)
            exit()
        if not port:
            print(terminalEffects.FAIL + '[-] No port was spesified.' + terminalEffects.ENDC)
            exit()
        self.host = host
        self.port = port
        self.secretKey = str(secretKey)
        print(terminalEffects.FINE + '[+] Development server running on http://' + host + ':' + port + terminalEffects.ENDC)
