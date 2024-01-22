from discord import Embed
from valve.source import a2s
from functions.servers import *
import requests

maps_tier = {"bkz_apricity_v3": 5, "bkz_blackrockshooter_vzp": 2, "bkz_bonus_z1": 2, "bkz_cakewalk": 3, "bkz_canadaszn": 2, "bkz_cauz_final": 2, "bkz_cauz_short": 4, "bkz_caves_go": 2, "bkz_cg_coldbhop": 2, "bkz_chillhop_go": 2, "bkz_dontstop": 3, "bkz_dydhop": 2, "bkz_evanstep": 4, "bkz_fapzor": 3, "bkz_fear4": 5, "bkz_goldbhop_csgo": 2, "bkz_goldbhop_v2go": 2, "bkz_greed": 2, "bkz_hellokitty_v2": 2, "bkz_impulse": 2, "bkz_iota_v3": 4, "bkz_itz_h25l": 2, "bkz_kartrider": 1, "bkz_levite_v2": 2, "bkz_lewlysex": 2, "bkz_measure": 2, "bkz_measure2_b03": 2, "bkz_nocturns_blue_gfix": 2, "bkz_pogo": 3, "bkz_sahara": 3, "bkz_underground_crypt_v3": 5, "bkz_uninspired_trash": 3, "bkz_volcanohop": 2, "bkz_zephyr_v2": 3, "kz_11342": 1, "kz_11735": 1, "kz_16pillars": 2, "kz_21loop_final_fix": 3, "kz_2fast": 3, "kz_2seasons_spring_final": 3, "kz_2seasons_winter_final": 4, "kz_420b": 2, "kz_4u_nature": 2, "kz_7in1": 2, "kz_8b1_brickngrass": 1, "kz_aaaa": 4, "kz_abandoned": 3, "kz_abstruse_od2": 4, "kz_acores": 2, "kz_adeline": 1, "kz_adv_cursedjourney": 3, "kz_adventure_v2": 2, "kz_aether_fix": 5, "kz_after_agitation_easy_fix": 2, "kz_afterlife": 6, "kz_ahful": 3, "kz_akrh_warehouse_v3": 2, "kz_alfama": 2, "kz_alfie": 5, "kz_alice_fix": 3, "kz_alien_city": 6, "kz_allure": 3, "kz_alouette_fix": 2, "kz_alpha": 5, "kz_alt_aztec": 2, "kz_alt_cargo": 1, "kz_altum_od": 5, "kz_amber_od": 3, "kz_ambition": 7, "kz_ancient_v3": 2, "kz_andromeda": 4, "kz_angina_final": 6, "kz_another_climb_map": 4, "kz_antharas": 5, "kz_antigeneric": 2, "kz_antimony": 4, "kz_antiquity": 2, "kz_anus": 2, "kz_apiisnotresponding": 1, "kz_arbitrary_words": 3, "kz_arcadium": 3, "kz_arcturus": 3, "kz_armored_core": 5, "kz_arrebol": 3, "kz_ascend_hv": 4, "kz_ashen": 2, "kz_asphyxiate": 2, "kz_asteroid_field_go": 2, "kz_atelectasis_sct": 4, "kz_athena": 3, "kz_atlantis_od3": 4, "kz_autobadges": 1, "kz_automata": 1, "kz_autumn_valley_fix": 3, "kz_auuughh": 5, "kz_avalon": 2, "kz_avoria": 5, "kz_aztec": 2, "kz_azure": 4, "kz_babycat_fix": 2, "kz_bacho": 3, "kz_backwards": 5, "kz_bananaysoda_v2": 5, "kz_banjo": 4, "kz_basicnoon": 2, "kz_basics_b02": 3, "kz_baxter": 1, "kz_beanguy_v2": 1, "kz_beginnerblock_go": 1, "kz_betapmaps": 4, "kz_betterdunjun": 2, "kz_beyond_fix": 3, "kz_bhop_algetic": 5, "kz_bhop_badges2": 5, "kz_bhop_badges3": 4, "kz_bhop_benchmark": 4, "kz_bhop_composure_f": 4, "kz_bhop_dusk_go": 4, "kz_bhop_essence": 4, "kz_bhop_exodus": 4, "kz_bhop_horseshit_9": 4, "kz_bhop_koki_niwa": 6, "kz_bhop_lego": 2, "kz_bhop_lj": 2, "kz_bhop_lucid": 4, "kz_bhop_mentalism": 5, "kz_bhop_monsterjam": 2, "kz_bhop_mosaic_od2": 3, "kz_bhop_northface": 4, "kz_bhop_nothing_go": 4, "kz_bhop_proxy_null": 3, "kz_bhop_rotebal3": 4, "kz_bhop_sakura": 3, "kz_bhop_skyworld_go": 4, "kz_bhop_slide": 6, "kz_bhop_watertemple": 2, "kz_bhop_zenith": 4, "kz_bible_black": 3, "kz_bigcastle": 3, "kz_bing": 2, "kz_binseebak": 3, "kz_bionic": 3, "kz_bir_dont_fix": 2, "kz_birrita_fix": 4, "kz_blackness": 6, "kz_blatherskite_v1": 3, "kz_blindcity_easy_fix": 3, "kz_blindcity_hard_final": 4, "kz_blockhardy2k": 3, "kz_blocks2006": 1, "kz_bloodline": 3, "kz_bluehop_mq": 4, "kz_bluerace_v2": 2, "kz_bluuu": 4, "kz_bombu": 3, "kz_boomblock": 1, "kz_bored": 3, "kz_bounce": 4, "kz_bozo": 6, "kz_breezeblocks": 1, "kz_brickblock_v2": 2, "kz_bridge17_fix": 2, "kz_brightblock": 1, "kz_buildings_final": 3, "kz_burnished": 3, "kz_byrem": 3, "kz_cabin_fix": 4, "kz_cajou": 2, "kz_camembert": 3, "kz_canyon": 2, "kz_carbon": 4, "kz_cargo": 2, "kz_carp_v2": 2, "kz_carpet": 5, "kz_cartooncastle_go": 1, "kz_cascade_v4": 3, "kz_castlehops_v3": 2, "kz_cataclysm": 3, "kz_catalyst_gfix": 3, "kz_catharsis_global": 2, "kz_caulis_v2": 1, "kz_cdr_myst": 2, "kz_cdr_rustenborg": 4, "kz_cdr_slash_final": 4, "kz_celestial": 3, "kz_cellblock_go2": 1, "kz_cereal": 3, "kz_cf_foliage": 7, "kz_cf_hestia": 3, "kz_cf_slide": 3, "kz_cf_snakeskin": 2, "kz_cg_brick_rmk": 3, "kz_cg_lighthops": 3, "kz_checkmate": 2, "kz_cheese": 2, "kz_cheetos_fix": 1, "kz_chessblock": 1, "kz_chillin": 3, "kz_chinablock": 3, "kz_chloroplast": 6, "kz_choka_fix": 5, "kz_chopchop": 4, "kz_christmas_fix": 2, "kz_chrysoprase": 1, "kz_chunky_peanut_butter": 2, "kz_citadel": 4, "kz_civilizations": 4, "kz_cliffhanger_go_global": 1, "kz_climb": 6, "kz_coastline_fix": 3, "kz_colorcode": 3, "kz_colors_v2": 3, "kz_combobreaker": 2, "kz_combohop_c02": 2, "kz_comboking7k": 3, "kz_comboya": 2, "kz_communityblock": 2, "kz_communityjump3": 4, "kz_comp_2022": 2, "kz_comp_global": 2, "kz_complex": 2, "kz_concept": 3, "kz_concretejungle": 2, "kz_conifer": 1, "kz_conrun_mq": 4, "kz_conrun_scrub": 3, "kz_conspiracy": 3, "kz_construction": 2, "kz_continuum": 6, "kz_coronado_fix": 3, "kz_correguachin_reisido": 3, "kz_cousucks": 2, "kz_cranking_the_hog": 1, "kz_crash_fix": 3, "kz_crate_delight_go": 1, "kz_cratespeed": 1, "kz_crypt_final": 3, "kz_crysis": 3, "kz_cthulhu": 6, "kz_cuberunfast": 2, "kz_custos": 5, "kz_cyb_adrenaline_fix": 3, "kz_cybersand": 1, "kz_d_decompile": 6, "kz_dabitu_fix2": 6, "kz_dakow": 1, "kz_dale": 1, "kz_daniel": 1, "kz_dank_stacks": 3, "kz_dark_fury": 1, "kz_date2": 3, "kz_de_bhop": 1, "kz_default": 3, "kz_dejavu": 3, "kz_delirium": 2, "kz_delphinium": 1, "kz_demonhours": 4, "kz_depot": 3, "kz_desolate": 2, "kz_dethroned": 5, "kz_devon": 2, "kz_diajonal": 3, "kz_difficultas_discendi": 3, "kz_dimensions_v1": 2, "kz_dishonest": 5, "kz_district_d01": 3, "kz_divert": 6, "kz_divided": 4, "kz_dontjump": 4, "kz_doubletake": 2, "kz_doveen": 2, "kz_drops_od": 3, "kz_drunkards": 6, "kz_dryness": 2, "kz_duality_v2": 3, "kz_dungeon": 2, "kz_dust": 3, "kz_dvn_cube_fixed": 2, "kz_dvn_dull": 2, "kz_dvn_redcarpet": 2, "kz_dyd_ladderjumps": 4, "kz_dystopia_h": 6, "kz_dzy_beyond_v2": 2, "kz_dzy_reach_v2": 3, "kz_ea_beneath": 1, "kz_echo": 2, "kz_edifice": 3, "kz_edp445": 2, "kz_egyptianbox": 3, "kz_egyptmap": 2, "kz_ehcivec": 2, "kz_eilrahc": 2, "kz_eimeristzurueck": 2, "kz_emblem": 2, "kz_emblem_bonus": 1, "kz_emptiness": 3, "kz_envy": 4, "kz_ephemeral": 2, "kz_epiphany_v2": 4, "kz_epusbridge": 2, "kz_erbajerb": 2, "kz_erinome": 3, "kz_eros_v2": 1, "kz_erratum_v2": 6, "kz_euclide_illusionary": 4, "kz_eudora": 4, "kz_eventide": 4, "kz_everything": 4, "kz_evilcorp": 4, "kz_excape": 3, "kz_excavate_b": 2, "kz_exemplum_fix": 3, "kz_exoteric": 1, "kz_experiment": 2, "kz_exps_cursedjourney": 3, "kz_ext_bblocks": 2, "kz_f_salted_banana": 4, "kz_fabrik": 2, "kz_failed_fastrun_rt": 5, "kz_farm_v2": 3, "kz_fas2map": 2, "kz_fastcombomap": 3, "kz_fastcombowombo_v2": 3, "kz_fastmap": 1, "kz_fatigue_v2": 2, "kz_fikablock": 1, "kz_final_ascension": 2, "kz_flabbergast": 4, "kz_floatingislands": 2, "kz_flying_rabbits": 1, "kz_foggywarehouse_v2": 2, "kz_forchi": 3, "kz_forestrace_go": 1, "kz_forgettable": 2, "kz_forgotten_fix": 4, "kz_free_ahful": 4, "kz_freezing_ridge": 2, "kz_frenzy": 2, "kz_frozen_go": 1, "kz_func_detail_v2": 6, "kz_fury": 2, "kz_fused": 3, "kz_futureblock": 3, "kz_galaxy_go2": 1, "kz_gallus": 3, "kz_gary": 2, "kz_gemischte_gefuehlslagen": 6, "kz_generic": 2, "kz_genesis": 2, "kz_gfy_blueberry": 4, "kz_gfy_devcastle": 4, "kz_gfy_final": 4, "kz_gfy_fortroca": 4, "kz_gfy_limit": 2, "kz_gfy_strawberry_": 4, "kz_gfy_tech": 4, "kz_ggsh": 5, "kz_ggurk": 2, "kz_ghat": 1, "kz_ghs": 1, "kz_giantbean": 1, "kz_gigablock_go": 1, "kz_gitgud_final": 4, "kz_gkd_v2": 1, "kz_glassesospa_v1": 2, "kz_glide": 2, "kz_gloom": 4, "kz_glow": 2, "kz_gluttony": 4, "kz_gobbledygook": 4, "kz_goldenroad": 2, "kz_goldentabby": 3, "kz_gonbe": 3, "kz_goodluck_p": 4, "kz_goquicklol_v2": 6, "kz_grass_hard": 4, "kz_green": 3, "kz_greyorgray": 2, "kz_gus_sct2": 5, "kz_gy_agitation": 4, "kz_haki_v2": 1, "kz_halicarnassus_fs": 3, "kz_hammer": 3, "kz_haste": 4, "kz_hate": 2, "kz_hb_3kliksphilip": 1, "kz_hb_anduu": 2, "kz_hb_bacon": 2, "kz_hb_fafnir": 5, "kz_hb_fyksen": 2, "kz_hb_lowlita": 4, "kz_hb_lrs": 4, "kz_hb_smieszneznaczki": 3, "kz_headbongo": 4, "kz_heatvents_mq": 3, "kz_heaven_od": 4, "kz_hek": 3, "kz_hellinashop": 3, "kz_hemochromatosis": 6, "kz_hideous": 3, "kz_high_socks": 5, "kz_highland": 2, "kz_hikari_od": 3, "kz_hillside": 1, "kz_hitech": 5, "kz_hoist_fix": 5, "kz_holdmyhand": 2, "kz_holmu1": 2, "kz_holyspace": 3, "kz_hope": 5, "kz_how2slide_fix": 3, "kz_huber": 1, "kz_hydromancy": 3, "kz_hypothermia": 2, "kz_hyroblock": 1, "kz_ickkck": 3, "kz_igneous": 2, "kz_illusion_gfix": 3, "kz_iluvprok_global": 2, "kz_imaginary_final": 5, "kz_innit": 3, "kz_insomnia_fix": 4, "kz_inspired": 4, "kz_intercourse!": 1, "kz_internatus": 4, "kz_invision": 3, "kz_island": 3, "kz_itz_transcendent": 3, "kz_itz_updown": 4, "kz_j2s_cupblock_go_fix2": 2, "kz_j2s_tetris_go": 2, "kz_j2s_westbl0ck": 1, "kz_janpu_final_fix": 1, "kz_jg_ditch": 3, "kz_johndoe": 2, "kz_jump_n_run": 2, "kz_kareful": 6, "kz_kat_colorblind": 3, "kz_kays": 1, "kz_kiwi_cod": 6, "kz_kiwi_hym": 7, "kz_kiwi_lars": 4, "kz_kiwideath": 7, "kz_kiwiexophoric": 7, "kz_kiwiexultation": 7, "kz_kiwifactory": 1, "kz_kiwimind": 6, "kz_kiwimirific": 1, "kz_kiwionerous": 2, "kz_kiwipsychosis": 7, "kz_kiwiqualia": 5, "kz_kiwislide": 7, "kz_kiwitech": 5, "kz_kiwiterror": 7, "kz_kiwitown": 2, "kz_kogamaostry": 2, "kz_kohze_sucks": 2, "kz_kukkojapallokidutus": 6, "kz_kzinga_fixed": 3, "kz_kzra_bars": 3, "kz_kzra_cliffy": 2, "kz_kzra_coast": 3, "kz_kzra_fustcaves": 2, "kz_kzra_greycliff": 2, "kz_kzra_hohum": 3, "kz_kzra_morath": 3, "kz_kzra_oddland": 1, "kz_kzra_rockloy": 3, "kz_kzra_rocky": 3, "kz_kzra_shortclimb_v2": 1, "kz_kzra_skaxis": 3, "kz_kzra_slidely": 4, "kz_kzra_slidepuf": 4, "kz_kzra_stonebhop": 2, "kz_kzra_stoneishbhop": 2, "kz_kzra_suhu": 1, "kz_kzra_undercastle": 2, "kz_kzra_voovblock": 3, "kz_kzra_whitesquare": 3, "kz_kzro_2boxes1room": 1, "kz_kzro_basalt": 2, "kz_kzro_beknowater": 1, "kz_kzro_brickstgrass_v2": 2, "kz_kzro_bronea": 2, "kz_kzro_cavehole": 3, "kz_kzro_cavernste_v2": 2, "kz_kzro_chairs": 4, "kz_kzro_cryscosrun": 2, "kz_kzro_darkhole": 1, "kz_kzro_excitedbhop": 2, "kz_kzro_fastcliff": 1, "kz_kzro_gohome": 2, "kz_kzro_greybrickbhop": 2, "kz_kzro_hardhoodoo": 7, "kz_kzro_hardvalley": 6, "kz_kzro_hexonay": 5, "kz_kzro_jaashs": 2, "kz_kzro_justgrab": 1, "kz_kzro_mountainbhop": 2, "kz_kzro_mountainhaya": 2, "kz_kzro_mountainroad": 5, "kz_kzro_mountainsein": 2, "kz_kzro_mountainsnow": 2, "kz_kzro_sekiseibhop": 3, "kz_kzro_shima_v2": 1, "kz_kzro_skyrocks": 6, "kz_kzro_slidesmear": 3, "kz_kzro_smallcanyon": 1, "kz_kzro_speedcavescape": 1, "kz_kzro_sunmountainset": 2, "kz_kzro_syotiles": 1, "kz_kzro_tamlair": 3, "kz_kzro_wallblocks": 2, "kz_kzro_whiterock": 2, "kz_kzro_yaruna": 1, "kz_kzse_aztectemple": 2, "kz_ladderall": 4, "kz_ladderdespair": 5, "kz_ladderhell_fix": 4, "kz_ladderhorror": 7, "kz_lair": 3, "kz_lastwork_p1": 4, "kz_lastwork_p2": 6, "kz_lavablock_global": 3, "kz_layercake": 1, "kz_lazy": 2, "kz_lego": 2, "kz_lego_two_redux_v3": 3, "kz_legoland": 3, "kz_leto_v2": 1, "kz_levels": 2, "kz_life_final": 3, "kz_linoleum": 3, "kz_lionharder": 7, "kz_lionheart": 6, "kz_list_gnida_v2": 5, "kz_littlerock_v2": 1, "kz_lmn": 1, "kz_loathe": 4, "kz_loftroofs": 3, "kz_longjumps_easy": 3, "kz_longjumps_space": 4, "kz_lookout": 2, "kz_lost_marketplace_gfix": 3, "kz_lovely": 5, "kz_lovesick": 3, "kz_ltt": 6, "kz_lume": 4, "kz_luonto": 1, "kz_lust": 2, "kz_luv_less": 4, "kz_mac": 1, "kz_machinery": 2, "kz_magus": 3, "kz_malignom_short": 4, "kz_man_everest_go_fix": 1, "kz_mandelbrot": 4, "kz_matilda_np": 2, "kz_maxine": 6, "kz_maya": 3, "kz_mazemerized": 6, "kz_meander": 4, "kz_mediumcastle": 3, "kz_megabhop_v2": 1, "kz_megalodon": 3, "kz_memento": 2, "kz_mescaline_f": 4, "kz_mess": 5, "kz_metalrun_global": 2, "kz_micropenis": 1, "kz_microwave": 3, "kz_mieszaneuczucia": 6, "kz_mike_v4": 2, "kz_milehigh": 3, "kz_minimal_combo": 2, "kz_minimalism": 2, "kz_minimountain_f": 1, "kz_modernvomit": 5, "kz_module": 4, "kz_monstrosity": 6, "kz_moon_fix": 7, "kz_moonlight": 3, "kz_moorerutan": 2, "kz_moorish": 2, "kz_morebricks_msq": 1, "kz_morestairs_msq": 3, "kz_motivated": 3, "kz_msp_comatose": 2, "kz_mushrruption_v8": 4, "kz_mz": 1, "kz_nassau": 2, "kz_nature_remaster": 1, "kz_natureblock_scte": 1, "kz_nb_final": 2, "kz_nbdy_maps": 6, "kz_nebula": 3, "kz_neon_portal": 4, "kz_neoncity_z": 6, "kz_nieh": 4, "kz_nightcastle": 4, "kz_nightfall": 3, "kz_nightmare_v2": 3, "kz_nix_od": 5, "kz_nomibo": 4, "kz_noobfort": 5, "kz_nuclear": 2, "kz_nyc_v1": 3, "kz_nymph": 4, "kz_oasis": 3, "kz_obsidian": 1, "kz_okaychamp": 5, "kz_oldstuff": 2, "kz_oloramasa": 6, "kz_olympus": 3, "kz_ominous2": 2, "kz_openspace": 3, "kz_opus": 2, "kz_orangejuice_v2": 3, "kz_orbolution_v2": 3, "kz_otakuroom": 3, "kz_overgrowth": 3, "kz_overjoyed": 2, "kz_owtetad": 1, "kz_p1": 6, "kz_paintball_tv_fix": 2, "kz_pamehcilc": 3, "kz_pamxul_wip": 4, "kz_pantheism_p02": 4, "kz_paradise": 2, "kz_peak_global": 2, "kz_pendulum": 6, "kz_perf_darkcave": 2, "kz_perfunctory": 2, "kz_persona_is_a_dictator": 3, "kz_persona_is_a_furry": 5, "kz_phamous": 1, "kz_pharaoh_csgo": 2, "kz_pharos_fix": 1, "kz_phaztec": 1, "kz_pianoclimb_go": 2, "kz_pineforest_v2": 3, "kz_piranha": 1, "kz_pixelrun_v2": 3, "kz_plains": 2, "kz_pollution": 3, "kz_porridge": 3, "kz_portal_fix": 2, "kz_portalclimb": 6, "kz_prefix_cliche": 3, "kz_prekeeper": 3, "kz_prima": 2, "kz_prismus": 2, "kz_procrastination_f": 6, "kz_progressive": 3, "kz_project": 2, "kz_prolific": 1, "kz_prototype": 4, "kz_psychosomatic": 6, "kz_psyk": 2, "kz_psytime_go": 2, "kz_purgatory": 6, "kz_quadrablock": 3, "kz_quadrant_fix": 3, "kz_question": 4, "kz_quick7_v2": 2, "kz_quicksand": 2, "kz_quickshot": 1, "kz_quixotic": 3, "kz_railings": 3, "kz_rainrun_kn_f": 1, "kz_rarkovosis": 6, "kz_rcn_impermanence": 2, "kz_rcn_optimisery": 3, "kz_reach_v2": 3, "kz_rectangle": 4, "kz_redemption_csgo": 2, "kz_redline": 1, "kz_refract": 2, "kz_refuge": 3, "kz_remedy_v2": 2, "kz_research": 3, "kz_retreat": 2, "kz_retribution_v2_final": 6, "kz_return": 4, "kz_reverse": 4, "kz_rise": 3, "kz_rlk": 5, "kz_rockclimb": 2, "kz_rockjungle_v2": 3, "kz_rocks_global": 1, "kz_roman": 3, "kz_rompenutrias_asheglado": 4, "kz_ronja": 1, "kz_rumzor": 2, "kz_rush2sk8": 4, "kz_rush2suck": 1, "kz_sanctuary": 1, "kz_sandbox": 7, "kz_sandstone_mq": 1, "kz_sandstorm_ez": 3, "kz_sandyhill_hoc": 3, "kz_sc_collapse": 5, "kz_sc_ruins": 5, "kz_sc_surf": 5, "kz_scicret": 6, "kz_scum": 4, "kz_sendhelp_final": 4, "kz_serenity": 2, "kz_shaft_fix": 2, "kz_shark_gc": 4, "kz_shell": 6, "kz_shortcut_tx": 3, "kz_signs_v2": 2, "kz_silk": 2, "kz_simple_sp": 5, "kz_simplejourney": 4, "kz_simplicity_v2": 1, "kz_simplyhard": 5, "kz_sky_lake": 4, "kz_skybridge": 3, "kz_skyhotel": 2, "kz_skytower": 2, "kz_slate": 3, "kz_slide_0x7_n1m0": 4, "kz_slide_arid": 7, "kz_slide_bozo": 3, "kz_slide_cave": 4, "kz_slide_concrete": 4, "kz_slide_deee": 6, "kz_slide_dydanhomon": 4, "kz_slide_era": 5, "kz_slide_isnt_kz": 5, "kz_slide_kissa": 3, "kz_slide_koira": 3, "kz_slide_leto": 3, "kz_slide_or_dont": 3, "kz_slide_pallokala": 3, "kz_slide_pisauva": 4, "kz_slide_piss": 4, "kz_slide_purple_x": 5, "kz_slide_red": 6, "kz_slide_rovod": 5, "kz_slide_svn_extreme": 6, "kz_slide_svn_temple": 4, "kz_slide_vaahtera": 4, "kz_slide_wasteland": 5, "kz_slidebober": 6, "kz_slidemap_fix": 6, "kz_sloth": 1, "kz_slowerrun": 7, "kz_slowrun_global_fix": 6, "kz_slumpfrageous": 2, "kz_smallcastle": 3, "kz_smallmap": 3, "kz_smb": 1, "kz_sn_desert": 3, "kz_snowman_v2": 2, "kz_solidarity_v2": 3, "kz_something": 1, "kz_sonder": 2, "kz_souljaboy": 2, "kz_south": 4, "kz_sp1_aoirobhop": 2, "kz_sp1_behold": 3, "kz_sp1_bloodyljs_v2": 6, "kz_sp1_blueconcrete": 2, "kz_sp1_candles": 2, "kz_sp1_castaway": 2, "kz_sp1_driedblocks": 3, "kz_sp1_greenconcrete": 3, "kz_sp1_greyconcrete": 2, "kz_sp1_greyhollowrock": 2, "kz_sp1_hallwaybhop": 3, "kz_sp1_hiragana": 4, "kz_sp1_icecave": 5, "kz_sp1_inverseblocks": 2, "kz_sp1_kansopyon": 2, "kz_sp1_katakana": 5, "kz_sp1_kyuubisroom": 1, "kz_sp1_parallelblocks": 2, "kz_sp1_perf2win": 2, "kz_sp1_purpose": 3, "kz_sp1_redbrickbhop": 2, "kz_sp1_redconcrete": 2, "kz_sp1_rengapyon": 3, "kz_sp1_rockcanyonblocks": 2, "kz_sp1_saishuu": 4, "kz_sp1_shouryokou": 2, "kz_sp1_siedlungclimb": 2, "kz_sp1_spreadblocks": 2, "kz_sp1_strafechampion": 7, "kz_sp1_uchuunookuheki": 2, "kz_sp1_vines": 5, "kz_sp1_whiteblocks": 2, "kz_sp1_xmas2021": 3, "kz_spaceladders_v2": 2, "kz_spacemario_h": 6, "kz_spacemario_xt": 7, "kz_spacus": 3, "kz_spire": 2, "kz_spiritblockv2": 1, "kz_splifff": 2, "kz_splopkopsc_loverick": 2, "kz_sqrdsucks": 2, "kz_stepblock": 3, "kz_stepup": 3, "kz_strafehop_fix": 5, "kz_stranded": 4, "kz_streetblock": 2, "kz_structures": 3, "kz_strun_mq": 3, "kz_stuff_final": 2, "kz_sukblock_v2_fixed": 1, "kz_summercliff2_go": 1, "kz_sunstone": 2, "kz_suomi": 4, "kz_superstructure": 3, "kz_surf_abaddon": 6, "kz_surf_ace": 3, "kz_surf_blue": 4, "kz_surf_kim_hana_gl": 4, "kz_surf_larry": 6, "kz_swamped_v3": 4, "kz_sxb_biewan": 5, "kz_sxb_despacito": 5, "kz_sxb_makabaka": 6, "kz_sxb_poi": 4, "kz_sxb_remake": 5, "kz_sxb_xbcmzl": 6, "kz_symbiosis_final": 3, "kz_symmetry": 2, "kz_synergy_ez": 3, "kz_synergy_x": 5, "kz_synthesis_v2": 3, "kz_sz_goldenbean": 3, "kz_talltreeforest_v3": 3, "kz_talmaniac": 3, "kz_tangent": 3, "kz_technical_difficulties": 5, "kz_techtonic_v2_ldr": 5, "kz_tense": 7, "kz_terablock": 1, "kz_theaquila": 4, "kz_thinkblock": 2, "kz_thrombosis": 6, "kz_timescape_zero": 3, "kz_tmnf_e05": 2, "kz_tomb_fix": 1, "kz_toonadventure_go": 2, "kz_toonrun_final": 2, "kz_toughluck_fix": 2, "kz_tour_de_nuke_rt": 2, "kz_tq": 3, "kz_tradeblock_go": 1, "kz_tranquillity": 2, "kz_trashsurf": 4, "kz_trazodon_fix": 4, "kz_tribute": 4, "kz_tron_global": 3, "kz_twiivo": 2, "kz_twilight_od": 3, "kz_twister": 3, "kz_unity_collab": 3, "kz_unity_u01": 2, "kz_unknownspace": 2, "kz_unmake": 7, "kz_unnamed": 5, "kz_variety_fix": 4, "kz_vci_apprentice": 2, "kz_verv3_gg": 3, "kz_victoria": 2, "kz_village": 3, "kz_violet_fix": 1, "kz_vittu_mika_persse": 3, "kz_vnl_crimdaddy": 4, "kz_vnl_crimdaughter": 3, "kz_vnl_crimson": 4, "kz_vnl_crimstmas": 3, "kz_void": 3, "kz_w1_holiday": 7, "kz_wafflehouse_easy": 6, "kz_wafflehouse_hard": 7, "kz_wafflehouse_x": 7, "kz_warehouse": 2, "kz_wasabi": 2, "kz_waterhole": 3, "kz_weebfactory_censored": 2, "kz_weightless": 2, "kz_wetbricks": 2, "kz_whatever_v2": 3, "kz_whereyoufrom": 2, "kz_why": 4, "kz_winterize": 4, "kz_woodstock_v2": 1, "kz_woodstonegrass_final": 2, "kz_woodworld": 2, "kz_xand": 1, "kz_xiaobitu": 4, "kz_xmas2008": 1, "kz_xmas2009": 1, "kz_xmas2020": 2, "kz_xmas2022": 2, "kz_xtremeblock_v2": 2, "kz_yanse": 4, "kz_yes": 3, "kz_yoink": 4, "kz_za_tileblock": 1, "kz_zaloopazxc": 6, "kz_zhongbitu": 6, "kz_zhop_freestyle": 4, "kz_zhop_function3": 4, "kz_zhop_son_fix": 3, "kz_ziggurath_final": 4, "kz_zoomer_fix": 4, "kz_zxp_final4": 4, "kz_zxp_interstellar_v2": 3, "kz_zxp_undia": 4, "kzpro_concrete_c02": 4, "kzpro_gull_pidr_reborn": 5, "kzpro_justrun_sp": 3, "kzpro_psilocybin": 6, "kzpro_wrath": 7, "skz_bananaysoda_2": 5, "skz_makalaka": 6, "skz_map": 1, "skz_odious_v2": 6, "skz_pride": 3, "skz_sati": 5, "skz_sequence_shot": 5, "vnl_cat": 4, "vnl_caverun": 4, "vnl_farewell_fix": 5, "vnl_invasion": 4, "vnl_lea": 3, "vnl_ll_nuke": 2, "vnl_oy_lj": 6, "vnl_sewers": 7, "vnl_simplebrickrooms": 5, "vnl_slidegarden": 3, "vnl_undefined": 3, "vnl_whiterun": 1, "xc_alt_nephilim": 3, "xc_cliffjump_fix": 1, "xc_dreamland2": 3, "xc_dtt_nasty_go": 1, "xc_fox_shrine_japan_fr": 3, "xc_karo4": 3, "xc_lucid_global": 2, "xc_minecraft2_global": 3, "xc_minecraft3_global": 2, "xc_minecraft4": 2, "xc_nephilim": 3, "xc_powerblock_rc1": 2, "xc_secret_valley_global_fix": 3, "xc_skycastle": 2, "xc_supermario_go_gfix": 2, "xc_umbrella_global": 3}


# Functions
def format_seconds(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours >= 10:
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    elif hours >= 1:
        return "{}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    else:
        return "{:02}:{:02}".format(int(minutes), int(seconds))


def query_server_embed(server: Server) -> Embed:
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            try:
                tier = maps_tier[info['map']]
            except Exception:
                print("Can not get server tier")
                tier = 'T0'

            players_str = ''
            for player in players['players']:
                players_str += f"\n{player['name']} - {format_seconds(player['duration'])}"

            embed = Embed(
                title=f'{info['map']} - T{tier}',
                description=players_str,
                color=0x58b9ff,
            )

            embed.set_author(name=f"{info['server_name']}    {info['player_count']}/{info['max_players']}")
            embed.url = f'http://redirect.axekz.com/{server.id}'
            embed.set_image(url=f"https://raw.githubusercontent.com/KZGlobalTeam/map-images/master/images/{info['map']}.jpg")

            return embed
    except Exception as e:
        print(f"Error: {e}")
        return Embed(
            title="Error"
        )


def query_server_details(server: Server) -> str:  # NOQA
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            try:
                tier = maps_tier[info['map']]
            except Exception:
                tier = 'T0'

        content = (f"Server: {info['server_name']}"
                   f"\nMap: {info['map']} T{tier}"
                   f"\nPlayers: {info['player_count']}/{info['max_players']}")
        if players:
            content += "\nPlayer List:"
            for player in players['players']:
                content += f"\n{player['name']}\t - Time: {format_seconds(player['duration'])}"

        return content
    except Exception as e:
        print(f"Error: {e}")


def query_server_simple(server):  # NOQA
    try:
        with a2s.ServerQuerier((server.ip, server.port)) as s:
            info = s.info()
            players = s.players()
            try:
                tier = maps_tier[info['map']]
            except Exception:
                tier = 'T0'
        content = (f"[**AXE GOKZ {server.name_short[:2]}#{server.name_short[2]}**](http://redirect.axekz.com/{server.id}):  "
                   f"*{info['map']}* "
                   f'**T{tier}**  '
                   f"{info['player_count']}/{info['max_players']}\n")

        if players:
            players_str = ''
            for player in players['players']:
                content += f"`{player['name']}`  "
                players_str += f"`{player['name'].replace('`', '')}`"
            if players_str != '':
                content += "\n"
        return content
    except Exception as e:
        print(f"Error: {e}")
        return ""


def fetch_map_tier(map_name: str):
    try:
        response = requests.get('https://kztimerglobal.com/api/v2.0/maps/name/' + map_name)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the response as JSON (assuming the API returns JSON)
            data = response.json()
            return data['difficulty']
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None


def query_all_servers() -> str:
    info_data = ''
    for s in SERVER_LIST:
        info_data += query_server_simple(s)

    return info_data


if __name__ == "__main__":
    rs = query_all_servers()
    print(rs, type(rs))