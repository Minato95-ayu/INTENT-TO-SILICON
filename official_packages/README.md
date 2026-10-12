# Package Samples: Status

This directory is a set of unverified package sketches. It is not an official package registry or a runnable package set: the VM CLI has no package resolver and AAYU module imports are not implemented. Basic actions work, but do not make these package examples importable.

Some sample functions return fixed demo strings or call undefined APIs such as `ai::generate`, `json::parse`, and `ml::kmeans_fit`. Do not use them as working AI, vision, RAG, authentication, crypto, or data-frame libraries. Each package needs a real implementation, dependency contract, and tests before it can be advertised as usable.
