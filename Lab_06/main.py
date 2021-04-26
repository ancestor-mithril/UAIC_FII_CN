from functions import get_function_domain, spline_interpolation, min_squares_interpolation, function_2, function_2_d


def run():
    x = get_function_domain()
    min_squares_interpolation(x, f=function_2, df=function_2_d)
    spline_interpolation(x, f=function_2, df=function_2_d)


if __name__ == "__main__":
    run()


