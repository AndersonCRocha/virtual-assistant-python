from Assistant import Assistant


if __name__ == '__main__':
    assintant = Assistant()

    print('Olá, sou o assistence virtual Ted!\n')
    
    while(True):
        try:
            assintant.init()
        except KeyboardInterrupt:
            print('Finalizando.')
            quit()
