"""
Tanium ATT&CK mapping
Author: Ruben Bouman, Sirius Security
License: GPL-3.0 License
Reference:
https://www.siriussecurity.nl/blog/2021/6/2/mapping-vendor-products-to-mitre-attack-tanium
"""

import json
from datetime import datetime
from constants import *
from generic import *
from copy import deepcopy
from io import StringIO
import argparse
import os

SCORE = 1

def get_tanium_signals_from_file(filename):
    """
    Loads the Tanium signal-feed (JSON) file
    :param filename: the filename of the file to be loaded
    :return: a dictionary representation of the signals in the JSON file
    """
    with open(filename) as f:
        return json.load(f)['signals']

def generate_dettect_techniques_yaml_file(signals):
    """
    Loops through all the Tanium signals and generates a DeTT&CT techniques YAML file containing all the (sub) techniques from the Tanium feed.
    :param signals: dictionary object with all Tanium signals
    :return:
    """
    yaml_file = dict()
    yaml_file['version'] = 1.2
    yaml_file['file_type'] = 'technique-administration'
    yaml_file['name'] = 'Tanium'
    yaml_file['platform'] = ['Windows', 'Linux', 'macOS']
    yaml_file['techniques'] = []
    today = datetime.now()

    techniques = {}
    for signal in signals:
        signal_techniques = signal['mitreAttacks']['v7']['techniques']
        for signal_technique in signal_techniques:
            if signal_technique['id'] not in techniques.keys():
                techniques[signal_technique['id']] = generate_techniques_object(signal['name'], signal['platforms'], signal_technique['id'], signal_technique['name'], SCORE, today)
            else:
                update_techniques_object(techniques[signal_technique['id']], signal['name'], signal['platforms'], SCORE, today)

    # location field was a set to force unique items, convert it to list to comply DeTT&CT datatype:
    for technique_id, technique in techniques.items():
        for d in technique['detection']:
            d['location'] = list(d['location'])
    yaml_file['techniques'] = list(techniques.values())

    # generate the contents for the yaml file:
    _yaml = init_yaml()
    file = StringIO()
    _yaml.dump(yaml_file, file)
    file.seek(0)
    file_lines = file.readlines()

    # remove the single quotes from the date
    yaml_file_lines = fix_date_and_remove_null(file_lines, today, input_type='list')

    # write the yaml contents to a file:
    output_filename = 'techniques-tanium.yaml'
    with open(output_filename, 'w') as f:
        f.writelines(yaml_file_lines)
    print('YAML file written: ' +output_filename)
    print()
    print('Now use DeTT&CT to generate ATT&CK Navigator file:')
    print('  python dettect.py d -ft %s -l' % output_filename)
    print()
    print('Scores for all (sub) techniques are set to \'%d\'' % SCORE)

def generate_techniques_object(signal_name, signal_platforms, technique_id, technique_name, score, today):
    """
    Helper function to generate the technique object within the DeTT&CT techniques YAML file.
    :param signal_name: Name of the Tanium signal, to be included in the location field
    :param signal_platform: Platform where the Tanium signal applies to
    :param technique_id: ATT&CK (sub) technique ID.
    :param technique_name: ATT&CK (sub) technique name
    :param score: DeTT&CT score
    :param today: Date to be included in the score_logbook
    :return: technique object for the DeTT&CT techniques YAML file
    """
    tech = deepcopy(YAML_OBJ_TECHNIQUE)
    tech['technique_id'] = technique_id
    tech['technique_name'] = technique_name

    tech['detection'] = []
    for platform in signal_platforms:
        tech['detection'].append(generate_detection_object(signal_name, platform, score, today))
    return tech

def generate_detection_object(signal_name, platform, score, today):
    """
    Helper function to generate the detection object within the technique object within the DeTT&CT techniques YAML file.
    :param signal_name: Name of the Tanium signal, to be included in the location field
    :param signal_platform: Platform where the Tanium signal applies to
    :param score: DeTT&CT score
    :param today: Date to be included in the score_logbook
    :return: new detection object for a technique object
    """
    detection = deepcopy(YAML_OBJ_DETECTION)
    detection['applicable_to'] = []
    if platform == 'windows':
        detection['applicable_to'].append('windows endpoints')
    elif platform == 'linux':
        detection['applicable_to'].append('linux endpoints')
    elif platform == 'mac':
        detection['applicable_to'].append('macos endpoints')

    detection['score_logbook'][0]['score'] = score
    detection['score_logbook'][0]['date'] = today
    detection['location'] = {'Tanium: ' +signal_name,}
    return detection

def update_techniques_object(technique, signal_name, signal_platforms, score, today):
    """
    Helper function to update an existing detection object within the technique object within the DeTT&CT techniques YAML file.
    :param signal_name: Name of the Tanium signal, to be included in the location field
    :param signal_platform: Platform where the Tanium signal applies to
    :param score: DeTT&CT score
    :param today: Date to be included in the score_logbook
    :return: updated detection object for a technique object
    """
    for platform in signal_platforms:
        detection = None
        # Make sure the signal is added to the right applicable_to detection object:
        if platform == 'windows':
            for d in technique['detection']:
                if 'windows' in ''.join(d['applicable_to']):
                    detection = d
        elif platform == 'linux':
            for d in technique['detection']:
                if 'linux' in ''.join(d['applicable_to']):
                    detection = d
        elif platform == 'mac':
            for d in technique['detection']:
                if 'mac' in ''.join(d['applicable_to']):
                    detection = d

        if detection is None:
            detection = generate_detection_object(signal_name, platform, score, today)
            technique['detection'].append(detection)
        else:
            detection['location'].add('Tanium: ' +signal_name)
            if score > detection['score_logbook'][0]['score']:
                detection['score_logbook'][0]['score'] = score


if __name__ == '__main__':
    menu_parser = argparse.ArgumentParser(description='Generates a DeTT&CT YAML file from the Tanium signals-feed in order to generate an ATT&CK Navigator layer.', epilog='Source: https://github.com/siriussecurity/')
    menu_parser.add_argument('-f', '--filename', help='Tanium signals file. Download it from https://content.tanium.com/files/misc/ThreatResponse/ThreatResponse.html. Choose the V3 version.')
    args = menu_parser.parse_args()
    if args.filename:
        if os.path.exists(args.filename):
            tanium_signals = get_tanium_signals_from_file(args.filename)
            generate_dettect_techniques_yaml_file(tanium_signals)
        else:
            print('Given file does not exist.')
    else:
        menu_parser.print_help()