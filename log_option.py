from modules import api, log

if __name__ == '__main__':
    api.initialize()
    api.updateTokensAutomatic()
    log.startAutomatic()
