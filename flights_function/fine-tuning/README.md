### Fine-tuning process

I plan to create fine-tuned models for at least all three of the params functions.

I started with destination function, because it performed the worst out of the box. I got significantly better performance with fine-tuned GPT-3.5 than GPT-4 without fine-tuning.

To create training data for destination parameter function I used Chat-GPT (using GPT-4) to save on API costs (I do not recommend this approach though because it was time consuming).
Most training examples had to be modified, because the answer was not exactly what I wanted. Airport codes often included a few that were not relevant, or some obvious relevant airports were missing.

I stored them as a json file to data/ and used **dest_ft_parset.py** to format it correctly for training.

I then separeted them to training data and validation data. I used **data_validation.py** to verify that the format is correct.

**fine-tuning.py** was used for the actual fine-tuning job.

In this folder I also have **time_answer_script.py**. It's not finished, but it will be used to generate training data to fine-tune time params function.

Also, there is an unfinished script **log_parser.py** that I was planning to use to make training data out of real user queries.
