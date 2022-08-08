#!/usr/bin/env python3


BUILTIN_PARAMETER_SCHEMA = [
    {
        "key": "SAMPLE_INFO",
        "type": "string",
        "required": True,
        "blank": False,
    },
    {
        "key": "OUT_DIR",
        "type": "string",
        "required": True,
        "blank": False,
    },
    {
        "key": "TASK_URL",
        "type": "string",
        "required": False,
        "blank": True,
        "default": "",
    },
]
