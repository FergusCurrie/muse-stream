import pandas as pd 


def csv_to_h5(filename: str) -> None:
    df = pd.read_csv(filename)
    print('loaded datarames')
    df.to_hdf('eeg_data.h5', key='df', mode='w', format='table', complib='blosc', complevel=9)


if __name__ == "__main__":
    csv_to_h5('eeg_data.csv')