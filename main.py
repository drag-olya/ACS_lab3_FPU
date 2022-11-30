# Simulation model of a mathematical processor
# Variant 12.9.1
# 12 bits for characteristic
# 9 bits for mantissa
# formula #1: 3/4*x + x/y + pi

from FPU_class import FPU


def list2str(l):
    return ''.join(l)


def main():

    fpu = FPU()

    print('Done by Olha Drahomeretska\nVariant 12.9.1\n')
    print(list2str(['s '] + ['p']*fpu.P + [' n '] + ['m']*fpu.M) + ': number in IEEE74 format')
    print(f'{list2str(fpu.max)}: maximum positive (2 - 2 ^(-{fpu.M})) * 2 ^ {fpu.BIAS}')
    print(f'{list2str(fpu.min)}: minimum negative -(2 - 2 ^(-{fpu.M})) * 2 ^ {fpu.BIAS}')
    print(f'{list2str(fpu.min_non_zero)}: minimum positive 1 * 2 ^ -({fpu.M + fpu.BIAS - 1})')
    print(f'{list2str(fpu.num1_0E0)}: number + 1.0E0')
    print(f'{list2str(fpu.inf)}: +inf')
    print(f'{list2str(fpu._inf)}: -inf')
    print(f'{list2str(fpu.dec2ieee74(0.008))}: non-normilized (0.008)')
    print(f'{list2str(fpu.NaN)}: NaN value\n')

    print('formula to calculate: 3/4*x + x/y + pi\n')

    x = input('Enter x: ')
    y = input('Enter y: ')
    print()

    fpu.do_command('mov pi')
    fpu.do_command(f'mov {y}')
    fpu.do_command(f'mov {x}')
    fpu.do_command('div')
    fpu.do_command('add')
    fpu.do_command(f'mov {x}')
    fpu.do_command('mov 4')
    fpu.do_command('mov 3')
    fpu.do_command('div')
    fpu.do_command('mult')
    fpu.do_command('add')


main()
