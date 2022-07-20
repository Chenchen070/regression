import matplotlib.pyplot as plt
import seaborn as sns

def plot_variable_pairs(df):
    sns.pairplot(df, corner=True)
    plt.show()


def plot_categorical_and_continous_vars(categorical_var, continuous_var, df):
    
    figure, axes = plt.subplots(1,4, figsize=(25,12))
    
    sns.countplot(x=categorical_var, data=df.sample(10000, random_state=123), ax=axes[0])
    sns.barplot(x=categorical_var, y=continuous_var, data=df.sample(10000, random_state=123), ax=axes[1])
    sns.boxplot(categorical_var, continuous_var, data=df.sample(10000, random_state=123), ax=axes[3])
    sns.jointplot(x=categorical_var, y=continuous_var, data=train.sample(10000, random_state=123), kind='reg', ax=axes[2])
    
    plt.show()