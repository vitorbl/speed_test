import speedtest
import pandas as pd
import numpy as np
from datetime import datetime
import os
import time

# based on https://stackoverflow.com/a/48290130
def test():
    try:
        s = speedtest.Speedtest()
        s.get_servers()
        s.get_best_server()
        s.download()
        s.upload()
        res = s.results.dict()
        sv_info = {
            "server_" + key_: res["server"][key_] for key_ in res["server"].keys()
        }
        res.pop("server")
        cli_info = {
            "client_" + key_: res["client"][key_] for key_ in res["client"].keys()
        }
        res.pop("client")
        res.update({"download": res["download"] * 1e-6, "upload": res["upload"] * 1e-6})
        res.update(sv_info)
        res.update(cli_info)
    except:
        {
            "download": 0,
            "upload": 0,
            "ping": np.nan,
            "timestamp": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "bytes_sent": np.nan,
            "bytes_received": np.nan,
            "share": np.nan,
            "server_url": np.nan,
            "server_lat": np.nan,
            "server_lon": np.nan,
            "server_name": np.nan,
            "server_country": np.nan,
            "server_cc": np.nan,
            "server_sponsor": np.nan,
            "server_id": np.nan,
            "server_host": np.nan,
            "server_d": np.nan,
            "server_latency": np.nan,
            "client_ip": np.nan,
            "client_lat": np.nan,
            "client_lon": np.nan,
            "client_isp": np.nan,
            "client_isprating": np.nan,
            "client_rating": np.nan,
            "client_ispdlavg": np.nan,
            "client_ispulavg": np.nan,
            "client_loggedin": np.nan,
            "client_country": np.nan,
        }
    return {x: [y] for x, y in res.items()}


i = 1
while True:
    test_results = pd.DataFrame(test())
    if os.path.isfile("speed_test.csv"):
        test_results.to_csv(
            "speed_test.csv", index=False, header=False, sep=";", decimal=",", mode="a"
        )
    else:
        test_results.to_csv("speed_test.csv", index=False, sep=";", decimal=",")
    print(
        "[TESTE #{} {}]\nVelocidade de Donwload: {:.2f} Mb | Velocidade de Upload: {:.2f} Mb | Ping : {} s".format(
            i,
            test_results["timestamp"].iloc[0],
            test_results["download"].iloc[0],
            test_results["upload"].iloc[0],
            test_results["ping"].iloc[0],
        )
    )
    if (i % 5) == 0:
        time.sleep(60 * 30)
    i += 1
