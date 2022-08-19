from sugarscape_cg.model import SugarscapeCg
from mesa import batch_run
import pandas as pd
import numpy as np
from datetime import datetime

params={"width":50, "height":50, "initial_population":100, "initial_population_bt": range(0,201,50), "vento":range(0,6,1)}

experiments_per_parameter_configuration = 200

max_steps_per_simulation = 30

results=batch_run(
	SugarscapeCg,
	parameters=params,
	iterations=experiments_per_parameter_configuration,
	max_steps=max_steps_per_simulation,
	number_processes=1,
	data_collection_period=-1,
	display_progress=True,
)

results_df=pd.DataFrame(results)

now = str(datetime.now()).replace(":","-").replace(" ","-")

#results_df.to_csv(datetime.now().strftime("%Y_%m_%d_%H_%M_%S_")+"experimento.csv")

# define um prefixo para o nome do arquivo que vai guardar os dados do modelo
# contendo alguns dados dos experimentos
file_name_suffix = ("_iter_" + str(experiments_per_parameter_configuration)+
"_steps_" + str(max_steps_per_simulation)+ "_" +
now)

# define um prefixo para o nome para o arquivo de dados
model_name_preffix = "SugarscapePestsControlModel"

# define o nome do arquivo
file_name = model_name_preffix + "_model_data" + file_name_suffix + ".csv"

results_df.to_csv(file_name)
