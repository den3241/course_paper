""" Импорт библиотек """
from random import randint # Библиотека для получения случайных значений
from numpy import zeros # Библиотека для заполнения массивов
from time import time # Библиотека для получения времени
from itertools import product # Библиотека для упращения работы с перестановками
import matplotlib.pyplot as plt
import numpy


data = {x: y for x, y in (tuple(map(eval, i.split())) for i in open('args.txt', 'r').readlines())}
numpoints = len(data)
x, y = zip(*data.items())
for i in  range(numpoints):
    print(f'x = {x[i]}; y = {y[i]}')

amax = 100
bmax = 100
cmax = 100
amin = -100
bmin = -100
cmin = -100


""" Переменные и массивы """
flag = 0
nmin = 0
nmax = 0
st = time() # Время начала работы программы
numgen = 3 # Количество генов
uzel = 3 # Количество узлов
numchrom = 200000
minnumchrom = (uzel + 1)**numgen # Количество хромосом
print("Минимальное кол-во хромосом для узлов:", minnumchrom)
print('Хромосом задано:', numchrom)
if numchrom < minnumchrom: flag = 1
maxgen = [0] * numgen # Максимальное значение генов
mingen = [0] * numgen # Минимальне значение генов
dg = [0] * numgen # Диапазон генов
pop = zeros((numchrom,numgen)) # Лучшая популяция
popnew = zeros((numchrom,numgen)) # Промежуточная популяция
#максимальное и минимальное значения
for i in range(numgen):
    maxgen[i] = 10000
    mingen[i] = 0
    dg[i] = maxgen[i] - mingen[i]

fitpop = [0] * numchrom


""" Функции """
def fit(num): # Фитнес-функция
    # Вытаскиваем гены из хромосомы
    p = []
    for i in range(numgen): p.append(pop[num][i])
    a = pop[num][0]
    b = pop[num][1]
    c = pop[num][2]
    afact = (amax - amin) * a / dg[0] + amin
    bfact = (bmax - bmin) * b / dg[1] + bmin
    cfact = (cmax - cmin) * c / dg[2] + cmin
    """ ОПРЕДЕЛЕНИЕ ФИТНЕС-ФУНКЦИИ (ГЕНЫ НАХОДЯТСЯ В МАССИВЕ p) """
    summ = 0
    for i in range(numpoints):
        summ = summ + (afact * x[i]**2 + bfact * x[i] + cfact - y[i])**2
    return 10000 - summ

def getfitpop(): # Поиск минимума по популяции
    for i in range(numchrom):
        fitpop[i] = fit(i)

def nachpop(): # Создание начальной популяции
    for i in range(numchrom):
        for j in range(numgen): pop[i][j] = mingen[j] + randint(0,dg[j])
    
    if not flag:
        spisok = [i for i in range(uzel + 1)]
        
        nu = 0
        for i in product(spisok, repeat = numgen):
            for j in range(numgen): pop[nu][j] = int(mingen[j] + ((maxgen[j] - mingen[j]) / uzel) * i[j]) 
            nu += 1

""" Основной код """
e = int(input("Введите количество эпох (единицы): "))
mut = int(input("Введите вероятность мутации (проценты): "))
dmut = int(input("Введите диапозон мутации (проценты): "))
nachpop() # Создание начальной популяции


for z in range(e): # Пробег по эпохам для поиска лучшего значения
    print() # Пропуск строки
    getfitpop()
    
    maxpopp = max(fitpop)
    minpopp = min(fitpop)
    nmax = fitpop.index(maxpopp)
    
    for i in range(numchrom):
        for j in range(numgen): popnew[i][j] = pop[nmax][j] # Переписываем всю попляцию на лучшую хромосому
            
    for i in range(numchrom): # Выживаемость хромосом
        if maxpopp > minpopp: v = (fit(i) - minpopp) * 100 / (maxpopp - minpopp) # Если максимальное значение по полуции больше минимального, то рассчитываем выживаемость хромосомы
        if maxpopp == minpopp: v = 100 # Если популяция выродилась и максимальное значение равно минимальному то выживаемость равна 100
        if randint(0, 100) < v: # Если выживаемость больше рандомного числа то хромосома выживает
            for j in range(numgen): popnew[i][j] = pop[i][j] # Переписываем выжившую хромосому в новую популяцию

    for i in range(numchrom):
        for j in range(numgen): pop[i][j] = popnew[i][j] # Переписываем всю новую популяцию в основную
    
    print(f"Эпоха №{z+1}") # Вывод номера эпохи в консоль
    
    for i in range(numchrom): # Скрещивание (обмен хромосомами)
        ro1 = randint(0, numchrom - 1) # Определяем родителя №1
        ro2 = randint(0, numchrom - 1) # Определяем родителя №2
        rg = randint(0, numgen - 1) # Определяем номер гена для скрещивания
        ob1=pop[ro1][rg]
        ob2=pop[ro2][rg]
        pop[ro1][rg]=ob2
        pop[ro2][rg]=ob1
        
    print(f'Фитнес-функция: {int(maxpopp)}') # Вывод максимальной фитнес функции для текущей эпохи
    
    for i in range (numchrom): # МУТАЦИЯ Пробегаемся по всемм хромосомам
        for j in range(numgen): # Проегаемся по всем генам
            if randint(0, 100) < mut: # Если вероятность мутации больше рандомного числа то происходит мутацияРассчитываем величину мутации (от -dmut до dmut случайным образом)
                dmut1 = dmut - 2 * randint(0, dmut) # Рассчитываем величину мутации (от -dmut до dmut случайным образом)
                m=int(dmut1*pop[i][j]/100)
                if mingen[j] < (pop[i][j] + m) < maxgen[j]: pop[i][j] += m # Произошла мутация в текущей хромосоме
    
    # Вывод данных хромосомы
    # print(f'Хромосома: ', end='')
    # for i in pop[nmax]: print(f'{i}; ', end='')
    # print()

# Вывод лучшего решения
print('-' * 80) # Вывод черты
print("Лучшее решение: ")
getfitpop()
maxpopp = max(fitpop)
indexmax = fitpop.index(maxpopp)
print(f" - Фитнес-функция: {int(maxpopp)}")
print(f' - Хромосома: ', end='')
abest = pop[indexmax][0]
bbest = pop[indexmax][1]
cbest = pop[indexmax][2]
abestfact = (amax - amin) * abest / dg[0] + amin
bbestfact = (bmax - bmin) * bbest / dg[1] + bmin
cbestfact = (cmax - cmin) * cbest / dg[2] + cmin
print('a =', round(abestfact, 1), 'b =', round(bbestfact, 1), 'c =', round(cbestfact, 1))
print()
print() # Пропуск строки
print(f"Время работы программы (секунд): {int(time()-st)}") # Вывод времени работы программы

fig, ax=plt.subplots()
y1 = lambda x: abestfact * x**2 + bbestfact * x + cbestfact
x1 = numpy.linspace(min(x), max(x), 1000)
plt.plot(x1, y1(x1))
plt.scatter(x, y, edgecolors="red", c="red")
plt.show()