import pandas as pd

#int prob, string diff, string diff, int week
def writeToDataSheet(prob, diff, date):
    newData = {
        'Problem': [prob], 
        'Dificulty': [diff], 
        'Date': [date]
    }
    df = pd.DataFrame(newData)
    df.to_csv('Sent problems BTA.csv', mode='a', index=False, header=False)
    return True

def numberBeenUsed(num):
    data = pd.read_csv("Sent problems BTA.csv")
    problemNums = data.Problems
    for prob in problemNums:
        if num == prob:
            return True

    else:
        return False