"""Hack assembler (Nand to Tetris, Project 6).
Extra feature (K=87, K mod 3 = 0): writes all labels and variables
with their addresses to symbols.txt.

Usage: python assembler.py Prog.asm   ->  Prog.hack + symbols.txt
"""
import sys

COMP = {
    '0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100',
    'A': '0110000', '!D': '0001101', '!A': '0110001', '-D': '0001111',
    '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
    'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
    'D&A': '0000000', 'D|A': '0010101',
    'M': '1110000', '!M': '1110001', '-M': '1110011', 'M+1': '1110111',
    'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
    'D&M': '1000000', 'D|M': '1010101',
}
DEST = {'': '000', 'M': '001', 'D': '010', 'MD': '011',
        'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}
JUMP = {'': '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011',
        'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

def predefined():
    t = {'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
         'SCREEN': 16384, 'KBD': 24576}
    for i in range(16):
        t['R%d' % i] = i
    return t

def clean(line):
    return line.split('//')[0].replace(' ', '').replace('\t', '').strip()

def assemble(path):
    with open(path) as f:
        raw = f.readlines()
    symbols = predefined()
    builtin = set(symbols)
    # ---------- First pass: labels ----------
    lines, rom = [], 0
    for text in raw:
        s = clean(text)
        if not s:
            continue
        if s.startswith('('):
            label = s[1:-1]
            symbols[label] = rom          # label = address of NEXT instruction
        else:
            lines.append(s)
            rom += 1
    # ---------- Second pass: translate ----------
    out, next_var = [], 16
    for s in lines:
        if s.startswith('@'):
            v = s[1:]
            if v.isdigit():
                n = int(v)
            else:
                if v not in symbols:      # new variable
                    symbols[v] = next_var
                    next_var += 1
                n = symbols[v]
            out.append(format(n, '016b'))
        else:
            dest, jump = '', ''
            if '=' in s:
                dest, s = s.split('=', 1)
            if ';' in s:
                s, jump = s.split(';', 1)
            out.append('111' + COMP[s] + DEST[dest] + JUMP[jump])
    base = path.rsplit('.', 1)[0]
    with open(base + '.hack', 'w') as f:
        f.write('\n'.join(out) + '\n')
    # ---------- Extra feature: symbols.txt ----------
    with open('symbols.txt', 'w') as f:
        for name, addr in sorted(symbols.items(), key=lambda kv: kv[1]):
            if name not in builtin:
                f.write('%s\t%d\n' % (name, addr))
    return out

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Usage: python assembler.py File.asm')
    assemble(sys.argv[1])
