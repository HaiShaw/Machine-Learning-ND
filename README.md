# Machine-Learning-ND

## Repo for Udacity Machine Learning Nanodegree Projects


### Project: Titanic Survival Exploration
#### Description:
In this project, I create decision functions that attempt to predict survival outcomes from the 1912 Titanic disaster based on each passenger’s features, such as sex and age. I start with a simple algorithm and increase its complexity until I am able to accurately predict the outcomes for at least 80% of the passengers in the provided data.


### Project: Predicting Boston Housing Prices
#### Description:
In this project, I apply basic machine learning concepts on data collected for housing prices in the Boston, Massachusetts area to predict the selling price of a new home. I first explore the data to obtain important features and descriptive statistics about the dataset. Next, I properly split the data into testing and training subsets, and determine a suitable performance metric for this problem. I then analyze performance graphs for a learning algorithm with varying parameters and training set sizes. This enables me to pick the optimal model that best generalizes for unseen data. Finally, I test this optimal model on a new sample and compare the predicted selling price to my statistics.


### Project: Creating a Student Intervention System
#### Description:
As education has grown to rely more on technology, vast amounts of data has become available for examination and prediction. Logs of student activities, grades, interactions with teachers and fellow students, and more, are now captured in real time through learning management systems like Canvas and Edmodo. This is especially true for online classrooms, which are becoming popular even at the primary and secondary school level. Within all levels of education, there exists a push to help increase the likelihood of student success, without watering down the education or engaging in behaviors that fail to improve the underlying issues. Graduation rates are often the criteria of choice, and educators seek new ways to predict the success and failure of students early enough to stage effective interventions. A local school district has a goal to reach a 95% graduation rate by the end of the decade by identifying students who need intervention before they drop out of school.
In this project my task is to model the factors that predict how likely a student is to pass their high school final exam, by constructing an intervention system that leverages supervised learning techniques. The board of supervisors has asked me to find the most effective model that uses the least amount of computation costs to save on the budget. I analyze the dataset on students' performance and develop a model that will predict the likelihood that a given student will pass, quantifying whether an intervention is necessary.


### Project: Creating Customer Segments
#### Description:
In this project I apply unsupervised learning techniques on product spending data collected for customers of a wholesale distributor in Lisbon, Portugal to identify customer segments hidden in the data. I first explore the data by selecting a small subset to sample and determine if any product categories highly correlate with one another. Afterwards, I preprocess the data by scaling each product category and then identifying (and removing) unwanted outliers. With the good, clean customer spending data, I then apply PCA transformations to the data and implement clustering algorithms to segment the transformed customer data. Finally, I compare the segmentation found with an additional labeling and consider ways this information could assist the wholesale distributor with future service changes.


### Project: Train a Smartcab to Drive
#### Description:
In this project I apply reinforcement learning techniques for a self-driving agent in a simplified world to aid it in effectively reaching its destinations in the allotted time. I first investigate the environment the agent operates in by constructing a very basic driving implementation. Once my agent is successful at operating within the environment, I then identify each possible state the agent can be in when considering such things as traffic lights and oncoming traffic at each intersection. With states identified, I then implement a Q-Learning algorithm for the self-driving agent to guide the agent towards its destination within the allotted time. Finally, I improve upon the Q-Learning algorithm to find the best configuration of learning and exploration factors to ensure the self-driving agent is reaching its destinations with consistently positive results.
