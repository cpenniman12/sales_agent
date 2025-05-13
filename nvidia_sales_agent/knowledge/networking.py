"""
Knowledge base for NVIDIA Networking & DPUs
"""

NETWORKING_KNOWLEDGE = """
# NVIDIA Networking & DPUs

NVIDIA Networking delivers high-performance, software-defined networking solutions for the modern data center. With a complete portfolio of adapters, switches, and Data Processing Units (DPUs), NVIDIA offers end-to-end networking infrastructure for AI and accelerated computing.

## NVIDIA BlueField DPUs

NVIDIA BlueField Data Processing Units (DPUs) are a new class of programmable processor that combines network interface capabilities with a programmable ARM-based compute complex and hardware acceleration engines to offload and accelerate networking, storage, and security functions.

Product Line:
- BlueField-3 DPU: 400Gb/s networking with accelerated cyber security
- BlueField-2 DPU: 200Gb/s networking with hardware acceleration
- BlueField-2X DPU: Adds NVIDIA Ampere GPU for AI processing
- BlueField Software: DOCA SDK for DPU programming

## NVIDIA ConnectX SmartNICs

NVIDIA ConnectX SmartNICs provide high-performance, hardware acceleration for networking tasks, delivering the highest throughput and lowest latency for data center applications.

Product Line:
- ConnectX-7: 400Gb/s Ethernet and NDR 400Gb/s InfiniBand
- ConnectX-6 Dx: 200Gb/s with advanced security offloads
- ConnectX-6 Lx: Cost-effective 25/50Gb/s Ethernet adapter
- ConnectX-5: 100Gb/s Ethernet and EDR 100Gb/s InfiniBand

## NVIDIA Quantum InfiniBand

NVIDIA Quantum InfiniBand provides the highest performing interconnect technology for HPC and AI workloads, with extremely low latency and high throughput.

Product Line:
- Quantum-2 Switch: NDR 400Gb/s InfiniBand with 64 ports
- Quantum-1 Switch: HDR 200Gb/s InfiniBand with 40 ports
- SHARPv3: In-network computing technology
- UCX: Unified Communication X framework for high-performance networking

## NVIDIA Spectrum Ethernet

NVIDIA Spectrum Ethernet switches deliver high-performance networking for data centers with industry-leading port speeds, densities, and smart features for cloud environments.

Product Line:
- Spectrum-4: 51.2Tb/s Ethernet switch with 400GbE ports
- Spectrum-3: 12.8Tb/s Ethernet switch with 400GbE ports
- Spectrum-2: 6.4Tb/s Ethernet switch with 100/200GbE ports
- NVIDIA Cumulus Linux: Open networking operating system
- NVIDIA DENT: Distributed Enterprise Network operating system

## NVIDIA DOCA Software

NVIDIA DOCA is a software framework for developing applications on the BlueField DPU. It includes software libraries, drivers, APIs, sample code, and documentation.

Key Components:
- DOCA Runtime: Core libraries and services for DPU applications
- DOCA Flow: Framework for packet processing and flow programming
- DOCA Telemetry: Monitoring and analytics services
- DOCA Security: Framework for security applications
- DOCA Storage: Libraries for storage acceleration

## Zero Trust Security

NVIDIA's Zero Trust security architecture combines DPUs, SmartNICs, and security software to protect data centers and applications from evolving threats.

Key Features:
- Hardware isolation of security functions
- In-line encryption and decryption
- Distributed firewall capabilities
- East-west traffic protection
- AI-enhanced security monitoring

## NVIDIA Air

NVIDIA Air is a virtual environment for testing, validating, and developing modern data center networking solutions, allowing users to simulate complex networks before deployment.

Key Features:
- Virtual lab environment for network testing
- Support for NVIDIA Cumulus Linux
- Pre-built topologies and automation tools
- Integration with CI/CD pipelines
- Cloud-based accessibility
""" 