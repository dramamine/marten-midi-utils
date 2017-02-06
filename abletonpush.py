# Ableton Push Basic MIDI Implementation.pdf
# https://app.box.com/s/w900ll2tq3tj83raes2a
#
class AbletonPush:
  midiin = None
  midiout = None
  def __init__(self, Output, Input):
    # assume these are open
    self.midiin = Input
    self.midiout = Output

  def clearDisplayLine(self, line):
    idx = 28 + line
    msg = [240, 71, 127, 21, idx, 0, 0, 247]
    self.midiout.send_message(msg)

  def set_display_line(self, line, str):
    msg = [240, 71, 127, 21, 24, 0, 69, 0] + self.get_bytes(str) + [247]
    print "my msg:", msg
    self.midiout.send_message(msg)

  def clearDisplay(self):
    # TODO map
    for i in range(0,3):
      self.clearDisplayLine(i)

  def get_bytes(self, str):
    bytes = []
    for c in str:
      bytes.append(int(c.encode('hex'), 16))
    # print "chars?", len(bytes)
    # pad to 68
    while len(bytes) < 68:
      bytes.append(30)
    return bytes