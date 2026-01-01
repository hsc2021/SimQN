# SimQN

- [SimQN](#simqn)
  - [Overview](#overview)
  - [Roadmap](#roadmap)
  - [Why choose SimQN?](#why-choose-simqn)
  - [Installation](#installation)
  - [First sight of SimQN](#first-sight-of-simqn)
  - [Get Help](#get-help)
  - [Release History](#release-history)
  - [How to contribute?](#how-to-contribute)
  - [License and Authors](#license-and-authors)
  - [Ciatation](#ciatation)

## Overview

[![Pytest](https://github.com/QNLab-USTC/SimQN/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/QNLab-USTC/SimQN/actions/workflows/pytest.yml)
![Flake8](https://github.com/QNLab-USTC/SimQN/actions/workflows/flake8.yml/badge.svg)

**[Attention]** Most of existing&future studies in [QNLab](https://qnlab-ustc.com/) are evaluated on SimQN platform, if you would like to follow our work or seek for an easy-to-use quantum network simulator, you cannot miss SimQN! Please check out the following publication for details. **([Link](https://ieeexplore.ieee.org/abstract/document/10024900/) and [PDF](https://infonetlijian.github.io/homepage/PDF_files/2023-%E3%80%90IEEE%20Network%E3%80%91-SimQN_a_Network-layer_Simulator_for_the_Quantum_Network_Investigation.pdf)).**  

Welcome to SimQN's documentation. SimQN is a discrete-event-based network simulation platform for quantum networks.
SimQN enables large-scale investigations, including QKD protocols, entanglement distributions protocols, and routing algorithms, resource allocation schemas in quantum networks. For example, users can use SimQN to design routing algorithms for better QKD performance. For more information, please refer to the [Documents](https://qnlab-ustc.github.io/SimQN/).

SimQN is a Python3 library for quantum networking simulation. It is designed to be general purpose. It means that SimQN can be used for both QKD network, entanglement distribution networks, and other kinds of quantum networks' evaluation. The core idea is that SimQN makes no architecture assumption. Since there is currently no recognized network architecture in quantum network investigations, SimQN stays flexible in this aspect.

SimQN provides high performance for large-scale network simulation. SimQN uses [Cython](https://cython.org/) to compile critical codes in C/C++ libraries to boost the evaluation. Also, along with the commonly used quantum state-based physical models, SimQN provides a higher-layer fidelity-based entanglement physical model to reduce the computation overhead and brings convenience for users in evaluation. Last but not least, SimQN provides several network auxiliary models for easily building network topologies, producing routing tables and managing multiple session requests.

## Roadmap

![Roadmap](https://github.com/QNLab-USTC/QuantumNetworkWebsite/blob/main/static/images/simqn_roadmap.png)

- Currently, we are foucsing on developing the 0.2.x version of SimQN, which will include:
  - Useful network utilities, such as more random topology generators, routing algorithms, and session request generators, real topology adaptors, and Multi-path routing algorithms.
  - Representative quantum network protocols, such as Q-CAST routing protocol, PS/PU routing protocol, REPS routing protocol for quantum information networks, and CASCADE error correction protocol for QKD networks.

- The follwing functions will be included in the future versions:
  - Practical quantum network entities, such as quantum repeaters, quantum switches, and quantum benchmarking devices.
  - Useful network utilities, such as random request traffic generators.
  - Support for Quantum network stack protocols, incluing KM protocols, routing protocols in QKD networks, and entanglement distribution protocols in quantum information networks.
  - Realization of easy-to-use GUI for SimQN.
  
## Why choose SimQN?

SimQN is designed as a functional and easy-to-use simulator, like [NS3](https://www.nsnam.org/) in classic networks, it provides numerous functions for anyone who wants to simulate a QKD network or entanglement-based network. 

Compared with the existing quantum network simulators, the developers pay more attention to simulation in the network area. Currently, a network simulation can be complicated, as users may have to implement routing algorithms and multiply protocols in different layers to complete a simulation. SimQN aims to break down this problem by providing a modulized quantum node and reusable algorithms and protocols. As a result, users can focus on what they study and reuse other built-in modules. The developers believe this will significantly reduce the burden on our users. As for the physics area, SimQN can also simulate quantum noise, fidelity, and more. Thus, if you focus on the research of the quantum network area, SimQN can be a competitive choice.  

**The main advantages of SimQN can be summarized as follows.**
- Easy-to-use with Python
- High-efficiency simulator core
- Customizable qubit model
- Built-in quantum internet protocol stack
- Mainstream quantum applications support, e.g., QKD, quantum networking, and distributed quantum computing (incoming)
- Periodical updates for academia-related functions and state-of-the-art solutions in the community  (you are welcome to highlight your work and contribute your code on SimQN)
- ...


## Installation

Install and update using `pip`:
```
pip3 install -U qns
```

## First sight of SimQN

Here is an example of using SimQN.

``` Python

    from qns.simulator.simulator import Simulator
    from qns.network.topology import RandomTopology
    from qns.network.protocol.entanglement_distribution import EntanglementDistributionApp
    from qns.network import QuantumNetwork
    from qns.network.route.dijkstra import DijkstraRouteAlgorithm
    from qns.network.topology.topo import ClassicTopology
    import qns.utils.log as log
    import logging

    init_fidelity = 0.99   # the initial entanglement's fidelity
    nodes_number = 150     # the number of nodes
    lines_number = 450     # the number of quantum channels
    qchannel_delay = 0.05  # the delay of quantum channels
    cchannel_delay = 0.05  # the delay of classic channels
    memory_capacity = 50   # the size of quantum memories
    send_rate = 10         # the send rate
    requests_number = 10   # the number of sessions (SD-pairs)

    # generate the simulator
    s = Simulator(0, 10, accuracy=1000000)

    # set the log's level
    log.logger.setLevel(logging.INFO)
    log.install(s)

    # generate a random topology using the parameters above
    # each node will install EntanglementDistributionApp for hop-by-hop entanglement distribution
    topo = RandomTopology(nodes_number=nodes_number,
                          lines_number=lines_number,
                          qchannel_args={"delay": qchannel_delay},
                          cchannel_args={"delay": cchannel_delay},
                          memory_args=[{"capacity": memory_capacity}],
                          nodes_apps=[EntanglementDistributionApp(init_fidelity=init_fidelity)])

    # build the network, with Dijkstra's routing algorithm
    net = QuantumNetwork(topo=topo, classic_topo=ClassicTopology.All, route=DijkstraRouteAlgorithm())

    # build the routing table
    net.build_route()

    # randomly select multiple sessions (SD-pars)
    net.random_requests(requests_number, attr={"send_rate": send_rate})

    # all entities in the network will install the simulator and do initiate works.
    net.install(s)

    # run simulation
    s.run()
```

## Get Help

- This [documentation](https://qnlab-ustc.github.io/SimQN/) may answer most questions.
    - The [tutorial](https://qnlab-ustc.github.io/SimQN/tutorials.html) here presents how to use SimQN.
    - The [API manual](https://qnlab-ustc.github.io/SimQN/modules.html) shows more detailed information.
- Welcome to report bugs at [Github](https://github.com/QNLab-USTC/SimQN).

## Release History

- v0.2.2(Released 2026.01)
  - *New functions!!!*
  - Simulator Core: Hash Bucket Based Event Scheduler.
  - Network Utilities: Add Real Topology Generator, including AboveNetTopology, AGISTopology and Creat Topology From GML File Download From [The Internet Topology Zoo](https://topology-zoo.org/dataset.html). Update the Dijkstra-based Routing Utility.

- v0.2.1(Released 2025.04)
  - *New functions!!!*
  - Network Utilities: Add Random Topology Generator, including ER model, BA model, and dual-BA model.
  - Applications: Add CASCADE Error Correction and Privacy Amplification Process for BB84 Protocol.

- v0.1.5(Released 2022.09)
  - *New functions!!!*
  - Simulator Core: Cython Optimization, Multi-process Support.
  - Quantum Entitise: Quantum Memory, Delay Model.
  - Tools: Monitor Tools.

- v0.1.4(Released 2022.03)
  - *New functions!!!*
  - Simulator Core: Priority Queue Based Event Scheduler.
  - Physical Backends: Qubit Model, EPR Model, Quantum Gates.
  - Quantum Entitise: Quantum Node, Quantum Channel.
  - Network Utilities: Topology Generator, Routing Utility.
  - Applications: BB84 Protocol, Entanglement Swapping Protocol.
  - Tools: Rnd Tools.

## How to contribute?
Welcome to contribute through Github Issue or Pull Requests. Please refer to the [develop guide](https://qnlab-ustc.github.io/SimQN/develop.html). If you have any questions, you are welcome to contact the developers via e-mail.

## License and Authors

SimQN is an open-source project under [GPLv3](/LICENSE) license. The authors of the paper includes:
* Lutong Chen (ertuil), School of Cyber Science and Technology, University of Science and Technology of China, China. elliot.98@outlook.com
* Jian Li(infonetlijian), School of Cyber Science and Technology, University of Science and Technology of China, China. 
* Kaiping Xue (kaipingxue), School of Cyber Science and Technology, University of Science and Technology of China, China. xue.kaiping@gmail.com
* Nenghai Yu, School of Cyber Science and Technology, University of Science and Technology of China, China.
* Ruidong Li, Institute of Science and Engineering, Kanazawa University, Japan.
* Qibin Sun, School of Cyber Science and Technology, University of Science and Technology of China, China.
* Jun Lu, School of Cyber Science and Technology, University of Science and Technology of China, China.

Other contributors includes:
* Zirui Xiao, School of Cyber Science and Technology, University of Science and Technology of China, China.
* Yuqi Yang, School of Cyber Science and Technology, University of Science and Technology of China, China.
* Bing Yang, School of Cyber Science and Technology, University of Science and Technology of China, China.
* Xumin Gao, School of Cyber Science and Technology, University of Science and Technology of China, China.

## Citation

Please cite this publication if you use SimQN in your research.

```Bibtex
@article{chen2023simqn,
  title={SimQN: A network-layer simulator for the quantum network investigation},
  author={Chen, Lutong and Xue, Kaiping and Li, Jian and Yu, Nenghai and Li, Ruidong and Sun, Qibin and Lu, Jun},
  journal={IEEE Network},
  volume={37},
  number={5},
  pages={182--189},
  year={2023},
  publisher={IEEE},
  doi={10.1109/MNET.130.2200481}
}
```
