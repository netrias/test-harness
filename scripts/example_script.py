import argparse
import datetime as dt
import os
import importlib
import types
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from test_harness_class import TestHarness

from th_model_instances.hamed_models.random_forest_classification import random_forest_classification

# SET PATH TO DATA FOLDER IN LOCALLY CLONED `versioned-datasets` REPO HERE:
# Note that if you clone the `versioned-datasets` repo at the same level as where you cloned the `protein-design` repo,
# then you can use VERSIONED_DATASETS = os.path.join(Path(__file__).resolve().parents[3], 'versioned-datasets/data')
VERSIONED_DATA = os.path.join(Path(__file__).resolve().parents[3], 'versioned-datasets/data')
print("Path to data folder in the locally cloned versioned-datasets repo was set to: {}".format(VERSIONED_DATA))
print()

PWD = os.getcwd()
HERE = os.path.realpath(__file__)
PARENT = os.path.dirname(HERE)
RESULTSPATH = os.path.dirname(PARENT)
print("PWD:", PWD)
print("HERE:", HERE)
print("PARENT:", PARENT)
print("RESULTSPATH:", RESULTSPATH)
print()


def main():
    # Reading in data from versioned-datasets repo.
    # This will only work if you have cloned versioned-datasets at the same level as protein-design.
    # Using the versioned-datasets repo is probably what most people want to do, but you can read in your data however you like.
    combined_data = pd.read_csv(os.path.join(VERSIONED_DATA, 'protein-design/aggregated_data/all_libs_cleaned.v1.aggregated_data.csv'),
                                comment='#', low_memory=False)

    # Using a subset of the data for testing, and making custom train/test splits.
    data_RD_16k = combined_data.loc[combined_data['dataset_original'] == 'Rocklin'].copy()
    train1, test1 = train_test_split(data_RD_16k, test_size=0.2, random_state=5,
                                     stratify=data_RD_16k[['topology', 'dataset_original']])

    # Grouping Dataframe read in for leave-one-out analysis.
    grouping_df = pd.read_csv(os.path.join(VERSIONED_DATA, 'protein-design/metadata/protein_groupings_by_uw.metadata.csv'), comment='#',
                              low_memory=False)
    grouping_df['dataset'] = grouping_df['dataset'].replace({"longxing_untested": "t_l_untested",
                                                             "topmining_untested": "t_l_untested"})

    feature_cols_to_normalize = ['AlaCount', 'T1_absq', 'T1_netq', 'Tend_absq', 'Tend_netq', 'Tminus1_absq',
                                 'Tminus1_netq', 'abego_res_profile', 'abego_res_profile_penalty',
                                 'avg_all_frags', 'avg_best_frag', 'bb', 'buns_bb_heavy', 'buns_nonheavy',
                                 'buns_sc_heavy', 'buried_minus_exposed', 'buried_np', 'buried_np_AFILMVWY',
                                 'buried_np_AFILMVWY_per_res', 'buried_np_per_res', 'buried_over_exposed',
                                 'chymo_cut_sites', 'chymo_with_LM_cut_sites', 'contact_all',
                                 'contact_core_SASA', 'contact_core_SCN', 'contig_not_hp_avg',
                                 'contig_not_hp_avg_norm', 'contig_not_hp_internal_max', 'contig_not_hp_max',
                                 'degree', 'dslf_fa13', 'entropy', 'exposed_hydrophobics',
                                 'exposed_np_AFILMVWY', 'exposed_polars', 'exposed_total', 'fa_atr',
                                 'fa_atr_per_res', 'fa_dun_dev', 'fa_dun_rot', 'fa_dun_semi', 'fa_elec',
                                 'fa_intra_atr_xover4', 'fa_intra_elec', 'fa_intra_rep_xover4',
                                 'fa_intra_sol_xover4', 'fa_rep', 'fa_rep_per_res', 'fa_sol', 'frac_helix',
                                 'frac_loop', 'frac_sheet', 'fxn_exposed_is_np', 'hbond_bb_sc', 'hbond_lr_bb',
                                 'hbond_lr_bb_per_sheet', 'hbond_sc', 'hbond_sr_bb', 'hbond_sr_bb_per_helix',
                                 'helix_sc', 'holes', 'hphob_sc_contacts', 'hphob_sc_degree', 'hxl_tors',
                                 'hydrophobicity', 'largest_hphob_cluster', 'lk_ball', 'lk_ball_bridge',
                                 'lk_ball_bridge_uncpl', 'lk_ball_iso', 'loop_sc', 'mismatch_probability',
                                 'n_charged', 'n_hphob_clusters', 'n_hydrophobic', 'n_hydrophobic_noA',
                                 'n_polar_core', 'n_res', 'nearest_chymo_cut_to_Cterm',
                                 'nearest_chymo_cut_to_Nterm', 'nearest_chymo_cut_to_term',
                                 'nearest_tryp_cut_to_Cterm', 'nearest_tryp_cut_to_Nterm',
                                 'nearest_tryp_cut_to_term', 'net_atr_net_sol_per_res', 'net_atr_per_res',
                                 'net_sol_per_res', 'netcharge', 'nres', 'nres_helix', 'nres_loop', 'nres_sheet',
                                 'omega', 'one_core_each', 'p_aa_pp', 'pack', 'percent_core_SASA',
                                 'percent_core_SCN', 'pro_close', 'rama_prepro', 'ref', 'res_count_core_SASA',
                                 'res_count_core_SCN', 'score_per_res', 'ss_contributes_core',
                                 'ss_sc', 'sum_best_frags', 'total_score', 'tryp_cut_sites', 'two_core_each',
                                 'worst6frags', 'worstfrag']

    # TestHarness usage starts here, all code before this was just data input code.
    th = TestHarness(output_path=RESULTSPATH)

    rf_classification_model = random_forest_classification()

    th.add_custom_runs(test_harness_models=rf_classification_model, training_data=train1, testing_data=test1,
                       data_and_split_description="just testing things out!",
                       cols_to_predict=['stabilityscore_2classes', 'stabilityscore_calibrated_2classes'],
                       feature_cols_to_use=feature_cols_to_normalize, normalize=True, feature_cols_to_normalize=feature_cols_to_normalize,
                       feature_extraction=False, predict_untested_data=False)

    th.add_leave_one_out_runs(test_harness_models=rf_classification_model, data=data_RD_16k, data_description="data_RD_16k",
                              grouping=grouping_df, grouping_description="grouping_df", cols_to_predict='stabilityscore_2classes',
                              feature_cols_to_use=feature_cols_to_normalize, normalize=True,
                              feature_cols_to_normalize=feature_cols_to_normalize, feature_extraction=False)

    th.execute_runs()


if __name__ == '__main__':
    main()
