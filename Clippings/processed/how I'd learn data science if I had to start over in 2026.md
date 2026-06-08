---
title: "how I'd learn data science if I had to start over in 2026"
source: "https://www.youtube.com/watch?v=nzRtG-CzP58"
author:
  - "[[The Almost Astrophysicist]]"
published: 2025-06-25
created: 2026-06-08
description: "After working as a data scientist at Uber and now Stripe, I’ve seen what’s useful, what’s noise, and how to build the kind of foundation that actually lasts. Whether you're just starting out or trying"
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=nzRtG-CzP58)

After working as a data scientist at Uber and now Stripe, I’ve seen what’s useful, what’s noise, and how to build the kind of foundation that actually lasts. Whether you're just starting out or trying to reconnect with the basics — I hope this helps you find your version of the path 🚀  
  
If I had to start learning data science all over again in 2025… this would be my exact roadmap 🧭 From Python and SQL to machine learning, statistics, and actually understanding what matters in a real tech job — this is how I’d approach learning data science today (without getting lost in 12 course tabs and a sea of contradictory advice 😅)  
  
Wherever you are in your journey, you’re not behind — you’re just getting started ✨  
  
🕒 Timestamps  
00:00 a full roadmap outline  
02:39 SQL + solving problems!  
07:02 python + example  
09:44 ML info + project ideas + random regression explanation  
14:22 math math math  
16:31 stats basics  
18:41 business acumen  
  
🔗 Links  
1\. https://datalemur.com/questions/laptop-mobile-viewership  
2\. https://datalemur.com/questions/repeated-payments  
3\. https://www.classes.cs.uchicago.edu/archive/2024/  
4\. deep learning pdf: https://udlbook.github.io/udlbook/  
  
🧠 Keywords: learn data science, data science 2025, data science roadmap, how to become a data scientist, data science from scratch, SQL for beginners, python for data science, machine learning for beginners, no CS degree, data science career path  
  
👉 Subscribe if you’re into real, unfiltered data science content. And leave a comment if anything hits — would love to hear your story too.  
  
\-------------------------------------------------------------------------------------------------------------------------------------------  
Welcome to The Almost Astrophysicist — I’m Priya, a data scientist sharing real, unfiltered stories about navigating tech 💻, burnout 🧠, career growth 📈, and (mostly) just learning out loud. From physics undergrad to startups, Uber, and Stripe, I’ve picked up a lot (and maybe made a lot of mistakes too 😅). This channel is where I break down what it’s actually like to work in tech, reflect on the messy parts of ambition, and talk through both the qualitative and quantitative sides of building a meaningful career. Expect technical data science content, chat about what it's like working at high-growth companies, dealing with imposter syndrome, and figuring out what “success” even means.  
  
Subscribe if you’re into data science that feels a little more human 🤍 — and comment anytime, I’d love to hear your story too!!  
  
LinkedIn: https://www.linkedin.com/in/priya-l-520311145/

## Transcript

### a full roadmap outline

**0:00** · Okay, so data science is basically stats, mathematics, computer science, sometimes econ, and it's all just rolled up into one. And it is impossible for everyone to know everything in data science. I feel like I learned data science on the fly kind of through my computational physics classes in college towards the end of college and then I immediately just joined as a data scientist in the workforce.

**0:22** · I really learned most of what I know throughout my last six years in tech, being at a startup, going to Uber, now being at Stripe, and now I feel like I have a much better idea about what you actually need to know to be a data scientist. So, let's get straight into it. There are going to be some examples, some Jupyter notebooks, me going through SQL, and a lot of information about what data science is like actually in the real world in the tech industry.

**0:48** · Our main sections are going to be SQL, Python, machine learning/modeling with some math concepts sprinkled in, stats, and business acumen. Those five areas are really generally what consists of being a data scientist. We're going to tackle all of them. We're actually also going to have an interview scale and a practicality scale because we all know that what you have to learn for a data science interview is not what the job is going to be like. We know those like Lee code algorithms don't show up in your day-to-day job.

**1:19** · So just understanding the practicality of a concept whether it's going to help you in the interview stage or not separately will be useful.

**1:28** · I also want to note that the proportion of these five different topics I'm going to talk about is going to differ throughout different stages of your data science career. A product data scientist for example really needs to be fantastic at SQL experimentation and statistics and business acumen. that differs a lot from a data scientist that perhaps focuses on the go to market and sales side which is what I did at Uber.

**1:51** · I think in that role ML modeling like time series causal inference models regressions that was the most important thing as well as just some basic stats and a lot of business acumen. So while one area might not be super important to you now that could very easily change as you switch roles and evolve in your career. Before we get straight into it, for those of you who may not know me, I'm Pria. I post about data science on YouTube. The last year and a half has been a bit of a whirlwind in so many ways.

**2:23** · So, I haven't posted as much, but I'm really trying to prioritize it now.

**2:27** · So, if you have anything you want to know about data science, want to follow the journey, have any questions about big tech, comment down below. Please subscribe to follow the journey if you're interested. And yeah, let's get into it.

### SQL + solving problems!

**2:40** · SQL is the most underrated tool in a data scientist's toolkit by far. And I can tell you this having been in the industry for 6 years. I did not use SQL as much as I use it now in my current role. And I have learned so much about its benefits and how amazing it is. It's going to help you understand the data you're working with, clean your data, understand data structures, and give you a very, very strong foundation in data pre-learning all of Python. This is also going to be 80 to 90% of your job if you're going to go the data analyst route.

**3:10** · And nowadays with this tough market, starting as a data analyst and just switching internally is such a great route. So I really think you want to hone in your basics and your foundation first, which has to start at SQL. I would 100% prioritize this first just to understand like what the data world even looks like. And I'll go through a couple of examples. I picked two different examples, one easy and one hard from data lemur, which is one of the best resources. I know it has a lot of interview questions, but I think that you should just start practicing SQL. It is plain English syntax.

**3:42** · It is very very easy to pick up. I would say the most common SQL situations like things that I use like literally every single day. I use case one statements, sums, counts, the basic aggregations with the case when statement as well as window functions. It is so great to use window functions in SQL rather than pandas.rolling or like you know whatever you want to do in Python. It's much more inefficient.

**4:07** · Python and pandas is great for data manipulation on a much smaller scale but it's going to eat into your RAM make your notebooks crash if you're working with very large data sets. Even if you're in data bricks like it's going to crash and if you're analyzing data as your job you're going to have way more than a million rows of data. And once you hit a million rows pandas out the window. I know you can use spice. That's a different conversation. But let's get back to SQL. Let's go on data lemur and look at the first example. Here's a quick data interview question that's basically about like basic case one statements and aggregations.

**4:37** · You can see how easy it is. It's all plain English.

**4:42** · And I really think the more questions like this you work on. You have to start somewhere and starting with these basic functions is the way you can build out and learn more. And I'm telling you, these kinds of questions actually do come up in interviews. Like I've interviewed other people. I've been interviewed. I've had SQL interviews and I literally had a question that was like a sum over a case one with a couple of group eyes. However, the one I'm going to go into next, that example, it took me a good 8 to 10 minutes and I did have to check documentation. But again, documentation is your best friend.

**5:11** · So over here you see that you want to identify payments made by the same merchant with the same credit card that happened within 10 minutes of each other. So there's a lot of things going on here. So the way I set everything up was just having like the three things that all need to be consistent. The merchant ID, the credit card ID, and the amount of the transaction.

**5:32** · And then you could do a count of how many transactions occurred that have consistency across those three, which would represent a potentially duplicate transaction and then getting the transaction timestamp and getting the lag between this row and the previous row using that partition of merchant credit card amount. And then you just do a simple filter where you find all of the transactions where the merchant had more than one transaction and that was within 10 minutes.

**6:00** · So it is very structured and easy to get to the answer if you're familiar with the general functionality and just how to search documentation. The two functions that I knew existed but I wasn't entirely sure like what the syntax would be was lag and epic. But I will tell you during interviews you are never expected to get it 100%. If you just said, "Hey, I know there's a function that exists that does this. I'll use that function." That is absolutely good enough. Most companies do not require your code to run.

**6:29** · I had an interview with Apple and like they didn't require it was a software engineer interview too and they didn't require the code to run. They just wanted to make sure everything was logically sound. I would say the best resources for SQL are just going to be like, you know, finding something on Corsera Data Camp. I actually have a data camp premium subscription because my work covers it and I would absolutely recommend just going through a 3h hour 4-hour module. You could do it for free and then just practicing on data lemur.

**6:58** · Those two are absolutely fantastic.

### python + example

**7:03** · The next general region once you kind of feel like you have a good ground understanding of SQL, you understand different data structures, how you can clean up data, I would definitely learn Python. This is the number one language across the industry. You probably already know that, so I'm not going to talk about it too much. But you really want to just understand the basic functions in Python. For example, the main libraries that I would use as a data scientist just to like make it as simple as possible would be pandas, numpy, mapplot, and seabour.

**7:32** · So pandas to create your data frame and start like data manipulation, analyzing all of your data. Numpy allows you to do more mathematical functions and mapp just help you visualize the data. Like these are just like basic functions that you could start with alongside having some sort of course that you're following.

**7:56** · Hands-on courses are the most important.

**7:58** · I learned Python in a CS course in college. I had to take this like CS120s course at Chicago for my astrophysics degree. And I learned everything in Python in 10 weeks. I started from literally zero to learning all of Python. Well, okay. Okay, not all of Python, but like the basics of Python that were required for the course in 10 weeks. You can find the syllabus and the structure of the course online. You just need to understand the structure of how to learn the basics. You can find it like with the Chicago syllabus, MIT open courseware on data camp, Corsera, UDMI.

**8:32** · The basics of Python you should be able to find anywhere online. Here's a quick example of how to build the most basic set in Python. You just import all of your libraries. These four really make up like a core workflow and you're going to use this whenever you're building ML models as well. You can then import your data set. Here I'm just going to create like a very basic dictionary and we're going to convert that dictionary into a pandas data frame. So these are two different structures. And now we can combine like these features create a new column that gives us more information.

**9:02** · And once I have the data I want I could just create a very easy bar plot visualization. You can always throw this into chat GBT and get like a beautiful visualization like code. We have chatgbt now. It is game changer. I use it very regularly. Actually for code I use claude 3.7 not chatgbt but you could really like switch play around. So with these like super basic like four cells we got a data frame from a dictionary.

**9:30** · We created a new column which is feature engineering and we created a basic visual for the result. So I'm telling you, you got to do little things like this to build up if you are starting from scratch.

### ML info + project ideas + random regression explanation

**9:45** · Okay, now we're at ML modeling. You know, I know most of you skipped SQL and Python to get here. This is the most interesting. You do need basics to get to this. My first like year in the workforce, I was mostly just a lot of data analysis. And like honestly even when you get to ML 80% of your job going to be cleaning the data that is going into your ML model. Hyper tuning is not going to be most of your job. But let's get into ML.

**10:09** · The first thing if you have not worked with this before you haven't built machine learning models I really think building intuition is your first step. I would highly recommend watching Stat Quest and highly recommend the deep learning book. Just going through the Stat Quest YouTube homepage, you can see the different groupings of videos that you need to watch and what order you need to watch them in. For example, before you're trying to learn about how a neural networks, you need to understand a basic linear regression.

**10:41** · There is so much that goes into it. So, building intuition just generally on what you even need to learn is important. going through Stat Quest's homepage, looking at the groupings of videos, looking just at the index of the deep learning book and start reading deep learning like just it's a novel.

**10:57** · Every morning read two or three sections. It takes about 10 minutes and you're going to build a lot of intuition. It's not a lot of heavy math in there. If you're really starting from scratch, let me give you an example flow of how you would learn something about a machine learning model. I wrote everything out for this video. So, I got an exact flow for you. So if you're really starting from scratch, look into all the concepts that go into a linear regression. Start from what is a linear regression? What is the purpose of a linear regression? What is the gradient descent algorithm?

**11:26** · What is that algorithm doing to minimize the loss function? What is a loss function? How can bias or variance in your data set affect the results of using linear regression as your model? And then you go in that order of like breaking down one machine learning model into its components. and then learning about these components and that's how you build intuition and all of this is broken out for us already with stat quest with all of these books. I also have data ace the data science interview which helps you build intuition.

**11:55** · So you should screenshot this but here's like a potential order of operations on how to learn machine learning. Handholding is very important when you're first trying to delve into machine learning. I imagine a lot of you are trying to learn this yourself and you're not in school.

**12:13** · Or if you are in school, you're super lucky. Like you're lucky. But if you're learning this yourself, you do need some courses and some books, some handholding to get yourself to a place where you feel comfortable being able to interview. Chad GBT is going to be your best friend, especially when it comes to learning about like how to learn data science in the ML space. Let's go into what an ML pipeline even is. So, like I said before, 80% of your job is cleaning data. That is a fact.

**12:39** · Anyone who says that their job isn't is like likely a PhD getting paid double what I'm getting paid has someone like me working for them that does the data cleaning. But like most people are going to be cleaning data for the rest of their lives. So, you clean your data, you do a train test split, so you can actually test the basic version of your model.

**13:00** · You can cross- validate your results based on whatever parameters you put in.

**13:04** · You could also do a grid search across different parameters, but you want to understand what these parameters mean in statistical terms. Like just have chat GPT open while you're learning something. Watch a YouTube video on your desktop, have chat GPT open, pause the video when you don't understand a term, and talk to chat GPT about the term.

**13:22** · Like we have like a built-in assistant.

**13:24** · Now, the coding is not the hard part.

**13:26** · Honestly, it's about the intuition, the math, the stats, everything that goes into why things work a certain way in data science. In terms of projects, like you really want to touch the basics of like regression and classification in supervised learning, right? I would say number one, those are the two things you want to look at. So for regression, you could just go to Kaggle or you could ask Chat GPT for a data set. Just get a data set on like housing information and then you could predict how much the house costs like any sort of like continuous variable prediction.

**13:56** · You could do that with like a basic linear regression.

**14:00** · That could be your first project. So, here's a couple of examples of different projects that you could possibly look into. And finding data sets nowadays is super easy. So, if you don't have Python on your laptop, just download Anaconda and then type Jupyter Notebook into your terminal and then start building out your Python notebooks, testing different things out, reading in different CSVs locally.

### math math math

**14:24** · I want to talk about sprinkling math and like how that falls into like learning all of these machine learning models and derivatives and integrals and linear algebra. Absolutely like the base of all of the work you're going to do in these machine learning models. Like everything's already built in in Python packages, so we don't see it. But I'm telling you, like understanding the basics of this math is very important.

**14:46** · So again, going into Stat Quest, looking into like different videos about linear algebra, like you'll learn all of this though. That order of operations I gave you about like learning what is a linear regression, you go to gradient descent.

**14:57** · That's all derivatives, right? That's like an algorithm that you're trying to minimize. You really need to understand linear algebra, matrices, matrix operations. I use that in my day-to-day.

**15:07** · I build transition matrices out. Like my life depends on it in multiple different jobs that I've had. derivatives and integrals are used in the algorithms we're going to use especially regression like linear regression understanding the difference between L1 regularization L2 regularization like when it comes to ridge regression you're basically minimizing the sum between the squares of your weights so like your coefficients are always going to be similar to each other because like you know 0.02 squared is going to be lower than 0.02 02, right?

**15:38** · So you're trying to minimize that. Whereas for L1 regularization, which is lasso regression, it's going to be the absolute value of the sum of your weights. So a lot of those weights go to zero. So when you think about like you have like a 100 features, 50 of them, the weights are going to zero because they're not that important in understanding the variability in your data set. That's basically just cleaning up all of your data, picking the features that are most important, and then you can create a model off of that.

**16:05** · So all of this is coming from derivatives and integrals. I wouldn't say you need to pull out a math textbook and learn all of this, but I think I want you to be curious about what is going into these ML models that you're throwing data into. Every time you encounter a new model or you're trying to learn about it, get curious. Dive deep into how is this even working? Like what are the components of this model?

**16:27** · What is the base of the model's inputs and outputs?

### stats basics

**16:33** · Okay, we're almost done. This video is so long. I'm sorry, but you got to know everything. The next one is stats. This is something that I actually have to learn a lot about in my current job at Stripe, and I didn't really use it in other jobs. I was more of like a businessy data scientist, for lack of a better way of saying it. And now I'm definitely needing to be even more technical, especially on the stat side.

**16:58** · I would say experimentation is very important and general statistics in terms of sampling. So, in terms of experimentation, just go to Corsera.

**17:06** · There's so many free videos that you can watch to understand what it takes to set up an experiment. For example, if we're creating a new feature on one of the Stripe applications, you need to test all of these things before we can just put it out to see, hey, is this actually going to be used? Is it going to be useful? Is it making us more money?

**17:23** · There's always going to be a metric that needs to be improved. And I personally took one stats class in college and that was it. So, I'm really learning like honestly with you on the job. For this section, I had to think about like what are all the things that I didn't know and I encountered in this job and I felt dumb for not knowing any of this. So, you really want to understand like population versus sample. What is population variance? The types of errors that you expose yourself to in the experiment cuz no experiment is going to be perfect. So, which error are you more okay with? And how can you balance your experiment that way?

**17:54** · But you need to understand like what is this feature trying to measure? Are we trying to improve cost? Are we trying to reduce latency? like what are we trying to do with this feature? So thinking about what you're measuring. Can your sampling setup and methodology actually help you measure this phenomenon and then figure out hypothesis testing like do you have enough of a population that you're going to test this on? Is this going to cost you a lot? So on and understanding confidence intervals like there's so many things that go into an experiment.

**18:20** · I'm actually running my first experiment at the company right now and it is a lot and it really naturally happens like with on the ground learning. So, if you're going into jobs that have like interviews that require all of this, you really unfortunately just have to like build the intuition somehow yourself without that hands-on practical experience, which is why like some sort of online course could be useful.

### business acumen

**18:44** · And lastly, the thing that you really do just learn with time, but it is the most pivotal thing about being a data scientist is business acumen. We're not software engineers. We're data scientists. We're almost conduits from figuring out what is actually going on with the business in the data to presenting that to either our product managers, our leaders, potentially directly to different like client-f facing teams like sales. At the end of the day, the coolest data science things might not make the most impact to the business. So, you have to understand what's required.

**19:15** · For example, when I was doing sales forecasting, I did that at the startup I was at, Drizzly. And the model I used for sales forecasting at Drizzly was so different from the data I used with Uber because Uber was growing at such a rapid pace. It had so many different seasonality factors and just growth factors and coefficients that I needed to add in compared to Drizzly which was like in the alcohol beverage space. Had very consistent growth over time that was representative of how the company was doing at the time.

**19:43** · You can also get really creative if you have good business acumen. You're paying attention in meetings. you're talking to your product managers, the engineers, the people that create the data that you're working with, like the sales team that influences the payments we're getting. If you understand how everything fits in together, you can get very robust data sets together. For example, if you're trying to predict user churn and you're fully aware of like the data that the business has, you could really curate everything.

**20:10** · Like I made a list, but like you could have payment volume, transactions, recency of transactions, the type of users and demographic data, industry, business size, interventions, time to processing their payments, and so on. You can just put everything together, throw it into a lasso regression, which will give you the most important features. You could also go through a principal component analysis to figure out like which of these features are the most important and have the most variance in our data set. Machine learning is not one model.

**20:38** · It's like a hybrid of multiple models, approaches, stats, reasoning, math concepts, just everything together. And I think business acumen is really what ties everything together in making you a good data scientist. And yes, I also make slideshows for work. And that's not super common, but I do have to do it because data communication is really important. So, there's basically like a lot of things you need to know. I talked a lot in this video, but I really hope it helped gave you a starting ground to understand like how I would learn everything, the order of operations.

**21:06** · And I hope it gives you a little bit of like relief knowing that, you know, I'm someone that I think I interview generally pretty well. I have a job in tech and I really don't know everything.

**21:19** · And I think honestly every data scientist I work with will tell you that they have no idea how most things work.

**21:26** · You just have to learn on the job, be adaptable, be able to problem solve, and you'll be fine. And don't forget to subscribe and like, follow for the journey. I really appreciate it. Thank you so much and I'll see you at the next