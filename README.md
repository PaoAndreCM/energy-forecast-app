---
title: Energy Forecast App
emoji: ⚡
colorFrom: blue
colorTo: green
sdk: docker
app_port: 8501
---

# Germany Electricity Consumption Forecast
...rest of your README...
# Energy Forecast App
> Day-ahead electricity consumption forecasting for Germany using PatchTST, with an interactive app to explore predictions and compare against actual grid load.

## Motivation
There are two kinds of european electricity markets: Day-Ahead and Intraday. Day-Ahead markets allow trading of electricity for each hour of the next day. An accurate day-ahead forecast contributes to more stable and predictable trading, with less dependency on last minute corrections with the intraday market. 

More accuracy in day-ahead forecasting also enables less waste of energy bought but not consumed. It could also be used to better plan when to use surplus energy for activities such as hydro pumping, allowing for this energy to be stored for when it is needed. 

Better planning could result in less dependency last minute fossil-fuel ramp up, contributing to the decarbonization of electricity production. 

## What It Does
This app is meant to predict day-ahead electricity consumption, initially in Germany, benchmarked against the SMARD platform. It will allow the user to visualize a prediction for the consumption of the next day, and compare it to the SMARD forecast. For selection of past days, it will also show a comparison with actual consumption.

## How It Works
The [patch-TST architecture](https://github.com/yuqinie98/PatchTST) has been used for this project. A model with this architecture was trained on past consumption data provided by the [SMARD platform](https://www.smard.de/home). As input, the model takes in the actual consumption of the seven days prior to the forecasted day, in 15 minute intervals. As output, the model generates 96 predictions, corresponding to the forecasted consumption of the next day in 15 minute intervals.

<!-- ## Project Structure -->
<!-- ## Resulst -->

## Dev log
Link [here](DEVLOG.md)

## Next Steps
- Refactor thesis code (in Jupyter notebook) into clear structure
- Build streamlit app for model interface
- deploy app + model
- Create re-train pipeline
- Automate selection and load of best re-trained model


## References
[Patch-TST code](https://github.com/yuqinie98/PatchTST)
[Nie et al., 2023 — "A Time Series is Worth 64 Words"](https://arxiv.org/abs/2211.14730)
