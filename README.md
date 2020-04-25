# Final Project for Python Programming for Data Scientists and Natural Language Processing with Deep Learning courses at the Hertie School

Our project aims to analyze media coverage of the 2020 US Presidential primary election. To accomplish this, we have scrape the politics sections of eight US news outlets representing the ideological spectrum: Breitbart, Fox News, the Washington Times, AP, NBC, the New York Times, Politico, and Buzzfeed News. 
We scraped 9,950 articles and 246,967 sentences from March 1 - April 19th 2020 that mention at least one of the candidates who were in the race at that time. 
We then dive deeper into the 5,568 articles that mention Democratic front-runners Biden and Sanders and analyze 
1. the level of coverage each candidate received,
2. the sentiment of sentences relating to each candidate, and 
3. patterns of descriptive language associated with each candidate based on a qualitative analysis of neural network predictions.

In terms of the level of coverage, we find that Biden received about 37% more coverage than Sanders, and that overall coverage of the candidates has dropped since the media’s attention shifted to covid-19. 

Sentiment analysis using the textblob library detected minimal differences between coverage of the two candidates, with Sanders’ overall average slightly more positive than Biden’s. 

To study patterns of descriptive language, we implemented a convolutional neural network model (CNN) with BERT embeddings to predict whether a sentence (with the candidate’s name removed) described Sanders or Biden. A qualitative analysis of the results showed language clearly associated with each candidate.
