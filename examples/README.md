# Examples: Verification Status

The end-to-end verified examples are in `../tests/`; they run through the Rust bootstrap compiler and VM in `../tests/run_tests.ps1`. Other files in this directory are demonstrations or prototypes and are not automatically verified by that test suite. Some use modules or host APIs that are not implemented. Basic user-defined actions are covered by `test_06_functions.aayu`.

Before relying on an example, run it with the VM and compiler built from the same checkout and check its output. Domain demos that print simulated blockchain, AI, HTTP, or UI results are demonstrations, not production integrations.
