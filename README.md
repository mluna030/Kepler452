# Post-Quantum Embedded System for Securing Deep Space Applications 
Kepler-452B

## Overview

Kepler452 is a post-quantum cryptographic embedded system designed for securing deep space applications. This project integrates state-of-the-art cryptographic schemes to provide robust security against quantum computing threats. Our research-driven approach focuses on applying **XMSS (eXtended Merkle Signature Scheme)** and **AES encryption** to ensure the integrity and confidentiality of communications in critical environments such as space missions.

Originally developed for the NASA Artemis program, Kepler452 showcases how post-quantum cryptographic principles can be implemented in embedded IoT systems, with a particular focus on securing autonomous Unmanned Ground Vehicles (UGVs) and Unmanned Aerial Vehicles (UAVs). This project leverages **the PYNQ-Z1 platform** for efficient hardware acceleration and cryptographic operations.

**This is an ongoing research project, and improvements will continue as we explore advancements in post-quantum cryptography.**

## Table of Contents

- [Key Features](#key-features)
- [Project Literature](#project-literature)
- [Technical Details](#technical-details)
- [License](#license)
- [Contact](#contact)

## Key Features

- **Post-Quantum Cryptographic Security**: Implements XMSS, a hash-based signature scheme resistant to quantum attacks.
- **Secure Drone and UGV Communication**: Cryptographic signing and encryption of telemetry data between UAVs and UGVs.
- **Embedded System Implementation**: Utilizes PYNQ-Z1 for hardware acceleration, improving efficiency and security.
- **Man-in-the-Middle Attack Mitigation**: Demonstrates attack scenarios and defenses against adversarial drones.
- **AES Encryption**: Ensures confidentiality of transmitted data.
- **Hardware-Optimized Performance**: Designed for real-time cryptographic operations on constrained embedded devices.

## Project Literature

This project is supported by extensive research and documentation. Below are key papers and reports associated with Kepler452:

- **[Secure Robotic Environment for NASA Artemis Program using XMSS Algorithm](docs/exec_sum.pdf)** – Executive summary detailing project goals and implementation.
- **[Post-Quantum Cryptographic Embedded System for Securing Deep Space Applications](docs/Post_Quantum_Cryptography.pdf)** – A comprehensive research paper discussing the implementation and challenges of post-quantum security in embedded systems.

## Technical Details

This project focuses on integrating post-quantum cryptographic primitives into an embedded system for deep space security applications. The key components include:

- **XMSS (eXtended Merkle Signature Scheme)**: A stateful hash-based digital signature scheme with quantum resistance.
- **AES Encryption**: Used for secure telemetry communication between UAVs and UGVs.
- **PYNQ-Z1 Hardware Acceleration**: Provides efficient cryptographic operations.
- **Attack Simulations**: Tests include adversarial drone scenarios attempting to intercept encrypted messages.

## License

This project is licensed under the [MIT License](docs/LICENSE).

## Contact

For inquiries and collaboration, contact:

Michael Luna - [michael.angelo.luna1@gmail.com](mailto:michael.angelo.luna1@gmail.com)

Project Link: [https://github.com/mluna030/Kepler452](https://github.com/your-repo/Kepler452)

