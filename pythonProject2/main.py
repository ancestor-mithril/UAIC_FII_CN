from functions import read_f, dehghan_hajarian


def run():
    f = read_f()
    x = dehghan_hajarian(f)
    print(x)


if __name__ == "__main__":
    run()
