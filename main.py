import shutil
import os
from time import sleep
from datetime import datetime, timedelta
from datetime import date as dt


path1 = r"W:\GidAnalysisData\Insatall\Logs"
path2 = r"T:\АГИД_выгрузка_сегодня"
privatepath = r"T:\Л"
tom = datetime.strftime(datetime.now() - timedelta(days=1), ".%Y-%m-%d")
nowd = datetime.strftime(datetime.now(), "%Y-%m-%d")
nowt = datetime.strftime(datetime.now(), "%H.%M")
ext = ".INFO"


def connect():
    try:
        os.system(r'net use T: \\10.1.32.12\temp /PERSISTENT:YES /USER:user pass')
        os.system(r'net use W: \\10.23.0.68\d /PERSISTENT:YES /USER:user pass')
        sleep(1)
        print("Сетевые диски подключены.")
        sleep(1)
    except:
        print("Ошибка при подключении сетевых дисков!\nПроверьте наличие сети, либо занятые буквы уже подключенных дисков.")

def inf():
    print("Вчера: "+tom.lstrip(".")+"\n")
    sleep(1)
    print("Файлы в папке "+ path1 + ":")
    print("############################")
    for file in os.listdir(path1):
        print(file+"\n____________________________")
    print("############################")
    sleep(1)

def checkpath():

    if os.path.exists(path2)!= True:
        print("В текущие сутки выгрузка не производилась, либо удалена пользователем! Проиводится формирование данных за текущие сутки:")
        sleep(1)
        makepath()
        copy()

    elif os.path.exists(path2)==True and str(dt.fromtimestamp(os.path.getctime(path2))) == nowd:
        print("Данные за текущие сутки уже были переданы. Обновление:")
        shutil.rmtree(path2, ignore_errors=False, onerror=None)
        sleep(2)
        makepath()
        copy()

    elif os.path.exists(path2)==True and dt.fromtimestamp(os.path.getctime(path2)) != nowd:
        newagid = os.path.join(privatepath, "АГИД_за_" + str(dt.fromtimestamp(os.path.getctime(path2))))
        os.rename(path2, newagid)
        print('Папка "АГИД выгрузка_сегодня" существует и переименована в соответствии с датой выгрузки. Производится формирование акутальных данных за текущие сутки:')
        sleep(1)
        makepath()
        copy()

    else:
        print("Произошла непредвиденная ошибка!!!")
        sleep(1)

def makepath():
    try:
        os.mkdir(path2)
        sleep(1)
        print('Папка "АГИД" за текущие сутки создана.')
    except:
        print("Не удалось создать папку.")

def copy():

    for file in os.listdir(path1):
        goname = os.path.splitext(file)[0]
        goext = os.path.splitext(file)[1]
        try:
            if goext == tom:
                shutil.copy2(os.path.join(path1, file), path2)
                tomext = file.split(".")[0] + "_" + file.split(".")[2]+".txt"
                os.rename(os.path.join(path2, file), os.path.join(path2, tomext))
                sleep(1)
                print("Данные "+file+" за вчерашние сутки ("+tom.lstrip(".")+") переданы.")
        except:
            print("Ошибка в передаче данных за вчерашние сутки")
        try:
            if goext==ext:
                shutil.copy2(os.path.join(path1, file), path2)
                newname = goname+"_"+ nowd+" до "+ nowt+".txt"
                newpath = os.path.join(path2, newname)
                oldpath = os.path.join(path2, file)
                os.rename(oldpath, newpath)
                sleep(1)
                print("Данные "+file+" за сегодняшние сутки до "+nowt + " переданы.")
                sleep(1)
        except:
            print("Ошибка в передаче данных за текущие сутки")

def main():
    connect()
    inf()
    checkpath()
main()
