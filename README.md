# CS6111-Project3

# Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
3. [Usage](#usage)
4. [Description of Project](#description-of-project)
    - [Database Selection](#database-selection)
    - [Internal Design](#internal-design)

# Introduction
This project focuses on the extraction of association rules from a real-world dataset using the Apriori algorithm. Our goal is to discover meaningful patterns between features in the dataset by finding frequent itemsets and generating high-confidence association rules.
Following the project description, we completed two major components:
- Defined and prepared our dataset of choice — the NYPD Shooting Incident Data (Historic).
- Implemented the Apriori algorithm from scratch, incorporating query optimization techniques to efficiently mine association rules.

This project strengthened our understanding of frequent itemset mining and association rule generation, key concepts in data mining and knowledge discovery. It also provided hands-on experience applying these algorithms to large, real-world data. This project was built for Project 3 of COMS6111 - Advanced Database Systems.

Developed by Phoebe Tang and Matthew Labasan.

# Getting Started
## Prerequisites
1. Python 3

## Installation
1. Clone the repository  
  `git clone https://github.com/adironene/CS6111-Project3.git`  
2. Move into the respository  
  `cd ./CS6111-Project3`  
3. Create a virtual environment and activate it  
    - `python3 -m venv dbproj`  
    - `source dbproj/bin/activate`  

# Usage
1. Run & replace with your parameters, using a query in quotations: 
  `python3 main.py <dataset_path> <support> <confidence>`
  - `<dataset_path>` is the path to the desired csv file
  - `<support>` minimum support for association rules - decimal between 0 and 1
  - `<confidence>` minimum confidence for association rules - decimal between 0 and 1
  - Ex : `python3 main.py ./INTEGRATED-DATASET.csv 0.1 0.5`

# Description of Project
## Dataset Selection
We decided to use the [NYPD Shooting Incident Data (Historic)](https://data.cityofnewyork.us/Public-Safety/NYPD-Shooting-Incident-Data-Historic-/833y-fsy8/about_data) to generate our INTEGRATED-DATASET.csv file. 
We did not make any modifications or combine any other tables, and the dataset was downloaded directly from the website without any query modifications. It was only renamed to ‘INTEGRATED-DATASET.csv’.

Using this dataset, we are able to obtain association rules that reveal relationships between perpetrator demographics and victim demographics, location and victim demographics, and more. These more informative association rules tend to appear at lower support thresholds, as not all rows will include relevant information for these rules.

These association rules can be valuable in identifying which demographics and areas within the city are more affected by shootings. This information could help focus resources on education initiatives about gun violence or guide decisions around enforcing stricter gun control measures in targeted areas. Additionally, it can inform outreach efforts toward communities that may benefit most from preventative resources. However, it is important to approach these findings thoughtfully and avoid using them to further stigmatize already marginalized populations.

## Internal Design
For a description of the internal design, please see p.3-6 of our report [here](./submission/Project3_Report.pdf).

For sample association rules, please see our result transcripts [here](./example-run.txt).

