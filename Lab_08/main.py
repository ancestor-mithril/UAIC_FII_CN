from functions import read_f, dehghan_hajarian


def run():
    f = read_f()
    while True:
        x = dehghan_hajarian(f)
        if x is None:
            continue
        print(x)
        if 3.41 < x < 3.42:
            break


if __name__ == "__main__":
    run()
