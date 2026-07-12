"""
=============================================================================
FILE: __init__.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from .math_lib import register_math_lib
from .string_lib import register_string_lib
from .list_lib import register_list_lib
from .map_lib import register_map_lib
from .file_lib import register_file_lib
from .path_lib import register_path_lib
from .json_lib import register_json_lib
from .time_lib import register_time_lib
from .random_lib import register_random_lib
from .http_lib import register_http_lib
from .crypto_lib import register_crypto_lib
from .core_lib import register_core_lib
from .database_lib import register_database_lib
from .regex_lib import register_regex_lib
from .env_lib import register_env_lib
from .process_lib import register_process_lib


from .logging_lib import register_logging_lib
from .testing_lib import register_testing_lib
from .compression_lib import register_compression_lib
from .concurrency_lib import register_concurrency_lib

from .networking_lib import register_networking_lib
from .encoding_lib import register_encoding_lib
