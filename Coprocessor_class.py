from math import inf, nan


class Coprocessor:
    P = 12  # bits for characteristic
    M = 9  # bits for mantissa

    def __init__(self):
        self.stack = []
        for _ in range(8):
            self.stack.append(['0 '] + ['0']*self.P + [' 0 '] + ['0']*self.M)

        self._dec_stack = []

        self.BIAS = 2 ** (self.P - 1) - 1
        self.max = ['0', ' '] + ['1'] * (self.P - 1) + ['0'] + [' 1 '] + ['1'] * self.M
        self.min = ['1', ' '] + ['1'] * (self.P - 1) + ['0'] + [' 1 '] + ['0'] * self.M
        self.min_non_zero = ['0', ' '] + ['0'] * (self.P - 1) + ['1'] + [' 1 '] + ['0'] * self.M
        self.num1_0E0 = ['0', ' '] + ['0'] * self.P + [' 0 '] + ['0'] * self.M
        self.inf = ['0', ' '] + ['1'] * self.P + [' 1 '] + ['0'] * self.M
        self._inf = ['1', ' '] + ['1'] * self.P + [' 1 '] + ['0'] * self.M
        self.NaN = ['0', ' '] + ['1'] * self.P + [' 1 '] + ['0'] * self.M

        self.PS = 0  # регістр статусу, може містити лише знак останнього результату
        self.PC = 0  # регістр лічильника команд
        self.TC = 0  # регістр лічильника тактів

    @staticmethod
    def _list2str(l):
        return ''.join(l)

    @staticmethod
    def _dec2bin(x, bits) -> list:
        bin_str = format(x, f'0{bits}b')
        return list(bin_str)

    @staticmethod
    def _bin2dec(x: list) -> int:
        return int(''.join(x), 2)

    @staticmethod
    def _float2bin(x, bits) -> list:
        res = []
        x -= 1
        for _ in range(bits):
            x *= 2
            if x >= 1:
                res.append('1')
                x -= 1
            else:
                res.append('0')
        return res

    def dec2ieee74(self, x: float) -> list:
        sign = ['0']
        q = 0
        if x < 0:
            sign = ['1']
            x = -x
        if x < 1:
            while x < 1:
                x *= 2
            return sign + [' '] + ['0']*self.P + [' 0 '] + self._float2bin(x, self.M)
        while x >= 2:
            q += 1
            x /= 2
        print(f'x  {x}')
        char = self.BIAS + q
        return sign + [' '] + self._dec2bin(char, self.P) + [' 1 '] + self._float2bin(x, self.M)

    def _print_stat(self, com):
        print(f'IR: {com}')
        for i in range(1, 9):
            print(f'R{i}: {self._list2str(self.stack[i-1])}')
        print(f'PS: {self.PS}')
        print(f'PC: {self.PC}')
        print(f'TC: {self.TC}')
        print('**********************************')

    def do_command(self, com: str):
        com = com.split()

        self.TC += 1
        self.PC += 1
        self._print_stat(com)

        try:
            if com[0] == 'mov':
                self.mov(float(com[1]))
            elif com[0] == 'add':
                self.add()
            elif com[0] == 'mult':
                self.mult()
            elif com[0] == 'div':
                self.div()
            else:
                raise Exception('Inappropriate command')

            self.TC += 1
            self._print_stat(com)
            self.TC = 0

        except Exception as err:
            print(str(err))

    def mov(self, x):
        self._dec_stack.append(x)
        for i in range(7, -1, -1):
            self.stack[i] = self.stack[i-1]
        x_ieee74 = self.dec2ieee74(x)
        self.stack[0] = x_ieee74
        self.PS = x_ieee74[0]

    def _refresh_stack(self, x):
        self._dec_stack.append(x)
        x_ieee74 = self.dec2ieee74(x)
        self.stack[0] = x_ieee74
        for i in range(1, 8):
            self.stack[i] = self.stack[i + 1]
        self.PS = x_ieee74[0]
        # check stack

    def div(self):
        x = self._dec_stack.pop()
        y = self._dec_stack.pop()
        # check stack
        if y == 0:
            if x > 0:
                self.stack[0] = self.inf
                self._dec_stack.append(inf)
            if x < 0:
                self.stack[0] = self._inf
                self._dec_stack.append(-inf)
            else:
                self.stack[0] = self.NaN
                self._dec_stack.append(nan)
        else:
            res = x / y
            self._refresh_stack(res)

    def add(self):
        x = self._dec_stack.pop()
        y = self._dec_stack.pop()
        res = x + y
        self._refresh_stack(res)
        # check stack

    def mult(self):
        x = self._dec_stack.pop()
        y = self._dec_stack.pop()
        res = x * y
        self._refresh_stack(res)


copr = Coprocessor()
copr.do_command('mov 3')
copr.do_command('mov 4')
"""
print(copr._list2str(copr.stack[2]))
print(copr._list2str(copr.min))
print(copr._list2str(copr.dec2ieee74(0.008)))
print(copr._list2str(copr.dec2ieee74(-7.3)))
print(copr._list2str(copr.dec2ieee74(2.31)))"""
