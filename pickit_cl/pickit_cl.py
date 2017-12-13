#!/usr/bin/env python
# 
# Upload videos to Youtube from the command-line using APIv3.
#
# Author: Arnau Sanchez <pyarnau@gmail.com>
# Project: https://github.com/tokland/youtube-upload
"""
Upload all videos in given folder to Youtube from the command-line which.

    $ pickit-cl --endingse="mp4, mpg" \
                     --description="Anne Sophie Mutter plays Beethoven" \
                     --category=Music \
                     --tags="mutter, beethoven" \
                     IDs.txt
"""
import os
import sys
from pathlib import Path
import optparse
from youtube_upload import lib
#from urllib.request import urlopen
#from urllib.request import URLError
try:
    import urllib2
    import lib.pickit_cl_ori_py2 as pickit_cl_ori
except ImportError:
    import urllib.request as urllib2
    import lib.pickit_cl_ori_py3 as pickit_cl_ori

import time



class OptionsError(Exception): pass

EXIT_CODES = {
    OptionsError: 2,
    NotImplementedError: 5,
}

def debug(obj, fd=sys.stderr):
    """Write obj to standard error."""
    print(obj, file=fd)

def catch_exceptions(exit_codes, fun, *args, **kwargs):
    """
    Catch exceptions on fun(*args, **kwargs) and return the exit code specified
    in the exit_codes dictionary. Return 0 if no exception is raised.
    """
    try:
        fun(*args, **kwargs)
        return 0
    except tuple(exit_codes.keys()) as exc:
        debug("[{0}] {1}".format(exc.__class__.__name__, exc))
        return exit_codes[exc.__class__]

def run_pickit(build_numbers, options, args):
    """Parse all files in file_list by using tokland/youtube-upload script."""
    pickitList_list = []
    for buildnumber in build_numbers:
        string = ""
        pickitList_list.append(pickit_cl_ori.main(buildnumber=buildnumber, fourthree=options.fourthree, buildtype=options.buildtype))
        
    if options.onefile:
        builds_string = "\n".join(pickitList_list)
        pickit_cl_ori.write_output(buildnumber='builds', buildtype=options.buildtype, pickitList=builds_string)
    else:
        for buildnumber in build_numbers:
            pickit_cl_ori.write_output(buildnumber=buildnumber, buildtype=options.buildtype, pickitList=pickitList)
        
def parse_options_error(parser, options, args):
    """Check errors in options."""
    required_options = []
    missing = [opt for opt in required_options if not getattr(options, opt)]
    if missing:
        parser.print_usage()
        msg = "Some required option are missing: {0}".format(", ".join(missing))
        raise OptionsError(msg)
        
        
def run_main(parser, options, args, output=sys.stdout):
    """Run the main scripts from the parsed options/args.
       And checks if the given folders exists beforehand."""
    parse_options_error(parser, options, args)
    #args = '53544'
    #print("args: {}".format(args))
    
    build_numbers = []
    if options.use_number_file:
        with open('{}'.format(options.number_file), 'r') as number_file:
            splited = str(number_file.read()).split('\n')
            for string in splited:
                build_numbers.append(string.strip())

    else:
        for string in args:
            build_numbers.append(string.strip())
    
    #print(build_numbers)
    for index, buildnumber in enumerate(build_numbers):
        try:
                url = 'http://www.diablofans.com/builds/{}'.format(buildnumber)
                page = urllib2.urlopen(url)
        except urllib2.URLError:
            raise('Url not found check build number {}'.format(buildnumber))
        except Exception:
            raise('Exception: {}'.format(Exception))
    
    if len(build_numbers) == 0:
        raise OptionsError("No existing Buildnumbers given.")
    
    run_pickit(build_numbers, options, args)

def main(arguments):
    """Define the usage and the options. And then parses the given options/args and give this to run_main()."""
    
    usage = """Usage: %prog [OPTIONS] NUMBER [NUMBER2 ...]

    Uploads all videos in the folders to Youtube."""
    parser = optparse.OptionParser(usage=usage)
    
    parser.add_option('', '--number-file', dest='number_file', 
        default = 'build_numbers.txt', help='Path to the build_numbers.txt')
    parser.add_option('-f', '--use-number-file', action="store_true",dest='use_number_file',
        default=False, help=r'Use build_numers.txt as input.')
    parser.add_option('', '--fourthree', dest='fourthree', type="int", 
        default = 3, help='Items must roll with all stats or stats - 1? \n E.G. If a helm needs Socket, CHC, Int, Vit roll with 4 or 3? \n [4\\3]')
    parser.add_option('-b', '--buildtype', dest='buildtype', metavar="STRING",
        default="build", help=r'Full file or just the build? [Full\Build]')
    parser.add_option('-s', '--severalfiles', action="store_false",dest='onefile',
        default=True, help=r'Write all Builds in several Files. Default is just one File.')

    
    #Fixes bug for the .exe in windows: The help will be displayed, when no arguments are given.
    if len(arguments) == 0:
        parser.print_help()
        return 0
    
    options, args = parser.parse_args(arguments)
    options.buildtype = options.buildtype.lower()   
    
    #print(options)
    
    run_main(parser, options, args)


def run():
    sys.exit(catch_exceptions(EXIT_CODES, main, sys.argv[1:]))
  
if __name__ == '__main__':
    run()