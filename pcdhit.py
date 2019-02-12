import logging
import lilbio

logging.basicConfig(
    # filename=<filename>,
    # filemode='a',
    format='%(module)-10s %(funcName)-20s: %(levelname)-8s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class PcdhitError(Exception):
    """Base class for pcdhit exceptions."""


class CdhitNotFoundError(PcdhitError):
    """cdhit not installed."""

    def __init__(self):
        message = 'check if cd-hit is installed.'
        super.__init__(message)


class IdentityThresholdError(PcdhitError):
    """ValueError for identity threshold."""

    def __init__(self):
        message = 'valid values are 0.7 <= thr <= 1.0'
        super.__init__(message)


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


def filter(records, thr=0.9):
    """Return non-redundant records from cd-hit output.

    cdhit: http://weizhongli-lab.org/cd-hit/
    cdhit will cluster sequences that meet a similarity threshold and return a
    representative record for each cluster:
    cdhit -i <fin> -c <thr> -o <fout>

    Parameters
    ----------
    records : iterable
        Iterable of (header, sequence) tuples.

    thr : float, optional (0.9)
        Sequence identity threshold (cd-hit '-c <thr>' option).

    Yields
    ------
    (header, sequence) : tuple (str, str)
        For each non-redundant record, a tuple containing header and sequence.

    """
    import subprocess

    # check for cd-hit on path
    cdhit_exe = is_command(['cd-hit', 'cdhit'])
    logger.debug('cd-hit executable: %r', cdhit_exe)
    if cdhit_exe is None:
        raise CdhitNotFoundError

    if not 0.7 <= thr <= 1.0:
        raise IdentityThresholdError

    # open tmp files
    with opentf() as fin, opentf() as fout:
        # write cd-hit input
        for rec in records:
            head, seq = rec
            seq = ''.join(seq)
            # remove gaps (cdhit takes unaligned sequences as input)
            # use 'X' as a placeholder
            print('>%s\n%s' % (head, seq.replace('-', 'X')),
                  file=fin)
        fin.flush()

        # run cd-hit
        subprocess.call('%s -i %s -o %s -c %s > cdhit.log' %
                        (cdhit_exe, fin.name, fout.name, thr),
                        shell=True)
        fout.flush()

        for rec in lilbio.parse(fout, fmt='fasta'):
            head, seq = rec
            # put gaps back
            yield head, seq.replace('X', '-')
