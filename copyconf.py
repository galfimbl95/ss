import os
from time import time
import aiofile  # для асинхронной записи в файл
import asyncio  # дает возможность коду работать асинхронно
import glob

laptops = [
    {
        'name': 'conf_1',
        'ipMikrotik': '10.0.88.81',
        'ipUbiquiti': '10.40.1.51',
        'problems': ''
    },
    {
        'name': 'conf_2',
        'ipMikrotik': '10.0.88.87',
        'ipUbiquiti': '10.40.1.232',
        'problems': ''
    },
    {
        'name': 'conf_3',
        'ipMikrotik': '10.0.88.124',
        'ipUbiquiti': '10.40.1.243',
        'problems': ''
    },
    {
        'name': 'conf_4',
        'ipMikrotik': '10.0.88.90',
        'ipUbiquiti': '10.40.1.117',
        'problems': ''
    },
    {
        'name': 'conf_5',
        'ipMikrotik': '10.0.88.97',
        'ipUbiquiti': '10.40.1.9',
        'problems': ''
    },
    {
        'name': 'conf_6',
        'ipMikrotik': '10.0.88.96',
        'ipUbiquiti': '10.40.1.49',
        'problems': ''
    },
    {
        'name': 'conf_7',
        'ipMikrotik': '10.0.88.89',
        'ipUbiquiti': '10.40.1.126',
        'problems': ''
    },
    {
        'name': 'conf_8',
        'ipMikrotik': '10.0.88.79',
        'ipUbiquiti': '10.40.1.24',
        'problems': ''
    },
    {
        'name': 'conf_9',
        'ipMikrotik': '10.0.88.117',
        'ipUbiquiti': '10.40.1.62',
        'problems': ''
    },
    {
        'name': 'conf_10',
        'ipMikrotik': '10.0.88.121',
        'ipUbiquiti': '10.40.1.254',
        'problems': ''
    },
    {
        'name': 'conf_11',
        'ipMikrotik': '10.0.88.126',
        'ipUbiquiti': '10.40.1.157',
        'problems': ''
    },
    {
        'name': 'conf_12',
        'ipMikrotik': '10.0.88.129',
        'ipUbiquiti': '10.40.1.83',
        'problems': ''
    },
    {
        'name': 'conf_13',
        'ipMikrotik': '10.0.88.132',
        'ipUbiquiti': '10.40.1.54',
        'problems': ''
    },

]


async def copyOnLaptop(sourceFilesDict, laptop):
    target_path = '\\\\{}\\Users\\user\\Desktop\\files'.format(
        laptop['ipMikrotik'])
    target_path2 = '\\\\{}\\Users\\user\\Desktop\\files'.format(
        laptop['ipUbiquiti'])

    # для каждого считанного файла...
    for key in sourceFilesDict:
        # пытаемся скопировать через микротик...
        try:
            # копирование реализовано в виде бинарной записи ранее бинарно считанного файла
            async with aiofile.AIOFile(target_path + '\\' + key, 'w+') as afp:
                writer = aiofile.Writer(afp)
                await writer(sourceFilesDict[key])
                await afp.fsync()
                print('Файл', key, 'скопирован на', laptop['name'])
        except:
            # если не получилось пытаемся через юбиквити
            try:
                async with aiofile.AIOFile(target_path2 + '\\' + key, 'w+') as afp:
                    writer = aiofile.Writer(afp)
                    await writer(sourceFilesDict[key])
                    await afp.fsync()
                    print('Файл', key, 'скопирован на', laptop['name'])
            except:
                laptop['problems'] = '+'
                print('Не удалось скопировать файл', key, 'на', laptop['name'])


def clearLaptops():
    t0 = time()
    for laptop in laptops:
        target_path = '\\\\{}\\Users\\user\\Desktop\\files\\*'.format(
            laptop['ipMikrotik'])
        target_path2 = '\\\\{}\\Users\\user\\Desktop\\files\\*'.format(
            laptop['ipUbiquiti'])

        try:
            files = glob.glob(target_path)
            for f in files:
                os.remove(f)
                print ('Файл', f, 'удален с', laptop['name'])
        except:
            print ('Не удалось удалить файлы с', laptop['name'])
        try:
            files = glob.glob(target_path2)
            for f in files:
                os.remove(f)
                print ('Файл', f, 'удален с', laptop['name'])
        except:
            print ('Не удалось удалить файлы с', laptop['name'])
    
    print('Удаление файлов завершено за', time() - t0)

        


async def main():
    t0 = time()
    tasks = []
    sourceFilesDict = {}

    # бинарно читаем файлы из папки C:\\transfer в словарь
    for directory, _, files in os.walk('C:\\transfer'):
        for file in files:
            with open(directory+'\\'+file, 'rb') as fileReader:
                sourceFilesDict.update({file: fileReader.read()})

    for laptop in laptops:
        # создаем очередь задач
        task = asyncio.create_task(copyOnLaptop(sourceFilesDict, laptop))
        tasks.append(task)
    # начинаем асинхронное выполнение задач из очереди
    await asyncio.gather(*tasks)

    # выводим "отчет"
    for laptop in laptops:
        print('Наличие проблем на', laptop['name'], ':', laptop['problems'])
    print('Выполнено за', time() - t0)


if __name__ == '__main__':
    while True:
        a = input(
            'Будем копировать файлы на ноуты или удалять с ноутов?\n1) копировать\n2) удалять\n')
        if a == '1':
            asyncio.run(main())            
        elif a == '2':
            clearLaptops()            
        else:
            print('Нужно ввести 1 или 2\n')

