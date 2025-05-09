import os
import glob
import pandas as pd
import xarray as xr

def extract_xco2_valid_points(file_path):
    try:
        ds = xr.open_dataset(file_path)
        valid = ds["xco2_quality_flag"].values == 0
        date_str = os.path.basename(file_path).split("-")[0]
        date = pd.to_datetime(date_str, format="%Y%m%d")

        return pd.DataFrame({
          "date": date,
          "latitude": ds["latitude"].values[valid],
          "longitude": ds["longitude"].values[valid],
          "xco2": ds["xco2"].values[valid], 
        })
    except Exception as e:
        print(f"⚠️ Erreur avec {file_path} : {e}")
        return pd.DataFrame()

# 📁 Dossier contenant les .nc
folder_path = "./"  # ⬅️ à adapter selon ton cas
output_path_all = "./xco2_2021_full.csv"
output_path_monthly = "./xco2_2021_monthly_means.csv"

# 📂 Récupérer tous les fichiers
file_paths = sorted(glob.glob(os.path.join(folder_path, "*.nc")))

# 📦 Fusionner toutes les données
all_data = pd.concat([extract_xco2_valid_points(f) for f in file_paths], ignore_index=True)

# 💾 Sauvegarde du fichier complet
all_data.to_csv(output_path_all, index=False)

# 📊 Calculer les moyennes mensuelles
all_data["month"] = all_data["date"].dt.to_period("M")
monthly_mean = all_data.groupby("month")["xco2"].mean().reset_index()
monthly_mean.columns = ["month", "xco2_mean"]

# 💾 Sauvegarde des moyennes mensuelles
monthly_mean.to_csv(output_path_monthly, index=False)

print(f"✅ Données fusionnées enregistrées : {output_path_all}")
print(f"📊 Moyennes mensuelles enregistrées : {output_path_monthly}")
