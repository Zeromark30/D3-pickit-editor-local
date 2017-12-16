#!/usr/bin/env python
#
# Upload videos to Youtube from the command-line using APIv3.
#
# Author: Arnau Sanchez <pyarnau@gmail.com>
# Project: https://github.com/tokland/youtube-upload
"""
Download Builds from http://www.diablofans.com/builds/BUILDNUMBER (like 57405)
with the given Buildnumber.
And stores them into output/*.ini for TurboHUD.
    $ pickit-cl --use-number-file --fourthree=4 --buildtype="full"
"""
import os
import sys
import optparse

import urllib.request as urllib2
import lib.pickit_cl_ori_py3 as pickit_cl_ori

import re

abs_dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, abs_dir_path)
# print(sys.path)


class OptionsError(Exception):
    pass


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
        pick = pickit_cl_ori.main(
            buildnumber=buildnumber,
            fourthree=options.fourthree,
            buildtype=options.buildtype)
        pickitList_list.append(pick)
    if options.onefile:
        builds_string = "\n".join(pickitList_list)
        pickit_cl_ori.write_output(
            buildnumber='builds',
            buildtype=options.buildtype,
            pickitList=builds_string)
    else:
        for buildnumber in build_numbers:
            pickit_cl_ori.write_output(
                buildnumber=buildnumber,
                buildtype=options.buildtype,
                pickitList=pickitList_list)


def parse_options_error(parser, options, args):
    """Check errors in options."""
    required_options = []
    missing = [opt for opt in required_options if not getattr(options, opt)]
    if missing:
        parser.print_usage()
        msg = "Some required option are missing: {0}".format(
            ", ".join(missing))
        raise OptionsError(msg)


def run_main(parser, options, args, output=sys.stdout):
    """Run the main scripts from the parsed options/args.
       It read in buildnumbers from args or from the build_numbers.txt file.
       And checks if the Builds for them exists on the site."""
    parse_options_error(parser, options, args)
    # args = '53544'
    # print("args: {}".format(args))
    build_numbers = []
    if options.use_number_file:
        pattern = re.compile('([^#]*)(#)(.*)')
        with open('{}'.format(options.number_file), 'r') as number_file:
            splited = str(number_file.read()).split('\n')
            print('splited: {}'.format(splited))
            for string in splited:
                f = pattern.findall(string)
                if len(f) is 0:
                    build_numbers.append(string.strip())
                else:
                    print("f[0][0]: {}".format(f[0][0]))
                    build_numbers.append(f[0][0].strip())

    else:
        for string in args:
            build_numbers.append(string.strip())

    # print(build_numbers)
    for index, buildnumber in enumerate(build_numbers):
        try:
                url = 'http://www.diablofans.com/builds/{}'.format(buildnumber)
                urllib2.urlopen(url)
        except urllib2.URLError:
            raise('Url not found check build number {}'.format(buildnumber))
        except Exception:
            raise('Exception: {}'.format(Exception))

        # removes empty elements
        for index, string in enumerate(build_numbers):
            if len(string) is 0:
                build_numbers.remove('')

    if len(build_numbers) is 0:
        raise OptionsError("No existing Buildnumbers given.")
    print('build_numbers: {}'.format(build_numbers))

    run_pickit(build_numbers, options, args)


def main(arguments):
    """Define the usage and the options. And then parses the given \
     options/args and give this to run_main()."""

    usage = """Usage: %prog [OPTIONS] BUILDNUMBER [BUILDNUMBER2 ...]

    Download Builds from http://www.diablofans.com/builds/BUILDNUMBER \
    (like 57405) with the given Buildnumber. And stores them into \
    output/*.ini for TurboHUD."""
    parser = optparse.OptionParser(usage=usage)

    parser.add_option(
        '', '--number-file', dest='number_file',
        default='build_numbers.txt',
        help='Path to a file containing a list of Buildnumbers. \
        [build_numbers.txt]')
    parser.add_option(
        '-f', '--use-number-file', action="store_true",
        dest='use_number_file', default=False,
        help=r'Use build_numers.txt as input. [False]')
    parser.add_option(
        '-4', '--fourthree', dest='fourthree', type="int",
        default=3, help='Items must roll with all stats or stats - 1? \n \
        E.G. If a helm needs Socket, CHC, Int, Vit roll with 4 or 3? [3]')
    parser.add_option(
        '-b', '--buildtype', dest='buildtype', metavar="STRING",
        default="build",
        help=r'Full file or just the build? (Full\Build) [Build]')
    parser.add_option(
        '-s', '--severalfiles',
        action="store_false", dest='onefile',
        default=True, help=r'Write all Builds in several Files. Default is just\
         one File. [True]')

    # Fixes bug for the .exe in windows: The help will be displayed, when no
    # arguments are given.
    if len(arguments) == 0:
        parser.print_help()
        return 0

    options, args = parser.parse_args(arguments)
    options.buildtype = options.buildtype.lower()

    # print(options)

    run_main(parser, options, args)


def run():
    sys.exit(catch_exceptions(EXIT_CODES, main, sys.argv[1:]))


if __name__ == '__main__':
    run()
