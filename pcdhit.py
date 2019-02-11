import logging
import lilbio

logger = logging.getLogger(__name__)


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
    """Indices of non-redundant records from cd-hit output.

    cdhit: http://weizhongli-lab.org/cd-hit/
    cdhot will cluster sequences that meet a similarity threshold. Record
    indices contain a representative record for each cluster.

    Parameters
    ----------
    seqs : iterable
        Sequence strings.

    thr : float, optional (0.9)
        Sequence identity threshold (cd-hit '-c <thr>' option).

    Returns
    -------
    (records, positions) : tuple
        records: indices of non-redundant records.

    """
    import subprocess

    # check for cd-hit on path
    cdhit_exe = is_command(['cd-hit', 'cdhit'])
    if cdhit_exe is None:
        logging.error('cd-hit not found. Redundant records wont be filtered.')

    if not 0.7 <= thr <= 1.0:
        raise ValueError(
            'Identity threshold should be in the [0.7,1.0] interval.')

    # open tmp files
    with opentf() as fpi, opentf() as fpo:
        # remove gaps (cdhit takes unaligned sequences as input)
        nrec = 0
        for rec in records:
            head, seq = rec
            seq = ''.join(seq)
            print('>%s\n%s' % (head, seq.replace('-', 'X')),
                  file=fpi)
            nrec += 1
        fpi.flush()

        # run cd-hit
        subprocess.call('%s -i %s -o %s -c %s > cdhit.log' %
                        (cdhit_exe, fpi.name, fpo.name, thr),
                        shell=True)
        fpo.flush()

        # indices of non-redundant records from cdhit output headers
        for rec in lilbio.parse(fpo, fmt='fasta'):
            head, seq = rec
            yield head, seq.replace('X', '-')
