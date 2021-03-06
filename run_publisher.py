from publisher import observer, event_handler, path
import time

if __name__ == '__main__':
    observer.schedule(event_handler, path = path)
    observer.start()
    print(f'Iniciando a observação do diretório -> {path}')
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
