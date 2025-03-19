from sensors.shake_sensor import shake_game

def main(): 
    while True:
        print("Select game choice: ")
        print("1. Shake Game")

        choice = input("Enter: ")

        if (choice == '1'): 
            shake_game()
        else:
            print("Invalid Choice")

if __name__ == "__main__":
    main()