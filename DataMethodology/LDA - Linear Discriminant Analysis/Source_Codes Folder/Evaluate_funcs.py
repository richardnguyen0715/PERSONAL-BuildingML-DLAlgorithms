from Libraries import *
from LDA_Implementation import *

def random_dataset(n_col, n_row):
    data = np.random.rand(n_row, n_col - 1)

    labels = np.random.randint(1, 4, size=(n_row, 1))

    #Comnbine data and labels
    X = np.hstack((data, labels))

    columns = [f'Feature{i+1}' for i in range(n_col - 1)] + ['Label']
    
    df = pd.DataFrame(X, columns=columns)
    
    return df

def Wine_processing():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    dataset = pd.read_csv(current_directory + '\Wine.csv', header=0)

    n_row = dataset.shape[0]
    n_col = dataset.shape[1]

    print(n_row, n_col)

    X = dataset.iloc[:, 0:(n_col - 1)].values.astype(float) 
    Y = dataset.iloc[:, n_col - 1].values

    n_components = np.unique(Y).shape[0] - 1

    lda = LDA(n_components)  # n_components = 2
    X_new = lda.fit_and_transform(X, Y)

    return X, Y

def Random_dataset_processing(n_row, n_col):
    dataset = random_dataset(n_col, n_row)
    
    n_row = dataset.shape[0]
    n_col = dataset.shape[1]

    print(n_row, n_col)

    X = dataset.iloc[:, 0:(n_col - 1)].values.astype(float) 
    Y = dataset.iloc[:, n_col - 1].values

    n_components = np.unique(Y).shape[0] - 1

    lda = LDA(n_components)  # n_components = 2
    X_new = lda.fit_and_transform(X, Y)

    return X, Y

def Plot(X_new, Y):
    plt.figure(figsize=(8, 6))
    for label in np.unique(Y):
        plt.scatter(X_new[Y == label, 0], X_new[Y == label, 1], label=f'Label: {label}', alpha=0.7)
    plt.xlabel('LDA Component 1')
    plt.ylabel('LDA Component 2')
    plt.title('LDA: 2D Visualization of Projected Data')
    plt.legend()
    plt.grid(True)
    plt.show()