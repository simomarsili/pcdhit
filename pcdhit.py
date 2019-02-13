import logging
import pkg_resources
from functools import wraps
import lilbio

project_name = 'pcdhit'
__version__ = pkg_resources.require(project_name)[0].version
__copyright__ = 'Copyright (C) 2019 Simone Marsili'
__license__ = 'BSD 3 clause'
__author__ = 'Simone Marsili <simo.marsili@gmail.com>'
__all__ = ['filter']


logger = logging.getLogger(__name__)


class PcdhitError(Exception):
    """Base class for pcdhit exceptions."""


class CdhitNotFoundError(PcdhitError):
    """cdhit not installed."""

    def __init__(self):
        message = 'check if cd-hit is installed.'
        super().__init__(message)


class CdhitCommandError(PcdhitError):
    """cdhit command failed."""


class IdentityThresholdError(PcdhitError):
    """ValueError for identity threshold."""

    def __init__(self):
        message = 'valid values are 0.7 <= thr <= 1.0'
        super().__init__(message)


def timeit(func):
    """Timeit decorator."""
    @wraps(func)
    def timed(*args, **kwargs):
        import time
        ts0 = time.time()
        result = func(*args, **kwargs)
        ts1 = time.time()
        logger.debug('%r: %2.4f secs', func, ts1 - ts0)
        return result
    return timed


def is_command(cmds):
    """Given a command returns its path, or None.
    Given a list of commands returns the first recoverable path, or None.
    """
    try:
        from shutil import which as which  # python3 only
    except ImportError:
        from distutils.spawn import find_executable as which

    if isinstance(cmds, str):
        return which(cmds)
    else:
        for cmd in cmds:
            path = which(cmd)
            if path is not None:
                return path
        return path


def opentf():
    import tempfile
    tempfile = tempfile.NamedTemporaryFile
    kwargs = {'delete': True,
              'mode': 'r+'}
    return tempfile(**kwargs)


@timeit
def print_input_fasta(records, f):
    # write cd-hit input
    for rec in records:
        head, seq = rec
        # store the original sequence in the header
        head = '@'.join([head, ''.join(seq)])
        seq = ''.join([c for c in seq if c != '-'])
        # remove gaps (cdhit takes unaligned sequences as input)
        # use 'X' as a placeholder
        print('>%s\n%s' % (head, seq), file=f)
    f.flush()


@timeit
def call_cdhit(cdhit_exe, fin, fout, threshold):
    import subprocess
    command = '%s -i %s -o %s -c %s' % (cdhit_exe, fin.name, fout.name,
                                        threshold)
    returncode = subprocess.Popen(command, shell=True).wait()
    if returncode != 0:
        raise CdhitCommandError


@timeit
def filter(records, threshold):
    """Filter non-redundant records via cd-hit.

    cdhit: http://weizhongli-lab.org/cd-hit/
    cdhit will cluster sequences that meet a similarity threshold and return a
    representative record for each cluster:
    cdhit -i <fin> -c <threshold> -o <fout>

    Parameters
    ----------
    records : iterable
        Iterable of (header, sequence) tuples.

    threshold : float, optional (0.9)
        Sequence identity threshold (cd-hit '-c <thr>' option).

    Yields
    ------
    (header, sequence) : tuple (str, str)
        For each non-redundant record, a tuple containing header and sequence.

    """

    # check for cd-hit on path
    cdhit_exe = is_command(['cd-hit', 'cdhit'])
    logger.debug('cd-hit executable: %r', cdhit_exe)
    if cdhit_exe is None:
        raise CdhitNotFoundError

    if not 0.7 <= threshold <= 1.0:
        raise IdentityThresholdError

    # open tmp files
    with opentf() as fin, opentf() as fout:

        print_input_fasta(records, fin)

        call_cdhit(cdhit_exe, fin, fout, threshold)

        for rec in lilbio.parse(fout, fmt='fasta'):
            head, seq = rec[0].split('@')
            yield head, seq
