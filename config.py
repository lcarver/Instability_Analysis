import os
class cf:
  def __init__(self):
    self.t1 = '2016-05-18 01:03:00.000'
    self.t2 = '2016-05-18 01:38:00.000'

    self.filln = 4938
    self.tag = '_HT'
    self.output_path = os.path.join('/afs/cern.ch/work/l/lcarver/public/Instability_Data','{:d}{:s}'.format(self.filln, self.tag))

    #For SUSSIX
    self.q1 = 0.27
    self.q2 = 0.295
    #
