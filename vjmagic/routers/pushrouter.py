# from push.listener import PushEventListener
from vjmagic import constants
import rtmidi
from vjmagic.routers.base import Router
from vjmagic.interface import outpututils

class PushRouter(Router):
  encoders = None
  encoder_controller = None

  # TODO probably want singletons for this
  def __init__(self, encoders=None, encoder_controller=None):
    Router.__init__(self, "push input")
    self.encoders = encoders
    self.encoder_controller = encoder_controller
    # setup inputs
    midiinputs = [rtmidi.MidiIn()]
    for idx, device in enumerate(midiinputs[0].get_ports()):
      if "ableton push" in device.lower():
        midiinputs[0].open_port(idx)
        midiinputs[0].set_callback(self.handler)

        midiinputs = [rtmidi.MidiIn()] + midiinputs

    # need this or it gets...garbage-collected?!?
    self.midiinputs = midiinputs

    # setup listeners
    self.listeners.append([[constants.STATUS_CH1, None, None],
      encoders.handle_push_turns, True])

    self.listeners.append([[constants.MIDI_NOTE_ON, None, None],
      self.handle_note_ons, True])

  # this handler's probably in every router
  def handler(self, event, data=None):
    print "AOL handler called"
    (status, data1, data2) = event[0]
    # TODO helpful for debugging
    print self.name, event[0]

    eater = False
    for [lstatus, ldata1, ldata2], cb, eat in self.listeners:
      if (lstatus == None or lstatus == status) and \
        (ldata1 == None or ldata1 == data1) and \
        (ldata2 == None or ldata2 == data2):

        # safer to ignore errors here; don't want to interrupt eating behavior
        try:
          cb(event[0])
        except Exception as e:
          print e

        # if one listener says eat it, then do that.
        eater = eater or eat

    # fwd any messages (that we didn't eat) onwards to the Push
    if not eater:
      print "sending it forward."
      outpututils.thru(event[0])

  # note ons are either:
  # - pressing colored buttons. route these through to Resolume
  # - touching knobs. send these to our encoders model
  def handle_note_ons(self, event, data=None):
    (status, data1, data2) = event
    if (data1 <= 8):
      print "touched by an angel"
      self.encoders.handle_push_touches(event)
    else:
      outpututils.thru(event)