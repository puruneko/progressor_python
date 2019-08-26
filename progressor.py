
class InOutProgressor():
  '''
  in / outを表示する
  callbackに関数を指定すると、その関数の第一引数にin / outメッセージ文字列をセットして実行する
  [MEMO]
  __init__ -> __enter__ -> impl_in
  phase -+> __enter__ -> impl_in
  enter -+> impl_in
  '''
  def __init__(self, label=None, terminator_in='>', terminator_out='<', terminator_msg='|', spacer='-', callback=None, spacer_increment=2, put_stdout=True):
    self.terminator_in = terminator_in
    self.terminator_out = terminator_out
    self.terminator_msg = terminator_msg
    self.spacer = spacer
    self.callback = callback
    self.spacer_increment = spacer_increment
    self.put_stdout = put_stdout
    self.label = [label] if label is not None else []
    self.depth = len(self.label) - 1
  def __increase(self, label):
    self.depth += 1
    self.label.insert(self.depth, label if label is not None else '')
  def __decrease(self):
    self.label.remove(self.label[self.depth])
    self.depth -= 1
  def phase(self, label=None):
    self.__increase(label)
    return self
  def enter(self, label=None):
    self.__increase(label)
    return self.__impl_in()
  def exit(self):
    self.__impl_out()
  def msg(self, label):
    s = self.spacer * (self.spacer_increment*(self.depth+1))
    label_line = '{s}{tm} {label}'.format(s=s, tm=self.terminator_msg, label=label)
    if self.put_stdout:
      print(label_line)
    if self.callback is not None:
      self.callback(label_line)
    return label_line
  def __impl_in(self):
    s = self.spacer * (self.spacer_increment*(self.depth+1))
    label_line = '{s}{ti} {label}'.format(s=s, ti=self.terminator_in, label=self.label[self.depth])
    if self.put_stdout:
      print(label_line)
    if self.callback is not None:
      self.callback(label_line)
    return label_line
  def __impl_out(self, label=None):
    s = self.spacer * (self.spacer_increment*(self.depth+1))
    label_line = '{to}{s} {label}'.format(s=s, to=self.terminator_out, label=self.label[self.depth])
    if self.put_stdout:
      print(label_line)
    if self.callback is not None:
      self.callback(label_line)
    self.__decrease()
    return label_line
  def __enter__(self):
    self.__impl_in()
    return self
  def __exit__(self, ex_type, ex_value, trace):
    if ex_type is None:
      self.__impl_out()

from logger import MyLogger
if __name__ == '__main__':
  lg = MyLogger()
  with InOutProgressor('level1', callback=lg.log_inf) as pg:
    with pg.phase('test') as pg2:
      pg2.enter('aaaa')
      print('!!!!')
      pg2.exit()