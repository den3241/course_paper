args = []
func = input('y = ')

i = 0
while True:
    i += 1
    arg = input(f'x{i} = ')

    if not arg or arg.isalpha():
        break

    args.append(arg)

kwargs = {eval(x): eval(func.replace('x', x)) for x in args}
data = '\n'.join(f'{x} {y}' for x, y in kwargs.items())
print(data)
open('args.txt', 'w').write(data)
print('Файл \'args.txt\' записан успешно')