# Temp Score Predictor

## 📘 Overview 
Does weather impact football games more than we think? Specifically, when teams play in temperatures they’re unaccustomed to, does it negatively affect their performance? This analysis looks at what team on an NFL Sunday is most "out of their element" in terms of weather. 

## 📊 How It Works
1. **Game Data**: Retrieve the week’s NFL games using [The Odds API](https://the-odds-api.com/)
2. **Weather Analysis**: 
- Collect historical weather data for each team's home city from [Visual Crossing](https://www.visualcrossing.com/), calculating the **mean temperature** and **standard deviation**.  
- Get the **forecasted kickoff temperature** for each game from [Open Weather Map](https://openweathermap.org/)
- - Calculate **z-scores** to determine how far the game-time temperature deviates from the team's home-city norm.
3. **Results**: The team with the largest absolute z-score is identified as the one most "out of their element" for that week. This result is posted to X (formerly Twitter)


## 💡 Considerations
- If a team is, in general, a lot better than another team it would be naive to think that just because they are going to be playing in weather that they aren't use to they are going to lose. Instead, this analysis looks at the lines already set by the sports books. They have much more features in their models and usually are able to predict the margins of each game relatively accurately. However, this model just assumes they don't take into account the difference in weather enough. For example, if a team is predicted to win by 10 points, but they are going to a temperature that is very different than one they are use to, this model would just predict that they are going to win by less than 10 points. Basically it just adds a small prediction on top of their prediction already based on some hard coded rules.