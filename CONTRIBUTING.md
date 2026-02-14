# Contributing to growatt2mqtt

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to `growatt2mqtt`. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## 🛠 How Can I Contribute?

### Reporting Bugs
This section guides you through submitting a bug report.
* **Check if the bug is already reported.** Search the [Issue Tracker](https://github.com/DEIN_USERNAME/growatt2mqtt/issues).
* **Use the Bug Report Template.** When you open a new issue, please use the provided YAML form. It asks for vital information like your inverter model and log output.

### Suggesting Enhancements
* **Use the Feature Request Template.** Describe exactly how the feature should work and why it is useful.
* **Register Maps:** If you have a Growatt inverter that is not yet supported, please share the Modbus Protocol documentation or a list of working registers.

---

## 💻 Development Setup

To set up your development environment locally:

1.  **Fork and Clone** the repository.
2.  **Create a Virtual Environment** (Python 3.10+ recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install Dependencies** (in editable mode):
    ```bash
    pip install -e .
    ```
4.  **Configuration:**
    Copy the example config and adjust it to your testing environment (or use a simulator):
    ```bash
    cp config.cfg.example growatt.cfg
    ```

---

## 🔌 Hardware & Modbus Guidelines (IMPORTANT)

Since this project interacts with physical hardware (High Voltage Inverters), please follow these safety rules:

### 1. Protect the EEPROM
Many Growatt inverters store settings in EEPROM/Flash memory, which has a limited number of write cycles (e.g., 100,000).
* **Do NOT** implement loops that write to Holding Registers every second.
* **Do NOT** change settings unnecessarily.
* If a register allows dynamic control (RAM), document it clearly.

### 2. PyModbus 3.x Syntax
We recently upgraded to `pymodbus` version 3.x.
* Do **not** use `unit=1`. Use `slave=1` instead.
* Do **not** use `.isError()`. Check for exceptions using `isinstance(rr, (ModbusException, ExceptionResponse))`.
* Please ensure your code is compatible with the new syntax.

### 3. Adding New Inverters
If you want to add support for a new Inverter model (e.g., SPH series):
* Create a new file in `growatt_2_mqtt/register_maps/`.
* Do not clutter `growatt.py` with hardcoded register addresses. Import them from the map file.

---

## 🚀 Pull Request Process

1.  **Create a Branch:** Please create a new branch for your feature or fix.
    * `feature/add-sph-support`
    * `fix/modbus-timeout`
2.  **Test Locally:**
    * If you have the hardware, test it on the real device.
    * If you changed the `Dockerfile`, try building it: `docker build .`
3.  **Update Documentation:** If you added a new feature or config option, please update `README.md`.
4.  **Submit PR:** Fill out the Pull Request Template describing your changes and **how you tested them**.

---

## 🎨 Style Guide

* **Python:** We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/).
* **Logging:** Please use the standard `logging` module (e.g., `self.log.info()`). Do **not** use `print()` statements.
* **Language:** Please keep code comments, commit messages, and pull request descriptions in **English**.

Thank you for your help!