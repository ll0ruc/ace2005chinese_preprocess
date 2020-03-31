# ace2005chinese_preprocess
ACE 2005 corpus preprocessing for Event Extraction task

## Prerequisites

1. Prepare **ACE 2005 dataset**. 

   (Download: https://catalog.ldc.upenn.edu/LDC2006T06. Note that ACE 2005 dataset is not free.)

2. Install the packages.
   ```
   pip install beautifulsoup4 nltk tqdm
   ```
   
## Usage

Run:

```bash
sudo python main.py --data=./data/ace_2005/Chinese
``` 

- Then you can get the parsed data in `output directory`. 

## Output

### Format

I follow the json format described in nlpcl-lab/ace2005-preprocessing
 [[github]](https://github.com/nlpcl-lab/ace2005-preprocessing)
repository like the bellow sample. But currently only sentence, event-mentions, entity-mentions, others information such as dependency tree, pos_tags, etc. will be added later.

If you want to know event types and arguments in detail, read [this document (ACE 2005 event guidelines)](https://www.ldc.upenn.edu/sites/www.ldc.upenn.edu/files/english-events-guidelines-v5.4.3.pdf).


**`sample.json`**
```json

[
   {
    "sentence": "两个星期来，藤森曾亲自带队搜捕 前情报顾问蒙特西诺斯，迄今蒙特西诺斯仍未落网",
    "golden-event-mentions": [
      {
        "arguments": [
          {
            "start": 29,
            "end": 34,
            "entity-type": "PER:Individual",
            "text": "蒙特西诺斯",
            "role": "Person"
          },
          {
            "start": 0,
            "end": 4,
            "entity-type": "TIM:time",
            "text": "两个星期",
            "role": "Time"
          }
        ],
        "trigger": {
          "start": 36,
          "end": 38,
          "text": "落网"
        },
        "event_type": "Justice:Arrest-Jail"
      }
    ],
    "golden-entity-mentions": [
      {
        "start": 16,
        "entity-type": "PER:Individual",
        "text": "前情报顾问",
        "end": 21,
        "phrase-type": "NOM"
      },
      {
        "start": 21,
        "entity-type": "PER:Individual",
        "text": "蒙特西诺斯",
        "end": 26,
        "phrase-type": "NAM"
      },
      {
        "start": 29,
        "entity-type": "PER:Individual",
        "text": "蒙特西诺斯",
        "end": 34,
        "phrase-type": "NAM"
      },
      {
        "start": 6,
        "entity-type": "PER:Individual",
        "text": "藤森",
        "end": 8,
        "phrase-type": "NAM"
      },
      {
        "start": 0,
        "entity-type": "TIM:time",
        "text": "两个星期",
        "end": 4,
        "phrase-type": "TIM"
      },
      {
        "start": 27,
        "entity-type": "TIM:time",
        "text": "迄今",
        "end": 29,
        "phrase-type": "TIM"
      }
    ]
  },
]


## Reference
- nlpcl-lab's ace2005-preprocessing repository,  [[github]](https://github.com/nlpcl-lab/ace2005-preprocessing)
