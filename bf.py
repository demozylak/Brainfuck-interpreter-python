from Core import input, output, source, memory, log
from Core import interpreter
from Core import version

import logging
import argparse

#argument parsing
parser = argparse.ArgumentParser(description="Commandline Brainfuck interpreter", 
            epilog="https://github.com/demozylak/Brainfuck-interpreter-python", 
            formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("file", metavar='FILE', type=argparse.FileType('r'), 
                        help="brainfuck source file to be interpreted")
parser.add_argument('--version', action='version', 
                        version='%(prog)s {version}'.format(version=version.__version__))
parser.add_argument('-r', '--read-from', dest='input_file', metavar='INPUT_FILE', 
                        type=argparse.FileType('r'), 
                        help="input file for brainfuck program") 
parser.add_argument('-i', '--input', dest='input_string', metavar='INPUT',
                        nargs='?', const='', help="input string for brainfuck program") 
parser.add_argument('-w', '--wrap', type=int, dest='wrap', metavar='MAXINT',
                        help="Wrap memory at specified size\nWithout flag wraps at 256\nSpecify -1 for no wrapping") 
parser.add_argument('-s', '--size', type=int, dest='size', metavar='SIZE',
                        help="Specify max memory size\nWithout argument memory is dynamic ( limited only by machine RAM )") 
parser.add_argument("-v", "--verbosity", dest='verbosity', action="count",
                    help="Increase logging verbosity ( add more v-s for more output )")

args = parser.parse_args()


# ** Arguments interpreting **

#Logging
if(args.verbosity == None):
    log.LogSetLevel(logging.CRITICAL)
elif(args.verbosity == 1):
    log.LogSetLevel(logging.INFO)
else:
    log.LogSetLevel(logging.DEBUG)

#Source
s = source.FileSource(args.file)

#Input
if(args.input_file != None):
    i = input.StringInput(args.input_file.read())
elif(args.input_string != None):
    i = input.StringInput(args.input_string)
else:
    i = input.StdinInput()

#Output
o = output.StdinOutput()

#Memory
if(args.wrap != None):
    if(args.wrap == -1):
        mem_wrap = False
    else:
        mem_wrap = True
        mem_maxint = args.wrap
else:
    mem_wrap = True
    mem_maxint = 256

if(args.size == None):
    mem_size = -1
else:
    mem_size = args.size
m = memory.Memory(size=mem_size, wrap=mem_wrap, maxint=mem_maxint)


#Run the interpreter
interpreter.Interpreter(s, i, o, m).run()

