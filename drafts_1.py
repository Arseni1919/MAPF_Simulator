import main


if __name__ == '__main__':
    # A function that returns the length of the value:

    def myFunc(e):
        return len(e)


    cars = ['Ford', 'Mitsubishi', 'BMW', 'VW']
    cars.extend(['a', 'b'])
    cars.extend(None)
    cars.sort(key=myFunc)
    print(cars)
    print(cars.pop(0))
    print(cars.pop())

    # ['VW', 'BMW', 'Ford', 'Mitsubishi']
    # VW
    # Mitsubishi
