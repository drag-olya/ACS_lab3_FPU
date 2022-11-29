from Coprocessor_class import Coprocessor


def list2str(l):
    return ''.join(l)


def main():

    c = Coprocessor()

    print('Done by Olha Drahomeretska\nVariant 12.9.1\n')
    print(list2str(['s '] + ['p']*c.P + [' n '] + ['m']*c.M) + ': number in IEEE74 format')
    print(f'{list2str(c.max)}: maximum positive ')
    print(f'{list2str(c.min)}: minimum negative')
    print(f'{list2str(c.min_non_zero)}: minimum positive')
    print(f'{list2str(c.num1_0E0)}: number + 1.0E0')
    print(f'{list2str(c.inf)}: +inf')
    print(f'{list2str(c._inf)}: -inf')
    print(f'{list2str(c.dec2ieee74(0.008))}: non-normilized (0.008)')
    print(f'{list2str(c.NaN)}: NaN value\n')

    print('formula to calculate: 3/4*x + x/y + pi')




main()
