from Libraries import *

class LDA():
    def __init__(self, n_components):
        self.n_components = n_components
        self.scalings = None
    
    def fit(self, X, y):
        n_features = X.shape[1]
        labels = np.unique(y)
        S_W = np.zeros((n_features, n_features))
        S_B = np.zeros((n_features, n_features))
        
        mean_overall = np.mean(X, axis=0)
        
        for c in labels:
            X_c = X[y == c]
            mean_class = np.mean(X_c, axis=0)
            
            for x in X_c:
                S_W += (x - mean_class).reshape(n_features, 1) @ (x - mean_class).reshape(1, n_features)
            
            n_c = X_c.shape[0]
            mean_diff = (mean_class - mean_overall).reshape(n_features, 1)
            S_B += n_c * (mean_diff @ mean_diff.T)
        
        #Cal the eigvalues and eigvectors
        eigvals, eigvecs = np.linalg.eig(np.linalg.pinv(S_W) @ S_B)
        
        #Descending Sort
        sorted_indices = np.argsort(eigvals)[::-1]
        
        #Since the output data has complex numbers due to the np.linalg.eig function, I will convert them back to real numbers.
        eigvals, eigvecs = eigvals[sorted_indices].real, eigvecs[:, sorted_indices].real

        
        if self.n_components:
            eigvecs = eigvecs[:, :self.n_components]
            
        self.scalings = eigvecs
    
    def transform(self, X):
        #Projecting data into new space
        return X @ self.scalings
    
    def fit_and_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)
    

