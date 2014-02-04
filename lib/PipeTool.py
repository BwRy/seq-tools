
import sys
from argparse import ArgumentParser, FileType

# A Unix-style pipe tool, which reads from stdin if it is not a
# tty-like device or optionally from a provided file and accepts
# switches.

class PipeTool():
    
    def __init__(self, description):
        self.description = description
        self._initializeOptParser()
        
    def _initializeOptParser(self):
        self.argParser = ArgumentParser(description = self.description)
        
        self.argParser.add_argument('-f', '--file', nargs='?',
                                    type = FileType('r'), default=sys.stdin,
                                    help='read input from the provided file')

        self.argParser.add_argument('-o', '--out', nargs='?', type=
                                    FileType('w'), default=sys.stdout,
                                    help = 'write output to provided file')

        self.argParser.add_argument('-e', '--echo', action='store_true',
            help="""echo input. This is useful to find out where the
            output generated by each line of input begins and where it
            ends.""")
    
    def run(self):
        """ Run the pipe tool. Call this function once all additional
        arguments have been provided """
        self._parseCommandLine()

        if self.args.file != sys.stdin or not sys.stdin.isatty():
            self._processStream()
        else:
            self._usage()
    
    def output(self, s):
        self.args.out.write(s)

    def _parseCommandLine(self):
        self.args = self.argParser.parse_args()
        
    
    def _processStream(self):
        self.streamStart()
        for line in self.args.file:
            if self.args.echo: print '#> ' + line,
            self.processLine(line.rstrip())
        self.streamEnd()

    def processLine(self, line):
        """ This function is called for each line read from the input
        source. Note that the newline character has already been
        removed when the function is called. Override this method to
        implement your tool"""
        pass

    def streamStart(self):
        """ Called when before reading the first item from the
        stream. Override."""
        pass
            
    def streamEnd(self):
        """ Called after reading the last item from the
        stream. Override."""
        pass

    def _usage(self):
        self.argParser.print_help()

if __name__ == '__main__':
    
    tool = PipeTool("foo")
    tool.run()
    
