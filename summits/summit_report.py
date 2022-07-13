import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import Dict, List

CLASSIFICATION_CODES = {'M': 'Munro',
                        'MT': 'Munro Top',
                        'C': 'Corbett',
                        'CT': 'Corbett Top',
                        'G': 'Graham',
                        'GT': 'Graham Top',
                        'D': 'Donald',
                        'DT': 'Donald Top',
                        'Ma': 'Marilyn',
                        'Hu': 'Hump',
                        'Tu': 'Tump',
                        'Sim': 'Simm',
                        'Hew': 'Hewitt',
                        'N': 'Nutall',
                        'W': 'Wainwright'}

PRIMARY_CLASSIFICATIONS = ['Munro', 'Corbett', 'Graham', 'Donald', 'Furth', 'Wainwright']
PRIMARY_TOP_CLASSIFICATIONS = ['Munro Top', 'Corbett Top', 'Graham Top', 'Donald Top']
HEIRARCHICAL_CLASSIFICATIONS = pd.Series(data={1: 'Hewitt',
                                               2: 'Nutall',
                                               3: 'Marilyn',
                                               4: 'Hump',
                                               5: 'Tump'})


@dataclass
class ReportedSummit:
    code: str
    name: str
    is_primary: bool
    is_top: bool


class ReportConfiguration:
    def __init__(self, summit_classes: List[ReportedSummit]):
        self.default_reported_summit = ReportedSummit(code='', name='', is_primary=False, is_top=False)
        self.classes = summit_classes + [self.default_reported_summit]
        self.class_dict = self._create_class_dict()
        self.hierarchy = self._create_class_hierarchy()
        self.highest_classification_rank = max(self.hierarchy.values())

    def _build_df(self):
        config = []
        for summit_type in self.classes:
            config_for_class = {}
            config_for_class.update({'code': summit_type.code,
                                     'name': summit_type.name,
                                     'is_primary': summit_type.is_primary,
                                     'is_top': summit_type.is_top})
            config.append(config_for_class)

        return pd.DataFrame(config)

    def _create_class_dict(self):
        return {c.name: c for c in self.classes}

    def _create_class_hierarchy(self):
        return {c.name: i for i, c in enumerate(self.classes) if not c.is_primary}

    def get_class(self, class_name: str) -> ReportedSummit:
        return self.class_dict.get(class_name, self.default_reported_summit)

    def get_rank(self, class_name: str) -> int:
        return self.hierarchy.get(class_name)

    def primary_classifications(self):
        return [c.name for c in self.classes if c.is_primary and not c.is_top]

    def primary_top_classifications(self):
        return [c.name for c in self.classes if c.is_primary and c.is_top]

    def secondary_classifications(self):
        return pd.Series(reversed([c.name for c in self.classes if not c.is_primary]))


def generate_summit_report(summits: pd.DataFrame) -> str:
    summit_classifications = get_summit_classifications(summits=summits,
                                                        classification_columns=list(CLASSIFICATION_CODES.keys()))
    summit_classifications = convert_classification_codes_to_names(summit_classifications, mapping=CLASSIFICATION_CODES)

    return 'no'


def get_summit_classifications(summits: pd.DataFrame,
                               classification_columns: List[str]) -> Dict[str, List[str]]:
    """
    Given a table of summits, return a dictionary where the keys are summit ID and the values are a list of
    corresponding applicable summit classifications

    :param summits: pd.DataFrame representing a database of summits
    :param classification_columns: A list of column names. The columns should be Boolean flags denoting whether a given
    summit belongs to the corresponding classification (values denoting True/False are 0/1 respectively).
    :return: A dictionary where the key is the database index, and the value is a list of corresponding classifications
    """
    columns_present = [c for c in summits.columns if c in classification_columns]
    df = (summits[columns_present] == 1).T

    summit_classification_codes = {}
    for summit in df.columns:
        classification_series = df[summit]
        print(classification_series)
        classifications = classification_series.loc[classification_series].index.to_list()
        summit_classification_codes.update({summit: classifications})

    return summit_classification_codes


def convert_classification_codes_to_names(summit_classifications: Dict[str, List[str]],
                                          mapping: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Given a dictionary of summits and their classification codes, apply the mapping to the classification codes to
    return a dictionary of summits and their classification names.

    :param summit_classifications: Dict where keys are summit identifiers, and values are lists of corresponding summit
    classification codes
    :param mapping: Dict defining a mapping between classification codes and classification names
    :return: Dict where keys are summit identifiers, and values are corresponding classification names
    """
    for idx, codes in summit_classifications.items():
        long_names = []
        for c in codes:
            long_name = mapping.get(c)
            if long_name is not None:
                long_names.append(long_name)

        summit_classifications.update({idx: long_names})
    return summit_classifications


def reduce_classification_list(summit_classifications: Dict[str, List[str]],
                               report_configuration: ReportConfiguration):
    """
    Report primary summit types, even if it is a duplication.
    Only report primary tops if they're also not primary non-tops

    Report non-primary summits only once, with the highest classification

    :param summit_classifications:
    :param report_configuration:
    :return:
    """
    result = {}

    for summit_name, summit_types in summit_classifications.items():
        final_summit_types = []
        highest_rank = report_configuration.secondary_classifications().index.max()

        is_primary_summit = np.any([t in report_configuration.primary_classifications() for t in summit_types])
        is_primary_top = np.any([t in report_configuration.primary_top_classifications() for t in summit_types])

        for summit_type in summit_types:
            # If this hill is a primary class, and this code is the primary class, always report
            if is_primary_summit and summit_type in report_configuration.primary_classifications():
                final_summit_types.append(summit_type)

            # If this hill is a primary top class and not also a primary class and  this code is not the primary top
            # class
            if is_primary_top and not is_primary_summit and summit_type in report_configuration.primary_top_classifications():
                final_summit_types.append(summit_type)

            # if it's neither a primary or a primary top
            if not (is_primary_summit or is_primary_top):
                # determine the classification rank
                hierarchical_classifications = report_configuration.secondary_classifications()
                rank = hierarchical_classifications.loc[hierarchical_classifications == summit_type].index.values
                if len(rank):  # if it has a rank...
                    rank = rank[0]
                    # if this ranks higher (i.e. it has a lower number than the current winner), replace the
                    # classification with the new one
                    if rank >= highest_rank:
                        highest_rank = rank
                        final_summit_types.append(summit_type)

        result.update({summit_name: final_summit_types})

    return result


def reduce_classification_list_old(summit_classifications: Dict[str, List[str]]):
    """
    Given a dictionary of summit identifiers and their classifications, reduce the classifications so that only the most
    relevant classifications are returned for each summit. For example, Munros are by definition also Munro tops, but
    this makes for verbose and tautological reporting.

    :param summit_classifications:
    :return:
    """
    result = {}

    for idx, codes in summit_classifications.items():
        final_codes = []
        highest_rank = HEIRARCHICAL_CLASSIFICATIONS.index.max()

        is_primary = np.any([c in PRIMARY_CLASSIFICATIONS for c in codes])
        is_primary_top = np.any([c in PRIMARY_TOP_CLASSIFICATIONS for c in codes])

        for c in codes:
            # If this hill is a primary class, and this code is the primary class, always report
            if is_primary and c in PRIMARY_CLASSIFICATIONS:
                final_codes.append(c)

            # If this hill is a primary top class and not also a primary class and  this code is not the primary top
            # class
            if is_primary_top and not is_primary and c in PRIMARY_TOP_CLASSIFICATIONS:
                final_codes.append(c)

            # if it's neither a primary or a primary top
            if not (is_primary or is_primary_top):
                # determine the classification rank
                rank = HEIRARCHICAL_CLASSIFICATIONS.loc[HEIRARCHICAL_CLASSIFICATIONS == c].index.values
                if len(rank):  # if it has a rank...
                    rank = rank[0]
                    # if this ranks higher (i.e. it has a lower number than the current winner), replace the
                    # classification with the new one
                    if rank <= highest_rank:
                        highest_rank = rank
                        final_codes.append(c)

        result.update({idx: final_codes})

    return result


if __name__ == '__main__':
    munro = ReportedSummit(code='M', name='Munro', is_primary=True, is_top=False)
    munro_top = ReportedSummit(code='MT', name='Munro Top', is_primary=True, is_top=True)
    hump = ReportedSummit(code='H', name='Hump', is_primary=False, is_top=False)
    tump = ReportedSummit(code='T', name='Tump', is_primary=False, is_top=False)

    config = ReportConfiguration([munro, munro_top, hump, tump])
    print(config._build_df())
