import argparse
import math

# consts
DEFAULT_C_PERIOD = 428 # check freq by period / 428 * 261.626
DEFAULT_C_FREQ = 261.626
FINETUNE_STEP = math.pow(2, 12.5 / 1200)

class PeriodTableWriter:
    def __init__(self, edosteps: int, cOffset: int, afreq: float = 440):
        self.edosteps = edosteps
        self.cOffset = cOffset
        self.afreq = afreq
        self.adJustedCNoteFreq = afreq / math.pow(2, cOffset / edosteps)

    def calcPeriodForNote(self, step: int, finetune: int, octave: int):
        noteFreq = self.adJustedCNoteFreq * math.pow(2, step / self.edosteps) * math.pow(2, octave) * math.pow(FINETUNE_STEP, finetune)
        return round(DEFAULT_C_PERIOD * DEFAULT_C_FREQ / noteFreq)

    def generateThreeRows(self, finetune: int):
        rslt = f'// finetune {finetune}'
        if finetune == 0:
            rslt += ' (no finetuning)'

        rslt += '\n'
        for octave in (-1, 0, 1):
            for note in range(self.edosteps):
                rslt += f'{self.calcPeriodForNote(note, finetune, octave)},'

            if octave == 1:
                rslt += '0,'
            rslt += '\n'

        return rslt

    def generateFrequenciesForEdo(self):
        rslt = ''
        for pos in range(8):
            rslt += self.generateThreeRows(pos)
            rslt += '\n'

        for neg in range(-8, 0):
            rslt += self.generateThreeRows(neg)
            rslt += '\n'

        return rslt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'Generate c arrays of pal amiga periods for a specified edo')
    parser.add_argument('--steps', type=int)
    parser.add_argument('--coffset', help='Offset from C to A. Since Protracker\'s base frequency is C, A is divided by this interval to get it.', type=int)
    parser.add_argument('--afreq', type=float, default=440)
    args = parser.parse_args()
    print(args.steps, args.coffset, args.afreq)
    writer = PeriodTableWriter(args.steps, args.coffset, args.afreq)
    print(writer.generateFrequenciesForEdo())
