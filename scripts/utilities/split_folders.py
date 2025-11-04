import splitfolders

splitfolders.ratio(
    input="datasets/mango_disease_dataset",
    output="datasets/mango_disease_dataset_split",
    seed=1337,
    ratio=(0.8, 0.2),
    move=False,
)

splitfolders.ratio(
    input="datasets/cotton_disease_dataset",
    output="datasets/cotton_disease_dataset_split",
    seed=1337,
    ratio=(0.8, 0.2),
    move=False,
)