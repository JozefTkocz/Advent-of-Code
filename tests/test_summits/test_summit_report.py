import pandas as pd

from summits.summit_report import get_summit_classifications, convert_classification_codes_to_names, \
    reduce_classification_list, ReportedSummit, ReportConfiguration


def test_get_summit_classifications():
    example_summits_df = pd.DataFrame({'class_1': [0, 0, 1],
                                       'class_2': [0, 1, 1],
                                       'class_3': [1, 1, 1]}, index=['summit_a', 'summit_b', 'summit_c'])
    expected_result = {'summit_a': ['class_3'],
                       'summit_b': ['class_2', 'class_3'],
                       'summit_c': ['class_1', 'class_2', 'class_3']}
    calculated_result = get_summit_classifications(summits=example_summits_df,
                                                   classification_columns=['class_1', 'class_2', 'class_3'])
    assert calculated_result == expected_result


def test_get_summit_classifications_include_classification_not_present_in_database():
    example_summits_df = pd.DataFrame({'class_1': [0, 0, 1],
                                       'class_2': [0, 1, 1],
                                       'class_3': [1, 1, 1]}, index=['summit_a', 'summit_b', 'summit_c'])
    expected_result = {'summit_a': ['class_3'],
                       'summit_b': ['class_2', 'class_3'],
                       'summit_c': ['class_1', 'class_2', 'class_3']}
    calculated_result = get_summit_classifications(summits=example_summits_df,
                                                   classification_columns=['class_1', 'class_2', 'class_3',
                                                                           'unrepresented_class'])
    assert calculated_result == expected_result


def test_convert_classification_codes_to_names():
    code_mapping = {'a': 'summit_type_a',
                    'b': 'summit_type_b',
                    'c': 'summit_type_c'}
    summit_classifications = {'summit_1': ['a'],
                              'summit_2': ['a', 'b'],
                              'summit_3': []}

    expected_result = {'summit_1': ['summit_type_a'],
                       'summit_2': ['summit_type_a', 'summit_type_b'],
                       'summit_3': []}
    calculated_result = convert_classification_codes_to_names(summit_classifications=summit_classifications,
                                                              mapping=code_mapping)
    assert calculated_result == expected_result


def test_reduce_classifications_list_extracts_primary_summits_and_primary_tops():
    summit_classifications = {'summit_1': ['Munro', 'Munro Top', 'Tump'],
                              'summit_2': ['Munro Top', 'Tump', 'Hump'],
                              'summit_3': ['Hump', 'Tump'],
                              'summit_4': ['Tump', 'Hump']}

    munro = ReportedSummit(code='M', name='Munro', is_primary=True)
    munro_top = ReportedSummit(code='MT', name='Munro Top', is_primary=True)
    hump = ReportedSummit(code='H', name='Hump', is_primary=False)
    tump = ReportedSummit(code='T', name='Tump', is_primary=False)

    report_config = ReportConfiguration([munro, munro_top, hump, tump])

    expected_result = {'summit_1': ['Munro'],
                       'summit_2': ['Munro Top'],
                       'summit_3': ['Hump, Tump'],
                       'summit_4': ['Tump, Hump']}
    calculated_result = reduce_classification_list(summit_classifications, report_config)
    assert calculated_result == expected_result