import pandas as pd

# step 1 - Load the dataset
df = pd.read_csv("dataset/banklist.csv")

print(df.head()) # prints the first 5 rows of the dataset
print("--------------------------------")
print(df.shape) # tells the row and column count of a dataset
print("--------------------------------")
print(df.dtypes) # tells the data type of each column
print("--------------------------------")
print(df.columns) # prints the column names of the dataset
print("--------------------------------")
print(df.info()) # prints the summary of the dataset
print("--------------------------------")
print(df.describe()) # prints the summary statistics of the dataset
print("--------------------------------")
print(df.isnull().sum()) # prints the number of null values in each column
print("--------------------------------")
print(df.duplicated().sum()) # prints the number of duplicated rows in the dataset


def main():
    print("Hello from data-analysis!")


if __name__ == "__main__":
    main()
