# #!/usr/bin/env python3
# import glob
# import os

# from ament_index_python import get_package_share_directory
# from dynamic_stack_decider import DSD


# def test_dsd_valid():
#     # Create empty blackboard
#     dummy_blackboard = object
#     # Create DSD
#     dsd = DSD(dummy_blackboard())

#     # Find install path of package where the dsd and python files are located
#     dirname = get_package_share_directory("bitbots_body_behavior")

#     # Register actions and decisions
#     dsd.register_actions(os.path.join(dirname, "actions"))
#     dsd.register_decisions(os.path.join(dirname, "decisions"))

#     # Load all dsd files to check if they are valid\
#     for dsd_file in glob.glob(os.path.join(dirname, "*.dsd")):
#         dsd.load_behavior(dsd_file)
