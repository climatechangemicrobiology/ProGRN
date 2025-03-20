class Helper:

    @staticmethod
    def strnames(n, nametype = 'o'):
        if nametype == 'p':
            return str(n) + (' patient' if n == 1 else ' patients')
        elif nametype == 'o':
            return str(n) + (' occurence' if n == 1 else ' occurences')

    @staticmethod
    def stredges(n):
        return str(n) + (' edge' if n == 1 else ' edges')

    @staticmethod
    def strpercent(n, m):
        pc = n*100.0/m
        return str(round(pc, 3) if pc < 0.01 else round(pc, 2)) + '%'
    
    @staticmethod
    def whitish(c):
        k = 220
        return c[0] > k and c[1] > k and c[2] > k