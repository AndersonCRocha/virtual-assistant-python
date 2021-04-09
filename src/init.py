from Assistant import Assistant


if __name__ == '__main__':
    assintant = Assistant()

    print('Olá, sou o assistence virtual Jubileu!\n')
    
    while(True):
        try:
            assintant.init()
        except KeyboardInterrupt:
            print('Finalizando.')
            quit()
