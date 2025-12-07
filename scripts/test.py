import os
import re
from pathlib import Path

# List of filenames
filenames = [
    "hopper_medium_4_4_256_60_0.99_100_25-09-01-19-46-46_500.pt",
    "hopper_medium_4_4_256_60_0.99_100_25-09-01-19-46-46_50.pt",
    "hopper_medium_4_4_256_60_0.99_100_25-09-01-19-46-46_450.pt",
    "hopper_medium_4_4_256_60_0.99_100_25-09-01-19-46-46_400.pt",
    "hopper_medium_4_4_256_60_0.99_100_25-09-01-19-46-46_350.pt",
    "hopper_medium_4_4_256_60_0.99_100_25-09-01-19-46-46_300.pt",
    "hopper_medium_4_4_256_60_0.99_100_25-09-01-19-46-46_250.pt",
    "hopper_medium_4_4_256_60_0.99_100_25-09-01-19-46-46_200.pt",
    "hopper_medium_4_4_256_60_0.99_100_25-09-01-19-46-46_150.pt",
    "hopper_medium_4_4_256_60_0.99_100_25-09-01-19-46-46_100.pt",
    "hopper_medium-replay_4_4_256_60_0.99_100_25-09-02-15-43-30_50.pt",
]

# Directory where files will be created
output_dir = "/opt/Elastic-DT/scripts/dt_runs"
#os.makedirs(output_dir, exist_ok=True)

# Create empty files
#for fname in filenames:
#    filepath = os.path.join(output_dir, fname)
#    with open(filepath, "w") as f:
#        pass  # creates an empty file
#
#print(f"Created {len(filenames)} empty files in '{output_dir}'")


def get_eval_checkpoints(chk_pt_dir, regex_pattern):

    pattern = re.compile(regex_pattern)
    grouped = {}

    for file in os.listdir(chk_pt_dir):
        if not pattern.match(file):
            continue
        
        # Example filename: dataset1_step=1000.ckpt
        # Extract dataset + step
        dataset = file.split("_")[1]  # adjust depending on naming scheme
        step_match = re.findall(r"[0-9]+", file)
        step = int(step_match[-1]) if step_match else -1
        #print('step : ', step, 'dataset : ',dataset )

        grouped.setdefault(dataset, []).append((step, file))

    # sort each group by step
    for dataset in grouped:
        grouped[dataset].sort(key=lambda x: x[0])
#
    return grouped

def eval_checkpoints(grouped):
    """
    Example evaluation loop using file iter as step for table naming.
    """
    for dataset, ckpts in grouped.items():
        for i, (step, ckpt_path) in enumerate(ckpts):
            table_name = f"{dataset}_iter{i}"
            print(f"{step} Evaluating {ckpt_path} -> Table: {table_name}")
            # TODO: call your evaluation function here

chk_pt_dir = "/opt/Elastic-DT/scripts/dt_runs/"
regex = "hopper_medium_*" # e.g. r".*step=\d+\.ckpt"
grouped = get_eval_checkpoints(chk_pt_dir, regex)

eval_checkpoints(grouped)

