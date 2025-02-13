from service import (
    logout, login, register, todo_add
)


def login_page():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    response = login(username, password)
    print(response.message)


def register_page():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    response = register(username, password)
    print(response.message)


def logout_page():
    response = logout()
    print(response.message)


def create_todo():
    title = input("Enter your title: ")
    response = todo_add(title)
    print(response.message)


def menu():
    print('Login       => 1')
    print('Register    => 2')
    print('Logout      => 3')
    print('Todo Create => 4')
    print('Exit        => q')
    return input('Enter your choice: ')


def run():
    while True:
        choice = menu()
        if choice == '1':
            login_page()
        elif choice == '2':
            register_page()
        elif choice == '3':
            logout_page()
        elif choice == '4':
            create_todo()
        elif choice == 'q':
            return
        else:
            print("Invalid choice")


if __name__ == "__main__":
    run()
