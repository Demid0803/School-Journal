# Создать базовый класс Figure, 
# сделать в котором будет конструктор, 
# square, perimetr. После этого создать классы 
# наследники и переопредлить для них эти 
# методы (Rectangle, Triangle, Cirlce)


class Figure:
    def __init__(self, square, perimetr) -> None:
        a_i = int(input())
        b_i = int(input())
        self.a = a_i
        self.b = b_i
        return a_i, b_i

    def Restangle(square, perimetr, a, b):
        square = a * b
        perimetr = (a + b) * 2
        return square, perimetr