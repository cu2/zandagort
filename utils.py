"""
Utility functions
"""

def multi_config(common_value, enum_):
    """Used in config to copy common values for all planet classes"""
    return {key: common_value.copy() for key in enum_.get_all_values()}
