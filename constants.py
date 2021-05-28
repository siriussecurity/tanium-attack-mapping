"""
The contents of this file are taken with permission from the DeTT&CT project (http://github.com/rabobank-cdc/DeTTECT).
"""

# YAML objects
YAML_OBJ_VISIBILITY = {'applicable_to': ['all'],
                       'comment': '',
                       'score_logbook':
                           [
                               {'date': None,
                                'score': 0,
                                'comment': '',
                                'auto_generated': True}
                           ]
                       }

YAML_OBJ_DETECTION = {'applicable_to': ['all'],
                      'location': [''],
                      'comment': '',
                      'score_logbook':
                          [
                              {'date': None,
                               'score': -1,
                               'comment': ''}
                      ]}

YAML_OBJ_TECHNIQUE = {'technique_id': '',
                      'technique_name': '',
                      'detection': [YAML_OBJ_DETECTION,],
                      'visibility': [YAML_OBJ_VISIBILITY,]}
