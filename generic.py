"""
The contents of this file are taken with permission from the DeTT&CT project (http://github.com/rabobank-cdc/DeTTECT).
"""

from ruamel.yaml import YAML
from ruamel.yaml.timestamp import TimeStamp as ruamelTimeStamp
import re

REGEX_YAML_DATE = re.compile(r'^[\s-]+date:.*$', re.IGNORECASE)


def fix_date_and_remove_null(yaml_file, date, input_type='ruamel'):
    """
    Remove the single quotes around the date key-value pair in the provided yaml_file and remove any 'null' values
    :param yaml_file: ruamel.yaml instance or location of YAML file
    :param date: string date value (e.g. 2019-01-01)
    :param input_type: input type can be a ruamel.yaml instance or list
    :return: YAML file lines in a list
    """
    _yaml = init_yaml()
    if input_type == 'ruamel':
        # ruamel does not support output to a variable. Therefore we make use of StringIO.
        file = StringIO()
        _yaml.dump(yaml_file, file)
        file.seek(0)
        new_lines = file.readlines()
    elif input_type == 'list':
        new_lines = yaml_file
    elif input_type == 'file':
        new_lines = yaml_file.readlines()

    fixed_lines = [l.replace('\'' + str(date) + '\'', str(date)).replace('null', '')
                   if REGEX_YAML_DATE.match(l) else
                   l.replace('null', '') for l in new_lines]

    return fixed_lines

def init_yaml():
    """
    Initialize ruamel.yaml with the correct settings
    :return: am uamel.yaml object
    """
    _yaml = YAML()
    _yaml.Representer.ignore_aliases = lambda *args: True  # disable anchors/aliases
    return _yaml

def get_technique_name(techniques, technique_id):
    for tech in techniques:
        if technique_id == tech['technique_id']:
            return tech['technique_name']
    return ''