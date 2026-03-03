def func(x):
    y = 2.5 * x**3 - 5.7 * x**2 + 7.3 * x - 6.4
    return y


args = []
numpoints = int(input('Количество точек: '))
for i in range(1, numpoints + 1):
    arg = eval(input(f'x{i} = '))
    args.append(arg)

kwargs = {x: func(x) for x in args}
data = '\n'.join(f'{x} {y}' for x, y in kwargs.items())
print(data)
open('args.txt', 'w').write(data)
print('Файл \'args.txt\' записан успешно')