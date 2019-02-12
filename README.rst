======
pcdhit
======
A Python interface to the cd-hit clustering program.


Basic Usage
===========
Given a collection of redundant biological sequence records (an iterable of
(header, sequence) tuples) and an identity threshold,
the **filter** function returns an iterable of non-redundant records::

  >>> import pcdhit
  >>> filtered_records = pcdhit.filter(records, thr=0.9)
  >>> next(filtered_records)
  ('A0A024W598_PLAFA/13-174', 'KLVFLGEQAVGKTSIITRFMYDTFDNNYQSTIGIDFLSKTLYLDEGPVRLQLWDTAGQERFRSLIPSYIRDSAAAIVVYDITNRQSFENTTKWIQDILNERGKDVIIALVGNKTDLGDLRKVTYEEGMQKAQEYNTMFHETSAKAGHNIKVLFKKIASKL--')
  >>> next(filtered_records)
  ('RAA5E_ARATH/14-175', 'KIVVIGDSAVGKSNLLSRYARNEFSANSKATIGVEFQTQSMEIEGKEVKAQIWDTAGQERFRAVTSAYYRGAVGALVVYDITRRTTFESVGRWLDELKIHSDTTVARMLVGNKCDLENIRAVSVEEGKALAEEEGLFFVETSALDSTNVKTAFEMVILDIY-')

The non-redundant records are parsed from the cd-hit output file::

  $ cdhit -i <redundant_alignment> -o <non_redundant_alignment> -c <identity_threshold>


  
