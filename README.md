# BigDataProject-SSML
### Information Regarding the Dataset :- Crime DataSet
1)The Train Dataset has a total of 9 columns and 878050 records.{Dates,Category,Descript,DayOfWeek,PdDistrict,Resolution,Address,X,Y}  
2)The Test Dataset has a total of 7columns and 884261 records.{Id,Dates,DayOfWeek,PdDistrict,Address,X,Y}     
3)The two datasets given have Dates,DayOfWeek,PdDistrict,Address,X,Y as the common attributes.    
  
### Problem Statement Identified from dataset  
Given the Common Features make Use of these features in order to predict the Category of crime committed given other set of attributes  
  
### Steps in completing this project:  
1)Fetching Data in Batches and PreProcessing
  Streaming steps:
  1. Run stream.py which creates a TCP socket over which data is sent
  2. In another py file we received the data from other end of TCP
  connection
  3. Converted the data received into a dataframe and then passed it for our
  preprocessing step
  Preprocessing steps that were done are as follows:
  1. Design off the schema based on the attributes and it’s data type.
  2. SInce most of the attributes were categorical we mapped the unique
  values for each categorical column to a numerical value.
  3. Extracted Date column to obtain new columns like Date ,Month, Hour,
  Minute, Year and added it to our new data frame with new updated
  schema.
  4. We created a new dataframe with only ‘category’ column as it is our
  predictor variable.
  5. Dropping of unnecessary columns like Descript, Resolution(as it was
  not present in our test csv file),Category(As it was our predictor
  variable) and Address(too many unique values to get accurate results).

2)Building Model 
  Next step towards our implementation was to build models.
  Since the model had to be built using an incremental approach i.e. fitting the
  data from each batch we have used three such models which support
  incremental fit which include Stochastic GradientDescent
  Classifier,NaiveBayes Classifier,Passive Aggressive Classifier.
3)Learning from train data
  After each batch of Data is preprocessed we fed the data to our models and
  store the final trained model in the current directory using the concept of pickle
  and joblib.
4)Testing Your Model 
  After streaming the entire data and training the model we started streaming
  the test data and preprocessed similar to our training data ,then used a stored
  model to predict the values for our category column.
5)Clustering
  As a part of clustering we used MinKBatchMeans to find the clusters on our
  test dataset.


### Involvment and Contribution of team members
1) Kuntal Gorai (PES2UG19CS198) --> Preprocessing,Streaming,Report Making,Effect of preprocessing on Accuarcy.(Assisted in making models also)
   Time spent: 50hrs+++
2) S Mahammad Aasheesh (PES2UG19CS341) --> Helped in Giving idea of Mappings,Dealing with Models.
   Time Spent: 40hrs ++
4) S V S C Santosh (PES2UG19CS346) --> Preprocessing,Streaming,Report Making,Effect of preprocessing on Accuarcy.(Assisted in making models also).
   Time Spent: 50hrs+++
4) Sai Eeshan Reddy Tallapalli --> Incremental Models idea and assistance has been provided in Making model.
   Time Spent: 30hrs+++


