import sys

def add(somthing: str):
    print("something")

if __name__ == "__main__":
    args = sys.argv[1:]

    if(args[0] == 'add'):
        add(args[1])