# Predictive Tool Based on Opinion Formation Models from Sociophysics

This is a very preliminary and rough draft of how I could be spending my 
next few years doing a PhD.

Todo: References

## Goal

A tool which allows extracting issue topics and opinions from social networks
and make predict how these opinions will evolve over time.

## Problems 

### Gathering Data

Commonly done via costly and slow surveys. Scraping it from social networks
like Twitter is possible.

### Topic Extraction in Social Networks

This is mostly a data mining and machine learning problem that is currently
under a lot focus. Models and Algorithms exist and work reasonably well
according to researchers in the field.

### Opinion Extraction in Social Networks

This is very similar to the first problem and should be achievable if data is
available.

### Picking the Model

A variety of Models in Sociophysics have been shown to make reasonable
predictions on several occasions. The models differ considerably in their
nature. Picking the right model and parameters is highly nontrivial and
possibly requires expertise from both social psychologists and sociologists.
Some models do take into account the topological features (or the underlying
network) of the population.

In a first stage, the choice of model and parameters could be left to the user.

## Questions

- Do we have access to enough relevant data to test the software? I think yes,
  with the help of our collaborators and possibly some scraping we should have
  plenty.

- Are topic/opinion extraction tools accurate enough? I'm being told they
  usually are but fail totally in some cases.

- Are the models good enough to make reasonable predictions? Sociophysics
  researchers have published about a dozen examples where they worked well.
  Unfortunately we don't know how often they fail.

- What is this good for? Making democracies more efficient.
  
- Why do we need it? Once we have a working toolchain and everything but 
  the physics modelling has been abstracted away, the overhead of testing 
  new models is greatly reduced.
