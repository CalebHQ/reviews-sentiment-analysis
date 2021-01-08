from critics import main
from audience import run
from termcolor import colored


def menu():
    print('+==============================+')
    print('|' + ' '*8 + colored('RottenTomatoes', 'red') + ' '*8 + '|')
    print('|' + ' '*6 + colored('Sentiment Analysis', 'green') + ' '*6 + '|')
    print('+==============================+')
    print('+==============================+')
    print('|                              |')
    print('|' + ' '*3 + colored('1. All Audience Analysis', 'blue') + ' '*3 + '|')
    print('|' + ' '*4 + colored('2. All Critic Analysis', 'blue') + ' '*4 + '|')
    print('|' + ' '*11 + colored('q. Leave', 'red') + ' '*11 + '|')
    print('|                              |')
    print('+==============================+')
    print('|' + ' '*6 + colored('Enter your choice!', 'blue') + ' '*6 + '|')
    print('+==============================+')
    print('')


def start():
    choice = input(colored('> ', 'blue'))
    while choice != 'q':
        if choice == '1':
            run()
            break
        elif choice == '2':
            main()
        else:
            print(colored('Invalid', 'red'))
        choice = input(colored('> ', 'blue'))
    print(colored('Goodbye!', 'red'))


if __name__ == '__main__':
    menu()
    start()
