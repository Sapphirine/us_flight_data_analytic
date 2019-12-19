# EECS E6983 Project (19 Fall)
## US Flight analysis and visualization
### Author: Yue Luo(yl4003), Lingsong Gao(lg3018), Yuhao Cao(yc3518)


1.To run relevant local code, use `jupyter notebook` and use the code `part1.py`, `part2.py` and `part3.py`. You may need to download the data from this [Kaggle Page](https://www.kaggle.com/usdot/flight-delays) for the three csv files. `part1.py` is for data analysis and `part2.py` is for map visualization, `part3.py` is for delay analysis and prediction model

Possible packages you may need: basemap, plotly, pandas, matplotlib, numpy, sklearn, json...


2.To deploy web application it on GCP, create a normal VM instance and set up firewall rules.
Connect to GCP VM by:
`gcloud compute ssh --project <proj-id> --zone <zone> <instance-id>`

You need to save the three csv as `bigquery` tables in GCP.

Install Django. Clone this repo, get into `map_vis` and run the server by:
`python3 manage.py runserver 0.0.0.0:8000`

Visit the website at:
`http://35.231.69.190:8000/home` (Or set to the cluster's own External IP)

3.To run the web application, run `python3 manage.py runserver` and check it at `http://127.0.0.1:8000/home`. 