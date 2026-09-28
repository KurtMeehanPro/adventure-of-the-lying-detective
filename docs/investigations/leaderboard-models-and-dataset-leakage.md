# Leaderboard Models and Dataset Leakage

When looking at some of the high scores in the leaderboard and in the Code section, I noticed Kagglers did one or both of the following:

- Used a pre-trained model that was larger than the base model (e.g. used XLM-R large)
- Used a model that had been fine-tuned on some, or all, of the following datasets: SNLI, MNLI, ANLI, XNLI and then fine-tuned using the Watson examples

## As for using a larger pre-trained model to start…

In my submission notebook I decided to follow the herd and submit using the larger model. The competition did not mandate a specific model. It is interesting to see the better performance of more powerful models. I do think it’s difficult to make an apples-to-apples comparison and have a fair competition when participants use different pre-trained models. But, again, it’s interesting to see.

## As for using a model that’s been fine-tuned already on SNLI, MNLI, ANLI, XNLI…

My [investigation](https://github.com/KurtMeehanPro/adventure-of-the-lying-detective/blob/main/notebooks/03_watson_dataset_overlap.ipynb) showed that there was complete overlap between the examples used in Watson and examples found in MNLI and XNLI. It seems to me that the high scores using this method result from complete data leakage. The pre-trained and pre-fine-tuned model being used as the base model would likely have already been trained on the very same examples used in the Watson Test set! For obvious reasons, I will not be following the herd and will not be using this method.

## Musing

I wonder what the ultimate performance someone could obtain using the following constraints. It'd be interesting to know what techniques other Kagglers used to wring out performance given the same constraints.

- XLM-Roberta Base
- Fine-tuning ONLY using Watson examples provided

I was only able to reach about \~70% in my attempts with the Base Model.

With XLM-Roberta Large, on the other hand, I was able to hit \~80% with the same overall training approach and settings as I used with the Base Model.
