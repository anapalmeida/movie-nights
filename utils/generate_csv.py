def generate_csv(obejct, output_file_path):
    obejct.to_csv(output_file_path, index=False)

    return obejct
