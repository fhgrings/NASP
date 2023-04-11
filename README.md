> :memo: Note: This is still an experimental project. The releases were just for quick access of the artifacts presented in the publications (See [docs](docs/) folder.)

# NSSMF_CN

Network Sub Slice management Function for Core Network

## Design

Achitecture diagrams

### Activity Diagrams

Flow Diagrams

## Features

Contributions and features

## :construction: Future Work

- QER (QoS Enforcement Rule)
- CO-RE for tracing.
- PoC with OpenAirInterface

## Main Dependencies

Libs, patchs, hardwares and modules

## First Steps

How to group all primarly resources

## Build and Installation

The library is built and installed with

```
make install
```

The `package` folder is created with the headers, library and some binaries for testing.

```
package
├── bin       # Contains binaries for testing
├── include   # Contains headers
├── lib       # Contains libupf_xdp.a library
└── tests     # Contains scripts for testing
```

## How to Test

Troubleshoting

### Integration with other tools

HTTP servers
APIs
Databases 
Monitoring

## :rocket: Benchmark

Images, how to benchmark and results

## Tree

```
├── build: Generated build directory.
├── cmake: Cmake files configuration directory
├── extern: Submodule repositories
├── include: Include files
├── samples: Samples like XDP BPF hello world
├── src: Source files directory
├── tests: UTs, HTTP API srcs, scripts for testing, trex installation
├── Makefile: Encapsulate cmake calls for build, run samples, clean, etc
└── README.md: Readme file
```

## :notebook: Contacts

## :information_source: References

- [Paper - Run-time Adaptive In-Kernel BPF/XDP Solution for 5G UPF](docs/Paper___Run-time_Adaptive_In-Kernel_BPF_XDP_Solution_for_5G_UPF.pdf)
- [Paper - An In-Kernel Solution Based on XDP for 5G UPF: Design, Prototype and Performance Evaluation](docs/Paper___An_In_Kernel_Solution_Based_on_XDP__Design__Prototype_and_Performance_Evaluation.pdf)
- [Video - Project Overview](https://youtu.be/Av_k_fZKCfM)
- [Slides - Project Overview](https://docs.google.com/presentation/d/1osOheCFV3c3wn4hDbo5R3coL8nDeaxjVb7D33QT41jw/edit?usp=sharing)
- [Video - Performance Evaluation with UPF eBPF/XDP Library for 5G Core Network](https://www.youtube.com/watch?v=6KYFDMJJH2o)
