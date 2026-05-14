from qns.simulator.event import Event
from qns.simulator import Simulator, func_to_event
from qns.utils.log import *
from qns.simulator.stablepool import StableEventPool
from qns.entity import *
from qns.entity.cchannel.cchannel_ex import ClassicChannelEx


class AppS(Application):
    def __init__(self, dst):
        super().__init__()
        self.dst = dst
        self.i = 0
        self.rate = 1.0

    def start(self):
        self.send()

    def install(self, node, simulator: Simulator):
        return super().install(node, simulator)

    def send(self):
        n: QNode = self.get_node()
        c: ClassicChannelEx = n.get_cchannel(self.dst)

        c.send(ClassicPacket(f"{self.i:02d}"), self.dst)
        self.i += 1

        self._simulator.add_event(
            func_to_event(
                self._simulator.tc + self._simulator.time(sec=1.0 / self.rate),
                self.send,
            )
        )


class AppR(Application):
    def __init__(self):
        super().__init__()
        self.add_handler(self.recv)
        self.recved = []
        self.recved_time = []

    def recv(self, node, event: Event):
        packet: ClassicPacket = event.packet
        # debug(f"{self.get_node().name} recv {packet.msg}")
        self.recved.append(packet.msg)
        self.recved_time.append(self._simulator.tc)


def test(ex, tparam):
    sim = Simulator(0, 10, pool_cls=StableEventPool)

    install(sim)

    n1 = QNode("n1")
    n2 = QNode("n2")

    global c12
    if not ex:
        c12 = ClassicChannel(
            bandwidth=tparam[0],
            drop_rate=tparam[1],
            delay=tparam[2],
            max_buffer_size=tparam[3],
        )
    else:
        c12 = ClassicChannelEx(
            bandwidth=tparam[0],
            drop_rate=tparam[1],
            delay=tparam[2],
            max_buffer_size=tparam[3],
        )
        c12.reliable = True

    n1.add_cchannel(c12)
    n2.add_cchannel(c12)

    s1 = AppS(n2)
    r1 = AppR()
    n1.add_apps(s1)
    n2.add_apps(r1)

    s2 = AppS(n1)
    r2 = AppR()
    n2.add_apps(s2)
    n1.add_apps(r2)

    n1.install(sim)
    n2.install(sim)

    s1.rate = 1
    s2.rate = 1

    s1.start()
    s2.start()

    sim.run()

    print(f"n1->n2: {r1.recved}")
    print(f"time:{r1.recved_time}")
    print(f"\nn2->n1: {r2.recved}")
    print(f"time:{r2.recved_time}")


bidir = (2, 0, 0, 1)
print("============================")
print("bidir w/o Ex:")
test(False, bidir)
print("---------------")
print("bidir w/ Ex:")
test(True, bidir)

reliable = (0, 0.5, 1, 0)
print("============================")
print("reliable w/o Ex:")
test(False, reliable)
print("---------------")
print("reliable w/ Ex:")
test(True, reliable)
