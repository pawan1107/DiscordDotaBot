from datetime import datetime
import traceback


def logError(ex):
    tb = ex.__traceback__
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    file_object = open(f"{date}.log", "a")
    file_object.write("\n")
    file_object.write(f"\n{now} : {tb.tb_frame.f_code.co_name} | {tb.tb_frame.f_code.co_filename} | {tb.tb_lineno} | {ex}")
    file_object.close()