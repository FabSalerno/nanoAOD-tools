import h5py
import tensorflow as tf
import numpy as np
import json
import os
import multiprocessing 
import time
import tqdm


####### PARAMETERS #######
nPFCs=60
model_name="CNN_2D"
cut=0
#LSTM, CNN, CNN_2D, CNN_2D_prova, transformer, 
path_to_folder= f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_{nPFCs}_boosted_{model_name}_{cut}_pt"
# training set to update
inFile             = f"/eos/user/f/fsalerno/framework/MachineLearning/TrainingSet_PF_folder/Full/trainingSet.h5"
# updated training set
outFile            = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_2/Training_PF_2022_2_jets_{nPFCs}_boosted_{model_name}_{cut}_pt/trainingSet_mp.h5"
# model to load
model_to_load      = f"//eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_0_pt/Training_PF_2022_1_jets_{nPFCs}_boosted_{model_name}_{cut}_pt/model.h5"  
# score thresholds
score_thresholds   = f"/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_{nPFCs}_boosted_0_pt/Training_PF_2022_1_jets_{nPFCs}_boosted_{model_name}_{cut}_pt/score_thresholds_{nPFCs}_{model_name}_{cut}_pt.json"
thr                = "10%"                                        # threshold to select top candidates
batch_size = 1000
# Create directory if it doesn't exist
os.makedirs(path_to_folder, exist_ok=True)
print(f"Directory {path_to_folder} ready")

# Load threshold
with open(score_thresholds, "r") as fjson:
    thresholds = json.load(fjson)
thresholds = thresholds[thr]["thr"]
print(f"Using threshold: {thresholds}")

# Load model
#model = tf.keras.models.load_model(model_to_load)


def process_category(args):
    """
    Worker per processare una singola categoria (sottogruppo f[c][cat]).
    Apre il file in lettura, carica il modello, processa i dati a batch,
    applica il filtro e concatena i risultati.
    Ritorna una tupla:
      (group_key, cat_key, jets_filtered, fatjets_filtered, PFC_filtered, top_filtered, labels_filtered, num_samples)
    """
    inFile, group_key, cat_key, batch_size, thresholds, model_to_load = args

    # Carica il modello all'interno del processo figlio (evita problemi di pickling)
    model = tf.keras.models.load_model(model_to_load)

    with h5py.File(inFile, "r") as f:
        cat = f[group_key][cat_key]
        jets_dataset    = cat["jets"]
        fatjets_dataset = cat["fatjets"]
        PFC_dataset     = cat["PFC"]
        top_dataset     = cat["top"]
        labels_dataset  = cat["labels"]
        num_samples = jets_dataset.shape[0]
        true_tops_total = np.sum(labels_dataset == 1)
        false_tops_total = np.sum(labels_dataset == 0)

        jets_filtered_list    = []
        fatjets_filtered_list = []
        PFC_filtered_list     = []
        top_filtered_list     = []
        labels_filtered_list  = []

        for i in range(0, num_samples, batch_size):
            X_jet    = jets_dataset[i : i + batch_size]
            X_fatjet = fatjets_dataset[i : i + batch_size]
            X_PFC    = PFC_dataset[i : i + batch_size]
            X_top    = top_dataset[i : i + batch_size]
            y        = labels_dataset[i : i + batch_size]

            # Calcola il punteggio usando il modello
            score = model({"jet": X_jet, "fatjet": X_fatjet, "PFC": X_PFC, "top": X_top}).numpy().flatten()
            mask = score > thresholds

            jets_filtered_list.append(X_jet[mask])
            fatjets_filtered_list.append(X_fatjet[mask])
            PFC_filtered_list.append(X_PFC[mask])
            top_filtered_list.append(X_top[mask])
            labels_filtered_list.append(y[mask])

            print(f"Category {group_key}/{cat_key}, batch {i}-{i+batch_size}: {X_jet[mask].shape[0]} selected tops")

        # Concatenazione finale dei batch filtrati
        jets_filtered    = np.concatenate(jets_filtered_list, axis=0) if jets_filtered_list else np.array([])
        fatjets_filtered = np.concatenate(fatjets_filtered_list, axis=0) if fatjets_filtered_list else np.array([])
        PFC_filtered     = np.concatenate(PFC_filtered_list, axis=0) if PFC_filtered_list else np.array([])
        top_filtered     = np.concatenate(top_filtered_list, axis=0) if top_filtered_list else np.array([])
        labels_filtered  = np.concatenate(labels_filtered_list, axis=0) if labels_filtered_list else np.array([])

    return (group_key, cat_key, jets_filtered, fatjets_filtered, PFC_filtered, top_filtered, labels_filtered, num_samples, true_tops_total, false_tops_total)

def main():
    # Prepara la lista dei task: ogni task processa una categoria (sottogruppo)
    tasks = []
    with h5py.File(inFile, "r") as f:
        for c in f.keys():
            for cat in f[c].keys():
                tasks.append((inFile, c, cat, batch_size, thresholds, model_to_load))

    # Processa le categorie in parallelo usando multiprocessing
    with multiprocessing.Pool() as pool:
        results = list(tqdm.tqdm(pool.imap_unordered(process_category, tasks),
                                 total=len(tasks),
                                 desc="Processing categories"))

    # Salva i dati filtrati nel file di output HDF5 (come prima)
    with h5py.File(outFile, "w") as f_out:
        for res in results:
            group_key, cat_key, jets_filtered, fatjets_filtered, PFC_filtered, top_filtered, labels_filtered, _ = res
            grp = f_out.create_group(f"{group_key}/{cat_key}")
            grp.create_dataset("jets", data=jets_filtered, compression="gzip")
            grp.create_dataset("fatjets", data=fatjets_filtered, compression="gzip")
            grp.create_dataset("PFC", data=PFC_filtered, compression="gzip")
            grp.create_dataset("top", data=top_filtered, compression="gzip")
            grp.create_dataset("labels", data=labels_filtered, compression="gzip")
            print(f"Saved {jets_filtered.shape[0]} tops in {group_key}/{cat_key}")

    print(f"Dataset saved in {outFile}")

    # Costruisci il dizionario di riepilogo per il JSON:
    # per ogni categoria, salva il numero totale di eventi che hanno passato la selezione
    # e il numero totale di top presenti.
    summary_dict = {}
    for res in results:
        group_key, cat_key, _, _, _, top_filtered, labels_filtered, num_samples, true_tops_total, false_tops_total = res
        if group_key not in summary_dict:
            summary_dict[group_key] = {}
        summary_dict[group_key][cat_key] = {
            "n_selected_tops": int(top_filtered.shape[0]),
            "n_selected_true_tops": int(np.sum(labels_filtered == 1)),
            "n_selected_false_tops": int(np.sum(labels_filtered == 0)),
            "n_total_tops": int(num_samples),
            "n_total_true_tops": int(true_tops_total),
            "n_total_false_tops": int(false_tops_total)


        }

    # Salva il riepilogo in un unico file JSON
    json_filename = os.path.join(path_to_folder, "selected_tops_summary.json")
    with open(json_filename, "w") as jf:
        json.dump(summary_dict, jf, indent=4)
    print(f"JSON summary saved: {json_filename}")

if __name__ == "__main__":
    main()