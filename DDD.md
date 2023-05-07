# Document Driven Documentation
#### (Originally written in Microsoft Office Word) This documentation may not reflect the end-result for the endpoints present in the REST API and are subject to changes, but are provided as a starting point.

## Get all unique environments
Description: The database will consist of a multitude of runs. This method fetches all 
the unique environments that are present in the database at a given time.

Input: There should be no input for this method.

Output: A list of all the unique environments that were present in the database.

Error message: There is no input for this method. Therefore, the list will simply be empty if there are no enviroments in the database.

## Create a run 
Description: This method is for creating a run. There is no prevalent use case for this method at the current time
as the persistence of methods happen within the optimization module. However, the method
could be incorporated in the REST API for the time being and added if it seems useful at a later point. 
However, it should probably be commented out if not used, as the method would present an unneccesary security-hole.

Input: A JSON dictionary with all the parameters needed to create a run.

Output: The created run.

Error message: A response stating that parameters are lacking if they are, or a message stating that the run exists if it does. 

## List the best performing run for each algorithm that has been used with a selected environment
Description: For each unique algorithm that been optimized with the currently selected environment, 
the best performing run should be returned. Thus, this method should return a list of the same length
as the amount of unique algorithms that have been tuned using within the selected envrionment.

Input: A string representing the chosen environment.

Output: A list containing the top performing run for each unique environment within the environment-scope.

Error message: Returns no error message due to the fact that the input is not written by the user, 
but defined by the output of the "Get all unique environments" -method. Therefore, an environment that does not exist
can not be entered into this method. 

## List the top trials for a selected environment and a selected algorithm
Description: This method can be called on after an environment and an algorithm has been selected. 
The goal of this method is to provide a list of the best performing [environment x algorithm] combinations 
for the user to see. 

Input: A string representing the chosen environment; a string representing the chosen algortihm; a number representing
the limit (pagination).

Output: A list of length==limit or shorter if there were not enough database-entries.

Error message: No error message here as the method can only be called for environments 
and algorithms that have entries in the database. 

## Get a run by its ID
Description: Retrieves a run with the specified ID from the database.

Input: A string representing the run ID.

Output: The run with the specified ID.

Error message: Returns an exception if the run was not found.
