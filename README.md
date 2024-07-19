# **Baseball Batting Statistics, 1871-2012**
**Author:** Anne Marie Bogar<br/>
**Active Project Dates:** June 17-30, 2024<br/><br/>
## Summary
The goal of this project is to qery a list of baseball players and their batting stats from a database and manipulate, analyze and visualize the data in Python using pandas, matplotlib and seaborn. The data is cleaned and calculated columns are added, and then the DataFrames are reshapedd, regrouped and filtered to extract meaning from the data. Interesting insights are then visualized in easy-to-consume graphs using seaborn and matplotlib.
<br/>
## Data
The [data](https://www.kaggle.com/datasets/freshrenzo/lahmanbaseballdatabase) is from a collection of CSV files about baseball players between the years 1871 and 2012. The specific csv files used are the Master file and the Batting file.<br/><br/>

Master
- playerID - unique code assigned to each player
- birthYear - year of birth
- birthMonth - month of birth
- birthDay - day of birth
- nameFirst - first name
- nameLast - last name
- weight - player's weight in pounds
- height - player's height in inches
- bats - player's batting hand (left, right, both)
- throws - player's throwing hand (left, right)

Batting
- yearID - year
- stint - order of appearances in the season
- teamID - team
- lgID - league
- G - number of games played
- G_batting - number of games as a batter
- AB - at bats
- R - runs
- H - hits
- 2B - doubles
- 3B - triples
- HR - homeruns
- RBI - runs batted in
- SB - stolen bases
- CS - caught stealing
- BB - base on balls (walks)
- SO - strikeouts
- IBB - intentional walks
- HBP - hit by pitch
- SH - sacrifice hits
- SF - sacrifice flies
- GIDP - grounded into double play
- G_old - old version of games (depreciated)

## Questions Explored:
The first question explored was “Which active player had the most runs batted in (RBI) from 2005-2008?” 
In order to answer this question, the DataFrame was filtered to only include rows from the years 2005-2008, 
then grouped by the playerID so that the number of RBI could be added up for each player. 
The maximum number of RBI was found, and then the DataFrame was filtered to find the name of the player with the playerID relating to the max number of RBI. 
The answer is Joel Zumaya with 510 RBI.<br/><br/>
The second question was “How many double plays did Albert Pujols ground into (GIDP) in 2006?” 
The solution was rather simple, as the DataFrame was filtered for ‘name’ = ‘Albert Pujols’ and ‘yearID’ = 2006. 
The answer is that Albert Pujols grounded into 20 double plays in 2006.<br/><br/>
The third question explored was the distribution of triples per year up to 2012. 
A new DataFrame was created by grouping the yearID and then summing up the triples from each year. 
The majority of years (12) saw less than 100 triples. The rest were spaced out relatively evenly, although 4 years had more than 700 triples. 
Further analysis reveals that up until 1997, the number of triples had not yet reached 100 per year, while after 1997 the numbers climbed significantly each year. 
From 2007 to 2012, the number of triples exceeded 800. The reason for this is most likely that the players being analyzed were as of 2012 still active, 
so the majority of them have been playing from 2007 to 2012, and many of them have been playing since at least 1997. 
It is difficult to gauge just how the frequency of triples has changed over time because the majority of players playing in 1997 
and before are not active now and therefore cannot be counted in the histogram. Therefore, this histogram is misleading as it does not show the 
total distribution of triples for each year but rather the total number of triples for specific players.<br/><br/>
The fourth question explored was the relationship between triples and steals. A new DataFrame was created by grouping on playerID and summing up the 
number of triples and stolen bases for each player. The two features seem to be positively correlated, where the players with a high number of 
triples also tend to have a higher number of stolen bases. One possible theory to explain this correlation is that in order to hit a triple, the 
player must run relatively fast. A double can be accomplished if the ball is hit hard enough into the outfield, but a triple will only occur if the 
player can run to third base faster than the outfielder can field and throw the ball, which is a difficult feat to accomplish. 
Likewise, stealing a base requires speed as the runner must outrun the catcher’s throw to whichever base is being stolen. 
Since there are similar attributes needed to accomplish these two tasks, it makes sense that the two stats have a strong correlation.<br/><br/>
The fifth question explored was the relationship between the On Base Percentage of a player and certain batting stats such as Walks, Strikeouts, At Bats and Sacrifice Hits. 
In order to tackle this question, a new DataFrame was created by grouping the playerID and then summing up all the batting statistics in the original DataFrame. 
The OBP was then calculated by adding up the total number of hits, walks and hit by pitch incidents per player and then dividing that number by the sum 
of the total number of at bats, walks, hit by pitch incidents and sacrifice flies.<br/><br/>
*OBP = (hits + walks + hit by pitch) / (at bats + walks + hit by pitch + sacrifice flies)* <br/><br/>
Then, four scatterplots were created to look at the relationship between OBP and the other features. Overall, the best OBP to have compared to the other stats was around 0.4. 
Any higher of an OBP generally meant that the player did not actually have many at bats. Between the four stats, Walks, Strikeouts and At Bats had a generally positive correlation 
with OBP. Walks had the most clear-cut correlation, as players who are easily able to distinguish between a strike and a ball have a better chance of making it on base. 
At Bats was slightly less correlated but still strongly correlated, as the more chances a player has to bat the more likely they are to get on base. 
The Strikeouts, while still correlated, tended to be more pronounced at a slightly lower OBP. However, if a player is batting in the majority of games in a season, 
then there is a good likelihood that they will not only get on base often but also strikeout often. The Sacrifice Hits tended to be more strongly correlated with lower OBPs, 
which makes sense as a sacrifice hit or bunt has the intention of advancing the runner already on base to the detriment of the batter. 
A player with a high number of sacrifice hits will have a high percentage of making contact with the ball even though the OBP will suffer. 
And if a player has a good record of making contact and especially of bunting, they will be chosen more often to sacrifice hit, meaning their OBP will be lower.<br/><br/>
The sixth question explored was which stat most strongly impacted the decision to intentionally walk a batter. To answer this question, three scatterplots were created side by side 
using the DataFrame created for the fifth question summing up all the batting stats per player. Three stats were chosen for analysis: Homeruns, RBI and Triples. 
Homeruns and RBI understandably had a very high positive correlation, with RBI slightly more highly correlated. As intentional walks only happen if at least one other runner is on base,
minimizing the possibility of that runner scoring is the main goal so targeting batters with high numbers of homeruns and RBI is strategic. 
Interestingly though, there was no real correlation between triples and intentional walks. In fact, some of the players with the highest number of triples were hardly 
ever intentionally walked. What is interesting about this finding is that players with high triples numbers would presumably also have high RBI numbers, 
and as RBI had a high correlation to Intentional Walks, it would be assumed that triples would have a similar looking graph. However, as was revealed earlier, 
players with high numbers of triples also have high numbers of stolen bases because they are faster than the average player, so intentionally walking this type of 
player might in turn lead to more runs.<br/><br/>
The final question examined was the relationship between the batting stats and the batting preference of the player, i.e. do they bat right-handed, left-handed or can 
they bat on either side. This question was answered by creating a new DataFrame from the one created for question five. The DataFrame was grouped by ‘bats’ with values of 
either R, L or B and the stats were summed up for each type of batting. Then, a pie chart was created to show the actual percentage of all batters that could either bat right, 
left or both. Accompanying the pie chart were multiple bar charts analyzing the number of batting stats per batter for each batting type. 
Even though right-handed batters made up the majority of players, they had the least number for each stat, while ambidextrous batters, who made up only 9 percent of the total batters, 
had the highest numbers. Left-handed batters were always in the middle. A theory for the left-handed batters always doing better in the stats than right-handed batters 
could be that lefties usually have an advantage in that they hit better against right-handed pitchers and there are more right-handed pitchers in baseball than left-handed pitchers. 
The batters may not necessarily be better players but will always have a slight advantage. On the other hand, batters who can bat both on the right and the left not only 
have the advantage of deciding which side to bat on based on the pitcher, but are probably also generally better players because they have to work hard to perfect both types of batting.
This would explain why the stats are higher all-round, from hits to walks to stolen bases.

## Future Ideas
In the future, I would like to do a statistical analysis on the On Base Percentage correlations made in the graphs for question five. 
Is there a significant difference in OBP between people who walk more verses people who are simply at bat more often? <br/><br/>
I would also like to look into whether height and weight affect the batting stats. The assumption is that bigger players are more likely to hit doubles or homeruns, 
while smaller players would be better at stealing bases and getting runs. And if these assumptions do not hold true, then looking into why that is.
