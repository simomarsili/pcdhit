======
pcdhit
======
Python interface to the cd-hit clustering program.
Given a collection of redundant sequence records,
(an iterable of (header, sequence) tuples) and a sequence identity threshold,
the **filter** function returns an iterable of non-redundant records::

  >>> import pcdhit
  >>> filtered_records = pcdhit.filter(records, thr=0.9)

In practice, the function dumps the redundant records in a fasta alignment,
run cd-hit::

  $ cdhit -i <redundant_fasta> -o <non_redundant_fasta> -c <threshold>

via subprocess.Popen and parse the non-redundant records from the
cd-hit output file.
